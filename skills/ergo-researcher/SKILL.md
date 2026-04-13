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

## Curve fitting: use Python scripts

The LLM cannot compute polynomial regression. For every product's analysis phase, the research agent MUST write and execute a Python script:

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

# Normalize age to 0-1
min_age, max_age = ages.min(), ages.max()
t = (ages - min_age) / (max_age - min_age)

# Fit quadratic: price = a + b*t + c*t^2
coeffs = np.polyfit(t, prices, 2)  # returns [c, b, a]
quadratic, linear, base_price = coeffs

# Compute R²
predicted = base_price + linear * t + quadratic * t**2
ss_res = np.sum((prices - predicted) ** 2)
ss_tot = np.sum((prices - np.mean(prices)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# The base_price includes baseRate * units * (1+loading)
# We need to factor those out to get the ageCurve coefficients
# ... (product-specific extraction logic)

print(json.dumps({
    "age_curve": {"base": round(float(base_price/base_price), 4), 
                  "linear": round(float(linear/base_price), 4), 
                  "quadratic": round(float(quadratic/base_price), 4)},
    "r_squared": round(float(r_squared), 4),
    "base_price_at_min_age": round(float(base_price), 2),
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

**Realistic timing per product:**
- Structure crawl: ~5 min (navigate all steps, screenshot, document)
- Price sampling (50 data points at ~20s each): ~17 min
- Analysis (Python script): ~2 min
- Review: ~3 min
- **Total per product: ~27 min**

With 3 parallel sessions (Mode B): 14 products in ~2.5 hours.

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

**Global rule**: Maintain a minimum 5-second gap between any request to ergo.de, across ALL concurrent sessions. With 3 parallel sessions, each session waits 15 seconds between its own page loads.

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
