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

```markdown
**Base rates** (per €Xk/month): Grundschutz €A.AA, Komfort €B.BB, Premium €C.CC
**Age curve**: base=X.XX, linear=X.XX, quadratic=X.XX (description of shape)
**Loading**: XX%
**Calibration**: [typical customer profile] → ~€XX/month ✓
```

The calibration line is CRITICAL — it's the sanity check. The formula with the stated base rates, age curve, and loading MUST produce a price within 5% of the calibration target for the stated customer profile.

For flat-rate products, add: `(coverageUnit=defaultCoverage so units=1)` after the base rates.

### 4. Tiers

```markdown
**Tiers**:
- **Grundschutz**: [benefits, waiting period, limitations]
- **Komfort**: [benefits, improvements over Grundschutz]
- **Premium**: [benefits, improvements over Komfort]
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
3. [ ] Base rates produce calibration target price (within 5%)
4. [ ] Grundschutz < Komfort < Premium pricing
5. [ ] Age curve produces positive values across the entire age range
6. [ ] Risk class multipliers are in 0.5–3.0 range
7. [ ] Tier benefits meaningfully differentiate (not just price)
8. [ ] Wizard steps include at least: risk input → coverage → plan selection → personal data → summary
9. [ ] Form fields cover all data needed for the Supabase table columns
