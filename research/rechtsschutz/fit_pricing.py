#!/usr/bin/env python3
"""
ERGO Rechtsschutzversicherung - Pricing Analysis

Key finding: Rechtsschutz pricing is AGE-INDEPENDENT (flat rate).
There is no polynomial age curve to fit. Instead, pricing is determined by:
- Tier (Smart / Best)
- Bausteine (Privat, Beruf, Wohnen, Verkehr) -- additive pricing
- Family status (Single vs Familie)
- Discounts: under-25 Startbonus (-10%), SB 250 (-8.9%), SB 500 (-22.1%), 3-year (-10%)
"""

import json
import os

# Load collected data
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "price-matrix.json")) as f:
    data = json.load(f)

prices = data["pricing_data"]
single = prices["base_prices_monthly_sb150"]["single_arbeitnehmer"]
incr = prices["baustein_increments_single"]

print("=" * 70)
print("ERGO Rechtsschutzversicherung - Pricing Analysis")
print("=" * 70)

# 1. Verify additive Baustein model
print("\n1. BAUSTEIN ADDITIVITY CHECK")
print("-" * 40)

for tier in ["smart", "best"]:
    base = incr[tier]["privat_base"]
    beruf = incr[tier]["beruf_add"]
    wohnen = incr[tier]["wohnen_add"]
    verkehr = incr[tier]["verkehr_add"]

    # Check: P + B + W + V should equal all-4 price
    predicted_all4 = base + beruf + wohnen + verkehr
    actual_all4 = single[tier]["privat_beruf_wohnen_verkehr"]
    error = abs(predicted_all4 - actual_all4)

    print(f"  {tier.upper()}:")
    print(f"    P={base} + B={beruf} + W={wohnen} + V={verkehr} = {predicted_all4:.2f}")
    print(f"    Actual all-4: {actual_all4}")
    print(f"    Error: {error:.2f} EUR ({'EXACT' if error < 0.01 else 'MISMATCH'})")

    # Check intermediate: P + B
    predicted_pb = base + beruf
    actual_pb = single[tier]["privat_beruf"]
    error_pb = abs(predicted_pb - actual_pb)
    print(f"    P+B predicted: {predicted_pb:.2f}, actual: {actual_pb}, error: {error_pb:.2f}")

    # Check intermediate: P + B + W
    predicted_pbw = base + beruf + wohnen
    actual_pbw = single[tier]["privat_beruf_wohnen"]
    error_pbw = abs(predicted_pbw - actual_pbw)
    print(f"    P+B+W predicted: {predicted_pbw:.2f}, actual: {actual_pbw}, error: {error_pbw:.2f}")

# 2. Tier relationship
print("\n2. TIER RELATIONSHIP (Best / Smart ratios)")
print("-" * 40)

ratios = {}
for combo in ["privat", "privat_beruf", "privat_beruf_wohnen", "privat_beruf_wohnen_verkehr", "verkehr_only"]:
    if combo in single["best"] and combo in single["smart"]:
        ratio = single["best"][combo] / single["smart"][combo]
        ratios[combo] = ratio
        print(f"  {combo}: Best/Smart = {single['best'][combo]}/{single['smart'][combo]} = {ratio:.4f}")

avg_ratio = sum(ratios.values()) / len(ratios)
ratio_std = (sum((r - avg_ratio)**2 for r in ratios.values()) / len(ratios)) ** 0.5
print(f"\n  Average ratio: {avg_ratio:.4f}")
print(f"  Std dev: {ratio_std:.4f}")
print(f"  Conclusion: {'NOT multiplicative - variable ratios' if ratio_std > 0.02 else 'Approximately multiplicative'}")

# Individual Baustein ratios
print("\n  Baustein-level ratios:")
for baustein in ["privat_base", "beruf_add", "wohnen_add", "verkehr_add"]:
    if baustein in incr["best"] and baustein in incr["smart"]:
        ratio = incr["best"][baustein] / incr["smart"][baustein]
        print(f"    {baustein}: {incr['best'][baustein]}/{incr['smart'][baustein]} = {ratio:.4f}")

# 3. Family status multiplier
print("\n3. FAMILY STATUS MULTIPLIER")
print("-" * 40)
fam = prices["base_prices_monthly_sb150"]["familie_arbeitnehmer"]
for tier in ["smart", "best"]:
    fam_pb = fam[tier]["privat_beruf"]
    single_pb = single[tier]["privat_beruf"]
    mult = fam_pb / single_pb
    print(f"  {tier.upper()}: Familie/Single = {fam_pb}/{single_pb} = {mult:.4f}")

# 4. Under-25 Startbonus
print("\n4. UNDER-25 STARTBONUS")
print("-" * 40)
age_data = prices["age_effect"]["verification"]
print(f"  Age 20 Best P+B: {age_data['age_20_best_pb']}")
print(f"  Age 35 Best P+B: {age_data['age_35_best_pb']}")
print(f"  Age 60 Best P+B: {age_data['age_60_best_pb']}")
print(f"  Under-25 discount: exactly 10% (confirmed in UI label)")

# 5. SB discounts
print("\n5. SELBSTBETEILIGUNG DISCOUNTS")
print("-" * 40)
sb = prices["selbstbeteiligung_effect"]
print(f"  SB 150: {sb['sb_150']} EUR (base)")
print(f"  SB 250: {sb['sb_250']} EUR (discount: {sb['sb_250_discount']*100:.1f}%)")
print(f"  SB 500: {sb['sb_500']} EUR (discount: {sb['sb_500_discount']*100:.1f}%)")

# 6. Zahlungsweise discounts
print("\n6. ZAHLUNGSWEISE DISCOUNTS")
print("-" * 40)
zw = prices["zahlungsweise_effect"]
print(f"  Monatlich: {zw['monatlich']} EUR/mo")
print(f"  Vierteljahrlich: {zw['vierteljaehrlich']} EUR/qtr ({zw['vierteljaehrlich_monthly_equiv']:.2f} EUR/mo equiv, {zw['vierteljaehrlich_discount']*100:.1f}% discount)")
print(f"  Halbjahrlich: {zw['halbjaehrlich']} EUR/half ({zw['halbjaehrlich_monthly_equiv']:.2f} EUR/mo equiv, {zw['halbjaehrlich_discount']*100:.1f}% discount)")
print(f"  Jahrlich: {zw['jaehrlich']} EUR/yr ({zw['jaehrlich_monthly_equiv']:.2f} EUR/mo equiv, {zw['jaehrlich_discount']*100:.1f}% discount)")

# 7. Vertragsdauer discount
print("\n7. VERTRAGSDAUER DISCOUNT")
print("-" * 40)
vd = prices["vertragsdauer_effect"]
print(f"  1 Jahr: {vd['ein_jahr']} EUR/mo")
print(f"  3 Jahre: {vd['drei_jahre']} EUR/mo (discount: {vd['drei_jahre_discount']*100:.1f}%)")

# 8. Recommended pricing model
print("\n" + "=" * 70)
print("RECOMMENDED PRICING MODEL")
print("=" * 70)
print("""
Since pricing is age-independent with additive Bausteine:

  monthlyPremium = baustein_sum * family_multiplier * sb_discount * contract_discount * youth_discount * payment_mode_discount

Where:
  baustein_sum = sum of selected Baustein base prices for the chosen tier
  family_multiplier = 1.0 for Single/Alleinerziehend, ~1.12 for Paar/Familie
  sb_discount = 1.0 (SB 150), 0.911 (SB 250), 0.779 (SB 500)
  contract_discount = 1.0 (1yr), 0.90 (3yr)
  youth_discount = 0.90 (under 25), 1.0 (25+)
  payment_mode_discount = 1.0 (monthly), varies for other modes

This is NOT Template A/B/C from our existing models. Rechtsschutz needs a NEW template:
  - No age curve (flat rate)
  - No coverage amount
  - Additive Bausteine (not multiplicative tiers)
  - Multiple binary toggles instead of tier selection

Recommended: Template D - "Flat rate additive configurator"
""")

# 9. Vital variant analysis
print("8. VITAL (SENIOR) VARIANT")
print("-" * 40)
vital = prices["base_prices_monthly_sb150"]["vital_single_ruhestand"]
vital_incr = prices["baustein_increments_vital"]["smart"]
print(f"  Smart Vital Privat: {vital_incr['privat_base']} (vs regular {incr['smart']['privat_base']}, ratio: {vital_incr['privat_base']/incr['smart']['privat_base']:.3f})")
print(f"  Smart Vital Wohnen add: {vital_incr['wohnen_add']} (vs regular {incr['smart']['wohnen_add']}, ratio: {vital_incr['wohnen_add']/incr['smart']['wohnen_add']:.3f})")
print(f"  Smart Vital Verkehr add: {vital_incr['verkehr_add']} (vs regular {incr['smart']['verkehr_add']}, ratio: {vital_incr['verkehr_add']/incr['smart']['verkehr_add']:.3f})")
print(f"  Vital has DIFFERENT rates per Baustein -- not a simple multiplier of regular rates")

# Save fit results
fit_results = {
    "product": "rechtsschutz",
    "pricing_model": "flat_rate_additive_configurator",
    "age_curve": "NONE (flat rate, no age dependence)",
    "age_curve_r_squared": "N/A",
    "tier_relationship": "NOT multiplicative - each tier has independent Baustein prices",
    "baustein_model": "ADDITIVE - each Baustein adds a fixed amount",
    "family_multiplier": {
        "single": 1.0,
        "alleinerziehend": 1.0,
        "paar": {"smart": 1.111, "best": 1.123},
        "familie": {"smart": 1.111, "best": 1.123}
    },
    "smart_baustein_rates": {
        "privat": 16.71,
        "beruf": 7.83,
        "wohnen": 1.31,
        "verkehr": 8.30,
        "total_all4": 34.15
    },
    "best_baustein_rates": {
        "privat": 24.84,
        "beruf": 9.10,
        "wohnen": 1.83,
        "verkehr": 14.59,
        "total_all4": 50.36
    },
    "discounts": {
        "under_25_startbonus": -0.10,
        "sb_250": -0.089,
        "sb_500": -0.221,
        "3year_contract": -0.10,
        "quarterly_payment": -0.009,
        "semiannual_payment": -0.028,
        "annual_payment": -0.057
    },
    "recommended_template": "D (new: flat rate additive configurator)",
    "confidence": "HIGH"
}

with open(os.path.join(script_dir, "fit_results.json"), "w") as f:
    json.dump(fit_results, f, indent=2)

print(f"\nFit results saved to {os.path.join(script_dir, 'fit_results.json')}")
print("\nDone.")
