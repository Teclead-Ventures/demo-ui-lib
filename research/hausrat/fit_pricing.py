#!/usr/bin/env python3
"""
Analyze ERGO Hausratversicherung pricing data to derive base rates,
regional multipliers, and pricing model parameters.
"""

import json
import numpy as np

# Load data
with open("research/hausrat/price-matrix.json") as f:
    data = json.load(f)

print("=" * 60)
print("ERGO HAUSRATVERSICHERUNG PRICING ANALYSIS")
print("=" * 60)

# ============================================================
# 1. COVERAGE LINEARITY
# ============================================================
print("\n1. COVERAGE LINEARITY (München 80331)")
print("-" * 40)

coverage_data = data["coverage_linearity_data"]
m2_values = [d["inputs"]["m2"] for d in coverage_data]
coverage_values = [d["output"]["coverage"] for d in coverage_data]
smart_prices = [d["output"]["smart_monthly"] for d in coverage_data]
best_prices = [d["output"]["best_monthly"] for d in coverage_data]

# Check linearity: fit linear model price = a * m2 + b
m2_arr = np.array(m2_values)
smart_arr = np.array(smart_prices)
best_arr = np.array(best_prices)

# Linear fit for Smart
coeffs_smart = np.polyfit(m2_arr, smart_arr, 1)
smart_predicted = np.polyval(coeffs_smart, m2_arr)
ss_res_smart = np.sum((smart_arr - smart_predicted) ** 2)
ss_tot_smart = np.sum((smart_arr - np.mean(smart_arr)) ** 2)
r2_smart = 1 - ss_res_smart / ss_tot_smart

# Linear fit for Best
coeffs_best = np.polyfit(m2_arr, best_arr, 1)
best_predicted = np.polyval(coeffs_best, m2_arr)
ss_res_best = np.sum((best_arr - best_predicted) ** 2)
ss_tot_best = np.sum((best_arr - np.mean(best_arr)) ** 2)
r2_best = 1 - ss_res_best / ss_tot_best

print(f"Smart: price = {coeffs_smart[0]:.4f} * m2 + {coeffs_smart[1]:.4f}  (R²={r2_smart:.6f})")
print(f"Best:  price = {coeffs_best[0]:.4f} * m2 + {coeffs_best[1]:.4f}  (R²={r2_best:.6f})")

# Per-m2 rate
print(f"\nSmart rate per m²: €{coeffs_smart[0]:.4f}/month")
print(f"Best rate per m²:  €{coeffs_best[0]:.4f}/month")

# Per €5000 coverage rate (our model uses this)
# Coverage = 650 * m2, so €5000 = 5000/650 = 7.692 m2
rate_per_5k_smart = coeffs_smart[0] * (5000 / 650)
rate_per_5k_best = coeffs_best[0] * (5000 / 650)
print(f"\nSmart rate per €5k coverage: €{rate_per_5k_smart:.4f}/month")
print(f"Best rate per €5k coverage:  €{rate_per_5k_best:.4f}/month")

# Check actual data points
print("\nActual vs Predicted (Smart):")
for i, m2 in enumerate(m2_values):
    pred = coeffs_smart[0] * m2 + coeffs_smart[1]
    print(f"  {m2}m²: actual={smart_prices[i]:.2f}, predicted={pred:.2f}, diff={smart_prices[i]-pred:+.2f}")

print("\nActual vs Predicted (Best):")
for i, m2 in enumerate(m2_values):
    pred = coeffs_best[0] * m2 + coeffs_best[1]
    print(f"  {m2}m²: actual={best_prices[i]:.2f}, predicted={pred:.2f}, diff={best_prices[i]-pred:+.2f}")

# ============================================================
# 2. TIER RATIO
# ============================================================
print("\n\n2. TIER RATIO (Best/Smart)")
print("-" * 40)

# Use all regional data where we have both tiers
for dp in data["regional_data_points"]:
    city = dp["inputs"]["city"]
    smart = dp["output"]["smart_monthly"]
    best = dp["output"]["best_monthly"]
    ratio = best / smart
    print(f"  {city}: {ratio:.4f}")

# Also from coverage data
ratios = [best_prices[i] / smart_prices[i] for i in range(len(smart_prices))]
print(f"\n  Coverage data ratios: {[f'{r:.4f}' for r in ratios]}")
print(f"  Mean ratio: {np.mean(ratios):.4f}")

# Check if Best = Smart + constant or Best = Smart * multiplier
diffs = [best_prices[i] - smart_prices[i] for i in range(len(smart_prices))]
print(f"\n  Best - Smart differences: {[f'{d:.2f}' for d in diffs]}")
print(f"  Mean difference: {np.mean(diffs):.2f}")
print(f"  Std difference: {np.std(diffs):.4f}")

# Check if it's a constant offset
if np.std(diffs) < 0.1:
    print(f"  => ADDITIVE model: Best = Smart + {np.mean(diffs):.2f}")
else:
    print(f"  => MULTIPLICATIVE model: Best = Smart × {np.mean(ratios):.4f}")

# ============================================================
# 3. REGIONAL MULTIPLIERS
# ============================================================
print("\n\n3. REGIONAL MULTIPLIERS (relative to München)")
print("-" * 40)

# Reference: München
ref_smart = 9.01
ref_best = 12.40

print("Using Smart tier:")
regional_mults_smart = {}
for dp in data["regional_data_points"]:
    city = dp["inputs"]["city"]
    zip_code = dp["inputs"]["zip"]
    smart = dp["output"]["smart_monthly"]
    mult = smart / ref_smart
    regional_mults_smart[city] = mult
    print(f"  {city} ({zip_code}): {smart:.2f} / {ref_smart:.2f} = {mult:.4f}")

print("\nUsing Best tier:")
regional_mults_best = {}
for dp in data["regional_data_points"]:
    city = dp["inputs"]["city"]
    zip_code = dp["inputs"]["zip"]
    best = dp["output"]["best_monthly"]
    mult = best / ref_best
    regional_mults_best[city] = mult
    print(f"  {city} ({zip_code}): {best:.2f} / {ref_best:.2f} = {mult:.4f}")

# Check if regional multipliers are consistent across tiers
print("\nConsistency check (Smart mult / Best mult):")
for city in regional_mults_smart:
    if city in regional_mults_best:
        ratio = regional_mults_smart[city] / regional_mults_best[city]
        print(f"  {city}: {ratio:.4f}")

# ============================================================
# 4. FLOOR IMPACT
# ============================================================
print("\n\n4. FLOOR IMPACT")
print("-" * 40)

floor_data = data["floor_data"]
ref_floor = {"smart": 9.01, "best": 12.40}  # 2.OG reference
for fd in floor_data:
    floor = fd["inputs"]["floor"]
    smart = fd["output"]["smart_monthly"]
    best = fd["output"]["best_monthly"]
    smart_factor = smart / ref_floor["smart"]
    best_factor = best / ref_floor["best"]
    print(f"  {floor:12s}: Smart={smart:.2f} (×{smart_factor:.4f})  Best={best:.2f} (×{best_factor:.4f})")

# ============================================================
# 5. BUILDING TYPE
# ============================================================
print("\n\n5. BUILDING TYPE IMPACT")
print("-" * 40)

bt_data = data["building_type_data"]
mfh = bt_data[0]["output"]
efh = bt_data[1]["output"]
print(f"  MFH (2.OG): Smart={mfh['smart_monthly']:.2f}  Best={mfh['best_monthly']:.2f}")
print(f"  EFH:         Smart={efh['smart_monthly']:.2f}  Best={efh['best_monthly']:.2f}")
print(f"  EFH/MFH ratio: Smart={efh['smart_monthly']/mfh['smart_monthly']:.4f}  Best={efh['best_monthly']/mfh['best_monthly']:.4f}")

# ============================================================
# 6. AGE IMPACT
# ============================================================
print("\n\n6. AGE IMPACT (Startbonus)")
print("-" * 40)

age_data = data["age_data"]
for ad in age_data:
    age = ad["inputs"].get("age_at_start", "?")
    smart = ad["output"]["smart_monthly"]
    best = ad["output"]["best_monthly"]
    print(f"  Age {age}: Smart={smart:.2f}  Best={best:.2f}")

# Under-36 discount
under36_smart = age_data[0]["output"]["smart_monthly"]
base_smart = age_data[1]["output"]["smart_monthly"]
discount = 1 - under36_smart / base_smart
print(f"\n  Under-36 discount: {discount:.4f} ({discount*100:.1f}%)")
print(f"  Expected: 13% Startbonus")

# ============================================================
# 7. PAYMENT MODE DISCOUNTS
# ============================================================
print("\n\n7. PAYMENT MODE & CONTRACT DISCOUNTS")
print("-" * 40)

pm = data["payment_mode_data"]
print(f"  Annual discount factor: {pm['best_prices']['annual_discount_factor']:.4f} ({(1-pm['best_prices']['annual_discount_factor'])*100:.1f}% off)")

cd = data["contract_duration_data"]
print(f"  3-year contract factor: {cd['three_year_discount_factor']:.4f} ({(1-cd['three_year_discount_factor'])*100:.1f}% off)")

dd = data["deductible_data"]
print(f"  300€ deductible factor: {dd['deductible_factor']:.4f} ({(1-dd['deductible_factor'])*100:.1f}% off)")

# ============================================================
# 8. DERIVE BASE RATES
# ============================================================
print("\n\n8. DERIVED BASE RATES")
print("-" * 40)

# Our model: monthlyPremium = baseRate × coverageUnits × riskClassMultiplier × (1 + loading)
# For München (reference region), the base rate is the rate per coverage unit
# Coverage units = coverage / 5000

# From linear fit: price = slope * m2 + intercept
# But coverage = 650 * m2
# So price = slope * (coverage / 650) + intercept
# price = (slope / 650) * coverage + intercept

# If truly linear in coverage: price/coverageUnits should be constant
# coverageUnits = coverage / 5000

print("\nPrice per coverage unit (per €5k) for München:")
for i, m2 in enumerate(m2_values):
    cov = coverage_values[i]
    units = cov / 5000
    smart_per_unit = smart_prices[i] / units
    best_per_unit = best_prices[i] / units
    print(f"  {m2}m² ({cov}€, {units:.1f} units): Smart={smart_per_unit:.4f}  Best={best_per_unit:.4f}")

# The prices are NOT perfectly linear per unit - there's a base component
# Let me check if there's a fixed base + variable rate
# price = fixedBase + variableRate * units

smart_units = np.array([c / 5000 for c in coverage_values])
coeffs_smart_units = np.polyfit(smart_units, smart_arr, 1)
coeffs_best_units = np.polyfit(best_units := smart_units, best_arr, 1)

print(f"\n  Smart: price = {coeffs_smart_units[0]:.4f} × units + {coeffs_smart_units[1]:.4f}")
print(f"  Best:  price = {coeffs_best_units[0]:.4f} × units + {coeffs_best_units[1]:.4f}")

# R² for unit-based model
smart_pred_u = np.polyval(coeffs_smart_units, smart_units)
r2_smart_u = 1 - np.sum((smart_arr - smart_pred_u)**2) / np.sum((smart_arr - np.mean(smart_arr))**2)
best_pred_u = np.polyval(coeffs_best_units, best_units)
r2_best_u = 1 - np.sum((best_arr - best_pred_u)**2) / np.sum((best_arr - np.mean(best_arr))**2)
print(f"  R² Smart: {r2_smart_u:.6f}, R² Best: {r2_best_u:.6f}")

# ============================================================
# 9. COMPREHENSIVE MODEL
# ============================================================
print("\n\n9. COMPREHENSIVE PRICING MODEL")
print("-" * 40)

# Model: monthlyPrice = (baseRate_per_m2 * m2 + fixedBase) * regionMult * floorMult * buildingMult * ageMult * deductibleMult * contractMult / paymentMult

# München baseline (2.OG, MFH, age 36+, no deductible, 3-year, monthly)
# Smart: price = 0.1095 * m2 + 0.25 (from linear fit)
# Best:  price = 0.1095 * m2 + 3.67 (from linear fit)

print(f"Base model (München, 2.OG, MFH, age≥36, no SB, 3yr, monthly):")
print(f"  Smart: {coeffs_smart[0]:.4f} × m² + {coeffs_smart[1]:.4f}")
print(f"  Best:  {coeffs_best[0]:.4f} × m² + {coeffs_best[1]:.4f}")

print(f"\nRegional multipliers (vs München):")
for dp in sorted(data["regional_data_points"], key=lambda x: x["output"]["smart_monthly"]):
    city = dp["inputs"]["city"]
    zip_code = dp["inputs"]["zip"]
    smart = dp["output"]["smart_monthly"]
    mult = smart / ref_smart
    print(f"  {city:12s} ({zip_code}): ×{mult:.3f}")

print(f"\nFloor multiplier:")
print(f"  Keller/EG: ×{9.95/9.01:.3f}")
print(f"  1.OG+:     ×1.000")

print(f"\nBuilding type multiplier:")
print(f"  MFH: ×1.000")
print(f"  EFH: ×{9.55/9.01:.3f}")

print(f"\nAge discount:")
print(f"  Under 36: ×{1-0.13:.3f} (13% Startbonus)")
print(f"  36+:      ×1.000")

print(f"\nDeductible discount:")
print(f"  None:    ×1.000")
print(f"  300€:    ×{0.9274:.3f}")

print(f"\nContract duration:")
print(f"  1 year:  ×{1/0.8998:.3f}")
print(f"  3 years: ×1.000")

print(f"\nPayment frequency:")
print(f"  Monthly:     ×1.000")
print(f"  Annual:      ×{0.9434*12:.3f}/12 = ×{0.9434:.3f}")

# ============================================================
# 10. OUTPUT RESULTS AS JSON
# ============================================================
results = {
    "product": "hausrat",
    "ergo_tiers": ["Smart", "Best"],
    "our_tier_mapping": {"Smart": "grundschutz", "Best": "komfort"},
    "note": "ERGO has only 2 tiers (not 3). We need to map appropriately.",
    "coverage_model": {
        "type": "per_m2",
        "coverage_per_m2": 650,
        "min_m2": 10,
        "max_m2": 384,
        "smart_rate_per_m2_monthly": round(coeffs_smart[0], 4),
        "smart_base_monthly": round(coeffs_smart[1], 4),
        "best_rate_per_m2_monthly": round(coeffs_best[0], 4),
        "best_base_monthly": round(coeffs_best[1], 4),
        "coverage_linearity_r2_smart": round(r2_smart, 6),
        "coverage_linearity_r2_best": round(r2_best, 6)
    },
    "reference_city": "München (80331)",
    "regional_multipliers": {
        dp["inputs"]["city"]: round(dp["output"]["smart_monthly"] / ref_smart, 4)
        for dp in data["regional_data_points"]
    },
    "floor_multiplier": {
        "Keller": 1.1043,
        "Erdgeschoss": 1.1043,
        "1.OG": 1.0,
        "2.OG": 1.0,
        "3.OG+": 1.0
    },
    "building_type_multiplier": {
        "Mehrfamilienhaus": 1.0,
        "Einfamilienhaus": round(9.55 / 9.01, 4)
    },
    "age_discount": {
        "under_36_startbonus": 0.13,
        "under_36_factor": 0.87,
        "36_plus_factor": 1.0
    },
    "deductible_discount": {
        "none": 1.0,
        "300_eur": 0.9274,
        "300_eur_flexi": "not tested"
    },
    "contract_duration": {
        "1_year": round(1 / 0.8998, 4),
        "3_years": 1.0
    },
    "payment_frequency": {
        "monthly": 1.0,
        "annual": 0.9434
    },
    "add_on_modules": [
        "Diebstahl (10.000 EUR) - included in Best, optional in Smart",
        "Haus- und Wohnungsschutzbrief",
        "Glasversicherung",
        "Weitere Naturgefahren",
        "Unbenannte Gefahren (requires Weitere Naturgefahren)",
        "Fahrrad- und E-Bike-Schutz"
    ]
}

with open("research/hausrat/analysis_results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n\nResults saved to research/hausrat/analysis_results.json")

# ============================================================
# 11. COMPARISON WITH OUR CURRENT MODEL
# ============================================================
print("\n\n" + "=" * 60)
print("COMPARISON WITH CURRENT products.md ASSUMPTIONS")
print("=" * 60)

print("""
TIER MAPPING:
  Our assumption: Grundschutz / Komfort / Premium (3 tiers)
  ERGO reality:   Smart / Best (2 tiers)
  => Need to remove one tier or map differently

COVERAGE MODEL:
  Our assumption: €10k-€150k, step €5k, default €50k
  ERGO reality:   650€/m², 10-384m² → €6.5k-€249.6k
  => Coverage is derived from m², not freely chosen

PRICING:
  Our Komfort base: €0.53/5k/month
  ERGO Best equivalent: ~€{coeffs_best[0] * (5000/650):.2f}/5k/month (linear component only)
  Note: ERGO pricing has a significant fixed base component

REGIONAL MODEL:
  Our assumption: 4 zones (0.85, 1.0, 1.25, 1.5)
  ERGO reality:   ZIP-code-specific (continuous range {min([dp["output"]["smart_monthly"]/ref_smart for dp in data["regional_data_points"]]):.2f}-{max([dp["output"]["smart_monthly"]/ref_smart for dp in data["regional_data_points"]]):.2f})
  => Much more granular than 4 zones

AGE:
  Our assumption: age-independent (flat)
  ERGO reality:   Binary - 13% Startbonus for under 36
  => Not flat, but binary discount

FLOOR:
  Not in our model
  ERGO reality: Keller/EG ~10% surcharge, 1.OG+ base rate

BUILDING TYPE:
  Not in our model
  ERGO reality: EFH ~6% surcharge vs MFH
""")
