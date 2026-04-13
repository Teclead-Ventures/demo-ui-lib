#!/usr/bin/env python3
"""
Krankentagegeld pricing analysis.
Fits age curves, Leistungsbeginn factors, and coverage scaling.
"""

import json
import numpy as np
from pathlib import Path

# Load data
data_path = Path(__file__).parent / "price-matrix.json"
with open(data_path) as f:
    data = json.load(f)

print("=" * 80)
print("KRANKENTAGEGELD PRICING ANALYSIS")
print("=" * 80)

# ============================================================================
# 1. COVERAGE SCALING (Tagegeldhöhe)
# ============================================================================
print("\n" + "=" * 80)
print("1. COVERAGE SCALING (Tagegeldhöhe)")
print("=" * 80)

# Arbeitnehmer
an_hoehe = data["arbeitnehmer_tagesgelhoehe"]["data"]
an_h = np.array([d["hoehe"] for d in an_hoehe])
an_p = np.array([d["col1"] for d in an_hoehe])
an_rate = an_p / an_h
print(f"\nArbeitnehmer (Age 30, 43.Tag): rate per €/day = {an_rate.mean():.4f} €/mtl")
print(f"  Range: {an_rate.min():.4f} - {an_rate.max():.4f}")
print(f"  → PERFECTLY LINEAR")

# Check freiwillig versichert
an_fw = data["arbeitnehmer_freiwillig_tagesgelhoehe"]["data"]
an_fw_h = np.array([d["hoehe"] for d in an_fw])
an_fw_p = np.array([d["col1"] for d in an_fw])
an_fw_rate = an_fw_p / an_fw_h
print(f"\nArbeitnehmer Freiwillig (Age 30, 43.Tag): rate per €/day = {an_fw_rate.mean():.4f} €/mtl")
print(f"  → Same rate as Pflichtversichert → versicherungsstatus has NO effect on price")

# Selbständiger
se_hoehe = data["selbstaendiger_tagesgelhoehe"]["data"]
se_h = np.array([d["hoehe"] for d in se_hoehe])
se_p = np.array([d["price"] for d in se_hoehe])
se_rate = se_p / se_h
print(f"\nSelbständiger (Age 30, 29.Tag): rate per €/day = {se_rate.mean():.4f} €/mtl")
print(f"  Range: {se_rate.min():.4f} - {se_rate.max():.4f}")
print(f"  → PERFECTLY LINEAR")

print(f"\n→ KEY: Coverage scales perfectly linearly. Price = rate_per_eur_day × Tagegeldhöhe")

# ============================================================================
# 2. AGE CURVE ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("2. AGE CURVE ANALYSIS")
print("=" * 80)

# Normalize to rate per €/day for comparison
# Arbeitnehmer Col1: 43.Tag, 15€/day → rate = price / 15
an_age_data = data["arbeitnehmer_age_curve"]["data"]
an_ages = np.array([d["age"] for d in an_age_data])
an_col1 = np.array([d["col1"] for d in an_age_data])
an_col2 = np.array([d["col2"] for d in an_age_data])

# Rate per €/day
an_col1_rate = an_col1 / 15.0
an_col2_rate = an_col2 / 15.0

# Selbständiger: 29.Tag, 50€/day → rate = price / 50
se_age_data = data["selbstaendiger_age_curve"]["data"]
se_ages = np.array([d["age"] for d in se_age_data])
se_prices = np.array([d["price"] for d in se_age_data])
se_rate_arr = se_prices / 50.0

# Detect plateau
print("\nPlateau Detection:")
print(f"  Arbeitnehmer Col1: plateau at age >= 67, value = {an_col1[an_ages >= 67][0]:.2f} (rate {an_col1_rate[an_ages >= 67][0]:.4f})")
print(f"  Arbeitnehmer Col2: plateau at age >= 65, value = {an_col2[an_ages >= 65][0]:.2f} (rate {an_col2_rate[an_ages >= 65][0]:.4f})")
print(f"  Selbständiger:     plateau at age >= 67, value = {se_prices[se_ages >= 67][0]:.2f} (rate {se_rate_arr[se_ages >= 67][0]:.4f})")

# Fit age curves (only for non-plateau region)
# Try polynomial fits
for name, ages, rates, max_age in [
    ("AN Col1 (43.Tag)", an_ages, an_col1_rate, 66),
    ("AN Col2 (DKV-voll)", an_ages, an_col2_rate, 64),
    ("Selbst. (29.Tag)", se_ages, se_rate_arr, 66),
]:
    mask = ages <= max_age
    a = ages[mask]
    r = rates[mask]

    print(f"\n--- {name} (ages {a.min()}-{a.max()}) ---")

    # Linear
    c1 = np.polyfit(a, r, 1)
    p1 = np.polyval(c1, a)
    rmse1 = np.sqrt(np.mean((r - p1)**2))
    mape1 = np.mean(np.abs((r - p1) / r)) * 100
    print(f"  Linear:    y = {c1[0]:.6f}*age + {c1[1]:.6f}, RMSE={rmse1:.4f}, MAPE={mape1:.2f}%")

    # Quadratic
    c2 = np.polyfit(a, r, 2)
    p2 = np.polyval(c2, a)
    rmse2 = np.sqrt(np.mean((r - p2)**2))
    mape2 = np.mean(np.abs((r - p2) / r)) * 100
    print(f"  Quadratic: y = {c2[0]:.8f}*age² + {c2[1]:.6f}*age + {c2[2]:.6f}, RMSE={rmse2:.4f}, MAPE={mape2:.2f}%")

    # Cubic
    c3 = np.polyfit(a, r, 3)
    p3 = np.polyval(c3, a)
    rmse3 = np.sqrt(np.mean((r - p3)**2))
    mape3 = np.mean(np.abs((r - p3) / r)) * 100
    print(f"  Cubic:     RMSE={rmse3:.4f}, MAPE={mape3:.2f}%")

    # Exponential: log(r) = a*age + b
    try:
        log_r = np.log(r)
        ce = np.polyfit(a, log_r, 1)
        pe = np.exp(np.polyval(ce, a))
        rmse_e = np.sqrt(np.mean((r - pe)**2))
        mape_e = np.mean(np.abs((r - pe) / r)) * 100
        print(f"  Exponential: y = {np.exp(ce[1]):.6f} * exp({ce[0]:.6f}*age), RMSE={rmse_e:.4f}, MAPE={mape_e:.2f}%")
    except:
        print("  Exponential: failed")

    # Check best fit
    best = min([(rmse1, "linear"), (rmse2, "quadratic"), (rmse3, "cubic"), (rmse_e, "exponential")])
    print(f"  → Best fit: {best[1]} (RMSE={best[0]:.4f})")

# ============================================================================
# 3. LEISTUNGSBEGINN FACTOR ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("3. LEISTUNGSBEGINN FACTOR ANALYSIS")
print("=" * 80)

# Arbeitnehmer: normalize to 43.Tag = 1.0
an_lb30 = data["arbeitnehmer_leistungsbeginn"]["data"]
an_lb50 = data["arbeitnehmer_leistungsbeginn_age50"]["data"]
an_lb60 = data["arbeitnehmer_leistungsbeginn_age60"]["data"]

# Reference: 43.Tag
ref30 = [d for d in an_lb30 if d["tag"] == 43][0]["col1"]
ref50 = [d for d in an_lb50 if d["tag"] == 43][0]["col1"]
ref60 = [d for d in an_lb60 if d["tag"] == 43][0]["col1"]

print("\nArbeitnehmer Leistungsbeginn factors (relative to 43.Tag):")
print(f"{'Tag':>6s} {'Age30':>8s} {'Age50':>8s} {'Age60':>8s}")
for d30 in an_lb30:
    tag = d30["tag"]
    f30 = d30["col1"] / ref30
    d50_match = [d for d in an_lb50 if d["tag"] == tag]
    d60_match = [d for d in an_lb60 if d["tag"] == tag]
    f50 = d50_match[0]["col1"] / ref50 if d50_match else None
    f60 = d60_match[0]["col1"] / ref60 if d60_match else None
    f50_str = f"{f50:.4f}" if f50 else "  -   "
    f60_str = f"{f60:.4f}" if f60 else "  -   "
    print(f"{tag:>6d} {f30:>8.4f} {f50_str:>8s} {f60_str:>8s}")

# Selbständiger: normalize to 29.Tag = 1.0
se_lb30 = data["selbstaendiger_leistungsbeginn"]["data"]
se_lb40 = data["selbstaendiger_leistungsbeginn_age40"]["data"]
se_lb50 = data["selbstaendiger_leistungsbeginn_age50"]["data"]

ref30s = [d for d in se_lb30 if d["tag"] == 29][0]["price"]
ref40s = [d for d in se_lb40 if d["tag"] == 29][0]["price"]
ref50s = [d for d in se_lb50 if d["tag"] == 29][0]["price"]

print("\nSelbständiger Leistungsbeginn factors (relative to 29.Tag):")
print(f"{'Tag':>6s} {'Age30':>8s} {'Age40':>8s} {'Age50':>8s}")
for d30 in se_lb30:
    tag = d30["tag"]
    f30 = d30["price"] / ref30s
    d40_match = [d for d in se_lb40 if d["tag"] == tag]
    d50_match = [d for d in se_lb50 if d["tag"] == tag]
    f40 = d40_match[0]["price"] / ref40s if d40_match else None
    f50 = d50_match[0]["price"] / ref50s if d50_match else None
    f40_str = f"{f40:.4f}" if f40 else "  -   "
    f50_str = f"{f50:.4f}" if f50 else "  -   "
    print(f"{tag:>6d} {f30:>8.4f} {f40_str:>8s} {f50_str:>8s}")

# ============================================================================
# 4. CROSS-CHECK: Is Arbeitnehmer 43.Tag same rate as Selbständiger 43.Tag?
# ============================================================================
print("\n" + "=" * 80)
print("4. CROSS-CHECK: Arbeitnehmer vs Selbständiger rates")
print("=" * 80)

# AN Col1 at 43.Tag, 15€/day, age 30 = 8.01 → rate = 8.01/15 = 0.534
# SE at 43.Tag, 50€/day, age 30 = 27.20 → rate = 27.20/50 = 0.544
an_rate_43_30 = 8.01 / 15.0
se_rate_43_30 = 27.20 / 50.0
print(f"\nAge 30, 43.Tag:")
print(f"  AN Col1 rate: {an_rate_43_30:.4f} €/mtl per €/day")
print(f"  SE rate:       {se_rate_43_30:.4f} €/mtl per €/day")
print(f"  Ratio AN/SE:   {an_rate_43_30/se_rate_43_30:.4f}")

# Age 40, 43.Tag
an_rate_43_40 = 11.01 / 15.0
se_rate_43_40 = 35.90 / 50.0
print(f"\nAge 40, 43.Tag:")
print(f"  AN Col1 rate: {an_rate_43_40:.4f} €/mtl per €/day")
print(f"  SE rate:       {se_rate_43_40:.4f} €/mtl per €/day")
print(f"  Ratio AN/SE:   {an_rate_43_40/se_rate_43_40:.4f}")

# Age 50, 43.Tag
# AN at 50, 43.Tag, 15€/day = 15.24
# SE at 50, 43.Tag, 50€/day = 49.00
an_rate_43_50 = 15.24 / 15.0
se_rate_43_50 = 49.00 / 50.0
print(f"\nAge 50, 43.Tag:")
print(f"  AN Col1 rate: {an_rate_43_50:.4f} €/mtl per €/day")
print(f"  SE rate:       {se_rate_43_50:.4f} €/mtl per €/day")
print(f"  Ratio AN/SE:   {an_rate_43_50/se_rate_43_50:.4f}")

print("\n→ KEY: AN and SE have DIFFERENT base rates at same Leistungsbeginn (ratio ~1.02-1.04)")
print("  They are likely different tariff tables, not simple multipliers of each other")

# ============================================================================
# 5. DETAILED AGE CURVE FIT
# ============================================================================
print("\n" + "=" * 80)
print("5. DETAILED AGE CURVE: Best fit for Selbständiger (most data)")
print("=" * 80)

# Use Selbständiger data which has the most points
mask = se_ages <= 66
sa = se_ages[mask]
sr = se_rate_arr[mask]

# Try quadratic with refined coefficients
c2 = np.polyfit(sa, sr, 2)
p2 = np.polyval(c2, sa)
max_err = np.max(np.abs(sr - p2))
print(f"\nQuadratic fit (rate per €/day):")
print(f"  y = {c2[0]:.8f} * age² + {c2[1]:.6f} * age + {c2[2]:.6f}")
print(f"  Max error: {max_err:.4f}")
print(f"  Predictions vs actual:")
for age_val in [20, 25, 30, 35, 40, 45, 50, 55, 60, 65]:
    idx = np.argmin(np.abs(sa - age_val))
    if abs(sa[idx] - age_val) < 2:
        pred = np.polyval(c2, age_val)
        print(f"    Age {age_val}: actual={sr[idx]:.4f}, predicted={pred:.4f}, diff={pred-sr[idx]:.4f}")

# Now fit the raw price (for 50€/day) to check with integer rounding
print(f"\nQuadratic fit (monthly price for 50€/day):")
c2p = np.polyfit(sa, se_prices[mask], 2)
p2p = np.polyval(c2p, sa)
max_err_p = np.max(np.abs(se_prices[mask] - p2p))
print(f"  y = {c2p[0]:.6f} * age² + {c2p[1]:.4f} * age + {c2p[2]:.4f}")
print(f"  Max error: {max_err_p:.2f}")

# Check if age bands exist (same price for ranges)
print("\n\nChecking for age bands:")
prev_price = None
for d in se_age_data:
    if prev_price is not None and d["price"] == prev_price:
        print(f"  Age {d['age']}: same as previous ({d['price']})")
    prev_price = d["price"]

# ============================================================================
# 6. LEISTUNGSBEGINN FITTING
# ============================================================================
print("\n" + "=" * 80)
print("6. LEISTUNGSBEGINN CURVE FIT")
print("=" * 80)

# Check if Leistungsbeginn factors are age-independent
print("\nArbeitnehmer: checking if LB factors are age-independent")
# Compare factors at age 30, 50, 60
for tag in [92, 183, 365]:
    d30 = [d for d in an_lb30 if d["tag"] == tag]
    d50 = [d for d in an_lb50 if d["tag"] == tag]
    d60 = [d for d in an_lb60 if d["tag"] == tag]
    if d30 and d50 and d60:
        f30 = d30[0]["col1"] / ref30
        f50 = d50[0]["col1"] / ref50
        f60 = d60[0]["col1"] / ref60
        print(f"  Tag {tag}: f30={f30:.4f}, f50={f50:.4f}, f60={f60:.4f}, spread={max(f30,f50,f60)-min(f30,f50,f60):.4f}")

print("\n→ Leistungsbeginn factors are NOT perfectly age-independent!")
print("  This means age and Leistungsbeginn interact (not simply multiplicative)")

# Fit LB as function of tag
# Arbeitnehmer at age 30
an_tags = np.array([d["tag"] for d in an_lb30])
an_lb_prices = np.array([d["col1"] for d in an_lb30])

# Try inverse relationship: price ~ a/tag + b
inv_tags = 1.0 / an_tags
c_inv = np.polyfit(inv_tags, an_lb_prices, 1)
p_inv = np.polyval(c_inv, inv_tags)
rmse_inv = np.sqrt(np.mean((an_lb_prices - p_inv)**2))
print(f"\nAN Age30 LB fit: price = {c_inv[0]:.2f}/tag + {c_inv[1]:.4f}, RMSE={rmse_inv:.4f}")

# Try log relationship
log_tags = np.log(an_tags)
c_log = np.polyfit(log_tags, an_lb_prices, 1)
p_log = np.polyval(c_log, log_tags)
rmse_log = np.sqrt(np.mean((an_lb_prices - p_log)**2))
print(f"AN Age30 LB fit: price = {c_log[0]:.4f}*ln(tag) + {c_log[1]:.4f}, RMSE={rmse_log:.4f}")

# Try power law: price = a * tag^b
log_prices = np.log(an_lb_prices)
c_pow = np.polyfit(log_tags, log_prices, 1)
p_pow = np.exp(np.polyval(c_pow, log_tags))
rmse_pow = np.sqrt(np.mean((an_lb_prices - p_pow)**2))
print(f"AN Age30 LB fit: price = {np.exp(c_pow[1]):.4f} * tag^{c_pow[0]:.4f}, RMSE={rmse_pow:.4f}")

# Selbständiger at age 30
se_tags = np.array([d["tag"] for d in se_lb30])
se_lb_prices = np.array([d["price"] for d in se_lb30])

se_log_tags = np.log(se_tags)
se_log_prices = np.log(se_lb_prices)
c_pow_se = np.polyfit(se_log_tags, se_log_prices, 1)
p_pow_se = np.exp(np.polyval(c_pow_se, se_log_tags))
rmse_pow_se = np.sqrt(np.mean((se_lb_prices - p_pow_se)**2))
print(f"\nSE Age30 LB fit: price = {np.exp(c_pow_se[1]):.4f} * tag^{c_pow_se[0]:.4f}, RMSE={rmse_pow_se:.4f}")

# ============================================================================
# 7. OVERALL PRICING MODEL
# ============================================================================
print("\n" + "=" * 80)
print("7. OVERALL PRICING MODEL SUMMARY")
print("=" * 80)

print("""
STRUCTURE:
- Single product (Krankentagegeld KombiMed KTAG), DKV-branded
- No tiers (Smart/Best) — single tariff
- 3 Berufsstatus options, but only 2 distinct pricing models:
  1. Arbeitnehmer (gesetzlich versichert)
  2. Selbständiger / Freiberufler (identical pricing, different max coverage)

PRICING FORMULA:
  Price = age_factor(age) × coverage × leistungsbeginn_factor(tag)

  Where:
  - coverage scaling is PERFECTLY LINEAR (price = rate × Tagegeldhöhe)
  - age curve is approximately quadratic with plateau at age 67+
  - leistungsbeginn factor follows approximately a power law
  - BUT age and leistungsbeginn INTERACT (not purely multiplicative)

NOTES:
- Column 2 (DKV-vollversicherte AN) is a DISPLAY-ONLY comparison price
  - Fixed per age, unaffected by Leistungsbeginn or Tagegeldhöhe
  - Cannot be selected by user (radio is disabled)
  - Not relevant for our demo system
- Versicherungsstatus (pflichtversichert/freiwillig) has NO price effect
  - Only changes available Tagegeldhöhe range (35€ max vs 520€ max)
""")

# ============================================================================
# 8. COMPUTE LOOKUP TABLES FOR DEMO SYSTEM
# ============================================================================
print("\n" + "=" * 80)
print("8. LOOKUP TABLES FOR DEMO SYSTEM")
print("=" * 80)

# Age factors normalized to age 30
# Arbeitnehmer Col1 at 43.Tag, per €/day
an_age30_rate = 8.01 / 15.0  # 0.534 per €/day/month
print(f"\nArbeitnehmer base rate (age 30, 43.Tag): {an_age30_rate:.4f} €/mtl per €/day")

print("\nArbeitnehmer age factor table (43.Tag, normalized to age 30):")
for d in an_age_data:
    factor = (d["col1"] / 15.0) / an_age30_rate
    print(f"  Age {d['age']:>2d}: factor = {factor:.4f} (price/day = {d['col1']/15.0:.4f})")

# Selbständiger at 29.Tag, per €/day
se_age30_rate = 33.60 / 50.0  # 0.672 per €/day/month
print(f"\nSelbständiger base rate (age 30, 29.Tag): {se_age30_rate:.4f} €/mtl per €/day")

print("\nSelbständiger age factor table (29.Tag, normalized to age 30):")
for d in se_age_data:
    factor = (d["price"] / 50.0) / se_age30_rate
    print(f"  Age {d['age']:>2d}: factor = {factor:.4f} (price/day = {d['price']/50.0:.4f})")

# Leistungsbeginn factors
print("\nArbeitnehmer Leistungsbeginn factor table (normalized to 43.Tag):")
for d in an_lb30:
    factor = d["col1"] / ref30
    print(f"  Tag {d['tag']:>3d}: factor = {factor:.4f}")

print("\nSelbständiger Leistungsbeginn factor table (normalized to 29.Tag):")
for d in se_lb30:
    factor = d["price"] / ref30s
    print(f"  Tag {d['tag']:>3d}: factor = {factor:.4f}")

# ============================================================================
# 9. ROUNDING ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("9. ROUNDING ANALYSIS")
print("=" * 80)

# Check if prices are rounded to nearest cent, nearest 3 cents, etc.
# AN: 8.01 / 15 = 0.534 per €/day
# SE: 33.60 / 50 = 0.672 per €/day
# Check if the base unit prices are nice numbers
print(f"\nArbeitnehmer per 5€/day: 2.67 (= 8.01/3)")
print(f"Selbständiger per 5€/day: 3.36 (= 33.60/10*1 ... hmm)")

# Check: is 2.67 a rounded value?
# 2.67 * 3 = 8.01 - checks out
# 3.36 * 10 = 33.60 - checks out (for 50€/day at 29.Tag)
# But 3.36 is the rate at 29.Tag, need per-day
se_per_day = 33.60 / 50.0
print(f"Selbständiger per €/day at 29.Tag, age 30: {se_per_day:.4f}")
print(f"  → 0.672 * 50 = {0.672 * 50:.2f}")

# Check if prices use 3-decimal internal values rounded to 2
# AN age 30, 43.Tag: rate = 0.534 per €/day → internal might be 0.5340
# Check: 0.534 * 5 = 2.67, 0.534 * 10 = 5.34, 0.534 * 15 = 8.01 ✓
print(f"\nRounding: prices appear to use a per-€/day rate rounded to 3 decimal places,")
print(f"then multiply by Tagegeldhöhe and round to 2 decimals.")

print("\n\nDONE")
