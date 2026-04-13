#!/usr/bin/env python3
"""Collect ERGO Risikoleben prices via playwright-cli."""
import subprocess
import time
import re
import json
import sys

SESSION = "risikoleben"
BASE_URL = "https://www.ergo.de/de/Produkte/Lebensversicherung/Risikolebensversicherung/abschluss"

def cli(cmd, timeout=15):
    """Run a playwright-cli command and return output."""
    full_cmd = f"playwright-cli -s={SESSION} {cmd}"
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

def wait(seconds=3):
    time.sleep(seconds)

def click_weiter():
    """Click the weiter button via eval."""
    result = cli('eval \'(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return "clicked"}} return "not found"})()\'')
    return "clicked" in result

def click_berechnen():
    """Click Jetzt berechnen button."""
    result = cli('eval \'(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="Jetzt berechnen"){btns[i].click();return "clicked"}} return "not found"})()\'')
    return "clicked" in result

def dismiss_cookies():
    """Dismiss cookie dialog if present."""
    snap = cli("snapshot")
    if "Alle akzeptieren" in snap:
        ref = re.search(r'button "Alle akzeptieren" \[ref=(\w+)\]', snap)
        if ref:
            cli(f"click {ref.group(1)}")
            wait(2)
            return True
    return False

def get_snapshot():
    return cli("snapshot")

def extract_prices(snap):
    """Extract Grundschutz, Komfort, Premium prices from snapshot."""
    prices = {}
    # Look for radio buttons with prices
    grund = re.search(r'radio "Grundschutz ([\d,]+) € mtl\."', snap)
    komfort = re.search(r'radio "Komfort ([\d,]+) € mtl\."', snap)
    premium = re.search(r'radio ".*Premium ([\d,]+) € mtl\."', snap)

    if grund:
        prices["grundschutz"] = float(grund.group(1).replace(",", "."))
    if komfort:
        prices["komfort"] = float(komfort.group(1).replace(",", "."))
    if premium:
        prices["premium"] = float(premium.group(1).replace(",", "."))
    return prices

def navigate_wizard(birth_day, birth_month, birth_year, smoker_class, coverage=200000, term=20):
    """Navigate the full wizard and return prices.

    smoker_class: 1=Nichtraucher 10+, 2=Nichtraucher 1+, 3=Raucher
    """
    print(f"  Navigating: born={birth_day}.{birth_month}.{birth_year}, smoker={smoker_class}, coverage={coverage}, term={term}")

    # Fresh start - delete data and reopen
    cli("delete-data")
    wait(2)
    cli(f'open "{BASE_URL}" --headed', timeout=30)
    wait(5)

    # Dismiss cookies
    dismiss_cookies()

    # Step 1: Who to insure (Mich selbst is default)
    snap = get_snapshot()
    if "Wen möchten" not in snap:
        print("    ERROR: Not at step 1")
        return None
    click_weiter()
    wait(3)

    # Step 2: Birth date
    snap = get_snapshot()
    tag_ref = re.search(r'spinbutton "Tag" \[ref=(\w+)\]', snap)
    monat_ref = re.search(r'spinbutton "Monat" \[ref=(\w+)\]', snap)
    jahr_ref = re.search(r'spinbutton "Jahr" \[ref=(\w+)\]', snap)

    if not tag_ref:
        print("    ERROR: Birth date fields not found")
        return None

    cli(f"click {tag_ref.group(1)}")
    cli(f'type "{birth_day}"')
    wait(0.5)
    cli(f"fill {monat_ref.group(1)} \"{birth_month}\"")
    cli(f"fill {jahr_ref.group(1)} \"{birth_year}\"")
    cli("press Tab")
    wait(2)

    if not click_weiter():
        print("    ERROR: Could not advance from birth date")
        return None
    wait(3)

    # Step 3: Absicherungsform (constant is default)
    click_weiter()
    wait(3)

    # Step 4: Versicherungssumme
    snap = get_snapshot()
    # Find the combobox for coverage
    combo_ref = re.search(r'combobox \[ref=(\w+)\]', snap)
    if combo_ref:
        # Format coverage with dots for German number format
        cov_str = f"{coverage:,}".replace(",", ".")
        cli(f'fill {combo_ref.group(1)} "{cov_str}"')
        cli("press Tab")
        wait(2)
    click_weiter()
    wait(3)

    # Step 5: Laufzeit
    snap = get_snapshot()
    lauf_combo = re.search(r'combobox \[ref=(\w+)\]', snap)
    if lauf_combo:
        cli(f'fill {lauf_combo.group(1)} "{term}"')
        cli("press Tab")
        wait(2)
    click_weiter()
    wait(3)

    # Step 6: Beruf
    snap = get_snapshot()
    beruf_select = re.search(r'combobox "Beschäftigungsverhältnis" \[ref=(\w+)\]', snap)
    beruf_combo = re.search(r'combobox "Ausgeübter Beruf" \[ref=(\w+)\]', snap)

    if beruf_select:
        cli(f'select {beruf_select.group(1)} "Angestellter (nicht im öff. Dienst)"')
        wait(1)

    if beruf_combo:
        cli(f"click {beruf_combo.group(1)}")
        cli('type "Bankkauffrau"')
        wait(2)
        # Select from autocomplete
        cli('eval \'(() => { var opts = document.querySelectorAll("[role=option]"); for(var i=0;i<opts.length;i++){if(opts[i].textContent.trim()==="Bankkauffrau"){opts[i].click();return "clicked"}} return "not found"})()\'')
        wait(2)

    if not click_weiter():
        print("    ERROR: Could not advance from Beruf")
        return None
    wait(3)

    # Step 7: Raucher status
    snap = get_snapshot()
    if smoker_class == 1:
        # Nichtraucher 10+ years
        ref = re.search(r'radio "Nichtraucher.*10 Jahren.*" \[ref=(\w+)\]', snap)
    elif smoker_class == 2:
        # Nichtraucher 1+ year
        ref = re.search(r'radio "Nichtraucher.*1 Jahr.*" \[ref=(\w+)\]', snap)
    else:
        # Raucher
        ref = re.search(r'radio "Raucher.*" \[ref=(\w+)\]', snap)

    if ref:
        cli(f"click {ref.group(1)}")
        wait(2)
    else:
        print(f"    ERROR: Smoker radio not found for class {smoker_class}")
        return None

    if not click_weiter():
        print("    ERROR: Could not advance from Raucher")
        return None
    wait(3)

    # Step 8: Versicherungsbeginn - click Jetzt berechnen
    if not click_berechnen():
        print("    ERROR: Jetzt berechnen button not found")
        return None
    wait(5)

    # Extract prices
    snap = get_snapshot()
    prices = extract_prices(snap)

    if not prices:
        print("    ERROR: No prices found in result")
        print("    Snapshot excerpt:", snap[:500])
        return None

    print(f"    Prices: {prices}")
    return prices


def main():
    data_points = []

    # Sampling grid
    # Ages: 25, 30, 35, 40, 45, 50, 55, 60
    # For each age, birth year = 2026 - age (born March 15)
    ages = [25, 30, 35, 40, 45, 50, 55, 60]

    # Phase 1: All ages, Nichtraucher 10+, 200k, 20 years
    print("=== Phase 1: Age curve (Nichtraucher 10+, 200k, 20yr) ===")
    for age in ages:
        birth_year = 2026 - age
        prices = navigate_wizard("15", "03", str(birth_year), smoker_class=1, coverage=200000, term=20)
        if prices:
            for tier, price in prices.items():
                data_points.append({
                    "inputs": {
                        "age": age,
                        "coverage": 200000,
                        "tier": tier,
                        "smoker": "nichtraucher_10plus",
                        "term_years": 20
                    },
                    "output": {"monthly_price": price}
                })

    # Phase 2: All ages, Raucher, 200k, 20 years
    print("\n=== Phase 2: Raucher age curve (200k, 20yr) ===")
    for age in ages:
        birth_year = 2026 - age
        prices = navigate_wizard("15", "03", str(birth_year), smoker_class=3, coverage=200000, term=20)
        if prices:
            for tier, price in prices.items():
                data_points.append({
                    "inputs": {
                        "age": age,
                        "coverage": 200000,
                        "tier": tier,
                        "smoker": "raucher",
                        "term_years": 20
                    },
                    "output": {"monthly_price": price}
                })

    # Phase 3: Nichtraucher 1+ year, a few ages
    print("\n=== Phase 3: Nichtraucher 1+ year (200k, 20yr) ===")
    for age in [30, 40, 50]:
        birth_year = 2026 - age
        prices = navigate_wizard("15", "03", str(birth_year), smoker_class=2, coverage=200000, term=20)
        if prices:
            for tier, price in prices.items():
                data_points.append({
                    "inputs": {
                        "age": age,
                        "coverage": 200000,
                        "tier": tier,
                        "smoker": "nichtraucher_1plus",
                        "term_years": 20
                    },
                    "output": {"monthly_price": price}
                })

    # Phase 4: Coverage variations (age 35, non-smoker 10+, 20yr)
    print("\n=== Phase 4: Coverage variations (age 35, NS10+, 20yr) ===")
    for coverage in [100000, 400000]:
        prices = navigate_wizard("15", "03", "1991", smoker_class=1, coverage=coverage, term=20)
        if prices:
            for tier, price in prices.items():
                data_points.append({
                    "inputs": {
                        "age": 35,
                        "coverage": coverage,
                        "tier": tier,
                        "smoker": "nichtraucher_10plus",
                        "term_years": 20
                    },
                    "output": {"monthly_price": price}
                })

    # Phase 5: Term variations (age 35, non-smoker 10+, 200k)
    print("\n=== Phase 5: Term variations (age 35, NS10+, 200k) ===")
    for term in [10, 15, 25, 30]:
        prices = navigate_wizard("15", "03", "1991", smoker_class=1, coverage=200000, term=term)
        if prices:
            for tier, price in prices.items():
                data_points.append({
                    "inputs": {
                        "age": 35,
                        "coverage": 200000,
                        "tier": tier,
                        "smoker": "nichtraucher_10plus",
                        "term_years": term
                    },
                    "output": {"monthly_price": price}
                })

    # Save results
    result = {
        "product": "risikoleben",
        "sampled_at": "2026-04-13",
        "source_url": BASE_URL,
        "ergo_tier_names": {
            "grundschutz": "Grundschutz",
            "komfort": "Komfort",
            "premium": "Premium"
        },
        "tier_mapping": {
            "grundschutz": "Grundschutz",
            "komfort": "Komfort",
            "premium": "Premium"
        },
        "smoker_classes": {
            "nichtraucher_10plus": "Nichtraucher (nie oder 10+ Jahre)",
            "nichtraucher_1plus": "Nichtraucher (1+ Jahr)",
            "raucher": "Raucher (innerhalb des letzten Jahres)"
        },
        "data_points": data_points
    }

    output_path = "/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/.claude/worktrees/agent-af48ec77/research/risikoleben/price-matrix.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n=== Saved {len(data_points)} data points to {output_path} ===")

    # Print summary
    print("\nSummary of collected prices:")
    for dp in data_points:
        inp = dp["inputs"]
        print(f"  Age={inp['age']}, Tier={inp['tier']}, Smoker={inp['smoker']}, Cov={inp['coverage']}, Term={inp['term_years']}: {dp['output']['monthly_price']} EUR")

if __name__ == "__main__":
    main()
