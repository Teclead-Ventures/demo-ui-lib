#!/bin/bash
# Fast ERGO Risikoleben price collector
# Usage: ./collect.sh <birth_year> <smoker: 1|2|3> [coverage] [term]
# smoker: 1=NS10+, 2=NS1+, 3=Raucher

set -e
S="risikoleben"
YEAR=$1
SMOKER=$2
COV=${3:-200000}
TERM=${4:-20}

export PYTHONUNBUFFERED=1

# Close and reopen
playwright-cli -s=$S close 2>/dev/null || true
sleep 1
playwright-cli -s=$S open "https://www.ergo.de/de/Produkte/Lebensversicherung/Risikolebensversicherung/abschluss" --headed 2>&1 >/dev/null
sleep 5

# Dismiss cookies
playwright-cli -s=$S eval '(() => { var d = document.querySelector("#usercentrics-root"); if(d && d.shadowRoot){var b=d.shadowRoot.querySelector("[data-testid=uc-accept-all-button]"); if(b){b.click();return "ok"}} var btns=document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.includes("Alle akzeptieren")){btns[i].click();return "ok2"}} return "none"})()' 2>&1 >/dev/null
sleep 2

# Step 1: weiter (Mich selbst default)
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 2: Birth date
SNAP=$(playwright-cli -s=$S snapshot 2>&1)
TAG_REF=$(echo "$SNAP" | grep -oP 'spinbutton "Tag" \[ref=\K\w+')
MON_REF=$(echo "$SNAP" | grep -oP 'spinbutton "Monat" \[ref=\K\w+')
YR_REF=$(echo "$SNAP" | grep -oP 'spinbutton "Jahr" \[ref=\K\w+')
playwright-cli -s=$S click $TAG_REF 2>&1 >/dev/null
playwright-cli -s=$S type "15" 2>&1 >/dev/null
sleep 0.3
playwright-cli -s=$S fill $MON_REF "03" 2>&1 >/dev/null
playwright-cli -s=$S fill $YR_REF "$YEAR" 2>&1 >/dev/null
playwright-cli -s=$S press Tab 2>&1 >/dev/null
sleep 2
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 3: Absicherungsform (constant default)
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 4: Versicherungssumme
SNAP=$(playwright-cli -s=$S snapshot 2>&1)
COMBO_REF=$(echo "$SNAP" | grep -oP 'combobox \[ref=\K\w+' | head -1)
COV_FMT=$(printf "%'.0f" $COV | sed 's/,/./g')
playwright-cli -s=$S fill $COMBO_REF "$COV_FMT" 2>&1 >/dev/null
playwright-cli -s=$S press Tab 2>&1 >/dev/null
sleep 2
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 5: Laufzeit
SNAP=$(playwright-cli -s=$S snapshot 2>&1)
LAUF_REF=$(echo "$SNAP" | grep -oP 'combobox \[ref=\K\w+' | head -1)
playwright-cli -s=$S fill $LAUF_REF "$TERM" 2>&1 >/dev/null
playwright-cli -s=$S press Tab 2>&1 >/dev/null
sleep 2
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 6: Beruf
SNAP=$(playwright-cli -s=$S snapshot 2>&1)
BERUF_SEL=$(echo "$SNAP" | grep -oP 'combobox "Beschäftigungsverhältnis" \[ref=\K\w+')
BERUF_COMBO=$(echo "$SNAP" | grep -oP 'combobox "Ausgeübter Beruf" \[ref=\K\w+')
playwright-cli -s=$S select $BERUF_SEL "Angestellter (nicht im öff. Dienst)" 2>&1 >/dev/null
sleep 1
playwright-cli -s=$S click $BERUF_COMBO 2>&1 >/dev/null
playwright-cli -s=$S type "Bankkauffrau" 2>&1 >/dev/null
sleep 2
playwright-cli -s=$S eval '(() => { var opts = document.querySelectorAll("[role=option]"); for(var i=0;i<opts.length;i++){if(opts[i].textContent.trim()==="Bankkauffrau"){opts[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 2
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 7: Raucher
SNAP=$(playwright-cli -s=$S snapshot 2>&1)
if [ "$SMOKER" = "1" ]; then
  REF=$(echo "$SNAP" | grep -oP 'radio "Nichtraucher.*10 Jahren.*" \[ref=\K\w+')
elif [ "$SMOKER" = "2" ]; then
  REF=$(echo "$SNAP" | grep -oP 'radio "Nichtraucher.*1 Jahr.*" \[ref=\K\w+')
else
  REF=$(echo "$SNAP" | grep -oP 'radio "Raucher.*" \[ref=\K\w+')
fi
playwright-cli -s=$S click $REF 2>&1 >/dev/null
sleep 2
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="weiter" && !btns[i].disabled){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 3

# Step 8: Jetzt berechnen
playwright-cli -s=$S eval '(() => { var btns = document.querySelectorAll("button"); for(var i=0;i<btns.length;i++){if(btns[i].textContent.trim()==="Jetzt berechnen"){btns[i].click();return 1}} return 0})()' 2>&1 >/dev/null
sleep 5

# Extract prices
SNAP=$(playwright-cli -s=$S snapshot 2>&1)
GRUND=$(echo "$SNAP" | grep -oP 'radio "Grundschutz \K[\d,]+(?= €)')
KOMFORT=$(echo "$SNAP" | grep -oP 'radio "Komfort \K[\d,]+(?= €)')
PREMIUM=$(echo "$SNAP" | grep -oP 'radio ".*Premium \K[\d,]+(?= €)')

AGE=$((2026 - YEAR))
echo "AGE=$AGE|SMOKER=$SMOKER|COV=$COV|TERM=$TERM|GRUND=$GRUND|KOMFORT=$KOMFORT|PREMIUM=$PREMIUM"
