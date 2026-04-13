#!/bin/bash
# Collect prices from ERGO Rechtsschutz configurator
# This script reads the current price via playwright-cli eval

SESSION="rechtsschutz"

read_price() {
  local result=$(playwright-cli -s=$SESSION eval 'document.querySelector("[class*=price], [class*=beitrag], [class*=Price]")?.textContent' 2>&1)
  echo "$result" | grep -o '[0-9]*,[0-9]*' | head -1 | tr ',' '.'
}

echo "Price: $(read_price)"
