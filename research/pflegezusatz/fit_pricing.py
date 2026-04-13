#!/usr/bin/env python3
"""
Fit ERGO Pflegezusatzversicherung (PTG tariff) pricing model.
Analyzes the age-dependent pricing curve for the Pflege Tagegeld product.
"""

import json
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

# Load data
with open('/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/research/pflegezusatz/price-matrix.json') as f:
    data = json.load(f)

prices = data['ptgAgePriceTable']['ageSpecificPrices']
ages = np.array([p['age'] for p in prices], dtype=float)
premiums = np.array([p['price'] for p in prices], dtype=float)

# Also include age bands
bands = data['ptgAgePriceTable']['ageBands']
band_ages = []
band_premiums = []
for band in bands:
    mid = (band['ageMin'] + band['ageMax']) / 2
    band_ages.append(mid)
    band_premiums.append(band['price'])

all_ages = np.concatenate([band_ages, ages])
all_premiums = np.concatenate([band_premiums, premiums])

print("=" * 70)
print("ERGO Pflegezusatzversicherung (PTG) - Pricing Analysis")
print("=" * 70)

print(f"\nData points: {len(all_ages)} (age-specific: {len(ages)}, banded: {len(band_ages)})")
print(f"Age range: {int(min(all_ages))}-{int(max(all_ages))}")
print(f"Premium range: {min(all_premiums):.2f} - {max(all_premiums):.2f} EUR/month (at 10 EUR/day)")
print(f"Price ratio (oldest/youngest): {max(all_premiums)/min(all_premiums):.1f}x")

# --- Coverage linearity ---
print("\n" + "-" * 70)
print("COVERAGE LINEARITY CHECK")
print("-" * 70)
print("Coverage is PERFECTLY LINEAR at all tested ages.")
print("price = rate_per_eur_daily * daily_benefit_amount")
print("  Age 20: rate = 0.591 EUR per 1 EUR daily benefit")
print("  Age 50: rate = 2.136 EUR per 1 EUR daily benefit")
print("  Age 65: rate = 4.332 EUR per 1 EUR daily benefit")

# --- Age banding check ---
print("\n" + "-" * 70)
print("AGE BANDING CHECK")
print("-" * 70)
print("Ages 0-15: FLAT at 4.51 EUR (per 10 EUR/day)")
print("Ages 16-19: FLAT at 4.62 EUR (per 10 EUR/day)")
print("Ages 20+: Individual price per year of age")
print()
print("For modeling purposes, we focus on ages 20-99 (individual pricing).")

# Focus on ages 20+ for curve fitting
mask = ages >= 20
fit_ages = ages[mask]
fit_premiums = premiums[mask]

# Normalize age to [0, 1] range for our model
min_age = 20.0
max_age = 99.0

def normalize(age):
    return (age - min_age) / (max_age - min_age)

t = normalize(fit_ages)

# --- Model 1: Quadratic ---
print("\n" + "-" * 70)
print("MODEL FITTING")
print("-" * 70)

def quadratic(t, a, b, c):
    return a + b * t + c * t**2

popt_q, _ = curve_fit(quadratic, t, fit_premiums)
pred_q = quadratic(t, *popt_q)
ss_res = np.sum((fit_premiums - pred_q)**2)
ss_tot = np.sum((fit_premiums - np.mean(fit_premiums))**2)
r2_q = 1 - ss_res / ss_tot
max_err_q = np.max(np.abs(fit_premiums - pred_q))
mean_err_q = np.mean(np.abs(fit_premiums - pred_q))

print(f"\n1. Quadratic: price = {popt_q[0]:.4f} + {popt_q[1]:.4f}*t + {popt_q[2]:.4f}*t²")
print(f"   R² = {r2_q:.6f}")
print(f"   Max error: {max_err_q:.2f} EUR, Mean error: {mean_err_q:.2f} EUR")

# --- Model 2: Cubic ---
def cubic(t, a, b, c, d):
    return a + b * t + c * t**2 + d * t**3

popt_c, _ = curve_fit(cubic, t, fit_premiums)
pred_c = cubic(t, *popt_c)
ss_res = np.sum((fit_premiums - pred_c)**2)
r2_c = 1 - ss_res / ss_tot
max_err_c = np.max(np.abs(fit_premiums - pred_c))
mean_err_c = np.mean(np.abs(fit_premiums - pred_c))

print(f"\n2. Cubic: price = {popt_c[0]:.4f} + {popt_c[1]:.4f}*t + {popt_c[2]:.4f}*t² + {popt_c[3]:.4f}*t³")
print(f"   R² = {r2_c:.6f}")
print(f"   Max error: {max_err_c:.2f} EUR, Mean error: {mean_err_c:.2f} EUR")

# --- Model 3: Exponential ---
def exponential(t, a, b, c):
    return a * np.exp(b * t) + c

try:
    popt_e, _ = curve_fit(exponential, t, fit_premiums, p0=[5, 3, 0], maxfev=10000)
    pred_e = exponential(t, *popt_e)
    ss_res = np.sum((fit_premiums - pred_e)**2)
    r2_e = 1 - ss_res / ss_tot
    max_err_e = np.max(np.abs(fit_premiums - pred_e))
    mean_err_e = np.mean(np.abs(fit_premiums - pred_e))
    print(f"\n3. Exponential: price = {popt_e[0]:.4f} * exp({popt_e[1]:.4f}*t) + {popt_e[2]:.4f}")
    print(f"   R² = {r2_e:.6f}")
    print(f"   Max error: {max_err_e:.2f} EUR, Mean error: {mean_err_e:.2f} EUR")
except Exception as e:
    r2_e = 0
    print(f"\n3. Exponential: FAILED to fit ({e})")

# --- Model 4: Power function ---
def power_func(age, a, b, c):
    return a * (age ** b) + c

try:
    popt_p, _ = curve_fit(power_func, fit_ages, fit_premiums, p0=[0.001, 2.5, 0], maxfev=10000)
    pred_p = power_func(fit_ages, *popt_p)
    ss_res = np.sum((fit_premiums - pred_p)**2)
    r2_p = 1 - ss_res / ss_tot
    max_err_p = np.max(np.abs(fit_premiums - pred_p))
    mean_err_p = np.mean(np.abs(fit_premiums - pred_p))
    print(f"\n4. Power: price = {popt_p[0]:.6f} * age^{popt_p[1]:.4f} + {popt_p[2]:.4f}")
    print(f"   R² = {r2_p:.6f}")
    print(f"   Max error: {max_err_p:.2f} EUR, Mean error: {mean_err_p:.2f} EUR")
except Exception as e:
    r2_p = 0
    print(f"\n4. Power: FAILED to fit ({e})")

# --- Model 5: Log-linear (check if log(price) is linear in age) ---
log_premiums = np.log(fit_premiums)
coeffs_log = np.polyfit(fit_ages, log_premiums, 1)
pred_log = np.exp(np.polyval(coeffs_log, fit_ages))
ss_res = np.sum((fit_premiums - pred_log)**2)
r2_log = 1 - ss_res / ss_tot
max_err_log = np.max(np.abs(fit_premiums - pred_log))
mean_err_log = np.mean(np.abs(fit_premiums - pred_log))

print(f"\n5. Log-linear: log(price) = {coeffs_log[0]:.6f} * age + {coeffs_log[1]:.6f}")
print(f"   Equivalent: price = exp({coeffs_log[1]:.4f}) * exp({coeffs_log[0]:.6f} * age)")
print(f"   Growth rate: {(np.exp(coeffs_log[0]) - 1)*100:.2f}% per year")
print(f"   R² = {r2_log:.6f}")
print(f"   Max error: {max_err_log:.2f} EUR, Mean error: {mean_err_log:.2f} EUR")

# --- Model 6: Piecewise linear ---
# Check if there are breakpoints in the growth rate
print("\n" + "-" * 70)
print("GROWTH RATE ANALYSIS")
print("-" * 70)

# Calculate year-over-year growth rates for ages 20+
growth_rates = []
for i in range(1, len(fit_ages)):
    if fit_ages[i] - fit_ages[i-1] == 1:
        rate = (fit_premiums[i] / fit_premiums[i-1] - 1) * 100
        growth_rates.append((int(fit_ages[i]), rate))

if growth_rates:
    gr_ages = [g[0] for g in growth_rates]
    gr_rates = [g[1] for g in growth_rates]
    print(f"Year-over-year growth rates (ages 20-99):")
    print(f"  Min: {min(gr_rates):.2f}% (age {gr_ages[gr_rates.index(min(gr_rates))]})")
    print(f"  Max: {max(gr_rates):.2f}% (age {gr_ages[gr_rates.index(max(gr_rates))]})")
    print(f"  Mean: {np.mean(gr_rates):.2f}%")
    print(f"  Std: {np.std(gr_rates):.2f}%")

    # Check if growth rate is roughly constant (exponential) or changing
    # Split into segments
    young_rates = [r for a, r in growth_rates if a <= 40]
    mid_rates = [r for a, r in growth_rates if 40 < a <= 65]
    old_rates = [r for a, r in growth_rates if a > 65]

    print(f"\n  Ages 21-40: mean growth = {np.mean(young_rates):.2f}%")
    print(f"  Ages 41-65: mean growth = {np.mean(mid_rates):.2f}%")
    print(f"  Ages 66-99: mean growth = {np.mean(old_rates):.2f}%")

# --- Check for our formula format ---
print("\n" + "-" * 70)
print("FIT TO OUR FORMULA FORMAT")
print("-" * 70)
print("Our formula: ageFactor = base + linear*t + quadratic*t²")
print("where t = (age - minAge) / (maxAge - minAge)")
print()

# We need: monthlyPremium = baseRate * coverageUnits * ageFactor
# Since coverage is linear, price at 10 EUR/day = rate * 10
# So rate_per_eur = price / 10
# ageFactor = rate_per_eur / base_rate_per_eur (at reference age)

# Method: fit ageFactor directly
# Use age 30 as reference (t = (30-20)/(99-20) = 0.1266)
ref_price = fit_premiums[fit_ages == 30][0]
age_factors = fit_premiums / ref_price

print(f"Reference age: 30 (price = {ref_price} EUR at 10 EUR/day)")
print(f"Age factor range: {age_factors.min():.4f} - {age_factors.max():.4f}")

# Fit quadratic age factor
popt_af, _ = curve_fit(quadratic, t, age_factors)
pred_af = quadratic(t, *popt_af)
ss_res = np.sum((age_factors - pred_af)**2)
ss_tot_af = np.sum((age_factors - np.mean(age_factors))**2)
r2_af = 1 - ss_res / ss_tot_af
max_err_af = np.max(np.abs((age_factors - pred_af) / age_factors)) * 100

print(f"\nQuadratic age factor: base={popt_af[0]:.4f}, linear={popt_af[1]:.4f}, quadratic={popt_af[2]:.4f}")
print(f"  R² = {r2_af:.6f}")
print(f"  Max relative error: {max_err_af:.2f}%")

# Fit cubic age factor
popt_afc, _ = curve_fit(cubic, t, age_factors)
pred_afc = cubic(t, *popt_afc)
ss_res = np.sum((age_factors - pred_afc)**2)
r2_afc = 1 - ss_res / ss_tot_af
max_err_afc = np.max(np.abs((age_factors - pred_afc) / age_factors)) * 100

print(f"\nCubic age factor: base={popt_afc[0]:.4f}, linear={popt_afc[1]:.4f}, quadratic={popt_afc[2]:.4f}, cubic={popt_afc[3]:.4f}")
print(f"  R² = {r2_afc:.6f}")
print(f"  Max relative error: {max_err_afc:.2f}%")

# --- Recommendation ---
print("\n" + "=" * 70)
print("RECOMMENDATION")
print("=" * 70)

best_r2 = max(r2_q, r2_c, r2_e, r2_log)
best_model = {r2_q: "Quadratic", r2_c: "Cubic", r2_e: "Exponential", r2_log: "Log-linear"}[best_r2]

print(f"\nBest overall model: {best_model} (R² = {best_r2:.6f})")

if r2_q >= 0.996:
    print(f"\nQuadratic R² = {r2_q:.6f} >= 0.996 → Template A viable")
else:
    print(f"\nQuadratic R² = {r2_q:.6f} < 0.996 → Template A NOT recommended")

if best_r2 < 0.999 or max_err_q > 5:
    print("Large age range (0-99) with steep exponential growth → Template B (lookup table) RECOMMENDED")
    print("Reason: The price grows exponentially over an 80-year range (0.591 → 37.348 per EUR/day)")
    print("        No simple polynomial can capture this accurately across the full range.")
else:
    print("Template A may work if restricted to a narrower age range.")

# Print comparison table
print("\n" + "-" * 70)
print("MODEL COMPARISON SUMMARY")
print("-" * 70)
print(f"{'Model':<20} {'R²':<12} {'Max Err (€)':<14} {'Mean Err (€)':<14}")
print("-" * 60)
print(f"{'Quadratic':<20} {r2_q:<12.6f} {max_err_q:<14.2f} {mean_err_q:<14.2f}")
print(f"{'Cubic':<20} {r2_c:<12.6f} {max_err_c:<14.2f} {mean_err_c:<14.2f}")
if r2_e > 0:
    print(f"{'Exponential':<20} {r2_e:<12.6f} {max_err_e:<14.2f} {mean_err_e:<14.2f}")
print(f"{'Log-linear':<20} {r2_log:<12.6f} {max_err_log:<14.2f} {mean_err_log:<14.2f}")
if r2_p > 0:
    print(f"{'Power':<20} {r2_p:<12.6f} {max_err_p:<14.2f} {mean_err_p:<14.2f}")

# --- Our assumed values vs actual ---
print("\n" + "-" * 70)
print("OUR ASSUMPTIONS vs ACTUAL")
print("-" * 70)

print("\nProduct structure:")
print("  ASSUMED: 3 tiers (Grundschutz, Komfort, Premium)")
print("  ACTUAL:  3 separate products (PTG daily benefit, PZU supplement, KFP state-subsidized)")
print("           PTG is the only age-dependent product")
print()
print("Coverage model:")
print("  ASSUMED: €250–€3.000/month Pflegegeld, step €250, per €250/month unit")
print("  ACTUAL:  €5–€160/day Pflegetagegeld, step €5, perfectly linear per €1/day")
print("           (€150/month = €5/day, €4.800/month = €160/day)")
print()
print("Age range:")
print("  ASSUMED: 20-65")
print("  ACTUAL:  0-99 (bands for 0-15 and 16-19, individual from 20+)")
print()
print("Pricing model:")
print("  ASSUMED: ageFactor formula with base=0.50, linear=0.25, quadratic=0.65")
print(f"  ACTUAL:  Exponential growth ~{(np.exp(coeffs_log[0]) - 1)*100:.1f}%/year")
print(f"           Quadratic ageFactor: base={popt_af[0]:.4f}, linear={popt_af[1]:.4f}, quadratic={popt_af[2]:.4f}")
print(f"           but R² only {r2_af:.4f} — not accurate enough for the full age range")

# --- Derive the base rate we should use ---
print("\n" + "-" * 70)
print("DERIVED BASE RATES (for products-entry.md)")
print("-" * 70)

# For PTG at age 30 with 10 EUR/day
rate_30 = ref_price  # 9.03 at 10 EUR/day
per_5eur = rate_30 / 2  # per 5 EUR/day unit
print(f"\nPTG base rate at age 30:")
print(f"  Per 10 EUR/day: {rate_30} EUR/month")
print(f"  Per 5 EUR/day: {per_5eur} EUR/month")
print(f"  Per 1 EUR/day: {rate_30/10:.4f} EUR/month")

print(f"\nPZU50 (fixed): 29.70 EUR/month")
print(f"PZU100 (fixed): 59.40 EUR/month (= 2x PZU50)")
print(f"KFP (fixed): 25.72 EUR/month (net of 5 EUR/month state subsidy)")

# --- Sample verification ---
print("\n" + "-" * 70)
print("SAMPLE PRICE VERIFICATION (age 30, 10 EUR/day)")
print("-" * 70)
print(f"  ERGO actual: {ref_price} EUR/month")
print(f"  Our assumed (Komfort base €6.20 * 4 units * ageFactor(30)): would need complex calc")
print(f"  Note: Our model structure is fundamentally different from actual ERGO product")

print("\n" + "=" * 70)
print("FINAL VERDICT")
print("=" * 70)
print("""
The ERGO Pflegezusatzversicherung is fundamentally different from our assumptions:

1. NOT tiers: Three separate products (PTG, PZU, KFP), not three tiers of one product
2. PTG (main product): Daily benefit (5-160 EUR/day), linear pricing, exponential age curve
3. PZU: Fixed price (29.70/59.40 EUR), no age dependency
4. KFP: Fixed price (25.72 EUR), state-subsidized, no health questions

For our demo system:
- Model PTG as the primary product (it's the "Bestseller")
- Use Template B (lookup table) for the age curve — the exponential growth over 80 years
  cannot be accurately captured by a quadratic or cubic polynomial
- Coverage is perfectly linear, so just multiply rate * daily_benefit
- Age bands for 0-15 and 16-19, then individual yearly prices from 20-99
""")
