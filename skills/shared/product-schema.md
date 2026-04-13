# Product Entry Schema

This is the canonical format for a product entry in `tariff-designer/references/products.md`. The ergo-researcher MUST output entries in this exact format. The tariff-designer and demo-factory read this format.

All three skills share this contract. If you change the format here, update all three skills.

---

## Required sections (in order)

Every product entry MUST have these sections in this exact order:

### 1. Header

```markdown
## N. Full German Product Name (English Name)
```

N = sequential number. Used for reference only.

### 2. Parameter table

```markdown
| Parameter | Value |
|-----------|-------|
| **ID** | kebab-case-id |
| **Category** | person | property | liability | animal | travel |
| **Insured event** | what triggers payout |
| **Age range** | min–max |
| **Coverage** | €min–€max, step €step, default €default |
| **Coverage unit** | per €X or "flat rate (coverageUnit=defaultCoverage so units=1)" |
| **Risk class** | Field name: Class1 (multiplier), Class2 (multiplier), ... OR "None" |
| **Payment duration** | formula (e.g., "85 − age", "67 − age", "Annual renewal", "Ongoing") |
| **Waiting period** | Grundschutz: X, Komfort: Y, Premium: Z |
```

### 3. Pricing line

Choose the format that matches the product's pricing template (see pricing-model.md):

**Template A (polynomial — most products):**
```markdown
**Base rates** (per €Xk/month): Grundschutz €A.AA, Komfort €B.BB, Premium €C.CC
**Age curve**: base=X.XX, linear=X.XX, quadratic=X.XX (description of shape)
**Loading**: XX%
**Calibration**: [typical customer profile] → ~€XX/month ✓
```

**Template B (lookup table — exponential age curves):**
```markdown
**Pricing model: Lookup table** (age curve too steep for polynomial — quadratic R²=X.XX)
**Reference prices (€Xk, Xyr, reference risk class, monthly):**
[lookup table with ages × tiers]
**Risk class multipliers**: [per-age if age-dependent]
**Calibration**: [typical customer profile] → €XX.XX/month ✓
```

**Template A+step (step-function age bands — e.g., Unfall):**
```markdown
**Base rates** (per €Xk/month, reference risk class, under-threshold): Tier1 €A.AA, Tier2 €B.BB, Tier3 €C.CC
**Age curve**: Step function — [threshold age]: multiplier [X.X]× (e.g., "under-65: 1.0×, 65+: 2.0×")
**Risk class multipliers**: [class: mult, ...] — constant or age-dependent?
**Coverage scaling**: Linear (R²=X.XX) [with/without] fixed fee
**Calibration**: [typical profile] → €XX.XX/month ✓
```

**Template C (property/additive — per-m² products):**
```markdown
**Pricing model: Linear per-m² with ADDITIVE tier difference:**
[formula per tier]
**Regional multipliers**: [ZIP → multiplier table]
**Factor multipliers**: [floor, building type, age, deductible, contract]
**Calibration**: [typical property profile] → Tier1 €XX.XX, Tier2 €XX.XX ✓
```

**Template D (flat-rate configurator — additive Baustein/module pricing):**
```markdown
**Pricing model: Template D** (flat-rate additive configurator — no age curve, no coverage slider)
**Baustein base rates** (reference config, monthly):
[table of Baustein × tier prices]
**Pricing formula**: `price = bausteinSum × familyMult × sbDiscount × contractDiscount × youthDiscount`
**Factor multipliers**: [family, SB, contract, youth/senior]
**Calibration**: [typical config] → €XX.XX/month ✓
```

The calibration line is CRITICAL — it's the sanity check. The formula with the stated parameters MUST produce a price within 5% of the calibration target for the stated customer profile.

For flat-rate products, add: `(coverageUnit=defaultCoverage so units=1)` after the base rates.

### 4. Tiers

Products may have 2 tiers, 3 tiers, or no tiers (separate products). Use the format that matches ERGO's actual structure:

**3-tier products:**
```markdown
**Tiers**:
- **Grundschutz**: [benefits, waiting period, limitations]
- **Komfort**: [benefits, improvements over Grundschutz]
- **Premium**: [benefits, improvements over Komfort]
```

**2-tier products (e.g., Hausrat, Rechtsschutz):**
```markdown
**Note — Only 2 tiers**: ERGO [Product] has 2 tiers ([Name1]/[Name2]), NOT 3.
**Tiers** (ERGO names: [Name1] / [Name2]):
- **[Name1]** (→ grundschutz): [benefits]
- **[Name2]** (→ komfort): [benefits]
```

**Separate products, not tiers (e.g., Pflegezusatz):**
```markdown
**Note — Not tiers**: ERGO offers [N] **separate products**, not tiers of one product:
- **[Product1]** — [pricing model, age-dependent/fixed, description]
- **[Product2]** — [pricing model, fixed price €XX.XX, description]
- **[Product3]** — [pricing model, fixed price €XX.XX, description]
```

**3-tier with ERGO-specific names (e.g., Unfall: Basic/Smart/Best):**
```markdown
**Note — ERGO tier names**: [Name1] / [Name2] / [Name3] (not Grundschutz/Komfort/Premium). Keep ERGO's names.
**Tiers** (ERGO names):
- **[Name1]**: [benefits]
- **[Name2]**: [benefits]
- **[Name3]**: [benefits]
```

### 5. Wizard steps

```markdown
**Wizard steps**: Step1 → Step2 → Step3 → ... → Summary
```

### 6. Form fields

```markdown
**Form fields**: field1, field2 (type: description), field3, ...
```

### 7. Validation (if applicable)

```markdown
**Validation**: age range, field1 required, field2 pattern, ...
```

---

## Optional sections

### Source (added by ergo-researcher)

```markdown
**Source**: ergo.de — researched YYYY-MM-DD
**Evidence**: research/product-id/screenshots/, research/product-id/price-matrix.json
**Confidence**: HIGH | MEDIUM | LOW
**Discrepancies from previous entry**: [what changed and why]
```

This section is added by the ergo-researcher when it updates an entry based on real ERGO data. It provides traceability — you can see where the data came from and how confident the research is.

---

## Pricing parameter constraints

The pricing formula is:
```
monthlyPremium = baseRate × coverageUnits × ageFactor × riskClassMultiplier × paymentModeDiscount × (1 + loading)
ageFactor = base + linear × t + quadratic × t²
t = (age - minAge) / (maxAge - minAge)
```

Constraints for valid entries:
- `base` should be > 0 (the age factor at minimum age)
- `base + linear + quadratic` = the age factor at maximum age (should be > 0)
- `loading` between 0.15 and 0.35 (15-35% is realistic for German market)
- Base rates: Grundschutz < Komfort < Premium (always)
- Flat-rate products: ageCurve should be base=1.0, linear=0.0, quadratic=0.0

---

## Validation checklist

Before accepting a product entry (whether from ergo-researcher or manual creation):

1. [ ] All required sections present
2. [ ] ID is unique and kebab-case
3. [ ] Pricing template identified (A=polynomial, B=lookup, C=property)
4. [ ] Calibration target price matches within 5% using stated parameters
5. [ ] Tier pricing order: cheapest tier < most expensive tier
6. [ ] For Template A: Age curve produces positive values across entire age range
7. [ ] For Template B: Lookup table covers the full age range at 5-year intervals
8. [ ] For Template C: Regional multipliers sampled for at least 5 ZIP codes
9. [ ] Risk class multipliers in 0.5–4.0 range (extended from 3.0 — Risikoleben smoker reaches 3.92×)
10. [ ] If risk multipliers are age-dependent, per-age values documented
11. [ ] Tier benefits meaningfully differentiate (not just price)
12. [ ] Wizard steps match ERGO's actual flow (verified via screenshots)
13. [ ] Form fields cover all data needed for the Supabase table columns
14. [ ] Tier count matches ERGO (2 or 3 — don't assume 3)
