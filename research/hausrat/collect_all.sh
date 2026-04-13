#!/bin/bash
# Batch price collection for ERGO Hausrat
SESSION="hausrat"
RESULTS=""

collect() {
  local ZIP="$1" M2="$2" STREET="$3" YEAR="$4" LABEL="$5"

  echo ">>> Collecting: $LABEL (ZIP=$ZIP M2=$M2 YEAR=$YEAR)..."

  # Navigate to calculator
  playwright-cli -s=$SESSION goto "https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Hausratversicherung/abschluss" 2>&1 > /dev/null
  sleep 3

  # Create nav script with substituted values
  sed "s/M2_VALUE/$M2/g; s/ZIP_VALUE/$ZIP/g; s/STREET_VALUE/$STREET/g; s/YEAR_VALUE/$YEAR/g" research/hausrat/nav_wizard.js > research/hausrat/nav_current.js

  # Run wizard
  playwright-cli -s=$SESSION run-code --filename=research/hausrat/nav_current.js 2>&1 > /dev/null
  sleep 2

  # Extract Best price (default tab)
  local SNAP=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
  local BANNER=$(echo "$SNAP" | grep 'generic "banner"' | head -1 | sed 's/.*: //')
  local PRICE=$(echo "$SNAP" | grep -B2 'mtl\.' | head -1 | awk '{print $NF}')

  local BEST_PRICE=""
  local SMART_PRICE=""

  if echo "$BANNER" | grep -q "Best"; then
    BEST_PRICE="$PRICE"
    # Switch to Smart
    local SMART_TAB=$(echo "$SNAP" | grep 'tab "Smart"' | grep -o 'ref=e[0-9]*' | sed 's/ref=//')
    playwright-cli -s=$SESSION click "$SMART_TAB" 2>&1 > /dev/null
    sleep 3
    SMART_PRICE=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1 | grep -B2 'mtl\.' | head -1 | awk '{print $NF}')
  else
    SMART_PRICE="$PRICE"
    local BEST_TAB=$(echo "$SNAP" | grep 'tab "Best"' | grep -o 'ref=e[0-9]*' | sed 's/ref=//')
    playwright-cli -s=$SESSION click "$BEST_TAB" 2>&1 > /dev/null
    sleep 3
    BEST_PRICE=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1 | grep -B2 'mtl\.' | head -1 | awk '{print $NF}')
  fi

  echo "    $LABEL: Smart=$SMART_PRICE Best=$BEST_PRICE"
  RESULTS="${RESULTS}$LABEL|$ZIP|$M2|$YEAR|$SMART_PRICE|$BEST_PRICE\n"
}

# Coverage linearity test - München, different m2 values
collect "80331" "100" "Marienplatz" "1990" "Munich_100m2"
collect "80331" "120" "Marienplatz" "1990" "Munich_120m2"

# Regional variation test - 80m2 in different cities
collect "50667" "80" "Domkloster" "1990" "Koeln_80m2"
collect "01067" "80" "Altmarkt" "1990" "Dresden_80m2"
collect "24103" "80" "Holstenstrasse" "1990" "Kiel_80m2"
collect "54290" "80" "Hauptmarkt" "1990" "Trier_80m2"

# Age under 36 test
collect "80331" "80" "Marienplatz" "1995" "Munich_80m2_age31"

# Age over 36 test
collect "80331" "80" "Marienplatz" "1980" "Munich_80m2_age46"

echo ""
echo "=== ALL RESULTS ==="
echo -e "Label|ZIP|M2|Birth_Year|Smart_Monthly|Best_Monthly"
echo -e "$RESULTS"
