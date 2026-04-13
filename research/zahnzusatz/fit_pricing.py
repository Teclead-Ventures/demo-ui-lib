#!/usr/bin/env python3
"""
Curve fitting for ERGO Zahnzusatzversicherung pricing.

ERGO uses discrete age bands — NOT a continuous curve. This script:
1. Fits our quadratic age curve model to ERGO's band midpoints
2. Computes R² to show how well the polynomial approximates discrete bands
3. Derives base rates and tier multipliers
4. Compares with our current assumed parameters
"""

import json
import numpy as np

# ERGO Beitragstabelle (verified via calculator)
bands = [
    {"band": "0-20",  "mid": 10,  "DS75": 2.90,  "DS90": 3.70,  "DS100": 4.80},
    {"band": "21-25", "mid": 23,  "DS75": 5.70,  "DS90": 7.20,  "DS100": 9.20},
    {"band": "26-30", "mid": 28,  "DS75": 10.90, "DS90": 13.80, "DS100": 17.50},
    {"band": "31-40", "mid": 35,  "DS75": 17.40, "DS90": 21.70, "DS100": 27.60},
    {"band": "41-50", "mid": 45,  "DS75": 25.90, "DS90": 32.50, "DS100": 41.30},
    {"band": "51+",   "mid": 60,  "DS75": 34.80, "DS90": 44.40, "DS100": 57.80},
]

# Our current assumed parameters
OUR_PARAMS = {
    "base_rates": {"grundschutz": 2.70, "komfort": 3.29, "premium": 4.05},
    "coverage_unit": 250,  # per €250/year
    "default_coverage": 1500,  # €1500/year = 6 units
    "age_curve": {"base": 0.80, "linear": 0.35, "quadratic": 0.10},
    "loading": 0.22,
    "min_age": 18,
    "max_age": 75,
}

print("=" * 70)
print("ERGO Zahnzusatzversicherung — Pricing Analysis")
print("=" * 70)

# === Part 1: Tier ratios ===
print("\n--- Tier Ratios (DS75 : DS90 : DS100) ---")
for b in bands:
    r75 = b["DS75"] / b["DS100"]
    r90 = b["DS90"] / b["DS100"]
    print(f"  {b['band']:>7s}: DS75/DS100={r75:.3f}  DS90/DS100={r90:.3f}")

# Average tier ratios
avg_75 = np.mean([b["DS75"] / b["DS100"] for b in bands])
avg_90 = np.mean([b["DS90"] / b["DS100"] for b in bands])
print(f"\n  Average: DS75/DS100={avg_75:.3f}  DS90/DS100={avg_90:.3f}")
print(f"  → Tier ratios are very consistent across age bands (nearly constant multipliers)")

# === Part 2: Fit quadratic age curve to DS100 (reference tier) ===
print("\n--- Quadratic Age Curve Fit (DS100) ---")

ages = np.array([b["mid"] for b in bands], dtype=float)
prices_100 = np.array([b["DS100"] for b in bands], dtype=float)

# Normalize age to 0-1 range (using ERGO's actual age range 0-75)
min_age = 0
max_age = 75
t = (ages - min_age) / (max_age - min_age)

# Fit quadratic: price = a + b*t + c*t^2
# np.polyfit returns [c, b, a] for degree 2
coeffs = np.polyfit(t, prices_100, 2)
c_quad, c_lin, c_base = coeffs

# Compute R²
predicted = c_base + c_lin * t + c_quad * t * t
ss_res = np.sum((prices_100 - predicted) ** 2)
ss_tot = np.sum((prices_100 - np.mean(prices_100)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

print(f"  Raw polynomial: price = {c_base:.2f} + {c_lin:.2f}*t + {c_quad:.2f}*t²")
print(f"  R² = {r_squared:.4f}")
print(f"  Residuals: {[f'{r:.2f}' for r in (prices_100 - predicted)]}")

# === Part 3: Also try with age range 18-75 (our model's range) ===
print("\n--- Quadratic Age Curve Fit (DS100, using age range 18-75) ---")

min_age_our = 18
max_age_our = 75
t_our = (ages - min_age_our) / (max_age_our - min_age_our)

# For ages below 18, clip to 0
t_our = np.clip(t_our, 0, None)

coeffs_our = np.polyfit(t_our, prices_100, 2)
c_quad_our, c_lin_our, c_base_our = coeffs_our

predicted_our = c_base_our + c_lin_our * t_our + c_quad_our * t_our * t_our
ss_res_our = np.sum((prices_100 - predicted_our) ** 2)
ss_tot_our = np.sum((prices_100 - np.mean(prices_100)) ** 2)
r_squared_our = 1 - (ss_res_our / ss_tot_our)

print(f"  Raw polynomial: price = {c_base_our:.2f} + {c_lin_our:.2f}*t + {c_quad_our:.2f}*t²")
print(f"  R² = {r_squared_our:.4f}")

# Normalize to age factor (divide by price at reference age)
# Use the price at age 35 (Komfort calibration age) as reference
t_ref = (35 - min_age_our) / (max_age_our - min_age_our)
price_at_ref = c_base_our + c_lin_our * t_ref + c_quad_our * t_ref * t_ref
age_factor_base = c_base_our / price_at_ref
age_factor_linear = c_lin_our / price_at_ref
age_factor_quadratic = c_quad_our / price_at_ref

print(f"\n  Normalized age curve (factor relative to age 35):")
print(f"    base = {age_factor_base:.4f}")
print(f"    linear = {age_factor_linear:.4f}")
print(f"    quadratic = {age_factor_quadratic:.4f}")
print(f"    Factor at age 18 (t=0): {age_factor_base:.4f}")
print(f"    Factor at age 35 (t≈0.30): ~1.0000")
print(f"    Factor at age 75 (t=1): {age_factor_base + age_factor_linear + age_factor_quadratic:.4f}")

# === Part 4: Derive ERGO's effective base rates ===
print("\n--- Derived Base Rates ---")
print("  ERGO is a flat-rate product (no coverage slider)")
print("  Our model uses per-unit pricing. To map:")
print("  If we set coverageUnit = defaultCoverage (flat rate), then units = 1")
print("  Base rate = monthly price / ageFactor / (1 + loading)")

# Using age 35 as reference (ageFactor = 1.0 at this age)
# We need to figure out loading
# Since we don't know ERGO's loading, we'll derive base rates assuming various loadings

for loading in [0.20, 0.22, 0.25]:
    br_75 = 17.40 / 1.0 / (1 + loading)
    br_90 = 21.70 / 1.0 / (1 + loading)
    br_100 = 27.60 / 1.0 / (1 + loading)
    print(f"  Loading {loading:.0%}: DS75={br_75:.2f}, DS90={br_90:.2f}, DS100={br_100:.2f}")

# === Part 5: Compare with our assumed pricing ===
print("\n--- Comparison: Our Model vs ERGO Actual ---")

def our_price(age, tier):
    """Calculate price using our current products.md parameters."""
    units = OUR_PARAMS["default_coverage"] / OUR_PARAMS["coverage_unit"]  # 1500/250 = 6
    t = (age - OUR_PARAMS["min_age"]) / (OUR_PARAMS["max_age"] - OUR_PARAMS["min_age"])
    t = max(0, min(1, t))
    ac = OUR_PARAMS["age_curve"]
    age_factor = ac["base"] + ac["linear"] * t + ac["quadratic"] * t * t
    base_rate = OUR_PARAMS["base_rates"][tier]
    net = base_rate * units * age_factor
    return net * (1 + OUR_PARAMS["loading"])

print(f"\n  {'Age':>5s} | {'Our Komfort':>12s} | {'ERGO DS90':>10s} | {'Delta':>8s} | {'Delta%':>8s}")
print(f"  {'-'*5} | {'-'*12} | {'-'*10} | {'-'*8} | {'-'*8}")

test_ages = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
ergo_lookup = {10: 3.70, 23: 7.20, 28: 13.80, 35: 21.70, 45: 32.50, 60: 44.40}

for age in test_ages:
    our = our_price(age, "komfort")
    # Find ERGO band price
    if age <= 20: ergo = 3.70
    elif age <= 25: ergo = 7.20
    elif age <= 30: ergo = 13.80
    elif age <= 40: ergo = 21.70
    elif age <= 50: ergo = 32.50
    else: ergo = 44.40
    delta = our - ergo
    pct = (delta / ergo) * 100
    print(f"  {age:>5d} | {our:>12.2f} | {ergo:>10.2f} | {delta:>+8.2f} | {pct:>+7.1f}%")

# === Part 6: Derive corrected parameters for our model ===
print("\n--- Corrected Parameters for Our Model ---")

# Since ERGO is flat-rate, we should model it as flat-rate too
# Set coverageUnit = defaultCoverage so units = 1
# Then base_rate IS the monthly price at reference age / (1 + loading)

# Use loading = 22% (our current assumption)
loading = 0.22

# Derive base rates from the 31-40 band (mid=35, our reference age)
# With flat-rate: price = baseRate * 1 * ageFactor(35) * 1 * 1 * (1+loading)
# At age 35, ageFactor = 1.0, so: price = baseRate * (1+loading)
base_75 = 17.40 / (1 + loading)
base_90 = 21.70 / (1 + loading)
base_100 = 27.60 / (1 + loading)

print(f"  Coverage model: FLAT RATE (coverageUnit = defaultCoverage)")
print(f"  Base rates (assuming {loading:.0%} loading):")
print(f"    Grundschutz (DS75):  €{base_75:.2f}")
print(f"    Komfort (DS90):      €{base_90:.2f}")
print(f"    Premium (DS100):     €{base_100:.2f}")
print(f"  Age curve (normalized, age range 18-75):")
print(f"    base = {age_factor_base:.4f}")
print(f"    linear = {age_factor_linear:.4f}")
print(f"    quadratic = {age_factor_quadratic:.4f}")
print(f"  R² = {r_squared_our:.4f}")

# === Part 7: Verify corrected model against ERGO prices ===
print("\n--- Verification: Corrected Model vs ERGO ---")

def corrected_price(age, base_rate):
    t = (age - 18) / (75 - 18)
    t = max(0, min(1, t))
    age_factor = age_factor_base + age_factor_linear * t + age_factor_quadratic * t * t
    return base_rate * age_factor * (1 + loading)

print(f"\n  {'Age':>5s} | {'Model DS90':>11s} | {'ERGO DS90':>10s} | {'Delta%':>8s}")
print(f"  {'-'*5} | {'-'*11} | {'-'*10} | {'-'*8}")

for age in test_ages:
    model = corrected_price(age, base_90)
    if age <= 20: ergo = 3.70
    elif age <= 25: ergo = 7.20
    elif age <= 30: ergo = 13.80
    elif age <= 40: ergo = 21.70
    elif age <= 50: ergo = 32.50
    else: ergo = 44.40
    pct = ((model - ergo) / ergo) * 100
    print(f"  {age:>5d} | {model:>11.2f} | {ergo:>10.2f} | {pct:>+7.1f}%")

# === Part 8: Output results as JSON ===
results = {
    "age_curve": {
        "base": round(float(age_factor_base), 4),
        "linear": round(float(age_factor_linear), 4),
        "quadratic": round(float(age_factor_quadratic), 4)
    },
    "r_squared": round(float(r_squared_our), 4),
    "base_rates_at_loading_22pct": {
        "grundschutz": round(float(base_75), 2),
        "komfort": round(float(base_90), 2),
        "premium": round(float(base_100), 2)
    },
    "tier_ratios": {
        "DS75_to_DS100": round(float(avg_75), 4),
        "DS90_to_DS100": round(float(avg_90), 4)
    },
    "model_type": "flat_rate_with_age_bands",
    "ergo_uses_discrete_bands": True,
    "our_polynomial_approximation_r2": round(float(r_squared_our), 4),
    "note": "ERGO uses step-function pricing (age bands). Our polynomial is a smooth approximation."
}

with open("research/zahnzusatz/fit_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n\nResults saved to research/zahnzusatz/fit_results.json")
print(f"\nKey findings:")
print(f"  1. ERGO uses DISCRETE AGE BANDS, not a continuous curve")
print(f"  2. Our polynomial model approximates this with R²={r_squared_our:.4f}")
print(f"  3. ERGO is a FLAT-RATE product (no coverage slider)")
print(f"  4. Tier ratios are consistent: DS75≈{avg_75:.1%} of DS100, DS90≈{avg_90:.1%} of DS100")
