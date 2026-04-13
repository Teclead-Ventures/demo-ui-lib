#!/usr/bin/env python3
"""Collect ERGO Risikoleben prices via playwright-cli - streamlined version."""
import subprocess
import time
import re
import json
import sys

SESSION = "risikoleben"
BASE_URL = "https://www.ergo.de/de/Produkte/Lebensversicherung/Risikolebensversicherung/abschluss"

sys.stdout.reconfigure(line_buffering=True)

def cli(cmd, timeout=20):
    full = f"playwright-cli -s={SESSION} {cmd}"
    try:
        r = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"

def w(s=3):
    time.sleep(s)

def js_click_weiter():
    return cli('eval \'(() => { var b=document.querySelectorAll("button"); for(var i=0;i<b.length;i++){if(b[i].textContent.trim()==="weiter"&&!b[i].disabled){b[i].click();return "ok"}} return "no"})()\'')

def js_click_berechnen():
    return cli('eval \'(() => { var b=document.querySelectorAll("button"); for(var i=0;i<b.length;i++){if(b[i].textContent.trim()==="Jetzt berechnen"){b[i].click();return "ok"}} return "no"})()\'')

def snap():
    return cli("snapshot")

def extract_prices(s):
    p = {}
    m = re.search(r'radio "Grundschutz ([\d,]+) .* mtl', s)
    if m: p["grundschutz"] = float(m.group(1).replace(",", "."))
    m = re.search(r'radio "Komfort ([\d,]+) .* mtl', s)
    if m: p["komfort"] = float(m.group(1).replace(",", "."))
    m = re.search(r'radio ".*Premium ([\d,]+) .* mtl', s)
    if m: p["premium"] = float(m.group(1).replace(",", "."))
    return p

def collect_one(birth_year, smoker_class, coverage=200000, term=20):
    """smoker_class: 1=NS10+, 2=NS1+, 3=Raucher"""
    age = 2026 - birth_year
    print(f"  Collecting: age={age}, smoker={smoker_class}, cov={coverage}, term={term}", flush=True)

    # Close and reopen for fresh state
    cli("close")
    w(1)
    cli(f'open "{BASE_URL}" --headed', timeout=30)
    w(5)

    # Dismiss cookies
    s = snap()
    m = re.search(r'button "Alle akzeptieren" \[ref=(\w+)\]', s)
    if m:
        cli(f"click {m.group(1)}")
        w(2)

    # Step 1: weiter
    js_click_weiter()
    w(3)

    # Step 2: Birth date
    s = snap()
    tag = re.search(r'spinbutton "Tag" \[ref=(\w+)\]', s)
    mon = re.search(r'spinbutton "Monat" \[ref=(\w+)\]', s)
    yr = re.search(r'spinbutton "Jahr" \[ref=(\w+)\]', s)
    if not tag:
        print("    ERROR: no Tag field", flush=True)
        return None
    cli(f"click {tag.group(1)}")
    cli('type "15"')
    w(0.5)
    cli(f'fill {mon.group(1)} "03"')
    cli(f'fill {yr.group(1)} "{birth_year}"')
    cli("press Tab")
    w(2)
    js_click_weiter()
    w(3)

    # Step 3: Absicherungsform
    js_click_weiter()
    w(3)

    # Step 4: Versicherungssumme
    s = snap()
    combo = re.search(r'combobox \[ref=(\w+)\]', s)
    if combo:
        cov_str = f"{coverage:,}".replace(",", ".")
        cli(f'fill {combo.group(1)} "{cov_str}"')
        cli("press Tab")
        w(2)
    js_click_weiter()
    w(3)

    # Step 5: Laufzeit
    s = snap()
    lauf = re.search(r'combobox \[ref=(\w+)\]', s)
    if lauf:
        cli(f'fill {lauf.group(1)} "{term}"')
        cli("press Tab")
        w(2)
    js_click_weiter()
    w(3)

    # Step 6: Beruf
    s = snap()
    beruf_sel = re.search(r'combobox "Beschäftigungsverhältnis" \[ref=(\w+)\]', s)
    beruf_combo = re.search(r'combobox "Ausgeübter Beruf" \[ref=(\w+)\]', s)
    if beruf_sel:
        cli(f'select {beruf_sel.group(1)} "Angestellter (nicht im öff. Dienst)"')
        w(1)
    if beruf_combo:
        cli(f"click {beruf_combo.group(1)}")
        cli('type "Bankkauffrau"')
        w(2)
        cli('eval \'(() => { var o=document.querySelectorAll("[role=option]"); for(var i=0;i<o.length;i++){if(o[i].textContent.trim()==="Bankkauffrau"){o[i].click();return "ok"}} return "no"})()\'')
        w(2)
    js_click_weiter()
    w(3)

    # Step 7: Raucher
    s = snap()
    if smoker_class == 1:
        ref = re.search(r'radio "Nichtraucher.*10 Jahren.*" \[ref=(\w+)\]', s)
    elif smoker_class == 2:
        ref = re.search(r'radio "Nichtraucher.*1 Jahr.*" \[ref=(\w+)\]', s)
    else:
        ref = re.search(r'radio "Raucher.*" \[ref=(\w+)\]', s)
    if ref:
        cli(f"click {ref.group(1)}")
        w(2)
    js_click_weiter()
    w(3)

    # Step 8: Jetzt berechnen
    js_click_berechnen()
    w(5)

    # Extract
    s = snap()
    prices = extract_prices(s)
    if prices:
        print(f"    OK: {prices}", flush=True)
    else:
        print(f"    ERROR: no prices found", flush=True)
        # Debug
        for line in s.split("\n"):
            if "radio" in line.lower() or "preis" in line.lower() or "mtl" in line.lower():
                print(f"    DEBUG: {line.strip()}", flush=True)
    return prices

def main():
    data_points = []

    def add_prices(prices, age, smoker, coverage, term):
        if not prices:
            return
        smoker_map = {1: "nichtraucher_10plus", 2: "nichtraucher_1plus", 3: "raucher"}
        for tier, price in prices.items():
            data_points.append({
                "inputs": {"age": age, "coverage": coverage, "tier": tier,
                           "smoker": smoker_map[smoker], "term_years": term},
                "output": {"monthly_price": price}
            })

    # Already have age 35 from manual collection
    manual_35 = {"grundschutz": 7.54, "komfort": 9.54, "premium": 13.54}
    add_prices(manual_35, 35, 1, 200000, 20)

    # Also have coverage/term variations from manual
    add_prices({"grundschutz": 4.14, "komfort": 5.23, "premium": 7.85}, 35, 1, 100000, 20)
    add_prices({"grundschutz": 14.32, "komfort": 18.18, "premium": 24.94}, 35, 1, 400000, 20)
    add_prices({"grundschutz": 4.76, "komfort": 6.00, "premium": 8.86}, 35, 1, 200000, 10)
    add_prices({"grundschutz": 14.61, "komfort": 18.55, "premium": 25.43}, 35, 1, 200000, 30)

    # Phase 1: Nichtraucher 10+, 200k, 20yr - remaining ages
    print("=== Phase 1: NS10+, 200k, 20yr ===", flush=True)
    for age in [25, 30, 40, 45, 50, 55, 60]:
        p = collect_one(2026 - age, 1, 200000, 20)
        add_prices(p, age, 1, 200000, 20)

    # Phase 2: Raucher, 200k, 20yr
    print("\n=== Phase 2: Raucher, 200k, 20yr ===", flush=True)
    for age in [25, 30, 35, 40, 45, 50, 55, 60]:
        p = collect_one(2026 - age, 3, 200000, 20)
        add_prices(p, age, 3, 200000, 20)

    # Phase 3: Nichtraucher 1+, 200k, 20yr (3 ages)
    print("\n=== Phase 3: NS1+, 200k, 20yr ===", flush=True)
    for age in [30, 40, 50]:
        p = collect_one(2026 - age, 2, 200000, 20)
        add_prices(p, age, 2, 200000, 20)

    # Phase 4: Term variations (age 35, NS10+, 200k) - 15yr and 25yr (10 and 30 already done)
    print("\n=== Phase 4: Term variations ===", flush=True)
    for term in [15, 25]:
        p = collect_one(1991, 1, 200000, term)
        add_prices(p, 35, 1, 200000, term)

    # Save
    result = {
        "product": "risikoleben",
        "sampled_at": "2026-04-13",
        "source_url": BASE_URL,
        "ergo_tier_names": {"grundschutz": "Grundschutz", "komfort": "Komfort", "premium": "Premium"},
        "tier_mapping": {"grundschutz": "Grundschutz", "komfort": "Komfort", "premium": "Premium"},
        "smoker_classes": {
            "nichtraucher_10plus": "Nichtraucher (nie/10+ Jahre)",
            "nichtraucher_1plus": "Nichtraucher (1+ Jahr)",
            "raucher": "Raucher"
        },
        "data_points": data_points
    }

    out = "/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/.claude/worktrees/agent-af48ec77/research/risikoleben/price-matrix.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(data_points)} data points to price-matrix.json", flush=True)

    for dp in data_points:
        i = dp["inputs"]
        print(f"  {i['age']:>2}y {i['smoker']:<20s} {i['tier']:<12s} {i['coverage']:>7,} {i['term_years']:>2}yr => {dp['output']['monthly_price']:.2f} EUR", flush=True)

if __name__ == "__main__":
    main()
