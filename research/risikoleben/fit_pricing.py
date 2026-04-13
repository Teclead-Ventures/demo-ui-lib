#!/usr/bin/env python3
"""Analyze ERGO Risikoleben pricing data and fit models."""
import json
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent
MATRIX_PATH = BASE_DIR / "price-matrix.json"

with open(MATRIX_PATH) as f:
    data = json.load(f)

points = data["data_points"]

# ============================================================
# 1. Extract age curves for each tier (NS10+, 200k, 20yr)
# ============================================================
print("=" * 60)
print("1. AGE CURVES (Nichtraucher 10+, 200k, 20yr)")
print("=" * 60)

tiers = ["grundschutz", "komfort", "premium"]
smoker_classes = ["nichtraucher_10plus", "raucher", "nichtraucher_1plus"]

for tier in tiers:
    pts = [p for p in points if
           p["inputs"]["tier"] == tier and
           p["inputs"]["smoker"] == "nichtraucher_10plus" and
           p["inputs"]["coverage"] == 200000 and
           p["inputs"]["term_years"] == 20]
    pts.sort(key=lambda x: x["inputs"]["age"])

    ages = np.array([p["inputs"]["age"] for p in pts])
    prices = np.array([p["output"]["monthly_price"] for p in pts])

    print(f"\n  {tier.upper()}:")
    for a, p in zip(ages, prices):
        print(f"    Age {a:2d}: {p:8.2f} EUR")

    # Fit quadratic: price = a + b*age + c*age^2
    # Using normalized age for the formula
    min_age, max_age = 18, 65
    t = (ages - min_age) / (max_age - min_age)
    A = np.vstack([np.ones_like(t), t, t**2]).T
    coeffs, residuals, _, _ = np.linalg.lstsq(A, prices, rcond=None)

    # R^2
    ss_res = np.sum((prices - A @ coeffs) ** 2)
    ss_tot = np.sum((prices - np.mean(prices)) ** 2)
    r2_quad = 1 - ss_res / ss_tot

    print(f"    Quadratic fit: base={coeffs[0]:.4f}, linear={coeffs[1]:.4f}, quadratic={coeffs[2]:.4f}")
    print(f"    R^2 (quadratic): {r2_quad:.6f}")

    # Fit exponential: price = a * exp(b * age)
    log_prices = np.log(prices)
    A_exp = np.vstack([np.ones_like(ages), ages]).T
    coeffs_exp, _, _, _ = np.linalg.lstsq(A_exp, log_prices, rcond=None)
    exp_a = np.exp(coeffs_exp[0])
    exp_b = coeffs_exp[1]
    pred_exp = exp_a * np.exp(exp_b * ages)
    ss_res_exp = np.sum((prices - pred_exp) ** 2)
    r2_exp = 1 - ss_res_exp / ss_tot

    print(f"    Exponential fit: a={exp_a:.4f}, b={exp_b:.6f}")
    print(f"    R^2 (exponential): {r2_exp:.6f}")

    # Try cubic
    A_cub = np.vstack([np.ones_like(t), t, t**2, t**3]).T
    coeffs_cub, _, _, _ = np.linalg.lstsq(A_cub, prices, rcond=None)
    ss_res_cub = np.sum((prices - A_cub @ coeffs_cub) ** 2)
    r2_cub = 1 - ss_res_cub / ss_tot
    print(f"    Cubic fit R^2: {r2_cub:.6f}")

    # Report residuals
    pred_quad = A @ coeffs
    print(f"    Quadratic residuals:")
    for a, p, pq in zip(ages, prices, pred_quad):
        err_pct = (pq - p) / p * 100
        print(f"      Age {a:2d}: actual={p:8.2f}, predicted={pq:8.2f}, error={err_pct:+.1f}%")

# ============================================================
# 2. Smoker multipliers
# ============================================================
print("\n" + "=" * 60)
print("2. SMOKER MULTIPLIERS (vs Nichtraucher 10+)")
print("=" * 60)

for smoker in ["raucher", "nichtraucher_1plus"]:
    print(f"\n  {smoker}:")
    for tier in tiers:
        ns10_pts = {p["inputs"]["age"]: p["output"]["monthly_price"]
                    for p in points if
                    p["inputs"]["tier"] == tier and
                    p["inputs"]["smoker"] == "nichtraucher_10plus" and
                    p["inputs"]["coverage"] == 200000 and
                    p["inputs"]["term_years"] == 20}

        sm_pts = {p["inputs"]["age"]: p["output"]["monthly_price"]
                  for p in points if
                  p["inputs"]["tier"] == tier and
                  p["inputs"]["smoker"] == smoker and
                  p["inputs"]["coverage"] == 200000 and
                  p["inputs"]["term_years"] == 20}

        common_ages = sorted(set(ns10_pts.keys()) & set(sm_pts.keys()))
        ratios = []
        for age in common_ages:
            ratio = sm_pts[age] / ns10_pts[age]
            ratios.append(ratio)
            print(f"    {tier:>12s} age {age:2d}: NS10+={ns10_pts[age]:8.2f}, {smoker}={sm_pts[age]:8.2f}, ratio={ratio:.3f}")

        if ratios:
            print(f"    {tier:>12s} avg ratio: {np.mean(ratios):.3f} (std={np.std(ratios):.3f})")

# ============================================================
# 3. Coverage linearity check
# ============================================================
print("\n" + "=" * 60)
print("3. COVERAGE LINEARITY CHECK (age 35, NS10+, 20yr)")
print("=" * 60)

for tier in tiers:
    coverages = {}
    for p in points:
        if (p["inputs"]["tier"] == tier and
            p["inputs"]["smoker"] == "nichtraucher_10plus" and
            p["inputs"]["age"] == 35 and
            p["inputs"]["term_years"] == 20):
            coverages[p["inputs"]["coverage"]] = p["output"]["monthly_price"]

    if len(coverages) >= 2:
        print(f"\n  {tier}:")
        base_cov = 200000
        base_price = coverages.get(base_cov, 0)
        for cov in sorted(coverages.keys()):
            price = coverages[cov]
            ratio = price / base_price if base_price else 0
            expected_ratio = cov / base_cov
            print(f"    {cov:>10,} EUR: {price:8.2f} EUR (ratio vs 200k: {ratio:.3f}, expected: {expected_ratio:.3f})")

        # Check per-unit pricing
        per_unit = {cov: price / (cov / 1000) for cov, price in coverages.items()}
        print(f"    Price per 1000 EUR coverage: {per_unit}")

# ============================================================
# 4. Term duration effect
# ============================================================
print("\n" + "=" * 60)
print("4. TERM DURATION EFFECT (age 35, NS10+, 200k)")
print("=" * 60)

for tier in tiers:
    terms = {}
    for p in points:
        if (p["inputs"]["tier"] == tier and
            p["inputs"]["smoker"] == "nichtraucher_10plus" and
            p["inputs"]["age"] == 35 and
            p["inputs"]["coverage"] == 200000):
            terms[p["inputs"]["term_years"]] = p["output"]["monthly_price"]

    if terms:
        print(f"\n  {tier}:")
        for term in sorted(terms.keys()):
            print(f"    {term:2d} years: {terms[term]:8.2f} EUR")

# ============================================================
# 5. Tier ratios
# ============================================================
print("\n" + "=" * 60)
print("5. TIER RATIOS (Komfort/Grundschutz, Premium/Grundschutz)")
print("=" * 60)

for smoker in ["nichtraucher_10plus", "raucher"]:
    print(f"\n  {smoker}:")
    for age in [25, 30, 35, 40, 45, 50, 55, 60]:
        grund_price = None
        komfort_price = None
        premium_price = None
        for p in points:
            if (p["inputs"]["age"] == age and
                p["inputs"]["smoker"] == smoker and
                p["inputs"]["coverage"] == 200000 and
                p["inputs"]["term_years"] == 20):
                if p["inputs"]["tier"] == "grundschutz":
                    grund_price = p["output"]["monthly_price"]
                elif p["inputs"]["tier"] == "komfort":
                    komfort_price = p["output"]["monthly_price"]
                elif p["inputs"]["tier"] == "premium":
                    premium_price = p["output"]["monthly_price"]

        if grund_price and komfort_price and premium_price:
            k_ratio = komfort_price / grund_price
            p_ratio = premium_price / grund_price
            print(f"    Age {age:2d}: K/G={k_ratio:.3f}, P/G={p_ratio:.3f}")

# ============================================================
# 6. Base rate derivation (per 1000 EUR coverage per month)
# ============================================================
print("\n" + "=" * 60)
print("6. BASE RATE DERIVATION")
print("=" * 60)

# For the reference case: 35yo, NS10+, 200k, 20yr
# This is where we derive what goes into our demo model
for tier in tiers:
    pts_35 = [p for p in points if
              p["inputs"]["tier"] == tier and
              p["inputs"]["smoker"] == "nichtraucher_10plus" and
              p["inputs"]["age"] == 35 and
              p["inputs"]["coverage"] == 200000 and
              p["inputs"]["term_years"] == 20]
    if pts_35:
        price = pts_35[0]["output"]["monthly_price"]
        per_25k = price / (200000 / 25000)
        print(f"  {tier}: {price:.2f} EUR/month for 200k = {per_25k:.2f} EUR per 25k")

# ============================================================
# 7. Determine best model for our demo
# ============================================================
print("\n" + "=" * 60)
print("7. BEST MODEL FOR DEMO")
print("=" * 60)

# Get Komfort NS10+ 200k 20yr data as reference
komfort_ns10 = [(p["inputs"]["age"], p["output"]["monthly_price"])
                for p in points if
                p["inputs"]["tier"] == "komfort" and
                p["inputs"]["smoker"] == "nichtraucher_10plus" and
                p["inputs"]["coverage"] == 200000 and
                p["inputs"]["term_years"] == 20]
komfort_ns10.sort()
ages_k = np.array([x[0] for x in komfort_ns10])
prices_k = np.array([x[1] for x in komfort_ns10])

# Normalized t
min_age, max_age = 18, 65
t_k = (ages_k - min_age) / (max_age - min_age)

# Quadratic fit
A_k = np.vstack([np.ones_like(t_k), t_k, t_k**2]).T
coeffs_k, _, _, _ = np.linalg.lstsq(A_k, prices_k, rcond=None)
pred_k = A_k @ coeffs_k
ss_res_k = np.sum((prices_k - pred_k) ** 2)
ss_tot_k = np.sum((prices_k - np.mean(prices_k)) ** 2)
r2_k = 1 - ss_res_k / ss_tot_k

print(f"\n  Komfort (NS10+, 200k, 20yr) quadratic:")
print(f"    ageFactor = {coeffs_k[0]:.4f} + {coeffs_k[1]:.4f}*t + {coeffs_k[2]:.4f}*t^2")
print(f"    where t = (age - {min_age}) / ({max_age} - {min_age})")
print(f"    R^2 = {r2_k:.6f}")

# Also try exponential for Komfort
log_k = np.log(prices_k)
A_exp_k = np.vstack([np.ones_like(ages_k), ages_k]).T
c_exp_k, _, _, _ = np.linalg.lstsq(A_exp_k, log_k, rcond=None)
pred_exp_k = np.exp(c_exp_k[0]) * np.exp(c_exp_k[1] * ages_k)
r2_exp_k = 1 - np.sum((prices_k - pred_exp_k)**2) / ss_tot_k

print(f"\n  Komfort exponential:")
print(f"    price = {np.exp(c_exp_k[0]):.6f} * exp({c_exp_k[1]:.6f} * age)")
print(f"    R^2 = {r2_exp_k:.6f}")

# Smoker multiplier summary
print("\n  Smoker multipliers (Komfort, 200k, 20yr):")
komfort_raucher = {p["inputs"]["age"]: p["output"]["monthly_price"]
                   for p in points if
                   p["inputs"]["tier"] == "komfort" and
                   p["inputs"]["smoker"] == "raucher" and
                   p["inputs"]["coverage"] == 200000 and
                   p["inputs"]["term_years"] == 20}
komfort_ns10_dict = {p["inputs"]["age"]: p["output"]["monthly_price"]
                     for p in points if
                     p["inputs"]["tier"] == "komfort" and
                     p["inputs"]["smoker"] == "nichtraucher_10plus" and
                     p["inputs"]["coverage"] == 200000 and
                     p["inputs"]["term_years"] == 20}

raucher_ratios = []
for age in sorted(komfort_raucher.keys()):
    if age in komfort_ns10_dict:
        r = komfort_raucher[age] / komfort_ns10_dict[age]
        raucher_ratios.append(r)
        print(f"    Age {age}: ratio = {r:.3f}")
print(f"    Overall avg: {np.mean(raucher_ratios):.3f}, std: {np.std(raucher_ratios):.3f}")
print(f"    NOTE: Smoker multiplier is NOT constant across ages!")

# Coverage linearity summary
print("\n  Coverage linearity (Komfort, 35yo, NS10+, 20yr):")
k_100 = [p for p in points if p["inputs"]["tier"] == "komfort" and
         p["inputs"]["coverage"] == 100000 and p["inputs"]["age"] == 35 and
         p["inputs"]["smoker"] == "nichtraucher_10plus" and p["inputs"]["term_years"] == 20]
k_200 = [p for p in points if p["inputs"]["tier"] == "komfort" and
         p["inputs"]["coverage"] == 200000 and p["inputs"]["age"] == 35 and
         p["inputs"]["smoker"] == "nichtraucher_10plus" and p["inputs"]["term_years"] == 20]
k_400 = [p for p in points if p["inputs"]["tier"] == "komfort" and
         p["inputs"]["coverage"] == 400000 and p["inputs"]["age"] == 35 and
         p["inputs"]["smoker"] == "nichtraucher_10plus" and p["inputs"]["term_years"] == 20]

if k_100 and k_200 and k_400:
    p100 = k_100[0]["output"]["monthly_price"]
    p200 = k_200[0]["output"]["monthly_price"]
    p400 = k_400[0]["output"]["monthly_price"]
    print(f"    100k: {p100}, 200k: {p200}, 400k: {p400}")
    print(f"    200k/100k = {p200/p100:.3f} (expect 2.0)")
    print(f"    400k/200k = {p400/p200:.3f} (expect 2.0)")
    print(f"    400k/100k = {p400/p100:.3f} (expect 4.0)")
    # Not perfectly linear - there may be a base fee
    # Try: price = fixed + rate * coverage
    # Using 100k and 400k: fixed + rate*100k = p100, fixed + rate*400k = p400
    rate = (p400 - p100) / (400000 - 100000)
    fixed = p100 - rate * 100000
    pred_200 = fixed + rate * 200000
    print(f"    Linear model: price = {fixed:.4f} + {rate:.8f} * coverage")
    print(f"    Predicted 200k: {pred_200:.2f} (actual: {p200:.2f})")

# ============================================================
# 8. Output JSON summary
# ============================================================
print("\n" + "=" * 60)
print("8. JSON OUTPUT SUMMARY")
print("=" * 60)

# Collect all Grundschutz per-unit rates for NS10+ 20yr
grund_rates = {}
for p in points:
    if (p["inputs"]["tier"] == "grundschutz" and
        p["inputs"]["smoker"] == "nichtraucher_10plus" and
        p["inputs"]["coverage"] == 200000 and
        p["inputs"]["term_years"] == 20):
        grund_rates[p["inputs"]["age"]] = p["output"]["monthly_price"]

komfort_rates = {}
for p in points:
    if (p["inputs"]["tier"] == "komfort" and
        p["inputs"]["smoker"] == "nichtraucher_10plus" and
        p["inputs"]["coverage"] == 200000 and
        p["inputs"]["term_years"] == 20):
        komfort_rates[p["inputs"]["age"]] = p["output"]["monthly_price"]

premium_rates = {}
for p in points:
    if (p["inputs"]["tier"] == "premium" and
        p["inputs"]["smoker"] == "nichtraucher_10plus" and
        p["inputs"]["coverage"] == 200000 and
        p["inputs"]["term_years"] == 20):
        premium_rates[p["inputs"]["age"]] = p["output"]["monthly_price"]

# Compute tier ratios at age 35
g35 = grund_rates.get(35, 1)
k35 = komfort_rates.get(35, 1)
p35 = premium_rates.get(35, 1)

summary = {
    "product": "risikoleben",
    "pricing_model": {
        "type": "exponential_age_curve",
        "formula": "price = baseRate * (coverage/25000) * exp(growthRate * age) * smokerMultiplier * termFactor",
        "note": "Exponential fits better than quadratic due to steep age curve",
        "komfort_exponential": {
            "a": round(float(np.exp(c_exp_k[0])), 6),
            "b": round(float(c_exp_k[1]), 6),
            "r_squared": round(float(r2_exp_k), 6)
        },
        "komfort_quadratic": {
            "base": round(float(coeffs_k[0]), 4),
            "linear": round(float(coeffs_k[1]), 4),
            "quadratic": round(float(coeffs_k[2]), 4),
            "r_squared": round(float(r2_k), 6)
        }
    },
    "reference_prices_200k_20yr_ns10": {
        "grundschutz": {int(k): v for k, v in sorted(grund_rates.items())},
        "komfort": {int(k): v for k, v in sorted(komfort_rates.items())},
        "premium": {int(k): v for k, v in sorted(premium_rates.items())}
    },
    "tier_ratios_at_35": {
        "komfort_vs_grundschutz": round(k35 / g35, 4),
        "premium_vs_grundschutz": round(p35 / g35, 4),
        "premium_vs_komfort": round(p35 / k35, 4)
    },
    "smoker_multipliers_komfort": {
        "raucher_avg": round(float(np.mean(raucher_ratios)), 3),
        "raucher_by_age": {int(age): round(komfort_raucher[age] / komfort_ns10_dict[age], 3)
                           for age in sorted(komfort_raucher.keys()) if age in komfort_ns10_dict},
        "note": "Smoker multiplier increases with age - NOT constant"
    },
    "base_rates_per_25k_at_35_ns10_20yr": {
        "grundschutz": round(g35 / 8, 4),
        "komfort": round(k35 / 8, 4),
        "premium": round(p35 / 8, 4)
    }
}

print(json.dumps(summary, indent=2, ensure_ascii=False))

# Save
with open(BASE_DIR / "analysis_results.json", "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("\nAnalysis saved to analysis_results.json")
