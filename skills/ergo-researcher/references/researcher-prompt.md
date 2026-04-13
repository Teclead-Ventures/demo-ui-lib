# Research Agent Prompt Template

Each research agent crawls ONE ERGO product calculator. Replace `{{placeholders}}` before dispatching.

---

## Prompt

```
You are researching ERGO's actual {{PRODUCT_NAME}} online tariff calculator. Your job: document every field, capture pricing data, and reverse-engineer the pricing logic.

## Your product

**Product**: {{PRODUCT_NAME}} ({{PRODUCT_ID}})
**Calculator URL**: {{CALCULATOR_URL}}
**Playwright session**: Use `-s={{PRODUCT_ID}}` for all playwright-cli commands

## Our current assumptions

Read the existing entry for {{PRODUCT_ID}} in:
`/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/skills/tariff-designer/references/products.md`

And the pricing model:
`/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/skills/tariff-designer/references/pricing-model.md`

Your job is to verify or correct these assumptions with real data.

## Phase A: Structure crawl (~3 min)

1. Open the calculator:
```bash
playwright-cli -s={{PRODUCT_ID}} open {{CALCULATOR_URL}} --headed
playwright-cli -s={{PRODUCT_ID}} snapshot
```

2. **Dismiss cookie consent banner first** — look for "Alle akzeptieren" or "Alle Cookies akzeptieren" in the snapshot. Click it before doing anything else.

3. Take initial screenshot:
```bash
playwright-cli -s={{PRODUCT_ID}} screenshot --filename=research/{{PRODUCT_ID}}/screenshots/landing.png
```

4. Find and click the calculator entry point ("Beitrag berechnen", "Jetzt berechnen", etc.). Try `/abschluss` suffix if not on product page. Some products use a variant (e.g., Pflegezusatz uses `/abschluss-tagegeld`).

5. **Determine calculator type** before proceeding:
   - **Multi-step wizard** (most products): Has "weiter" buttons, step indicators, hash-based routing (#/step-name)
   - **Single-page configurator** (e.g., Pflegezusatz): All inputs on one page with instant price updates. May have just 1-2 dropdowns.
   - **Tabbed configurator** (e.g., Rechtsschutz, Hausrat): Wizard for intake steps, then a configurator page with tier tabs, toggles, and live pricing

6. At EVERY step of the wizard (or for each section of a single-page configurator):
   - `playwright-cli -s={{PRODUCT_ID}} snapshot` → record all visible fields
   - `playwright-cli -s={{PRODUCT_ID}} screenshot --filename=research/{{PRODUCT_ID}}/screenshots/step-N-name.png`
   - Document: step number, heading text, all field labels, field types, options, default values
   - Try leaving required fields empty and clicking next → capture validation messages

7. **Answer these discovery questions** during the structure crawl (critical for template selection):
   - How many tiers? (2 or 3? What are ERGO's names for them?)
   - Are they tiers of ONE product, or separate products with different calculators? (Pflegezusatz: 3 separate products)
   - Is there a coverage slider/input, or is coverage fixed by tier? (Rechtsschutz: fixed)
   - Does coverage use a standard unit (EUR) or something else (EUR/day, m²)?
   - Are there toggleable modules/Bausteine? (Rechtsschutz: Privat/Beruf/Wohnen/Verkehr)
   - Is there an age input? (Rechtsschutz: only for youth discount, not pricing)
   - What brand is the calculator? (Usually ERGO, but Pflegezusatz is DKV)

8. Write the structure to `research/{{PRODUCT_ID}}/structure.md`:
```markdown
# ERGO {{PRODUCT_NAME}} — Form Structure

**Source**: {{CALCULATOR_URL}}
**Researched**: [date]
**Total steps**: N

## Step 1: [heading text]
- Field: [label] — Type: [text/select/radio/slider/date/checkbox] — Options: [if applicable] — Required: [yes/no]
- Field: ...
- Validation: [error messages observed]

## Step 2: [heading text]
...
```

## Phase B: Price sampling (~8 min)

Systematically fill the form with varied inputs. Goal: build a price matrix with 50-100 data points.

### Sampling grid

{{#if AGE_DEPENDENT}}
**Ages to test**: {{AGE_SAMPLES}} (e.g., 25, 30, 35, 40, 45, 50, 55, 60)
**Coverage amounts**: {{COVERAGE_SAMPLES}} (e.g., min, 25%, 50%, 75%, max)
**Tiers**: All available tiers
**Risk classes**: All available options
{{else}}
**Coverage amounts**: {{COVERAGE_SAMPLES}}
**Tiers**: All available tiers  
**Risk classes**: All available options
{{/if}}

### Sampling procedure

**For early-step variables (age, birth date, risk class):** Start FRESH for each data point. Navigate from the calculator URL through all steps. Do NOT try to navigate back — ERGO wizards are React SPAs where back-navigation is unreliable for early steps.

**For same-page variables (tier selection):** Switch tiers on the plan page without restarting. This is fast.

**Smart sampling strategy** (learned 2026-04-13):
- 50 data points is sufficient for well-behaved products. 160 was overkill for Sterbegeld where coverage scaling is linear.
- For property products (Hausrat, Wohngebäude), collect 5-8 ZIP codes to characterize regional variation.
- For products with exponential age curves (Risikoleben, potentially Pflege), plan for a lookup table from the start — polynomial R² will be inadequate.
- Check if tier relationship is multiplicative (most products) or additive (Hausrat: Best = Smart + fixed amount).
- Check for fixed fee components (Sterbegeld has ~€1.80/month independent of coverage).

For each data point:
1. Navigate to the calculator start URL (fresh start)
2. Dismiss cookie banner if it reappears
3. Fill ALL fields with the test values. Use realistic German data for non-varied fields:
   - Primary: Anna Schmidt, Beispielstr. 12, 80331 München, deutsch, geb. 15.03.1990
   - Alternative: Thomas Weber, Hauptstr. 45, 50667 Köln, deutsch, geb. 08.11.1978
4. Navigate through all steps to the price display
5. Record: all input values + displayed monthly price + tier name
6. If the price page shows all tiers at once, record ALL tier prices (saves restarts)
7. Start fresh for the next data point

**Beitragstabelle note**: Of the 7 products researched (Zahnzusatz, Sterbegeld, Risikoleben, Hausrat, Rechtsschutz, Unfall, Pflegezusatz), only Zahnzusatz had a Beitragstabelle dialog. None of the other 6 had one. Still check (10-second effort), but don't count on it.

**Timing**: Wait 5 seconds between page loads:
```bash
playwright-cli -s={{PRODUCT_ID}} eval "await new Promise(r => setTimeout(r, 5000))"
```

**Error recovery**: If a data point fails after 2 retries, log it as failed in price-matrix.json and move on:
```json
{ "inputs": {...}, "output": null, "error": "description of failure" }
```

### Save raw data

Write to `research/{{PRODUCT_ID}}/price-matrix.json`:
```json
{
  "product": "{{PRODUCT_ID}}",
  "sampled_at": "YYYY-MM-DD",
  "source_url": "{{CALCULATOR_URL}}",
  "ergo_tier_names": {
    "tier1": "Basis",
    "tier2": "Smart",
    "tier3": "Best"
  },
  "tier_mapping": {
    "tier1": "grundschutz",
    "tier2": "komfort",
    "tier3": "premium"
  },
  "data_points": [
    {
      "inputs": {
        "age": 30,
        "coverage": 1500,
        "tier": "komfort",
        "risk_class": null,
        "payment_mode": "monthly"
      },
      "output": {
        "monthly_price": 18.90,
        "annual_price": null,
        "additional_notes": ""
      }
    }
  ]
}
```

## Phase C: Analysis (~3 min)

No browser needed for this phase. Close the browser:
```bash
playwright-cli -s={{PRODUCT_ID}} close
```

### Derive pricing parameters (use Python — do NOT estimate manually)

Write and execute a Python script at `research/{{PRODUCT_ID}}/fit_pricing.py`:

```bash
# Install numpy if needed
pip3 install numpy 2>/dev/null

# Write the script, then run it:
python3 research/{{PRODUCT_ID}}/fit_pricing.py
```

The script should:
1. Load `price-matrix.json`
2. Group data by tier, filter to reference risk class
3. **Multi-model fitting** (try ALL of these, report R² for each):
   a. Quadratic polynomial: `numpy.polyfit(t, prices, 2)`
   b. Cubic polynomial: `numpy.polyfit(t, prices, 3)`
   c. Exponential: `price = a * exp(b * age)` — needed for mortality/care products
   d. Piecewise/step function detection: for each pair of adjacent age samples, compute price ratio. If ratio is near-constant across most ages but has a sharp jump at one age threshold, this is a step function (Unfall: exact 2.0× jump at age 65)
   e. Age band detection: compute price variance within 5-year age bands — if near-zero within bands but jumps between bands, ERGO uses discrete age bands (Zahnzusatz: 6 flat bands)
4. **Check if pricing is age-independent**: If all age samples produce the same price (±1%), the product has no age curve (Rechtsschutz). Report "flat" and check for youth/senior discounts.
5. **Check tier relationship**:
   a. Multiplicative: compute ratio between tiers at each age — if constant (±5%), report multiplier
   b. Additive: compute difference between tiers at each age — if constant (±5%), report fixed delta (Hausrat: Best = Smart + €3.39)
   c. Age-dependent: if neither is constant, report the range and recommend lookup table
6. **Check if "tiers" are actually separate products**: If different "tiers" have completely different age curves, coverage models, or calculators, they may be separate products (Pflegezusatz: PTG is age-dependent, PZU/KFP are fixed-price). Note this in the output.
7. **Check for Baustein/module pricing**: If the product has toggleable modules (legal areas, coverage add-ons) that each add a fixed price, check if prices are perfectly additive (Rechtsschutz: 0.00 error). Report per-module prices.
8. **Check risk class multipliers at multiple ages** — if multiplier varies >10% across ages, it's age-dependent (Risikoleben smoker: 1.87-3.92×). Report per-age multipliers.
9. **Check for fixed fee**: Compare price at min coverage vs. extrapolated zero-coverage intercept. If non-zero, report fixed fee component (Sterbegeld: ~€1.80, Risikoleben: ~€0.91).
10. Derive base rates per tier (price at reference age / units)
11. Output results as JSON to `research/{{PRODUCT_ID}}/fit_results.json`

**Template selection** (include in output — 6 options):
- **Template A** (polynomial): Quadratic R² > 0.96, constant tier multipliers, coverage-proportional
- **Template A+step** (step function): Discrete age bands with sharp threshold (e.g., 1.0×/2.0× at age 65)
- **Template B** (lookup table): Quadratic R² < 0.96, or risk multipliers age-dependent, or exponential growth
- **Template C** (property/additive): Additive tier difference, per-m² or regional pricing
- **Template D** (flat-rate configurator): No age curve, no coverage slider, additive Baustein/module toggles
- **Template E** (Kfz-specific): Additive components (HP+VK) with separate SF lookup tables, no age curve

Use `/tmp/ergo-research-venv/bin/python3` (numpy already available in venv).

The script produces `research/{{PRODUCT_ID}}/fit_results.json` which you read to write the analysis.

### Write analysis

Write to `research/{{PRODUCT_ID}}/analysis.md`:
```markdown
# ERGO {{PRODUCT_NAME}} — Pricing Analysis

## Derived Parameters
- Base rates: Grundschutz €X.XX, Komfort €X.XX, Premium €X.XX (per [unit])
- Age curve: base=X.XX, linear=X.XX, quadratic=X.XX
- Age curve R²: X.XX
- Risk class multipliers: [class]: [multiplier], ...
- Loading estimate: XX%

## Comparison with Our Assumptions
| Parameter | Our value | ERGO actual | Delta |
|-----------|-----------|-------------|-------|
| Komfort base rate | €X.XX | €X.XX | ±X% |
| Age curve base | X.XX | X.XX | ±X |
| ...

## Data Quality
- Total data points: N
- Age curve fit R²: X.XX
- Confidence: HIGH | MEDIUM | LOW
- Notes: [any anomalies, missing data, or concerns]

## Non-polynomial patterns
[If ERGO uses age bands, breakpoints, or other non-polynomial pricing, document it here.
This is important — our pricing model assumes a smooth polynomial. If ERGO uses discrete bands,
we should note this as a limitation and suggest an enhancement to pricing-model.md.]
```

### Produce the updated products.md entry

Write the corrected product entry to `research/{{PRODUCT_ID}}/products-entry.md` in the EXACT format specified by `shared/product-schema.md`. Include the Source section:

```markdown
**Source**: ergo.de — researched YYYY-MM-DD
**Evidence**: research/{{PRODUCT_ID}}/screenshots/, research/{{PRODUCT_ID}}/price-matrix.json
**Confidence**: HIGH | MEDIUM | LOW
**Discrepancies from previous entry**: [what changed and why]
```

## Report back

Return this format:

```
RESEARCH_REPORT:
  PRODUCT: {{PRODUCT_ID}}
  STATUS: SUCCESS | PARTIAL | FAILED
  
  CALCULATOR_URL: <confirmed URL>
  CALCULATOR_TYPE: wizard | single-page | configurator
  
  STRUCTURE:
    Steps: N
    Fields: N
    Risk classes: [list or "none"]
    Tiers: [ERGO's tier names] → [our mapping]
  
  PRICING:
    Data points collected: N
    Age curve R²: X.XX
    Derived Komfort base rate: €X.XX (ours was €X.XX, delta ±X%)
    Risk class multipliers: [list]
    Loading estimate: XX%
    Confidence: HIGH | MEDIUM | LOW
  
  KEY_DIFFERENCES:
    - [what ERGO does differently from our assumption]
    - ...
  
  MISSING_FROM_OUR_MODEL:
    - [fields ERGO collects that we don't have]
    - [pricing factors we don't model]
    - ...
  
  UPDATED_ENTRY: See research/{{PRODUCT_ID}}/products-entry.md
```

## Critical rules

- Use `-s={{PRODUCT_ID}}` for ALL playwright-cli commands (named session for parallel support)
- Wait 3-5 seconds between page loads to avoid rate limiting
- Use realistic German test data for non-varied fields (names, addresses)
- If the calculator requires JavaScript interaction (React/SPA), use playwright-cli snapshot to find element refs
- If blocked by CAPTCHA or rate limiting, report PARTIAL with what you got
- All documentation in English (this is internal research, not user-facing)
- Save ALL screenshots — they're evidence for the client
- Close your browser session when done: `playwright-cli -s={{PRODUCT_ID}} close`
```

---

## How the team lead uses this

```python
# Pseudocode for dispatching research agents

for product in research_queue:
    prompt = TEMPLATE
        .replace("{{PRODUCT_ID}}", product.id)
        .replace("{{PRODUCT_NAME}}", product.name)
        .replace("{{CALCULATOR_URL}}", product.url)
        .replace("{{AGE_DEPENDENT}}", str(product.category in ["person", "animal"]))
        .replace("{{AGE_SAMPLES}}", product.age_samples)
        .replace("{{COVERAGE_SAMPLES}}", product.coverage_samples)
    
    result = spawn_agent(
        prompt=prompt,
        model="opus",
        description=f"Research ERGO {product.name}"
    )
```

### Parallel dispatch (up to 3)

```python
# Launch 3 at a time, each with its own playwright-cli session
batch = research_queue[:3]
agents = [spawn_agent(prompt=fill(p), model="opus", run_in_background=True) for p in batch]
# As each completes, spawn reviewer + start next product
```
