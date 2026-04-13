#!/usr/bin/env python3
"""
ERGO Wohngebäudeversicherung — Pricing Analysis
Analyzes collected data points to reverse-engineer the pricing model.
"""

import json
import numpy as np

# Load data
with open("/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/research/wohngebaeude/price-matrix.json") as f:
    data = json.load(f)

points = data["data_points"]

print("=" * 70)
print("ERGO Wohngebäudeversicherung — Pricing Analysis")
print("=" * 70)

# ============================================================
# 1. TIER RATIO ANALYSIS
# ============================================================
print("\n### 1. Tier Ratio (Best / Smart)")
ratios = []
for p in points:
    if p["best_annual"] and p["smart_annual"]:
        ratio = p["best_annual"] / p["smart_annual"]
        ratios.append(ratio)
        print(f"  DP{p['id']:2d}: Smart={p['smart_annual']:8.2f}  Best={p['best_annual']:8.2f}  ratio={ratio:.4f}")

ratios = np.array(ratios)
print(f"\n  Mean ratio:   {ratios.mean():.4f}")
print(f"  Std ratio:    {ratios.std():.6f}")
print(f"  Min/Max:      {ratios.min():.4f} / {ratios.max():.4f}")
print(f"  => Tier uplift is CONSTANT at ~{(ratios.mean()-1)*100:.1f}%")

TIER_RATIO = ratios.mean()

# ============================================================
# 2. DEDUCTIBLE ANALYSIS (München, 120m², year 2000)
# ============================================================
print("\n### 2. Deductible Factors")
sb_data = [(p["deductible"], p["smart_annual"], p["best_annual"])
           for p in points if p["plz"] == "80331" and p["sqm"] == 120
           and p["construction_year"] == 2000 and p["best_annual"]]

sb_base = [d for d in sb_data if d[0] == 0][0]
print(f"  Base (ohne SB): Smart={sb_base[1]:.2f}, Best={sb_base[2]:.2f}")

for sb, smart, best in sorted(sb_data):
    sf = smart / sb_base[1]
    bf = best / sb_base[2]
    print(f"  SB {sb:5d}€: Smart={smart:8.2f} ({sf:.3f})  Best={best:8.2f} ({bf:.3f})")

print(f"\n  SB factors: ohne=1.000, 500€=0.850, 1000€=0.800")

# ============================================================
# 3. M² ANALYSIS (München, year 2000, SB 500€)
# ============================================================
print("\n### 3. m² Pricing Analysis")
sqm_data = [(p["sqm"], p["smart_annual"], p["best_annual"])
            for p in points if p["plz"] == "80331"
            and p["construction_year"] == 2000 and p["deductible"] == 500
            and p["best_annual"]]

sqm_data.sort()
print("  SQM  | Smart   | Best    | Smart/m² | Best/m²")
print("  " + "-" * 50)
for sqm, smart, best in sqm_data:
    print(f"  {sqm:4d} | {smart:7.2f} | {best:7.2f} | {smart/sqm:8.3f} | {best/sqm:7.3f}")

# Fit linear model: price = a * sqm + b
sqm_arr = np.array([s[0] for s in sqm_data])
smart_arr = np.array([s[1] for s in sqm_data])
best_arr = np.array([s[2] for s in sqm_data])

# Linear fit
smart_coeffs = np.polyfit(sqm_arr, smart_arr, 1)
best_coeffs = np.polyfit(sqm_arr, best_arr, 1)

print(f"\n  Linear fit (Smart): {smart_coeffs[0]:.4f} * sqm + {smart_coeffs[1]:.2f}")
print(f"  Linear fit (Best):  {best_coeffs[0]:.4f} * sqm + {best_coeffs[1]:.2f}")

# Check fit quality
smart_pred = np.polyval(smart_coeffs, sqm_arr)
best_pred = np.polyval(best_coeffs, sqm_arr)
smart_r2 = 1 - np.sum((smart_arr - smart_pred)**2) / np.sum((smart_arr - np.mean(smart_arr))**2)
best_r2 = 1 - np.sum((best_arr - best_pred)**2) / np.sum((best_arr - np.mean(best_arr))**2)

print(f"  R² (Smart): {smart_r2:.6f}")
print(f"  R² (Best):  {best_r2:.6f}")

# Per-m² rate
print(f"\n  Smart rate per m²: {smart_coeffs[0]:.4f} €/m²/yr")
print(f"  Best rate per m²:  {best_coeffs[0]:.4f} €/m²/yr")
print(f"  Intercept (Smart): {smart_coeffs[1]:.2f} €/yr (base charge)")
print(f"  Intercept (Best):  {best_coeffs[1]:.2f} €/yr (base charge)")

# Also try quadratic
smart_coeffs2 = np.polyfit(sqm_arr, smart_arr, 2)
smart_pred2 = np.polyval(smart_coeffs2, sqm_arr)
smart_r2_q = 1 - np.sum((smart_arr - smart_pred2)**2) / np.sum((smart_arr - np.mean(smart_arr))**2)
print(f"\n  Quadratic fit R² (Smart): {smart_r2_q:.6f} (marginal improvement = {(smart_r2_q-smart_r2)*100:.3f}%)")

# Residuals
print("\n  Linear residuals (Smart):")
for sqm, actual, pred in zip(sqm_arr, smart_arr, smart_pred):
    print(f"    {int(sqm):4d}m²: actual={actual:.2f}  pred={pred:.2f}  err={actual-pred:+.2f} ({(actual-pred)/actual*100:+.1f}%)")

# ============================================================
# 4. REGIONAL FACTORS
# ============================================================
print("\n### 4. Regional Factors (120m², year 2000, SB 500€)")
regional = [(p["plz"], p["city"], p["smart_annual"])
            for p in points if p["sqm"] == 120
            and p["construction_year"] == 2000 and p["deductible"] == 500
            and p["smart_annual"]]

muc_smart = [r for r in regional if r[1] == "München"][0][2]
print(f"  Reference: München = {muc_smart:.2f}")
print()
for plz, city, smart in sorted(regional, key=lambda x: x[2]):
    factor = smart / muc_smart
    print(f"  {plz} {city:10s}: Smart={smart:7.2f}  factor={factor:.4f}")

# ============================================================
# 5. CONSTRUCTION YEAR ANALYSIS
# ============================================================
print("\n### 5. Construction Year Factors (München, 120m², SB 500€)")
year_data = [(p["construction_year"], p["smart_annual"], p["best_annual"])
             for p in points if p["plz"] == "80331" and p["sqm"] == 120
             and p["deductible"] == 500 and p["best_annual"]
             and p["construction_year"] != 2000]  # exclude base

# Add year 2000 base
year_data.append((2000, 681.44, 746.40))
year_data.sort()

muc_smart_2000 = 681.44
print(f"  Reference: year 2000 = {muc_smart_2000:.2f} (Smart)")
print()
for year, smart, best in year_data:
    factor = smart / muc_smart_2000
    print(f"  {year}: Smart={smart:7.2f}  factor={factor:.4f}  {'<-- SAME' if year in [1960, 1980] else ''}")

# Test for year bands
print("\n  Year band hypothesis:")
print("  Band 1: <= ~2000 -> factor ~1.068")
print("  Band 2: ~2001-2010 -> factor ~0.830 (interpolated)")
print("  Band 3: >= ~2010 -> factor decreasing with newer construction")
print()
print("  Note: 1960 and 1980 give IDENTICAL prices, suggesting pre-2000")
print("  houses are grouped together in a single band.")

# ============================================================
# 6. COMBINED PRICING MODEL
# ============================================================
print("\n### 6. Combined Pricing Model")
print()
print("  The ERGO Wohngebäudeversicherung pricing model consists of:")
print()
print("  PRICE = base_rate_per_sqm * sqm * regional_factor * year_factor * sb_factor * tier_factor")
print()
print("  Or equivalently (with intercept):")
print(f"  Smart(ohne SB) = {smart_coeffs[0]/0.85:.3f} * sqm + {smart_coeffs[1]/0.85:.1f}")
print(f"  With regional and year adjustments applied as multipliers.")
print()

# Compute the effective "ohne SB" linear model
# We measured with SB=500 which is factor 0.85
# So ohne SB = measured / 0.85
smart_ohne_slope = smart_coeffs[0] / 0.85
smart_ohne_intercept = smart_coeffs[1] / 0.85

print(f"  Base formula (Smart, ohne SB, München, year 2000):")
print(f"    price = {smart_ohne_slope:.3f} * sqm + {smart_ohne_intercept:.1f}")
print()
print(f"  Tier factor: Smart=1.000, Best={TIER_RATIO:.4f}")
print(f"  SB factors: ohne=1.000, 500€=0.850, 1000€=0.800")
print()
print(f"  Regional factors (vs München):")
for plz, city, smart in sorted(regional, key=lambda x: x[2]):
    factor = smart / muc_smart
    print(f"    {plz} {city:10s}: {factor:.4f}")
print()
print(f"  Year factors (vs 2000):")
for year, smart, best in year_data:
    factor = smart / muc_smart_2000
    print(f"    {year}: {factor:.4f}")

# ============================================================
# 7. CROSS-VALIDATION
# ============================================================
print("\n### 7. Cross-Validation")
print("  Testing model predictions against observed data:")
print()

errors = []
for p in points:
    if p["smart_annual"] is None:
        continue

    sqm = p["sqm"]
    year = p["construction_year"]
    plz = p["plz"]
    sb = p["deductible"]

    # Base prediction (Smart, München, year 2000, SB 500€)
    pred_base = smart_coeffs[0] * sqm + smart_coeffs[1]

    # Regional factor
    reg_factors = {
        "80331": 1.000,
        "54290": 678.87 / 681.44,  # Trier
        "50667": 797.20 / 681.44,  # Köln
        "10117": 596.01 / 681.44,  # Berlin
    }
    reg_f = reg_factors.get(plz, 1.0)

    # Year factor (from observed data at 120m², interpolated)
    year_factors = {1960: 1.068, 1980: 1.068, 2000: 1.000, 2010: 0.830, 2020: 0.660}
    yr_f = year_factors.get(year, 1.0)

    # SB factor
    sb_factors = {0: 1/0.85, 500: 1.0, 1000: 0.800/0.850}
    sb_f = sb_factors.get(sb, 1.0)

    # Only apply regional and year factors for non-baseline comparisons
    if sqm != 120 or year != 2000 or plz != "80331":
        pred_smart = pred_base * reg_f * yr_f * sb_f
    else:
        pred_smart = pred_base * sb_f

    actual = p["smart_annual"]
    err_pct = (pred_smart - actual) / actual * 100
    errors.append(abs(err_pct))

    print(f"  DP{p['id']:2d}: actual={actual:8.2f}  pred={pred_smart:8.2f}  err={err_pct:+5.1f}%")

print(f"\n  Mean absolute error: {np.mean(errors):.1f}%")
print(f"  Max absolute error:  {np.max(errors):.1f}%")

# ============================================================
# 8. TEMPLATE CLASSIFICATION
# ============================================================
print("\n### 8. Template Classification")
print()
print("  This product uses a UNIQUE template not seen in previous products.")
print("  Closest match: Template C (like Hausrat) but with key differences:")
print()
print("  SIMILARITIES to Hausrat (Template C):")
print("  - m²-based pricing (not coverage value)")
print("  - 2 tiers (Smart/Best)")
print("  - Regional multipliers")
print("  - Address-specific (ZIP + street + house number)")
print()
print("  DIFFERENCES from Hausrat:")
print("  - No age/birthday field at all")
print("  - Construction year is a major pricing factor")
print("  - Building characteristics (roof, floors, basement) affect price")
print("  - Separate peril toggles (Feuer, LW, Sturm/Hagel, Elementar)")
print("  - Linear price model (not pure per-m² like Hausrat)")
print("  - Has a meaningful intercept (base charge per building)")
print()
print("  PROPOSED: Template C-WG (Wohngebäude variant of Template C)")
print("  Formula: (slope * sqm + intercept) * region * year * sb * tier")


if __name__ == "__main__":
    print("\n\n=== DONE ===")
