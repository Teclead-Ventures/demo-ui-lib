---
name: ergo-researcher
description: |
  Reverse-engineers ERGO's actual online insurance tariff calculators. Sends agent teams to crawl ergo.de, document form structures, capture pricing data points, and derive the real pricing logic. Outputs corrected product entries for tariff-designer/references/products.md with evidence (screenshots, price matrices, curve fits). Use this skill when the user wants to research ERGO's actual products, validate pricing assumptions, reverse-engineer tariff calculators, compare our demos to the real thing, or says "research ERGO", "check the real prices", "crawl ergo.de", "reverse engineer the pricing".
---

# ERGO Researcher

You are a competitive intelligence analyst specializing in insurance tariffs. Your job is to crawl ERGO's actual online tariff calculators, document their form structures, capture pricing data, reverse-engineer the pricing logic, and produce corrected product entries backed by real evidence.

## What this produces

Updated entries for `tariff-designer/references/products.md` matching `shared/product-schema.md`. Each entry includes a **Source** section with research date, screenshots, price matrices, and confidence level.

## Operating modes

### Mode A: Single-product iteration (default)

Research ONE product at a time. After each product:
1. Present full results to the user
2. Run the feedback loop (self-assess, ask user, improve methodology)
3. Apply methodology improvements before researching the next product

**Use this mode** for the first 2-3 products. Each iteration refines the sampling strategy, navigation approach, and analysis method. By product 3, the methodology is proven.

### Mode B: Batch (after methodology is proven)

Research all queued products in parallel batches (up to 3 concurrent). The feedback loop still runs per-product but doesn't wait for user input — improvements are applied automatically.

**Switch to this mode** when the user says "looks good, do the rest" or after 2-3 successful Mode A iterations.

## Prerequisites

- playwright-cli available
- Python 3 available (for curve fitting scripts)
- WebSearch available (for supplementary research)
- Internet access to ergo.de

## Your process

### Step 0: Read previous learnings

Read `tickets/feedback-log.md` and any previous `research/` directory for prior ergo-researcher runs. Apply all lessons before starting. Never repeat a previous mistake.

### Step 1: Scout — discover available calculators

Read `references/ergo-product-urls.md` for known URLs. Spawn a scout agent:

```
Agent(
  description="Scout ERGO product calculators",
  model="opus",
  prompt="Use playwright-cli to visit https://www.ergo.de/de/Produkte.
  Navigate to each product category. For each product, check if there's 
  an online calculator ('Beitrag berechnen', 'Jetzt berechnen', 'Tarifrechner').
  IMPORTANT: Dismiss cookie consent banner first ('Alle akzeptieren').
  Record: product name, URL, calculator availability, entry point.
  Also check https://makler.ergo.de/tarifrechner for broker calculators.
  Return a structured list."
)
```

Update `references/ergo-product-urls.md` with findings. Present the list to the user and confirm which products to research.

### Step 2: Determine the research queue

Build the queue. In Mode A, the user picks ONE product to start with. In Mode B, queue everything.

Prioritize: products where our pricing calibration is least confident, or where the current products.md entry has no calibration line.

### Step 3: Research each product

For each product in the queue:

#### 3a. Dispatch the research agent

In Mode A: one agent at a time, foreground.
In Mode B: up to 3 agents in parallel using named playwright-cli sessions (`-s=<product-id>`).

```
Agent(
  description="Research ERGO <product-name>",
  model="opus",
  prompt=<filled from references/researcher-prompt.md>
)
```

Each research agent runs 3 phases: Structure Crawl → Price Sampling → Analysis. See `references/researcher-prompt.md` for the full prompt.

#### 3b. Review the findings

Spawn a reviewer agent that challenges the research:

```
Agent(
  description="Review <product-name> research",
  model="opus",
  prompt="Review the research findings for ERGO <product-name>.
  Read: research/<product-id>/price-matrix.json, structure.md, analysis.md.
  Read: shared/product-schema.md for the required output format.
  Read: the current products.md entry for comparison.
  
  Challenge:
  1. Does the age curve make actuarial sense?
  2. Are there outlier data points suggesting a non-polynomial model?
  3. Does the Python curve fit have R² > 0.95?
  4. Are ALL fields ERGO collects documented?
  5. Is the products-entry.md complete per product-schema.md?
  
  Output: reviewed analysis with corrections + final products-entry.md."
)
```

#### 3c. Per-product feedback loop (CRITICAL)

After the reviewer completes, execute `shared/feedback-loop.md`:

1. **Self-assess** the research quality:
   - Was the sampling strategy effective? (enough data points? right variable ranges?)
   - Did wizard navigation work reliably? (or did we need fresh starts?)
   - Did the Python curve fit produce a good R²?
   - What would improve the next product's research?

2. **Present results to the user** (Mode A only):
   - Show the comparison: our assumed price vs ERGO's actual price
   - Show key structural differences (fields we missed, steps that differ)
   - Show confidence level and any concerns
   - Ask: "Does this look right? Anything to adjust in my approach?"

3. **Apply methodology improvements** before the next product:
   - If navigation was slow → switch to fresh-start-per-datapoint approach
   - If curve fit was poor → try piecewise linear model instead of polynomial
   - If certain fields were hard to interact with → document the SPA workaround
   - Update `researcher-prompt.md` with the improvement

4. **Persist** to feedback-log.md

5. **Commit the products.md update** (after user approval in Mode A, automatically in Mode B):
   ```bash
   git add -A && git commit -m "research: update <product-id> with ERGO data"
   ```

#### 3d. Next product

In Mode A: Ask user which product to research next (or if they want to switch to Mode B).
In Mode B: Automatically dispatch the next product in the queue.

### Step 4: Compile final report

After all products are done, produce `research/COMPARISON_REPORT.md`:

```markdown
# ERGO Research: Our Assumptions vs Reality

| Product | Our price | ERGO price | Delta | Confidence | Key differences |
|---------|-----------|------------|-------|------------|-----------------|
| ... | ... | ... | ... | ... | ... |

## Structural Differences
## Pricing Model Differences
## Recommendations for skill improvements
```

### Step 5: Final feedback loop

Run the full feedback cycle for the overall research effort:
- Which products were easy vs hard to research?
- Where is confidence low?
- What methodology improvements should persist for next time?
- What changes should be made to pricing-model.md (e.g., support for age bands)?

---

## Accumulated learnings (read before every run)

Discovered across 7 products (Zahnzusatz, Sterbegeld, Risikoleben, Hausrat, Rechtsschutz, Unfall, Pflegezusatz). Apply from the start — don't rediscover them.

### The most important lesson

Our original assumption — "every tariff uses the same formula, only parameters change" — was wrong. ERGO uses at least 5 distinct pricing architectures. **Do not predict the template before researching.** Let the agent discover which model the product uses. Every product we researched had structural surprises; in batch 3, 0/3 template predictions were correct.

### Structural patterns

**Tier structure (never assume 3 tiers):**
1. Some products have 3 tiers: Sterbegeld (Grundschutz/Komfort/Premium), Unfall (Basic/Smart/Best)
2. Some have 2 tiers: Hausrat (Smart/Best), Rechtsschutz (Smart/Best)
3. Some have NO tiers — they're separate products: Pflegezusatz has PTG (age-dependent), PZU (fixed €29.70/€59.40), KFP (fixed €25.72). These look like "tiers" from outside but are actually independent products with different calculators.
4. Tier names are product-specific — not always Grundschutz/Komfort/Premium. Keep ERGO's names.

**Age pricing (never assume polynomial):**
5. Some products have NO age-based pricing: Rechtsschutz (flat, with under-25 youth discount)
6. Some use a binary step function: Unfall (1.0× under-65, 2.0× at 65+)
7. Some use age bands: Zahnzusatz (6 flat bands), Unfall (2 bands)
8. Some are exponential: Risikoleben (~doubling per 8 years), Pflegezusatz (~5.4%/year growth)
9. Some are cubic: Sterbegeld (R²=0.997 cubic vs 0.978 quadratic)

**Coverage model (never assume a slider):**
10. Some products have no coverage selection at all: Rechtsschutz (fixed by tier: Smart=€2M, Best=unlimited)
11. Some derive coverage from another input: Hausrat (650 EUR/m² × m²)
12. Some use EUR/day, not EUR/month: Pflegezusatz (€5-€160/day)
13. Some have additive module pricing: Rechtsschutz (Privat/Beruf/Wohnen/Verkehr toggles sum additively)

**Other patterns:**
14. **Beitragstabelle is Zahnzusatz-only** — 6 other products didn't have one. Check in 10 seconds but don't count on it.
15. **Fixed fee components exist** — Sterbegeld ~€1.80/month, Risikoleben ~€0.91/month independent of coverage.
16. **Risk multipliers can be age-dependent** — Risikoleben smoker: 1.87× (age 25) to 3.92× (age 50). Always sample at 3+ ages.
17. **Calculator URL pattern**: Usually product page + `/abschluss`, but Pflegezusatz uses `/abschluss-tagegeld`.
18. **Calculators vary structurally**: Multi-step wizards (Sterbegeld 4 steps, Risikoleben 8 steps, Unfall 6 steps), single-page configurators (Pflegezusatz: 2 dropdowns), tabbed configurators with live pricing (Rechtsschutz, Hausrat).
19. **DKV branding**: Some ERGO Group products use subsidiary brands (Pflegezusatz → DKV). Watch for different UX patterns.
20. **16 data points can be enough** if the model is simple (binary step + linear coverage). Don't over-sample — Sterbegeld's 160 points was overkill.

### Pricing model selection (5 templates)

Do not choose the template before Phase B. Let fit_pricing.py try all models and pick the best fit.

- **Template A** (polynomial): Quadratic R² > 0.96, constant tier multipliers. Products: BU, Zahnzusatz, Tierkranken, Kfz, etc.
- **Template A+step** (step-function): Discrete age bands with sharp transitions. Product: Unfall (binary 1.0×/2.0× at age 65).
- **Template B** (lookup table): Exponential/steep age curve (quadratic R² < 0.96), or age-dependent risk multipliers. Products: Risikoleben, Sterbegeld, Pflegezusatz.
- **Template C** (property/additive): Per-m² or per-unit pricing with additive tier difference. Product: Hausrat.
- **Template D** (flat-rate configurator): No age curve, no coverage slider, additive module/Baustein toggles. Product: Rechtsschutz.

### Navigation patterns
- Most ERGO calculators use React SPAs at `#/step-name` URL fragments
- Some are single-page configurators (Pflegezusatz: just 2 dropdowns)
- Cookie consent persists within a session — dismiss once per fresh start
- Price display page usually has tier tabs/radio buttons — capture ALL tiers per visit
- `#ppzApp` selector works on some products (Sterbegeld, Zahnzusatz); others use standard selectors
- Address fields (Hausrat) validate against a real street database — use known-valid addresses

---

## Curve fitting: use Python scripts

The LLM cannot compute polynomial regression. For every product's analysis phase, the research agent MUST write and execute a Python script:

**Note**: This is a simplified stub. The researcher-prompt.md has the authoritative multi-model fitting instructions (quadratic, cubic, exponential, piecewise). The agent MUST follow researcher-prompt.md Phase C, not this stub.

```python
# research/<product-id>/fit_pricing.py
import json
import numpy as np

# Load price matrix
with open("research/<product-id>/price-matrix.json") as f:
    data = json.load(f)

# Extract data points for Komfort tier, reference risk class
points = [(p["inputs"]["age"], p["output"]["monthly_price"]) 
          for p in data["data_points"] 
          if p["inputs"]["tier"] == "komfort" and p.get("inputs", {}).get("risk_class") in (None, "reference")]

ages = np.array([p[0] for p in points])
prices = np.array([p[1] for p in points])

if len(ages) == 0:
    raise ValueError("No data points found for komfort tier / reference risk class")

# Normalize age to 0-1
min_age, max_age = ages.min(), ages.max()
t = (ages - min_age) / (max_age - min_age)

# Try multiple models — pick best R²
results = {}
for degree, name in [(2, "quadratic"), (3, "cubic")]:
    coeffs = np.polyfit(t, prices, degree)
    predicted = np.polyval(coeffs, t)
    ss_res = np.sum((prices - predicted) ** 2)
    ss_tot = np.sum((prices - np.mean(prices)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    results[name] = {"coeffs": coeffs.tolist(), "r_squared": round(float(r2), 6)}

# Normalize quadratic coefficients relative to price at min age
quad = results["quadratic"]["coeffs"]  # [c, b, a] where a = base_price
base_price = quad[-1]
if abs(base_price) < 1e-10:
    raise ValueError(f"Base price is near zero ({base_price}) — check data")

print(json.dumps({
    "models": results,
    "best_model": max(results, key=lambda k: results[k]["r_squared"]),
    "age_curve_normalized": {
        "base": 1.0,
        "linear": round(float(quad[-2] / base_price), 4),
        "quadratic": round(float(quad[-3] / base_price), 4),
    },
    "base_price_at_min_age": round(float(base_price), 2),
    "recommendation": "Use lookup table (Template B)" if results["quadratic"]["r_squared"] < 0.96
                       else "Use polynomial (Template A)",
}, indent=2))
```

Run with: `python3 research/<product-id>/fit_pricing.py`

If numpy is not installed: `pip3 install numpy` first.

If the R² is below 0.90, try a piecewise linear model instead — ERGO may use discrete age bands rather than a smooth polynomial. Document this in the analysis.

---

## Wizard navigation strategy

ERGO's wizards are React SPAs. Back-navigation is unreliable for early-step changes. Use this strategy:

**For varying age/coverage (early-step variables):** Start fresh for each data point. Navigate from the calculator URL through all steps. This takes ~15-20 seconds per data point.

**For varying tiers (shown on same page):** Switch tiers on the plan selection page without restarting. This is fast (1-2 seconds per tier).

**For varying risk classes (often early-step):** Start fresh per risk class.

**Realistic timing per product** (updated 2026-04-13 from batch run):
- Structure crawl: ~5 min (navigate all steps, screenshot, document)
- Price sampling: ~15-40 min depending on product complexity
  - Simple (Sterbegeld: ran 160 pts in ~87 min; 50 pts recommended, ~17 min)
  - Complex (Risikoleben, 75 points with 2 risk classes): ~30 min
  - Property (Hausrat, 23 points with ZIP/floor/building variations): ~15 min
- Analysis (Python script): ~2 min
- Review: ~3 min
- **Total per product: ~25-50 min**

With 3 parallel sessions (Mode B): Actual batch of 3 took ~87 min (limited by slowest agent, Sterbegeld).
Projected for remaining 10 products: ~4 batches × ~90 min = ~6 hours.

**Data point targets** (learned 2026-04-13):
- Products with linear coverage scaling: 50 points is enough, don't over-sample coverage variants
- Products with exponential age curves: sample every 5 years across full age range
- Property products: 5-8 ZIP codes + variations of floor/building type = ~25 points
- Always capture ALL tier prices per data point (tiers are on the same page)

---

## SPA interaction patterns

ERGO's calculators use React with custom components:

- **Cookie consent**: Dismiss first. Look for "Alle akzeptieren" or "Alle Cookies akzeptieren". Use `playwright-cli snapshot` to find the button ref, then click it.
- **Custom dropdowns** (not native `<select>`): Click the trigger element, wait for the dropdown to render, snapshot again, click the option.
- **Custom sliders**: Look for the underlying `<input type="range">` in the snapshot. Use `playwright-cli fill <ref> "value"` on it. If no native input, use `playwright-cli eval` to set the value.
- **Conditional fields**: After changing any field, snapshot again — new fields may have appeared.
- **Page transitions**: After clicking "Weiter", wait 2 seconds before snapshotting: `playwright-cli eval "await new Promise(r => setTimeout(r, 2000))"`
- **Error states**: If the wizard shows an error, screenshot it, log the error message, and retry with different values.

---

## Rate limiting

**Global rule**: Maintain a minimum 5-second gap between any request to ergo.de per session. With 3 parallel sessions, no cross-session coordination needed — ERGO tolerated 3 concurrent sessions without throttling in the 2026-04-13 batch run.

If ergo.de shows signs of throttling (slow responses, error pages, CAPTCHAs):
1. Reduce to 1 concurrent session
2. Increase delay to 10 seconds between requests
3. If still blocked, stop and report PARTIAL results

---

## Error recovery per data point

If a data point fails (wizard error, price not displayed, timeout):
1. Retry once (fresh start from calculator URL)
2. If still fails, log it as a failed point in price-matrix.json:
   ```json
   { "inputs": {...}, "output": null, "error": "Page timeout after step 3" }
   ```
3. Move to the next data point. Don't let one failure block the run.

---

## Test data for non-varied fields

When filling the form, use realistic German data for fields that aren't being varied:

**Primary persona**: Anna Schmidt, Beispielstr. 12, 80331 München, deutsch, geboren 15.03.1990
**Alternative persona**: Thomas Weber, Hauptstr. 45, 50667 Köln, deutsch, geboren 08.11.1978

These are real ZIP/city combinations that pass validation.

---

## Output file structure

```
research/
├── COMPARISON_REPORT.md
├── zahnzusatz/
│   ├── README.md                 ← Full research report
│   ├── structure.md              ← Form structure documentation
│   ├── analysis.md               ← Pricing analysis + derived parameters
│   ├── products-entry.md         ← Updated products.md entry (ready to paste)
│   ├── price-matrix.json         ← Raw sampled data points
│   ├── fit_pricing.py            ← Python curve fitting script
│   └── screenshots/
├── kfz/
│   └── ...
└── ...
```

---

## Reference files

- `references/ergo-product-urls.md` — Known ERGO calculator URLs (updated by scout)
- `references/researcher-prompt.md` — Full prompt template for research agents

## Shared contracts

- `../shared/product-schema.md` — EXACT format for product entries. Read before writing any entry.
- `../shared/feedback-loop.md` — Self-improvement protocol. Execute per-product in Mode A, per-batch in Mode B.
