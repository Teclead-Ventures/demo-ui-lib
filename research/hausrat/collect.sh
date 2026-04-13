#!/bin/bash
# Robust price collection for ERGO Hausrat using playwright-cli
# Uses testid selectors which are stable across page loads
SESSION="hausrat"

collect_price() {
  local ZIP="$1"
  local M2="$2"
  local STREET="$3"
  local BIRTH_YEAR="$4"
  local BUILDING="$5"  # "mfh" or "efh"

  echo "=== ZIP=$ZIP M2=$M2 BIRTH=$BIRTH_YEAR BUILDING=$BUILDING ==="

  # Step 1: Navigate to calculator
  playwright-cli -s=$SESSION goto "https://www.ergo.de/de/Produkte/Hausrat-und-Gebaeudeversicherung/Hausratversicherung/abschluss" 2>&1 > /dev/null
  sleep 4

  # Step 1: Select building type
  if [ "$BUILDING" = "efh" ]; then
    playwright-cli -s=$SESSION eval 'document.querySelectorAll("button[class*=radio], button[class*=option]")[1]?.click()' 2>&1 > /dev/null
    sleep 1
  else
    # Mehrfamilienhaus - first option
    playwright-cli -s=$SESSION eval 'document.querySelectorAll("button[class*=radio], button[class*=option]")[0]?.click()' 2>&1 > /dev/null
    sleep 1
  fi
  # Click weiter using testid
  playwright-cli -s=$SESSION eval 'document.querySelector("[data-testid=submit-button]").click()' 2>&1 > /dev/null
  sleep 4

  # Step 2: Select floor (only for MFH)
  if [ "$BUILDING" = "mfh" ]; then
    # Select 2. Obergeschoss (4th option, index 3)
    playwright-cli -s=$SESSION eval 'document.querySelectorAll("button[class*=radio], button[class*=option]")[3]?.click()' 2>&1 > /dev/null
    sleep 1
    playwright-cli -s=$SESSION eval 'document.querySelector("[data-testid=submit-button]").click()' 2>&1 > /dev/null
    sleep 4
  fi

  # Step 3: Enter m2
  playwright-cli -s=$SESSION eval "document.querySelector('[data-testid=inputSizeHome]').value = ''" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill "$(playwright-cli -s=$SESSION snapshot 2>&1 | grep 'textbox.*ref=' | head -1 | sed 's/.*\[ref=\([^]]*\)\].*/\1/')" "$M2" 2>&1 > /dev/null
  sleep 1
  playwright-cli -s=$SESSION eval 'document.querySelector("[data-testid=submit-button]").click()' 2>&1 > /dev/null
  sleep 4

  # Step 4: Enter address
  playwright-cli -s=$SESSION eval "document.querySelector('[data-testid=street-name-input]').value = ''" 2>&1 > /dev/null
  playwright-cli -s=$SESSION eval "document.querySelector('[data-testid=street-name-input]')._valueTracker && document.querySelector('[data-testid=street-name-input]')._valueTracker.setValue('')" 2>&1 > /dev/null
  # Use fill commands with testid
  local SNAP=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
  local STREET_REF=$(echo "$SNAP" | grep 'textbox "street-name-input-input"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')
  local NUM_REF=$(echo "$SNAP" | grep 'textbox "street-number-input-input"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')
  local ZIP_REF=$(echo "$SNAP" | grep 'textbox "zip-code-input-input"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')

  playwright-cli -s=$SESSION fill "$STREET_REF" "$STREET" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill "$NUM_REF" "12" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill "$ZIP_REF" "$ZIP" 2>&1 > /dev/null
  sleep 4

  playwright-cli -s=$SESSION eval 'document.querySelector("[data-testid=submit-button]").click()' 2>&1 > /dev/null
  sleep 4

  # Step 5: Insurance start date (default is fine, just click weiter)
  playwright-cli -s=$SESSION eval 'document.querySelector("[data-testid=submit-button]").click()' 2>&1 > /dev/null
  sleep 4

  # Step 6: Birth date
  SNAP=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
  local DAY_REF=$(echo "$SNAP" | grep 'spinbutton "Tag"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')
  local MON_REF=$(echo "$SNAP" | grep 'spinbutton "Monat"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')
  local YEAR_REF=$(echo "$SNAP" | grep 'spinbutton "Jahr"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')

  playwright-cli -s=$SESSION fill "$DAY_REF" "15" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill "$MON_REF" "03" 2>&1 > /dev/null
  playwright-cli -s=$SESSION fill "$YEAR_REF" "$BIRTH_YEAR" 2>&1 > /dev/null
  sleep 2
  playwright-cli -s=$SESSION eval 'document.querySelector("[data-testid=submit-button]").click()' 2>&1 > /dev/null
  sleep 6

  # Step 7: Read prices
  SNAP=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)

  # Check which tier is selected and get prices
  local CURRENT_TIER=$(echo "$SNAP" | grep 'banner' | sed 's/.*: //')
  local CURRENT_PRICE=$(echo "$SNAP" | grep -A1 'generic \[ref=e397\]' | tail -1 | sed 's/.*: //' | tr -d '"')

  # Get coverage amount
  local COVERAGE=$(echo "$SNAP" | grep 'Versicherungssumme' | head -1 | sed 's/.*: //')

  echo "  Tier: $CURRENT_TIER Price: $CURRENT_PRICE Coverage: $COVERAGE"

  # Switch to other tier
  if echo "$CURRENT_TIER" | grep -q "Best"; then
    BEST_PRICE="$CURRENT_PRICE"
    # Switch to Smart
    SNAP2=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
    SMART_TAB=$(echo "$SNAP2" | grep 'tab "Smart"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')
    playwright-cli -s=$SESSION click "$SMART_TAB" 2>&1 > /dev/null
    sleep 3
    SNAP3=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
    SMART_PRICE=$(echo "$SNAP3" | grep -A1 'generic \[ref=e397\]' | tail -1 | sed 's/.*: //' | tr -d '"')
  else
    SMART_PRICE="$CURRENT_PRICE"
    # Switch to Best
    SNAP2=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
    BEST_TAB=$(echo "$SNAP2" | grep 'tab "Best"' | sed 's/.*\[ref=\([^]]*\)\].*/\1/')
    playwright-cli -s=$SESSION click "$BEST_TAB" 2>&1 > /dev/null
    sleep 3
    SNAP3=$(playwright-cli -s=$SESSION snapshot 'main' 2>&1)
    BEST_PRICE=$(echo "$SNAP3" | grep -A1 'generic \[ref=e397\]' | tail -1 | sed 's/.*: //' | tr -d '"')
  fi

  echo "  Smart: $SMART_PRICE  Best: $BEST_PRICE"
  echo "{\"zip\":\"$ZIP\",\"m2\":$M2,\"birth_year\":$BIRTH_YEAR,\"building\":\"$BUILDING\",\"smart_monthly\":\"$SMART_PRICE\",\"best_monthly\":\"$BEST_PRICE\",\"coverage\":\"$COVERAGE\"}" >> research/hausrat/raw_prices.jsonl
}

# Clear results
> research/hausrat/raw_prices.jsonl

# Coverage linearity test - München, different m2 values
collect_price "80331" "40" "Marienplatz" "1990" "mfh"
collect_price "80331" "60" "Marienplatz" "1990" "mfh"
collect_price "80331" "100" "Marienplatz" "1990" "mfh"
collect_price "80331" "120" "Marienplatz" "1990" "mfh"

# Regional variation - 80m2, different ZIPs
collect_price "50667" "80" "Domkloster" "1990" "mfh"
collect_price "01067" "80" "Altmarkt" "1990" "mfh"
collect_price "24103" "80" "Holstenstraße" "1990" "mfh"
collect_price "54290" "80" "Hauptmarkt" "1990" "mfh"

# Age test - München 80m2, under 36
collect_price "80331" "80" "Marienplatz" "1995" "mfh"

# Building type - Einfamilienhaus vs MFH
collect_price "80331" "80" "Marienplatz" "1990" "efh"

echo "=== COLLECTION COMPLETE ==="
cat research/hausrat/raw_prices.jsonl
