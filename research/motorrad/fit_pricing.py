#!/usr/bin/env python3
"""Analyze ERGO Motorradversicherung pricing model."""

import numpy as np
import json

# Load price matrix
with open('/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/research/motorrad/price-matrix.json') as f:
    data = json.load(f)

print("=" * 70)
print("ERGO Motorradversicherung Pricing Analysis")
print("=" * 70)
print()

# ============================================================
# 1. Verify HP formula: HP = HP_base_100 * SF_pct / 100
# ============================================================
print("1. HP PRICING FORMULA VERIFICATION")
print("-" * 40)

hp_data = data['hp_sf_test']['data']
for d in hp_data:
    if 'smart_hp' in d:
        expected = 22.16 * d['sf_pct'] / 100
        actual = d['smart_hp']
        diff = abs(actual - expected)
        print(f"  SF {d['sf']} ({d['sf_pct']}%): Smart HP = {actual:.2f}, "
              f"expected = {expected:.2f}, diff = {diff:.2f}")

print()

# Smart HP base at 100% = 22.16
# Best HP base at 100% = 26.99
smart_hp_base = 22.16
best_hp_base = 26.99
best_addon = 1.30

print(f"  Smart HP base (100%): {smart_hp_base:.2f} EUR/month")
print(f"  Best HP base (100%):  {best_hp_base:.2f} EUR/month")
print(f"  Best add-on (flat):   {best_addon:.2f} EUR/month")
print(f"  Best/Smart ratio:     {best_hp_base/smart_hp_base:.4f}")
print()

# ============================================================
# 2. Verify VK formula
# ============================================================
print("2. VK PRICING FORMULA VERIFICATION")
print("-" * 40)

vk_data = data['vk_sf_test']['data']
smart_vk_base = 78.49
best_vk_base = 106.45

for d in vk_data:
    # Smart VK
    expected_smart_vk = smart_vk_base * d['vk_sf_pct'] / 100
    actual_smart_vk = d['smart_vk']
    diff_smart = abs(actual_smart_vk - expected_smart_vk)

    # Best VK
    expected_best_vk = best_vk_base * d['vk_sf_pct'] / 100
    actual_best_vk = d['best_vk']
    diff_best = abs(actual_best_vk - expected_best_vk)

    print(f"  VK SF {d['vk_sf']} ({d['vk_sf_pct']}%):")
    print(f"    Smart: actual={actual_smart_vk:.2f}, expected={expected_smart_vk:.2f}, "
          f"diff={diff_smart:.2f}")
    print(f"    Best:  actual={actual_best_vk:.2f}, expected={expected_best_vk:.2f}, "
          f"diff={diff_best:.2f}")

# Try to find the correct Best VK base by fitting
best_vk_points = [(d['vk_sf_pct'], d['best_vk']) for d in vk_data]
# Linear fit: vk = base * pct/100
# Least squares: base = sum(vk * pct/100) / sum((pct/100)^2)
numerator = sum(vk * pct/100 for pct, vk in best_vk_points)
denominator = sum((pct/100)**2 for pct, _ in best_vk_points)
fitted_best_vk_base = numerator / denominator
print(f"\n  Fitted Best VK base: {fitted_best_vk_base:.2f} (vs observed at 100%: {best_vk_base})")

# Check residuals with fitted base
for pct, vk in best_vk_points:
    expected = fitted_best_vk_base * pct / 100
    print(f"    VK {pct}%: actual={vk:.2f}, fitted={expected:.2f}, diff={abs(vk-expected):.2f}")

print()

# ============================================================
# 3. TK verification (flat rate)
# ============================================================
print("3. TK PRICING VERIFICATION (FLAT RATE)")
print("-" * 40)

tk_data = data['tk_test']['data']
print(f"  Smart TK: {tk_data[0]['smart_tk']:.2f} (SF 0) vs {tk_data[1]['smart_tk']:.2f} (SF 10)")
print(f"  Best TK:  {tk_data[0]['best_tk']:.2f} (SF 0) vs {tk_data[1]['best_tk']:.2f} (SF 10)")
print(f"  => TK is FLAT (no SF scaling)")
print(f"  Smart TK flat: {tk_data[0]['smart_tk']:.2f} EUR/month")
print(f"  Best TK flat:  {tk_data[0]['best_tk']:.2f} EUR/month")
print()

# ============================================================
# 4. Age effect analysis
# ============================================================
print("4. AGE EFFECT ANALYSIS")
print("-" * 40)

age_data = data['age_effect_test']['data']
ages = [d['age'] for d in age_data]
prices = [d['hp_smart'] for d in age_data]

print("  Age vs Smart HP SF 10 price:")
for d in age_data:
    print(f"    Age {d['age']}: {d['hp_smart']:.2f} EUR")

# Compute age factor relative to the base (age 36)
base_price_age36 = 6.65
print(f"\n  Age factors (relative to age 36 = 1.00):")
for d in age_data:
    factor = d['hp_smart'] / base_price_age36
    print(f"    Age {d['age']}: factor = {factor:.4f}")

# Fit a quadratic: factor = a + b*age + c*age^2
factors = [p / base_price_age36 for p in prices]
A = np.array([[1, a, a**2] for a in ages])
coeffs = np.linalg.lstsq(A, factors, rcond=None)[0]
base, linear, quadratic = coeffs

print(f"\n  Quadratic age curve fit:")
print(f"    factor(age) = {base:.6f} + {linear:.6f} * age + {quadratic:.6f} * age^2")

# Check the fit
print(f"\n  Fit quality:")
for a, f_actual in zip(ages, factors):
    f_predicted = base + linear * a + quadratic * a**2
    print(f"    Age {a}: actual={f_actual:.4f}, predicted={f_predicted:.4f}, "
          f"diff={abs(f_actual-f_predicted):.4f}")

# Find minimum age
min_age = -linear / (2 * quadratic)
min_factor = base + linear * min_age + quadratic * min_age**2
print(f"\n  Minimum at age: {min_age:.1f}")
print(f"  Minimum factor: {min_factor:.4f}")

# Now express as: price(age) = hp_base_sf0 * sf_pct/100 * age_factor(age)
# hp_base_sf0 at age 36 = 22.16
# But hp_base_sf0 is age-dependent, so the actual base is:
# hp_base_sf0(age) = 22.16 * age_factor(age) / age_factor(36)
# Since we normalized to age 36, the formula simplifies to:
# hp_monthly(age, sf) = hp_base * age_factor(age) * sf_pct/100

print()

# ============================================================
# 5. Best tier breakdown
# ============================================================
print("5. BEST TIER ANALYSIS")
print("-" * 40)

# For HP only:
# Smart total = HP_base * SF_pct/100 * age_factor
# Best total = Best_HP_base * SF_pct/100 * age_factor + best_addon

# Best/Smart HP ratio
ratio = best_hp_base / smart_hp_base
print(f"  Best/Smart HP base ratio: {ratio:.4f}")
print(f"  This means Best HP = Smart HP * {ratio:.4f}")
print(f"  Plus flat add-on: {best_addon:.2f} EUR/month")

# For VK:
# Best VK appears to have a similar ratio plus an additional component
# Let's compute the implied ratios
vk_ratio = best_vk_base / smart_vk_base
print(f"\n  Best/Smart VK base ratio: {vk_ratio:.4f}")

# Check if Best VK = Smart VK * ratio + flat?
for d in vk_data:
    smart = d['smart_vk']
    best = d['best_vk']
    implied_ratio = best / smart
    print(f"    VK SF {d['vk_sf_pct']}%: Smart={smart:.2f}, Best={best:.2f}, "
          f"ratio={implied_ratio:.4f}")

print()

# ============================================================
# 6. Summary
# ============================================================
print("=" * 70)
print("PRICING MODEL SUMMARY")
print("=" * 70)
print()
print("Template: E-variant (Kfz-like, additive HP+VK, SF lookup, WITH age curve)")
print()
print("Formula:")
print("  monthly = HP_base * age_factor(age) * SF_HP_pct/100")
print("          + VK_base * age_factor(age) * SF_VK_pct/100  (if VK)")
print("          + TK_flat                                      (if TK)")
print("          + tier_addon                                   (if Best)")
print()
print("Parameters (for Honda CBF 500, PLZ 80331, 6000km):")
print(f"  Smart HP base (at 100%, age ~46): ~{smart_hp_base * min_factor:.2f} EUR")
print(f"  Best HP base (at 100%, age ~46):  ~{best_hp_base * min_factor:.2f} EUR")
print(f"  Smart VK base (at 100%, age ~46): ~{smart_vk_base * min_factor:.2f} EUR")
print(f"  Best VK base (at 100%, age ~46):  ~{best_vk_base * min_factor:.2f} EUR")
print(f"  Smart TK flat: {tk_data[0]['smart_tk']:.2f} EUR")
print(f"  Best TK flat:  {tk_data[0]['best_tk']:.2f} EUR")
print(f"  Best addon (flat): {best_addon:.2f} EUR")
print()
print("Age curve (quadratic):")
print(f"  factor(age) = {base:.6f} + {linear:.6f}*age + {quadratic:.6f}*age^2")
print(f"  Minimum at age {min_age:.0f}, factor = {min_factor:.4f}")
print(f"  Age 26: factor = {base + linear*26 + quadratic*26**2:.4f}")
print(f"  Age 36: factor = {base + linear*36 + quadratic*36**2:.4f}")
print(f"  Age 46: factor = {base + linear*46 + quadratic*46**2:.4f}")
print(f"  Age 66: factor = {base + linear*66 + quadratic*66**2:.4f}")
print()
print("SF tables: 22 levels each (0 through 20+)")
print("  HP: 100, 74, 54, 48, 44, 40, 38, 36, 34, 32, 31, 30, 29, 28, 28,")
print("      27, 27, 26, 26, 25, 25, 24")
print("  VK: 100, 76, 55, 49, 46, 43, 40, 38, 36, 35, 34, 33, 32, 31, 30,")
print("      30, 29, 28, 28, 28, 27, 27")
print()
print("Key differences from Kfz:")
print("  1. Age curve EXISTS (Kfz had none)")
print("  2. Only 22 SF levels (Kfz had 51)")
print("  3. HP SF 0 = 100% (Kfz was 86%)")
print("  4. Motorcycle-specific: Motorradbekleidung Plus, Saisonkennzeichen")
print("  5. TK also shows SF info but price is flat (same as Kfz)")
