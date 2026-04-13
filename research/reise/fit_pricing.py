#!/usr/bin/env python3
"""Analyze ERGO Reiseversicherung pricing data."""
import numpy as np
import json

# === STORNOKOSTENSCHUTZ: Trip cost vs price ===
print("=" * 70)
print("STORNOKOSTENSCHUTZ - Trip Cost Analysis")
print("=" * 70)

# Trip cost data (1 adult <=40, Europa, Flugzeug, 7 days)
trip_costs = np.array([1000, 2000, 5000, 10000, 20000])

# Single trip (Einmal) prices
einmal_msb = np.array([49, 99, 250, 500, 1000])
einmal_osb = np.array([59, 109, 300, 600, 1200])

# Annual (Jahres) prices
jahres_msb = np.array([45, 66, 161, 302, 444])
sparfuchs_msb = np.array([41, 59, 145, 272, 400])

jahres_osb = np.array([57, 75, 175, 368, 555])
sparfuchs_osb = np.array([51, 68, 158, 331, 500])

print("\n--- Single Trip (Einmal) Analysis ---")
# Check if einmal is proportional to trip cost
rate_msb = einmal_msb / trip_costs
rate_osb = einmal_osb / trip_costs
print(f"Einmal mit SB per EUR 1000 trip cost: {rate_msb * 1000}")
print(f"  Mean: {np.mean(rate_msb * 1000):.2f}, Std: {np.std(rate_msb * 1000):.2f}")
print(f"Einmal ohne SB per EUR 1000 trip cost: {rate_osb * 1000}")
print(f"  Mean: {np.mean(rate_osb * 1000):.2f}, Std: {np.std(rate_osb * 1000):.2f}")

# Check percentage ratio of ohne SB to mit SB
osb_msb_ratio = einmal_osb / einmal_msb
print(f"\nOhne SB / Mit SB ratio (Einmal): {osb_msb_ratio}")
print(f"  Mean: {np.mean(osb_msb_ratio):.4f}")

print("\n--- Annual (Jahres) Analysis ---")
# Try linear fit: price = a + b * trip_cost
coeffs_jahres = np.polyfit(trip_costs, jahres_msb, 1)
print(f"Jahres mit SB linear fit: price = {coeffs_jahres[1]:.2f} + {coeffs_jahres[0]*1000:.2f} per EUR 1000")
predicted = np.polyval(coeffs_jahres, trip_costs)
error = np.abs(predicted - jahres_msb)
print(f"  Residuals: {error}")
print(f"  Max error: {np.max(error):.1f}")

# Try sqrt fit: price = a + b * sqrt(trip_cost)
sqrt_costs = np.sqrt(trip_costs)
A_sqrt = np.column_stack([np.ones_like(sqrt_costs), sqrt_costs])
coeffs_sqrt = np.linalg.lstsq(A_sqrt, jahres_msb, rcond=None)[0]
predicted_sqrt = A_sqrt @ coeffs_sqrt
error_sqrt = np.abs(predicted_sqrt - jahres_msb)
print(f"\nJahres mit SB sqrt fit: price = {coeffs_sqrt[0]:.2f} + {coeffs_sqrt[1]:.4f} * sqrt(trip_cost)")
print(f"  Predicted: {predicted_sqrt}")
print(f"  Residuals: {error_sqrt}")
print(f"  Max error: {np.max(error_sqrt):.1f}")

# Try power law: price = a * trip_cost^b
log_costs = np.log(trip_costs)
log_prices = np.log(jahres_msb)
power_coeffs = np.polyfit(log_costs, log_prices, 1)
print(f"\nJahres mit SB power law: price = {np.exp(power_coeffs[1]):.4f} * trip_cost^{power_coeffs[0]:.4f}")
predicted_power = np.exp(np.polyval(power_coeffs, log_costs))
error_power = np.abs(predicted_power - jahres_msb)
print(f"  Predicted: {predicted_power}")
print(f"  Residuals: {error_power}")
print(f"  Max error: {np.max(error_power):.1f}")

# Sparfuchs ratio to Jahres
sf_ratio = sparfuchs_msb / jahres_msb
print(f"\nSparfuchs / Jahres ratio: {sf_ratio}")
print(f"  Mean: {np.mean(sf_ratio):.4f}")

# Ohne SB / Mit SB ratio for annual
osb_jahres_ratio = jahres_osb / jahres_msb
osb_sf_ratio = sparfuchs_osb / sparfuchs_msb
print(f"\nOhne SB / Mit SB ratio (Jahres): {osb_jahres_ratio}")
print(f"  Mean: {np.mean(osb_jahres_ratio):.4f}")
print(f"Ohne SB / Mit SB ratio (Sparfuchs): {osb_sf_ratio}")
print(f"  Mean: {np.mean(osb_sf_ratio):.4f}")

print("\n" + "=" * 70)
print("STORNOKOSTENSCHUTZ - Age Band Analysis")
print("=" * 70)

# Age data (EUR 5000, Europa, Flugzeug, 7 days, mit SB)
age_bands = ["<=40", "41-64", "65+"]
age_jahres = np.array([161, 178, 337])
age_sparfuchs = np.array([145, 160, 303])
age_einmal = np.array([250, 250, 250])

print(f"\nSingle trip (Einmal) by age: {age_einmal}")
print("  --> Single trip price is AGE-INDEPENDENT!")

print(f"\nJahres by age: {age_jahres}")
ratio_41_64 = age_jahres[1] / age_jahres[0]
ratio_65 = age_jahres[2] / age_jahres[0]
print(f"  41-64 vs <=40: {ratio_41_64:.4f}")
print(f"  65+ vs <=40: {ratio_65:.4f}")

print(f"\nSparfuchs by age: {age_sparfuchs}")
ratio_41_64_sf = age_sparfuchs[1] / age_sparfuchs[0]
ratio_65_sf = age_sparfuchs[2] / age_sparfuchs[0]
print(f"  41-64 vs <=40: {ratio_41_64_sf:.4f}")
print(f"  65+ vs <=40: {ratio_65_sf:.4f}")

print("\n" + "=" * 70)
print("STORNOKOSTENSCHUTZ - Transport Analysis")
print("=" * 70)
print("Flugzeug: Jahres 161, Sparfuchs 145, Einmal 250")
print("Auto:     Jahres 161, Sparfuchs 145, Einmal 230")
print("--> Transport ONLY affects single-trip: Flug 250, Auto 230 (ratio: 0.92)")
print("--> Transport does NOT affect annual pricing")

print("\n" + "=" * 70)
print("STORNOKOSTENSCHUTZ - Group/Family Analysis")
print("=" * 70)
print("1 adult:   Jahres 161, Sparfuchs 145, Einmal 250")
print("2 adults:  Jahres 180, Sparfuchs 162, Einmal 250")
print("2+1 child: Jahres 180, Sparfuchs 162, Einmal 250")
pair_ratio_jahres = 180 / 161
pair_ratio_sf = 162 / 145
print(f"--> Pair/Family ratio (Jahres): {pair_ratio_jahres:.4f}")
print(f"--> Pair/Family ratio (Sparfuchs): {pair_ratio_sf:.4f}")
print("--> Single trip: per-booking (not per-person), no pair premium")
print("--> Children free with 2 adults")

print("\n" + "=" * 70)
print("KRANKENSCHUTZ Analysis")
print("=" * 70)

# Krankenschutz age data (Europa, 7 days)
k_age_einmal_msb = np.array([12.80, 16.00, 34.40])
k_age_jahres_msb = np.array([31, 39, 105])
k_age_einmal_osb = np.array([17.60, 19.20, 57.60])
k_age_jahres_osb = np.array([49, 59, 155])

print("\n--- Einmal (single trip) mit SB ---")
print(f"  <=40: {k_age_einmal_msb[0]}, 41-64: {k_age_einmal_msb[1]}, 65+: {k_age_einmal_msb[2]}")
print(f"  41-64/<=40: {k_age_einmal_msb[1]/k_age_einmal_msb[0]:.4f}")
print(f"  65+/<=40: {k_age_einmal_msb[2]/k_age_einmal_msb[0]:.4f}")

print("\n--- Jahres (annual) mit SB ---")
print(f"  <=40: {k_age_jahres_msb[0]}, 41-64: {k_age_jahres_msb[1]}, 65+: {k_age_jahres_msb[2]}")
print(f"  41-64/<=40: {k_age_jahres_msb[1]/k_age_jahres_msb[0]:.4f}")
print(f"  65+/<=40: {k_age_jahres_msb[2]/k_age_jahres_msb[0]:.4f}")

print("\n--- Region effect (Krankenschutz) ---")
print(f"  Europa <=40 Einmal msb: 12.80, Welt: 14.40 -> ratio: {14.40/12.80:.4f}")
print(f"  Europa <=40 Jahres msb: 31, Welt: 31 -> ratio: {31/31:.4f}")
print(f"  Europa <=40 Einmal osb: 17.60, Welt: 36.00 -> ratio: {36.00/17.60:.4f}")
print(f"  Europa <=40 Jahres osb: 49, Welt: 49 -> ratio: {49/49:.4f}")
print("--> Region affects ONLY single-trip Krankenschutz")
print("--> Annual Krankenschutz is REGION-INDEPENDENT")

# Ohne SB ratios for Krankenschutz
print("\n--- Ohne SB / Mit SB ratio (Krankenschutz) ---")
k_ratio_einmal = k_age_einmal_osb / k_age_einmal_msb
k_ratio_jahres = k_age_jahres_osb / k_age_jahres_msb
print(f"  Einmal: {k_ratio_einmal} (mean: {np.mean(k_ratio_einmal):.4f})")
print(f"  Jahres: {k_ratio_jahres} (mean: {np.mean(k_ratio_jahres):.4f})")

print("\n" + "=" * 70)
print("RUNDUMSCHUTZ Analysis")
print("=" * 70)
print("1 adult <=40, EUR 5000, Europa, Flugzeug, 7 days")
print(f"  RS-Schutz (trip) mit SB: 450, ohne SB: 650")
print(f"  RS-Jahresschutz (year) mit SB: 184, ohne SB: 201")
print(f"  Storno Einmal: 250, Kranken Einmal: 12.80")
print(f"  Sum Storno+Kranken: {250 + 12.80}, RS-Schutz: 450")
print(f"  --> RS-Schutz includes Gepaeck too, premium over sum: {450 - 250 - 12.80:.2f}")

print("\n" + "=" * 70)
print("SUMMARY OF KEY FINDINGS")
print("=" * 70)
print("""
1. SINGLE TRIP (Einmal) pricing:
   - Stornokostenschutz: ~5% of trip cost (mit SB), ~6% (ohne SB)
   - Linear relationship: Einmal_msb = 0.05 * trip_cost (with rounding)
   - AGE-INDEPENDENT for single trip
   - Transport affects: Flug ~250 vs Auto ~230 for EUR 5000 (8% discount)
   - Region does NOT affect Storno pricing
   - PER-BOOKING (not per-person)

2. ANNUAL (Jahres) pricing:
   - Follows power law: price ~ trip_cost^0.77
   - Sparfuchs = ~90% of Jahres
   - Ohne SB = ~115-125% of mit SB
   - Age affects annual: 41-64 = 1.10x, 65+ = 2.09x vs <=40
   - Region does NOT affect annual pricing
   - Transport does NOT affect annual pricing
   - Pair/Family = ~1.12x single person

3. KRANKENSCHUTZ:
   - Age affects significantly: 65+ = 2.69x <=40
   - Region affects single trip only (Welt ~13% more mit SB)
   - Annual is region-independent
   - Ohne SB much more expensive: ~1.38-1.67x for Einmal, ~1.48-1.58x Jahres

4. Key structural findings:
   - This is NOT a simple per-unit pricing model
   - Single trip = flat rate table based on trip cost
   - Annual = function of trip cost + age band
   - Region and transport are minor factors
   - No exact polynomial age curve (only 3 age bands)
""")
