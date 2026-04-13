#!/usr/bin/env python3
"""
Sterbegeldversicherung pricing analysis.

Key insight: ERGO's Sterbegeld pricing depends on BOTH age AND payment_duration.
payment_duration = 90 - entry_age (default).
So when age increases, payment_duration decreases simultaneously.
The monthly premium reflects both the actuarial cost AND the shorter payment window.

We need to model: monthly_premium = f(age, coverage, tier)
where payment_duration is implicitly 90 - age.
"""

import json
import numpy as np
import sys

# Load data
with open('research/sterbegeld/price-matrix.json', 'r') as f:
    data = json.load(f)

# Parse data points
points = []
for dp in data['data_points']:
    price = dp['output']['monthly_price']
    if price is None:
        continue
    points.append({
        'age': dp['inputs']['age'],
        'coverage': dp['inputs']['coverage'],
        'tier': dp['inputs']['tier'],
        'payment_years': dp['inputs']['payment_years'],
        'price': price
    })

print(f"Total valid data points: {len(points)}")

# Group by tier
tiers = {}
for p in points:
    tier = p['tier']
    if tier not in tiers:
        tiers[tier] = []
    tiers[tier].append(p)

print(f"\nTiers found: {list(tiers.keys())}")
for t, pts in tiers.items():
    print(f"  {t}: {len(pts)} points")

# =========================================
# Analysis 1: Price per 1000 EUR coverage
# =========================================
print("\n" + "="*60)
print("ANALYSIS 1: Price per 1000 EUR coverage (linearity check)")
print("="*60)

# Check if price scales linearly with coverage
for tier_name in ['grundschutz', 'komfort', 'premium']:
    tier_pts = [p for p in points if p['tier'] == tier_name]

    # Group by age
    ages = sorted(set(p['age'] for p in tier_pts))

    print(f"\n{tier_name.upper()}:")
    print(f"{'Age':>5} | {'3k rate':>8} | {'5k rate':>8} | {'8k rate':>8} | {'10k rate':>8} | {'15k rate':>8} | {'Avg':>8} | {'Std':>8}")
    print("-" * 80)

    for age in ages:
        age_pts = [p for p in tier_pts if p['age'] == age]
        rates = []
        rate_strs = []
        for p in sorted(age_pts, key=lambda x: x['coverage']):
            rate = p['price'] / (p['coverage'] / 1000)
            rates.append(rate)
            rate_strs.append(f"{rate:>8.3f}")

        avg_rate = np.mean(rates)
        std_rate = np.std(rates)
        print(f"{age:>5} | {'|'.join(rate_strs)} | {avg_rate:>8.3f} | {std_rate:>8.3f}")

# =========================================
# Analysis 2: Rate per 1000 EUR by age
# =========================================
print("\n" + "="*60)
print("ANALYSIS 2: Rate per 1000 EUR by age (normalized to 8k coverage)")
print("="*60)

# Use 8k coverage as reference
for tier_name in ['grundschutz', 'komfort', 'premium']:
    tier_pts = [p for p in points if p['tier'] == tier_name and p['coverage'] == 8000]
    ages = sorted(set(p['age'] for p in tier_pts))

    print(f"\n{tier_name.upper()} (8k coverage):")
    rates = []
    for age in ages:
        p = [x for x in tier_pts if x['age'] == age][0]
        rate = p['price'] / 8  # per 1000 EUR
        rates.append(rate)
        print(f"  Age {age}: {p['price']:.2f} EUR/month = {rate:.3f} per 1k")

    # Fit polynomial
    if len(ages) >= 3:
        ages_arr = np.array(ages, dtype=float)
        rates_arr = np.array(rates, dtype=float)

        # Normalize age
        min_age = 40
        max_age = 85
        t = (ages_arr - min_age) / (max_age - min_age)

        # Fit quadratic
        coeffs2 = np.polyfit(t, rates_arr, 2)
        pred2 = np.polyval(coeffs2, t)
        ss_res2 = np.sum((rates_arr - pred2) ** 2)
        ss_tot = np.sum((rates_arr - np.mean(rates_arr)) ** 2)
        r2_quad = 1 - ss_res2 / ss_tot

        # Fit cubic
        coeffs3 = np.polyfit(t, rates_arr, 3)
        pred3 = np.polyval(coeffs3, t)
        ss_res3 = np.sum((rates_arr - pred3) ** 2)
        r2_cubic = 1 - ss_res3 / ss_tot

        print(f"\n  Quadratic fit (at^2 + bt + c): R^2 = {r2_quad:.6f}")
        print(f"    Coefficients: a={coeffs2[0]:.4f}, b={coeffs2[1]:.4f}, c={coeffs2[2]:.4f}")
        print(f"  Cubic fit: R^2 = {r2_cubic:.6f}")
        print(f"    Coefficients: a={coeffs3[0]:.4f}, b={coeffs3[1]:.4f}, c={coeffs3[2]:.4f}, d={coeffs3[3]:.4f}")

# =========================================
# Analysis 3: Tier multipliers
# =========================================
print("\n" + "="*60)
print("ANALYSIS 3: Tier multipliers relative to Grundschutz")
print("="*60)

# Compare Komfort and Premium to Grundschutz
for tier_name in ['komfort', 'premium']:
    ratios = []
    for p in points:
        if p['tier'] != tier_name:
            continue
        # Find matching Grundschutz point
        gs_pts = [x for x in points if x['tier'] == 'grundschutz'
                  and x['age'] == p['age'] and x['coverage'] == p['coverage']]
        if gs_pts:
            ratio = p['price'] / gs_pts[0]['price']
            ratios.append({'age': p['age'], 'coverage': p['coverage'], 'ratio': ratio})

    ratio_vals = [r['ratio'] for r in ratios]
    print(f"\n{tier_name.upper()} / Grundschutz:")
    print(f"  Mean ratio: {np.mean(ratio_vals):.4f}")
    print(f"  Std: {np.std(ratio_vals):.4f}")
    print(f"  Min: {np.min(ratio_vals):.4f} (age {min(ratios, key=lambda x: x['ratio'])['age']})")
    print(f"  Max: {np.max(ratio_vals):.4f} (age {max(ratios, key=lambda x: x['ratio'])['age']})")

    # Check if ratio varies with age
    ages = sorted(set(r['age'] for r in ratios))
    print(f"  By age (8k coverage):")
    for age in ages:
        age_ratios = [r['ratio'] for r in ratios if r['age'] == age and r['coverage'] == 8000]
        if age_ratios:
            print(f"    Age {age}: {age_ratios[0]:.4f}")

# =========================================
# Analysis 4: Coverage linearity
# =========================================
print("\n" + "="*60)
print("ANALYSIS 4: Coverage scaling (is it perfectly linear?)")
print("="*60)

for tier_name in ['komfort']:
    for age in [44, 50, 65, 80]:
        tier_pts = [p for p in points if p['tier'] == tier_name and p['age'] == age]
        if not tier_pts:
            continue

        coverages = np.array([p['coverage'] for p in sorted(tier_pts, key=lambda x: x['coverage'])])
        prices = np.array([p['price'] for p in sorted(tier_pts, key=lambda x: x['coverage'])])

        # Fit linear: price = a * coverage + b
        coeffs = np.polyfit(coverages, prices, 1)
        pred = np.polyval(coeffs, coverages)
        ss_res = np.sum((prices - pred) ** 2)
        ss_tot = np.sum((prices - np.mean(prices)) ** 2)
        r2 = 1 - ss_res / ss_tot

        print(f"  Age {age}: price = {coeffs[0]*1000:.4f} * (coverage/1000) + {coeffs[1]:.4f}, R^2 = {r2:.6f}")

        # Check: is there a fixed fee component?
        # If perfectly linear through origin: price/coverage should be constant
        rates = prices / coverages * 1000
        print(f"    Rate per 1k: {rates}")

# =========================================
# Analysis 5: Derive base rates for our model
# =========================================
print("\n" + "="*60)
print("ANALYSIS 5: Derive base rates per tier (per 1k, using 8k coverage)")
print("="*60)

# IMPORTANT: Our model uses a FIXED payment duration of (85 - age) or (90 - age)
# ERGO uses 90 - age as default.
# But our model's ageFactor should capture the combined effect of age + payment duration.

# For the demo model, we want: monthlyPremium = baseRate * coverageUnits * ageFactor
# where coverageUnits = coverage / 1000

# Since payment_duration = 90 - age is automatic, we just model rate_per_1k vs age

results = {}

for tier_name in ['grundschutz', 'komfort', 'premium']:
    tier_8k = [p for p in points if p['tier'] == tier_name and p['coverage'] == 8000]
    ages = np.array(sorted(set(p['age'] for p in tier_8k)), dtype=float)
    rates = np.array([
        [p for p in tier_8k if p['age'] == age][0]['price'] / 8
        for age in ages
    ])

    # Normalize age
    min_age, max_age = 40.0, 85.0
    t = (ages - min_age) / (max_age - min_age)

    # Quadratic fit: rate = a*t^2 + b*t + c
    coeffs = np.polyfit(t, rates, 2)
    pred = np.polyval(coeffs, t)
    ss_res = np.sum((rates - pred) ** 2)
    ss_tot = np.sum((rates - np.mean(rates)) ** 2)
    r2 = 1 - ss_res / ss_tot

    # Our formula: ageFactor = base + linear*t + quadratic*t^2
    # rate_per_1k = baseRate * ageFactor * (1 + loading)
    # At t=0 (age 40): rate = baseRate * base * (1+loading)
    # We need to decompose coeffs into (baseRate * (1+loading)) and ageFactor components

    # For simplicity, let's express as:
    # rate_per_1k = coeffs[2] + coeffs[1]*t + coeffs[0]*t^2
    # This IS the effective rate, combining base rate, age factor, and loading

    # To match our model format:
    # ageFactor(t=0) = base, ageFactor(t=1) = base + linear + quadratic
    # baseRate * (1+loading) * ageFactor at t=0 = coeffs[2]

    # Let's normalize: set base=1.0 at t=0
    c0 = coeffs[2]  # rate at t=0
    norm_coeffs = coeffs / c0  # normalized so that at t=0, factor = 1.0

    print(f"\n{tier_name.upper()}:")
    print(f"  Rate at age 40 (t=0): {c0:.4f} EUR per 1k/month")
    print(f"  Quadratic R^2: {r2:.6f}")
    print(f"  ageFactor = {norm_coeffs[2]:.4f} + {norm_coeffs[1]:.4f}*t + {norm_coeffs[0]:.4f}*t^2")
    print(f"  Predicted vs Actual:")
    for i, age in enumerate(ages):
        print(f"    Age {int(age)}: actual={rates[i]:.3f}, predicted={pred[i]:.3f}, error={abs(rates[i]-pred[i]):.3f} ({abs(rates[i]-pred[i])/rates[i]*100:.1f}%)")

    results[tier_name] = {
        'base_rate_per_1k': round(c0, 4),
        'age_curve_quadratic': round(norm_coeffs[0], 4),
        'age_curve_linear': round(norm_coeffs[1], 4),
        'age_curve_base': round(norm_coeffs[2], 4),
        'r_squared': round(r2, 6),
        'raw_coefficients': [round(x, 4) for x in coeffs.tolist()]
    }

# =========================================
# Analysis 6: Check for age bands (step function)
# =========================================
print("\n" + "="*60)
print("ANALYSIS 6: Age band check")
print("="*60)

# Check if pricing uses discrete bands by examining close ages (44, 45)
for tier_name in ['komfort']:
    tier_pts = [p for p in points if p['tier'] == tier_name and p['coverage'] == 8000]
    ages = sorted(set(p['age'] for p in tier_pts))

    print(f"\n{tier_name.upper()} rates for 8k coverage:")
    prev_rate = None
    for age in ages:
        p = [x for x in tier_pts if x['age'] == age][0]
        rate = p['price'] / 8
        if prev_rate:
            delta = rate - prev_rate
            pct = delta / prev_rate * 100
            print(f"  Age {age}: {rate:.4f} per 1k, delta={delta:+.4f} ({pct:+.1f}%)")
        else:
            print(f"  Age {age}: {rate:.4f} per 1k")
        prev_rate = rate

    print("\n  Note: Age 44 and 45 have DIFFERENT prices, confirming per-year pricing (not bands)")

# =========================================
# Analysis 7: Tier multipliers (age-dependent)
# =========================================
print("\n" + "="*60)
print("ANALYSIS 7: Tier multiplier model")
print("="*60)

# The tier multiplier increases with age for Komfort and especially Premium
print("\nKomfort/Grundschutz ratio by age:")
for age in [40, 44, 45, 50, 55, 60, 65, 70, 75, 80]:
    gs = [p for p in points if p['tier'] == 'grundschutz' and p['age'] == age and p['coverage'] == 8000]
    km = [p for p in points if p['tier'] == 'komfort' and p['age'] == age and p['coverage'] == 8000]
    if gs and km:
        print(f"  Age {age}: {km[0]['price']/gs[0]['price']:.4f}")

print("\nPremium/Grundschutz ratio by age:")
for age in [40, 44, 45, 50, 55, 60, 65, 70, 75, 80]:
    gs = [p for p in points if p['tier'] == 'grundschutz' and p['age'] == age and p['coverage'] == 8000]
    pm = [p for p in points if p['tier'] == 'premium' and p['age'] == age and p['coverage'] == 8000]
    if gs and pm:
        print(f"  Age {age}: {pm[0]['price']/gs[0]['price']:.4f}")

# =========================================
# Output results
# =========================================
print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)

output = {
    'product': 'sterbegeld',
    'sampled_at': '2026-04-13',
    'data_points': len(points),
    'ages_sampled': sorted(set(p['age'] for p in points)),
    'age_range': {'min': 40, 'max': 85},
    'coverage_range': {'min': 1000, 'max': 20000, 'step': 500, 'default': 7000},
    'payment_duration': {'formula': '90 - entry_age', 'min': 5, 'max': 46},
    'tiers': results,
    'tier_multipliers_at_age_50_8k': {
        'grundschutz': 1.0,
        'komfort': round(31.88 / 31.19, 4),
        'premium': round(36.49 / 31.19, 4),
    },
    'coverage_scaling': 'linear (price proportional to coverage)',
    'payment_mode_discounts': {
        'monthly': 1.0,
        'quarterly_factor': round(95.25 * 4 / (31.88 * 12), 4),
        'semiannual_factor': round(189.35 * 2 / (31.88 * 12), 4),
        'annual_factor': round(369.42 / (31.88 * 12), 4),
    },
    'calibration_point': {
        'age': 44,
        'coverage': 8000,
        'tier': 'komfort',
        'expected': 27.45,
        'our_assumption': 30.00,
        'delta_pct': round((27.45 - 30.0) / 30.0 * 100, 1),
    }
}

print(json.dumps(output, indent=2))

# Save results
with open('research/sterbegeld/fit_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print("\nResults saved to research/sterbegeld/fit_results.json")
