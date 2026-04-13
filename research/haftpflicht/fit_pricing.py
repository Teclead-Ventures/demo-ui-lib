#!/usr/bin/env python3
"""
Pricing analysis for ERGO Privathaftpflichtversicherung.
Analyzes price-matrix.json and outputs fit_results.json.
"""

import json
import numpy as np
from pathlib import Path

BASE_DIR = Path("/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/research/haftpflicht")

with open(BASE_DIR / "price-matrix.json") as f:
    data = json.load(f)

points = data["data_points"]

# =============================================================================
# 1. Age analysis: Is there an age curve?
# =============================================================================

# Collect Single/Smart/base prices at different ages
single_smart_base = [(p["inputs"]["age"], p["output"]["monthly_price"])
                     for p in points
                     if p["inputs"]["family_status"] == "single"
                     and p["inputs"]["tier"] == "Smart"
                     and p["inputs"]["bausteine"] == []
                     and p["inputs"]["sb"] == "ohne"
                     and p["inputs"]["laufzeit"] == "3 Jahre"
                     and p["inputs"].get("zahlweise", "monatlich") == "monatlich"]

print("=== AGE ANALYSIS (Single/Smart/base) ===")
for age, price in sorted(single_smart_base):
    print(f"  Age {age}: {price:.2f} EUR")

# Check age-independence for >=36
ages_over_36 = [(a, p) for a, p in single_smart_base if a >= 36]
ages_under_36 = [(a, p) for a, p in single_smart_base if a < 36]

if ages_over_36:
    prices_over_36 = [p for _, p in ages_over_36]
    age_independent = max(prices_over_36) - min(prices_over_36) < 0.02
    print(f"\n  Ages >= 36: all {prices_over_36[0]:.2f} EUR? {age_independent}")

if ages_under_36 and ages_over_36:
    startbonus_ratios = []
    base_price = prices_over_36[0]
    for age, price in ages_under_36:
        ratio = price / base_price
        startbonus_ratios.append(ratio)
        print(f"  Age {age} Startbonus ratio: {ratio:.4f} (discount: {(1-ratio)*100:.1f}%)")

    avg_ratio = np.mean(startbonus_ratios)
    print(f"  Average Startbonus ratio: {avg_ratio:.4f} (discount: {(1-avg_ratio)*100:.1f}%)")

# =============================================================================
# 2. Family status analysis
# =============================================================================

print("\n=== FAMILY STATUS ANALYSIS ===")

# Get base prices by family status and tier (age 36, no bausteine/SB, 3yr, monthly)
family_prices = {}
for p in points:
    if (p["inputs"]["age"] >= 36
        and p["inputs"]["sb"] == "ohne"
        and p["inputs"]["laufzeit"] == "3 Jahre"
        and p["inputs"].get("zahlweise", "monatlich") == "monatlich"):

        fs = p["inputs"]["family_status"]
        tier = p["inputs"]["tier"]
        bausteine = p["inputs"]["bausteine"]

        # For Smart: need empty bausteine
        # For Best: default includes 3 bausteine
        if tier == "Smart" and bausteine == []:
            family_prices.setdefault(fs, {})[tier] = p["output"]["monthly_price"]
        elif tier == "Best" and set(bausteine) == {"Schlüsselverlust", "Neuwertentschädigung", "Forderungsausfall"}:
            family_prices.setdefault(fs, {})[tier] = p["output"]["monthly_price"]

print("\nBase prices (age >=36, ohne SB, 3J, monatlich):")
single_smart = family_prices.get("single", {}).get("Smart", 0)
single_best = family_prices.get("single", {}).get("Best", 0)

for fs in ["single", "alleinerziehend", "paar", "familie"]:
    if fs in family_prices:
        s = family_prices[fs].get("Smart", 0)
        b = family_prices[fs].get("Best", 0)
        s_mult = s / single_smart if single_smart else 0
        b_mult = b / single_best if single_best else 0
        print(f"  {fs:20s}: Smart={s:.2f} (x{s_mult:.4f}), Best={b:.2f} (x{b_mult:.4f})")

# =============================================================================
# 3. Baustein analysis (additive pricing)
# =============================================================================

print("\n=== BAUSTEIN ANALYSIS ===")

# Get individual Baustein prices (on Smart, Single, age 36)
baustein_base = 6.05  # Smart base, Single, 36

baustein_prices = {}
for p in points:
    if (p["inputs"]["family_status"] == "single"
        and p["inputs"]["tier"] == "Smart"
        and p["inputs"]["age"] >= 36
        and p["inputs"]["sb"] == "ohne"
        and p["inputs"]["laufzeit"] == "3 Jahre"
        and p["inputs"].get("zahlweise", "monatlich") == "monatlich"
        and len(p["inputs"]["bausteine"]) == 1):

        bs_name = p["inputs"]["bausteine"][0]
        bs_price = p["output"]["monthly_price"] - baustein_base
        baustein_prices[bs_name] = bs_price
        print(f"  {bs_name}: +{bs_price:.2f} EUR/month")

# Check additivity with 2 and 3 Bausteine
for p in points:
    if (p["inputs"]["family_status"] == "single"
        and p["inputs"]["tier"] == "Smart"
        and p["inputs"]["age"] >= 36
        and p["inputs"]["sb"] == "ohne"
        and p["inputs"]["laufzeit"] == "3 Jahre"
        and p["inputs"].get("zahlweise", "monatlich") == "monatlich"
        and len(p["inputs"]["bausteine"]) >= 2):

        expected = baustein_base + sum(baustein_prices.get(b, 0) for b in p["inputs"]["bausteine"])
        actual = p["output"]["monthly_price"]
        diff = actual - expected
        print(f"  {len(p['inputs']['bausteine'])} Bausteine: expected={expected:.2f}, actual={actual:.2f}, diff={diff:.2f}")

# =============================================================================
# 4. Tier relationship analysis
# =============================================================================

print("\n=== TIER RELATIONSHIP ===")

# Compare Smart (no Bausteine) vs Best (with 3 default Bausteine)
# Smart + all 3 Bausteine = 9.67, Best = 10.58
# Difference = 0.91 (coverage upgrade from 10M to 50M)

smart_with_3 = None
for p in points:
    if (p["inputs"]["family_status"] == "single"
        and p["inputs"]["tier"] == "Smart"
        and p["inputs"]["age"] >= 36
        and p["inputs"]["sb"] == "ohne"
        and len(p["inputs"]["bausteine"]) == 3
        and "Schlüsselverlust" in p["inputs"]["bausteine"]):
        smart_with_3 = p["output"]["monthly_price"]
        break

if smart_with_3:
    coverage_premium = single_best - smart_with_3
    print(f"  Smart + 3 Bausteine: {smart_with_3:.2f}")
    print(f"  Best (includes 3 Bausteine): {single_best:.2f}")
    print(f"  Coverage upgrade (10M→50M): +{coverage_premium:.2f} EUR/month")
    print(f"  This means Best = Smart base + 3 Bausteine + coverage premium")

# =============================================================================
# 5. SB analysis
# =============================================================================

print("\n=== SELBSTBETEILIGUNG ANALYSIS ===")

# Smart SB
smart_ohne = 6.05
smart_sb150 = 4.84
print(f"  Smart: ohne={smart_ohne}, SB150={smart_sb150}, ratio={smart_sb150/smart_ohne:.4f}, discount={((1-smart_sb150/smart_ohne)*100):.1f}%")

# Best SB
best_ohne = 10.58
best_sb150 = 9.19
print(f"  Best:  ohne={best_ohne}, SB150={best_sb150}, ratio={best_sb150/best_ohne:.4f}, discount={((1-best_sb150/best_ohne)*100):.1f}%")

# The SB discount is NOT a constant percentage
# Smart: 20.0% discount
# Best: 13.1% discount
# Likely: SB reduces the base premium component but not the Bausteine
# Test: Smart base discount = 6.05 - 4.84 = 1.21 EUR
# If only base gets 20% off: base_annual = 68.46, 20% = 13.692/12 = 1.141/month... doesn't match
# Alternative: SB is a fixed EUR reduction per tier
smart_sb_reduction = smart_ohne - smart_sb150
best_sb_reduction = best_ohne - best_sb150
print(f"  Smart SB reduction: {smart_sb_reduction:.2f} EUR/month")
print(f"  Best SB reduction: {best_sb_reduction:.2f} EUR/month")

# =============================================================================
# 6. Contract duration analysis
# =============================================================================

print("\n=== CONTRACT DURATION ANALYSIS ===")

smart_3yr = 6.05
smart_1yr = 6.72
duration_surcharge = smart_1yr / smart_3yr
print(f"  Smart 3-year: {smart_3yr:.2f}")
print(f"  Smart 1-year: {smart_1yr:.2f}")
print(f"  1-year / 3-year ratio: {duration_surcharge:.4f} ({(duration_surcharge-1)*100:.1f}% surcharge)")

# =============================================================================
# 7. Payment frequency analysis
# =============================================================================

print("\n=== PAYMENT FREQUENCY ANALYSIS ===")

# Base annual premium (from jährlich): 68.46
annual_base = 68.46
frequencies = {
    "jährlich": 68.46,
    "halbjährlich": 35.26 * 2,  # = 70.52
    "vierteljährlich": 17.97 * 4,  # = 71.88
    "monatlich": 6.05 * 12,  # = 72.60
}

for freq, annual in frequencies.items():
    surcharge = (annual / annual_base - 1) * 100
    print(f"  {freq:20s}: {annual:.2f} EUR/year ({surcharge:+.1f}% vs annual)")

# =============================================================================
# 8. Template recommendation
# =============================================================================

print("\n=== TEMPLATE RECOMMENDATION ===")
print("  Template D (flat-rate configurator with additive Bausteine)")
print("  Reasons:")
print("  - No continuous age curve (binary <36/>= 36 Startbonus only)")
print("  - No coverage slider (fixed by tier)")
print("  - Additive Baustein toggles")
print("  - 2 tiers (Smart/Best) like Rechtsschutz and Hausrat")
print("  - Family status as risk class (non-multiplicative across tiers)")

# =============================================================================
# OUTPUT: fit_results.json
# =============================================================================

results = {
    "product": "haftpflicht",
    "template": "D",
    "template_name": "flat-rate configurator with additive Bausteine",
    "confidence": "HIGH",
    "tiers": {
        "count": 2,
        "ergo_names": ["Smart", "Best"],
        "our_mapping": {"Smart": "grundschutz", "Best": "premium"},
        "coverage": {"Smart": "10 Mio. EUR", "Best": "50 Mio. EUR"},
        "coverage_slider": False
    },
    "age_model": {
        "type": "binary_band",
        "description": "No continuous age curve. Binary: <36 years at start → 13% Startbonus, >=36 → flat rate",
        "startbonus_threshold": 36,
        "startbonus_discount": 0.13,
        "startbonus_multiplier": 0.87
    },
    "family_status": {
        "options": ["single", "alleinerziehend", "paar", "familie"],
        "notes": "Alleinerziehend and Paar have identical pricing. 4 options map to 3 risk classes.",
        "risk_classes": {
            "single": {
                "smart_base_monthly": 6.05,
                "best_base_monthly": 10.58,
                "smart_multiplier_vs_single": 1.000,
                "best_multiplier_vs_single": 1.000
            },
            "paar_or_alleinerziehend": {
                "smart_base_monthly": 7.56,
                "best_base_monthly": 12.09,
                "smart_multiplier_vs_single": 1.250,
                "best_multiplier_vs_single": 1.143
            },
            "familie": {
                "smart_base_monthly": 9.07,
                "best_base_monthly": 13.60,
                "smart_multiplier_vs_single": 1.499,
                "best_multiplier_vs_single": 1.285
            }
        },
        "multiplier_note": "Family status multipliers differ between Smart and Best, suggesting the family surcharge is additive to the base tier rather than purely multiplicative"
    },
    "bausteine": {
        "description": "5 toggleable modules, additive pricing",
        "modules": {
            "Schlüsselverlust": {
                "add_monthly_single_smart": 1.21,
                "best_default": True,
                "smart_default": False
            },
            "Neuwertentschädigung": {
                "add_monthly_single_smart": 1.21,
                "best_default": True,
                "smart_default": False
            },
            "Forderungsausfall": {
                "add_monthly_single_smart": 1.21,
                "best_default": True,
                "smart_default": False
            },
            "Amts- und Diensthaftpflicht": {
                "add_monthly_single_smart": 1.93,
                "add_monthly_single_best": 1.94,
                "best_default": False,
                "smart_default": False
            },
            "Alleinstehende Familienangehörige": {
                "add_monthly": 0.00,
                "best_default": False,
                "smart_default": False,
                "note": "Free add-on, no price impact"
            }
        },
        "additivity_verified": True,
        "additivity_error": "< 0.02 EUR (rounding)"
    },
    "selbstbeteiligung": {
        "options": ["ohne", "150 EUR"],
        "default": "ohne",
        "smart_discount_pct": 20.0,
        "best_discount_pct": 13.1,
        "note": "Discount percentage differs by tier, suggesting SB reduces a base component only"
    },
    "vertragslaufzeit": {
        "options": ["1 Jahr", "3 Jahre"],
        "default": "3 Jahre",
        "one_year_surcharge_pct": 11.1,
        "three_year_is_base": True
    },
    "zahlungsweise": {
        "options": ["monatlich", "vierteljährlich", "halbjährlich", "jährlich"],
        "default": "monatlich",
        "annual_base_eur": 68.46,
        "surcharges": {
            "jährlich": 0.0,
            "halbjährlich": 3.0,
            "vierteljährlich": 5.0,
            "monatlich": 6.0
        },
        "surcharge_unit": "percent_vs_annual"
    },
    "base_rates_monthly_3yr_ohne_sb": {
        "description": "Base monthly prices (3-year contract, ohne SB, monatlich payment)",
        "single": {"Smart": 6.05, "Best": 10.58},
        "paar": {"Smart": 7.56, "Best": 12.09},
        "alleinerziehend": {"Smart": 7.56, "Best": 12.09},
        "familie": {"Smart": 9.07, "Best": 13.60}
    }
}

with open(BASE_DIR / "fit_results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nResults written to {BASE_DIR / 'fit_results.json'}")
print("DONE")
