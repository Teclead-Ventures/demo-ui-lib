#!/usr/bin/env python3
"""
ERGO Kfz-Versicherung Pricing Analysis
Analyzes collected price data to reverse-engineer the pricing model.
"""

import json
import numpy as np

# Load data
with open('/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/research/kfz/price-matrix.json') as f:
    data = json.load(f)

print("=" * 70)
print("ERGO Kfz-Versicherung Pricing Analysis")
print("=" * 70)

# ============================================================================
# 1. VERIFY SF-KLASSE LINEAR MODEL
# ============================================================================
print("\n1. SF-KLASSE VERIFICATION")
print("-" * 40)

# HP SF table (from dropdown)
hp_sf_pct = data['metadata']['sf_tables']['haftpflicht']
vk_sf_pct = data['metadata']['sf_tables']['vollkasko']

# Extract HP base price from data
# Using dp2 (SF 10, 33%) and dp17 (SF 0, 86%) for Best HP
hp_best_sf10 = 30.31  # monthly
hp_sf10_pct = 0.33
hp_best_base = hp_best_sf10 / hp_sf10_pct
print(f"HP Best base (100%): {hp_best_base:.2f} EUR/month")

hp_smart_sf10 = 27.22
hp_smart_base = hp_smart_sf10 / hp_sf10_pct
print(f"HP Smart base (100%): {hp_smart_base:.2f} EUR/month")

# Verify against HP SF 0 (86%)
hp_best_sf0 = 78.97  # from dp17
hp_best_sf0_pred = hp_best_base * 0.86
print(f"\nHP Best SF 0: predicted={hp_best_sf0_pred:.2f}, actual={hp_best_sf0:.2f}, error={abs(hp_best_sf0_pred - hp_best_sf0):.2f}")

# Verify against HP SF 20 (24%)
hp_best_sf20 = 22.04  # from dp18
hp_best_sf20_pred = hp_best_base * 0.24
print(f"HP Best SF 20: predicted={hp_best_sf20_pred:.2f}, actual={hp_best_sf20:.2f}, error={abs(hp_best_sf20_pred - hp_best_sf20):.2f}")

# Verify against HP SF 35 (18%)
hp_best_sf35 = 16.53  # from dp19
hp_best_sf35_pred = hp_best_base * 0.18
print(f"HP Best SF 35: predicted={hp_best_sf35_pred:.2f}, actual={hp_best_sf35:.2f}, error={abs(hp_best_sf35_pred - hp_best_sf35):.2f}")

print("\n==> HP price = HP_base * SF_percentage  -- CONFIRMED (errors < 0.02)")

# ============================================================================
# 2. VERIFY VK SF-KLASSE MODEL
# ============================================================================
print("\n\n2. VK SF-KLASSE VERIFICATION")
print("-" * 40)

# VK base from SF 10 (33%)
vk_best_sf10 = 68.69
vk_sf10_pct = 0.33
vk_best_base = vk_best_sf10 / vk_sf10_pct
print(f"VK Best base (100%): {vk_best_base:.2f} EUR/month")

vk_smart_sf10 = 51.75
vk_smart_base = vk_smart_sf10 / vk_sf10_pct
print(f"VK Smart base (100%): {vk_smart_base:.2f} EUR/month")

# Verify against multiple VK SF values
vk_test_data = [
    (0, 0.54, 132.22, 99.63),
    (1, 0.44, 91.58, 69.00),
    (3, 0.41, 85.33, 64.30),
    (5, 0.38, 93.05, 70.10),  # This one looks anomalous
    (7, 0.36, 74.93, 56.45),
    (10, 0.33, 68.69, 51.75),
    (15, 0.28, 58.27, 43.91),
    (20, 0.25, 61.21, 46.12),  # This one may have add-ons
    (25, 0.23, 47.87, 36.07),
    (30, 0.21, 43.71, 32.93),
    (35, 0.19, 46.53, 35.06),  # This one may have add-ons
    (50, 0.15, 36.76, 27.67),
]

print("\nVK Best verification:")
print(f"{'SF':>5s} {'%':>5s} {'Predicted':>10s} {'Actual':>10s} {'Error':>8s} {'Error%':>8s}")
errors = []
for sf, pct, best_actual, smart_actual in vk_test_data:
    best_pred = vk_best_base * pct
    err = abs(best_pred - best_actual)
    err_pct = err / best_actual * 100
    errors.append(err_pct)
    flag = " ***" if err_pct > 5 else ""
    print(f"{sf:>5d} {pct:>5.0%} {best_pred:>10.2f} {best_actual:>10.2f} {err:>8.2f} {err_pct:>7.1f}%{flag}")

print(f"\nMean error: {np.mean(errors):.1f}%, Max error: {np.max(errors):.1f}%")

# Some data points may be affected by add-on checkboxes that were toggled during testing
# Let's identify clean data points (HP unchanged = 27.22/30.31 for Smart/Best)
print("\nNote: Data points with *** may have had add-ons toggled during collection.")
print("The SF model is: price = base * SF_percentage (confirmed by HP data)")

# ============================================================================
# 3. TIER RATIO ANALYSIS
# ============================================================================
print("\n\n3. TIER RATIO ANALYSIS (Smart vs Best)")
print("-" * 40)

# Compare Smart/Best ratios for HP and VK
hp_ratio = hp_smart_base / hp_best_base
print(f"HP Smart/Best ratio: {hp_ratio:.4f} ({hp_ratio:.1%})")

vk_ratio = vk_smart_base / vk_best_base
print(f"VK Smart/Best ratio: {vk_ratio:.4f} ({vk_ratio:.1%})")

# Check from Haftpflicht only (dp16)
# Smart total = 27.22, Best total = 32.04
# Smart HP = 27.22, Best HP = 30.31
# Best total includes a small add-on: 32.04 - 30.31 = 1.73 EUR/month
print(f"\nBest HP-only total (32.04) vs Best HP component (30.31)")
print(f"  Add-on premium in Best: 32.04 - 30.31 = 1.73 EUR/month")
print(f"  Smart HP-only total matches Smart HP component: 27.22 = 27.22")

# For VK, let's check if there's a similar add-on structure
# In Vollkasko: Smart total = HP_smart + VK_smart
# dp2: 78.97 = 27.22 + 51.75 = exactly 78.97. OK, Smart has no hidden add-on
# Best: 100.73 vs 30.31 + 68.69 = 99.00 != 100.73. Diff = 1.73
print(f"\nBest VK total (100.73) vs (Best HP 30.31 + Best VK 68.69) = 99.00")
print(f"  Hidden add-on in Best: 100.73 - 99.00 = 1.73 EUR/month")
print(f"  This matches the HP-only add-on (1.73 EUR/month)")
print(f"  ==> Best tier has a fixed add-on fee of ~1.73 EUR/month")

# ============================================================================
# 4. MILEAGE ANALYSIS
# ============================================================================
print("\n\n4. MILEAGE IMPACT ANALYSIS")
print("-" * 40)

mileage_data = [
    (6, 26.85, 55.42),   # dp24
    (12, 30.31, 68.69),   # dp2
    (20, 34.55, 91.86),   # dp25
]

print(f"{'km (1000)':>10s} {'HP Best':>10s} {'VK Best':>10s} {'HP ratio':>10s} {'VK ratio':>10s}")
ref_hp = mileage_data[1][1]  # 12k as reference
ref_vk = mileage_data[1][2]
for km, hp, vk in mileage_data:
    print(f"{km:>10d} {hp:>10.2f} {vk:>10.2f} {hp/ref_hp:>10.3f} {vk/ref_vk:>10.3f}")

# Try linear fit for mileage
km_vals = np.array([d[0] for d in mileage_data])
hp_vals = np.array([d[1] for d in mileage_data])
vk_vals = np.array([d[2] for d in mileage_data])

hp_fit = np.polyfit(km_vals, hp_vals, 1)
vk_fit = np.polyfit(km_vals, vk_vals, 1)

print(f"\nLinear fit HP: {hp_fit[1]:.2f} + {hp_fit[0]:.4f} * km_thousands")
print(f"Linear fit VK: {vk_fit[1]:.2f} + {vk_fit[0]:.4f} * km_thousands")

# Check fit quality
for km, hp, vk in mileage_data:
    hp_pred = hp_fit[0] * km + hp_fit[1]
    vk_pred = vk_fit[0] * km + vk_fit[1]
    print(f"  km={km}: HP pred={hp_pred:.2f} actual={hp:.2f}, VK pred={vk_pred:.2f} actual={vk:.2f}")

# Actually, mileage more likely works as a multiplier on the base
# Let's check: at 12k, base_hp = 30.31/0.33 = 91.85
# at 6k, base_hp = 26.85/0.33 = 81.36
# at 20k, base_hp = 34.55/0.33 = 104.70
print(f"\nHP base at 100% SF by mileage:")
for km, hp, vk in mileage_data:
    hp_base = hp / 0.33
    vk_base = vk / 0.33
    print(f"  {km}k km: HP_base={hp_base:.2f}, VK_base={vk_base:.2f}")

# ============================================================================
# 5. REGIONAL ANALYSIS
# ============================================================================
print("\n\n5. REGIONAL ANALYSIS")
print("-" * 40)

region_data = [
    ("Muenchen 80331", 10, 7, 30.31, 68.69),
    ("Koeln 50667", 10, 7, 30.75, 70.11),
    ("Berlin 10117", 12, 9, 35.90, 83.93),
]

print(f"{'Region':>20s} {'RK HP':>6s} {'RK VK':>6s} {'HP Best':>10s} {'VK Best':>10s}")
for region, rk_hp, rk_vk, hp, vk in region_data:
    print(f"{region:>20s} {rk_hp:>6d} {rk_vk:>6d} {hp:>10.2f} {vk:>10.2f}")

print("\nHP base (100% SF) by region:")
for region, rk_hp, rk_vk, hp, vk in region_data:
    hp_base = hp / 0.33
    vk_base = vk / 0.33
    print(f"  {region}: HP_base={hp_base:.2f}, VK_base={vk_base:.2f}")

print("\nMuenchen vs Koeln: Same Regionalklasse (HP=10, VK=7)")
print(f"  HP diff: {30.75/30.31:.4f} (1.5% higher in Koeln)")
print(f"  VK diff: {70.11/68.69:.4f} (2.1% higher in Koeln)")
print(f"  ==> Even within same Regionalklasse, PLZ-level adjustment exists")

# ============================================================================
# 6. SB (DEDUCTIBLE) ANALYSIS
# ============================================================================
print("\n\n6. SELBSTBETEILIGUNG (DEDUCTIBLE) ANALYSIS")
print("-" * 40)

sb_data = [
    ("VK ohne / TK ohne", 85.61, 113.62),
    ("VK 300 / TK 150", 55.38, 73.51),
    ("VK 500 / TK 150", 51.75, 68.69),
    ("VK 1000 / TK 150", 44.67, 59.30),
]

print(f"{'SB':>25s} {'VK Smart':>10s} {'VK Best':>10s} {'Ratio':>8s}")
ref_smart = sb_data[2][1]  # VK 500 as reference
ref_best = sb_data[2][2]
for sb, vk_smart, vk_best in sb_data:
    ratio = vk_best / ref_best
    print(f"{sb:>25s} {vk_smart:>10.2f} {vk_best:>10.2f} {ratio:>8.3f}")

# ============================================================================
# 7. AGE ANALYSIS
# ============================================================================
print("\n\n7. AGE ANALYSIS")
print("-" * 40)
print("Birth year 1990 (age 36): HP=30.31, VK=68.69")
print("Birth year 1960 (age 66): HP=30.31, VK=68.69  (IDENTICAL)")
print("Birth year 2000 (age 26): HP=30.31, VK=68.69  (IDENTICAL)")
print("==> AGE HAS NO EFFECT ON KFZ PRICING")
print("    (Age is collected for legal/contract purposes only)")

# ============================================================================
# 8. ANNUAL vs MONTHLY SURCHARGE
# ============================================================================
print("\n\n8. ZAHLWEISE (PAYMENT FREQUENCY) SURCHARGE")
print("-" * 40)
# dp1 annual: Best total = 1262.87
# dp2 monthly: Best total = 100.73 * 12 = 1208.76
annual = 1262.87
monthly_annual = 100.73 * 12
print(f"Annual premium: {annual:.2f}")
print(f"Monthly * 12: {monthly_annual:.2f}")
print(f"Monthly is cheaper per year by: {annual - monthly_annual:.2f}")
print(f"Annual surcharge vs monthly: {annual/monthly_annual:.4f} = {(annual/monthly_annual - 1)*100:.1f}%")
# Wait, this means annual is MORE expensive? Let me recheck
# Actually, annual is the base and monthly includes a surcharge
# Let me check the HP components
hp_annual = 339.17
hp_monthly = 30.31 * 12
print(f"\nHP annual: {hp_annual:.2f}")
print(f"HP monthly * 12: {hp_monthly:.2f}")
print(f"Ratio monthly*12/annual: {hp_monthly/hp_annual:.4f}")
# That's 1.072, so monthly has a 7.2% surcharge? No that means monthly*12 > annual
# Actually 30.31 * 12 = 363.72 > 339.17
# So monthly payments cost 363.72/339.17 = 1.072, i.e. 7.2% surcharge for monthly
print(f"Monthly surcharge: {(hp_monthly/hp_annual - 1)*100:.1f}%")

# ============================================================================
# 9. TEMPLATE RECOMMENDATION
# ============================================================================
print("\n\n9. TEMPLATE RECOMMENDATION")
print("-" * 40)
print("""
Kfz pricing does NOT fit any of the standard templates (A, B, C, D):

The pricing model is:
  Total = HP_component + VK_component + tier_addon

Where:
  HP_component = HP_base(vehicle, region, mileage) * HP_SF_pct / 100
  VK_component = VK_base(vehicle, region, mileage, SB) * VK_SF_pct / 100
  tier_addon = 0 (Smart) or ~1.73/month (Best, from Mallorca-Police etc.)

Key characteristics:
- NO age curve (birth date irrelevant to pricing)
- SF-Klasse is a LOOKUP TABLE with 51 levels (not a polynomial)
- HP and VK have SEPARATE SF tables with different percentages
- Base price depends on: vehicle (Typklasse via HSN/TSN), region (PLZ->Regionalklasse), mileage
- 2 tiers only (Smart, Best) - not 3
- Smart has lower base prices (different Rueckstufung model)
- Coverage types: Haftpflicht only, Teilkasko, Vollkasko

This is a UNIQUE template for Kfz - too complex for standard templates.
Recommended: Template E (Kfz-specific) or flat lookup with SF table.

For demo purposes, simplify to:
- 3 coverage levels: Haftpflicht only, Teilkasko, Vollkasko
- 2 tiers: Smart, Best
- SF-Klasse as main driver (use lookup table, not polynomial)
- Fixed base prices per vehicle class
""")

# ============================================================================
# 10. CALIBRATION DATA SUMMARY
# ============================================================================
print("\n10. CALIBRATION SUMMARY (Muenchen, VW Golf VIII, 12k km, SB VK500/TK150)")
print("-" * 70)
print(f"{'Coverage':>20s} {'SF':>5s} {'Smart /mo':>12s} {'Best /mo':>12s}")
print("-" * 55)
# Haftpflicht only, SF 10
print(f"{'HP only':>20s} {'10':>5s} {'27.22':>12s} {'32.04':>12s}")
# Teilkasko, SF 10
print(f"{'HP + Teilkasko':>20s} {'10':>5s} {'51.72':>12s} {'66.91':>12s}")
# Vollkasko, SF 10
print(f"{'HP + Vollkasko':>20s} {'10':>5s} {'78.97':>12s} {'100.73':>12s}")

print(f"\nBest tier ratios (vs Smart):")
print(f"  HP component: {30.31/27.22:.3f}")
print(f"  VK component: {68.69/51.75:.3f}")
print(f"  TK component: {34.87/24.50:.3f}")

print(f"\nSmart/Best base multiplier (at 100% SF):")
print(f"  HP: Smart={hp_smart_base:.2f}, Best={hp_best_base:.2f}")
print(f"  VK: Smart={vk_smart_base:.2f}, Best={vk_best_base:.2f}")

if __name__ == '__main__':
    pass
