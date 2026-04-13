# ERGO Zahnzusatzversicherung — Pricing Analysis

## Derived Parameters

- **Base rates** (flat/month at age 35, assuming 22% loading):
  - Grundschutz (DS75): €14.26
  - Komfort (DS90): €17.79
  - Premium (DS100): €22.62
- **Age curve**: base=0.1270, linear=3.0809, quadratic=-0.5156
- **Age curve R²**: 0.9974 (at band midpoints only — see "Non-polynomial patterns")
- **Tier ratios**: DS75 ≈ 62% of DS100, DS90 ≈ 78% of DS100 (constant across age bands)
- **Loading**: Unknown (22% assumed for parameter derivation)

## Comparison with Our Assumptions

| Parameter | Our value | ERGO actual | Delta | Severity |
|-----------|-----------|-------------|-------|----------|
| **Pricing model** | Per €250/year unit | **FLAT RATE** | Structural mismatch | **CRITICAL** |
| **Coverage selection** | Slider €500–€5,000 | **None** (tariff = reimbursement %) | Structural mismatch | **CRITICAL** |
| **Grundschutz base** | €2.70/unit | €14.26 flat | N/A (different units) | N/A |
| **Komfort base** | €3.29/unit | €17.79 flat | N/A | N/A |
| **Premium base** | €4.05/unit | €22.62 flat | N/A | N/A |
| **Age curve base** | 0.80 | 0.1270 | −0.67 | **HIGH** |
| **Age curve linear** | 0.35 | 3.0809 | +2.73 | **HIGH** |
| **Age curve quadratic** | 0.10 | −0.5156 | −0.62 | **HIGH** |
| **Age shape** | Gentle linear increase | Nearly linear, steep | Shape wrong | **HIGH** |
| **Calibration age 35** | ~€22/month (6 units × per-unit) | €21.70 (flat rate) | −1.4% | OK |
| **Price at age 20** | ~€19.56 (per-unit) | €3.70 | **+429%** | **CRITICAL** |
| **Price at age 60** | ~€26.78 (per-unit) | €44.40 | **−40%** | **CRITICAL** |
| **Dental status field** | Yes (Sehr gut / Gut / etc.) | **Not present** | Extra field we invented | MEDIUM |
| **Missing teeth field** | Yes (0-10) | **Not present** | Extra field we invented | MEDIUM |
| **Risk class** | None (correct) | None | ✓ Match | — |
| **Waiting period** | Grundschutz: 8mo, Komfort: 3mo, Premium: none | **No waiting period** | Wrong | MEDIUM |
| **Tiers** | Benefit-differentiated | **Reimbursement %-differentiated** | Structural | MEDIUM |

## Data Quality

- **Total data points**: 28 (10 calculator-verified, 18 from official Beitragstabelle)
- **Age curve fit R²**: 0.9974 (at 6 band midpoints)
- **Confidence**: **HIGH** for pricing data (official Beitragstabelle + calculator verification)
- **Confidence**: **MEDIUM** for polynomial parameters (smooth curve doesn't capture band jumps)
- **Notes**:
  - Prices are identical within a band (verified: ages 42 and 48 both return €41.30)
  - All 3 tariffs verified at age 35 against Beitragstabelle — 100% match
  - Calculator flow verified end-to-end through all wizard steps

## Non-polynomial Patterns

**ERGO uses discrete age bands, NOT a polynomial curve.**

| Age Band | DS90 Price | Polynomial prediction | Error |
|----------|-----------|----------------------|-------|
| 0–20     | €3.70     | €5.09 (at age 20)    | +37.5% |
| 21–25    | €7.20     | €10.80 (at age 25)   | +50.0% |
| 26–30    | €13.80    | €16.33 (at age 30)   | +18.4% |
| 31–40    | €21.70    | €21.70 (at age 35)   | 0.0% (calibrated) |
| 41–50    | €32.50    | €31.91 (at age 45)   | −1.8% |
| 51+      | €44.40    | €45.94 (at age 60)   | +3.5% |

**The polynomial is a poor approximation at band boundaries.**
- At age 20 (top of 0-20 band), the polynomial predicts €5.09 but ERGO charges only €3.70
- At age 40 (top of 31-40 band), the polynomial predicts €26.89 but ERGO still charges €21.70
- The R² of 0.9974 is misleading because it only measures fit at 6 midpoints

**Recommendation for pricing-model.md**: Add support for a "band" pricing mode:
```
ageFactor = lookup_band(age, bands)
```
Where `bands` is a list of `{max_age, factor}` pairs. This would model ERGO's pricing exactly.

## Root Cause of Our Pricing Error

Our model assumed Zahnzusatz works like person-based insurance (continuous age curve, per-coverage-unit pricing). In reality:

1. **ERGO's tariffs ARE the coverage tiers** — DS75/DS90/DS100 = 75%/90%/100% reimbursement. There is no adjustable coverage amount.
2. **Pricing is flat per age band** — a step function, not a smooth polynomial
3. **The product is much cheaper for young people** than we assumed (€3.70 vs €19.56 at age 20)
4. **The product is much more expensive for older people** than we assumed (€44.40 vs €26.78 at age 60)
5. **Our per-unit model creates an artificial coverage slider** that ERGO doesn't have

This matters because our demo currently shows a coverage budget slider (€500–€5,000) that doesn't correspond to anything in ERGO's actual product.
