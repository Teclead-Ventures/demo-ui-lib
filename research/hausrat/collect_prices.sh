#!/bin/bash
# Price collection script for ERGO Hausratversicherung
# Collects prices for different ZIP codes and m2 values

SESSION="hausrat"
RESULTS_FILE="research/hausrat/raw_prices.jsonl"

# Clear results file
> "$RESULTS_FILE"

# Test configurations
# Format: ZIP CITY M2 STREET
CONFIGS=(
  "80331 München 40 Marienplatz"
  "80331 München 60 Marienplatz"
  "80331 München 80 Marienplatz"
  "80331 München 100 Marienplatz"
  "80331 München 120 Marienplatz"
  "50667 Köln 40 Domkloster"
  "50667 Köln 80 Domkloster"
  "50667 Köln 120 Domkloster"
  "01067 Dresden 40 Altmarkt"
  "01067 Dresden 80 Altmarkt"
  "01067 Dresden 120 Altmarkt"
  "24103 Kiel 40 Holstenstraße"
  "24103 Kiel 80 Holstenstraße"
  "24103 Kiel 120 Holstenstraße"
  "54290 Trier 40 Hauptmarkt"
  "54290 Trier 80 Hauptmarkt"
  "54290 Trier 120 Hauptmarkt"
)

collect_price() {
  local ZIP="$1"
  local CITY="$2"
  local M2="$3"
  local STREET="$4"

  echo "Collecting: ZIP=$ZIP M2=$M2..."

  # Navigate to calculator
  playwright-cli -s=$SESSION goto "https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Hausratversicherung/abschluss" 2>&1 | grep -q "Page URL"
  sleep 3

  # Step 1: Select Mehrfamilienhaus
  playwright-cli -s=$SESSION click e33 2>&1 > /dev/null
  sleep 1
  playwright-cli -s=$SESSION click e67 2>&1 > /dev/null
  sleep 3

  # Step 2: Select 2. OG
  playwright-cli -s=$SESSION click e172 2>&1 > /dev/null
  sleep 1
  playwright-cli -s=$SESSION click e186 2>&1 > /dev/null
  sleep 3

  # Step 3: Enter m2
  playwright-cli -s=$SESSION fill e215 "$M2" 2>&1 > /dev/null
  sleep 1
  playwright-cli -s=$SESSION click e222 2>&1 > /dev/null
  sleep 3

  # Step 4: Enter address
  playwright-cli -s=$SESSION fill e269 "$STREET" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill e275 "12" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill e282 "$ZIP" 2>&1 > /dev/null
  sleep 3
  playwright-cli -s=$SESSION click e292 2>&1 > /dev/null
  sleep 3

  # Step 5: Insurance start date (default tomorrow is fine)
  playwright-cli -s=$SESSION click e342 2>&1 > /dev/null
  sleep 3

  # Step 6: Birth date
  playwright-cli -s=$SESSION fill e370 "15" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill e373 "03" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill e376 "1990" 2>&1 > /dev/null
  sleep 1
  playwright-cli -s=$SESSION click e379 2>&1 > /dev/null
  sleep 5

  # Step 7: Read prices - Best (default)
  local BEST_PRICE=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1 | grep -A2 'generic \[ref=e397\]' | head -1 | sed 's/.*: //')

  # Switch to Smart
  playwright-cli -s=$SESSION click e408 2>&1 > /dev/null
  sleep 2
  local SMART_PRICE=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1 | grep -A2 'generic \[ref=e397\]' | head -1 | sed 's/.*: //')

  echo "{\"zip\":\"$ZIP\",\"city\":\"$CITY\",\"m2\":$M2,\"smart_monthly\":\"$SMART_PRICE\",\"best_monthly\":\"$BEST_PRICE\"}" >> "$RESULTS_FILE"
  echo "  -> Smart: $SMART_PRICE, Best: $BEST_PRICE"
}

for CONFIG in "${CONFIGS[@]}"; do
  read -r ZIP CITY M2 STREET <<< "$CONFIG"
  collect_price "$ZIP" "$CITY" "$M2" "$STREET"
done

echo "Done! Results in $RESULTS_FILE"
