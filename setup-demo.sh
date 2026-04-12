#!/usr/bin/env bash
set -euo pipefail

# ── Setup Demo Project ───────────────────────────────────────────────────────
# Creates a fresh full-stack demo project from the base template.
# Uses a shared Supabase instance with per-run table prefix.
#
# Usage:
#   ./setup-demo.sh                    → creates demo-run-YYYY-MM-DD-HHMM/
#   ./setup-demo.sh my-client-demo     → creates my-client-demo/
#   ./setup-demo.sh --clean            → removes ALL demo-run-* directories
#   ./setup-demo.sh --list-tables      → shows all demo tables in Supabase
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATE_DIR="$BASE_DIR/next-demo-base"
UI_LIB_DIR="$SCRIPT_DIR"

# ── Clean mode ────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--clean" ]]; then
  echo "Removing all demo-run-* directories in $BASE_DIR..."
  count=0
  for dir in "$BASE_DIR"/demo-run-*; do
    if [[ -d "$dir" ]]; then
      echo "  rm -rf $dir"
      rm -rf "$dir"
      ((count++))
    fi
  done
  echo "Cleaned $count demo directories."
  exit 0
fi

# ── Validate template exists ──────────────────────────────────────────────────
if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Error: Base template not found at $TEMPLATE_DIR"
  echo "Run this script from the demo-ui-lib directory."
  exit 1
fi

# ── Validate .env.local exists in template ────────────────────────────────────
if [[ ! -f "$TEMPLATE_DIR/.env.local" ]]; then
  echo "Error: No .env.local found in $TEMPLATE_DIR"
  echo ""
  echo "Create it with your Supabase credentials:"
  echo "  cp $TEMPLATE_DIR/.env.local.example $TEMPLATE_DIR/.env.local"
  echo "  # Then fill in NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY"
  exit 1
fi

# ── Project name + table prefix ──────────────────────────────────────────────
TIMESTAMP="$(date +%Y%m%d_%H%M)"
PROJECT_NAME="${1:-demo-run-$TIMESTAMP}"
TABLE_PREFIX="run_${TIMESTAMP}"
PROJECT_DIR="$BASE_DIR/$PROJECT_NAME"

if [[ -d "$PROJECT_DIR" ]]; then
  echo "Error: $PROJECT_DIR already exists."
  echo "Choose a different name or run: ./setup-demo.sh --clean"
  exit 1
fi

echo "═══════════════════════════════════════════════════════"
echo "  Setting up demo project: $PROJECT_NAME"
echo "  Table prefix: ${TABLE_PREFIX}"
echo "═══════════════════════════════════════════════════════"
echo ""

# ── Step 1: Copy base template (including .env.local) ────────────────────────
echo "1/7  Copying base template..."
cp -r "$TEMPLATE_DIR" "$PROJECT_DIR"
rm -rf "$PROJECT_DIR/.git"
rm -rf "$PROJECT_DIR/.next"

# ── Step 2: Set table prefix in .env.local ───────────────────────────────────
echo "2/7  Setting table prefix: ${TABLE_PREFIX}..."
if grep -q "NEXT_PUBLIC_TABLE_PREFIX" "$PROJECT_DIR/.env.local"; then
  sed -i '' "s/^NEXT_PUBLIC_TABLE_PREFIX=.*/NEXT_PUBLIC_TABLE_PREFIX=${TABLE_PREFIX}/" "$PROJECT_DIR/.env.local"
else
  echo "NEXT_PUBLIC_TABLE_PREFIX=${TABLE_PREFIX}" >> "$PROJECT_DIR/.env.local"
fi

# ── Step 3: Copy UI components ───────────────────────────────────────────────
echo "3/7  Copying UI component library..."
mkdir -p "$PROJECT_DIR/src/components/ui"
cp -r "$UI_LIB_DIR/src/components/"* "$PROJECT_DIR/src/components/ui/"

# ── Step 4: Copy theme ───────────────────────────────────────────────────────
echo "4/7  Copying theme..."
mkdir -p "$PROJECT_DIR/src/lib/theme"
cp -r "$UI_LIB_DIR/src/theme/"* "$PROJECT_DIR/src/lib/theme/"

# ── Step 5: Copy tickets + screenshots ───────────────────────────────────────
echo "5/7  Copying tickets and reference screenshots..."
cp -r "$UI_LIB_DIR/tickets/" "$PROJECT_DIR/tickets/"
mkdir -p "$PROJECT_DIR/screenshots/reference"
if [[ -d "$UI_LIB_DIR/screenshots/reference" ]]; then
  cp -r "$UI_LIB_DIR/screenshots/reference/"* "$PROJECT_DIR/screenshots/reference/" 2>/dev/null || true
fi

# ── Step 6: Install dependencies ─────────────────────────────────────────────
echo "6/7  Installing dependencies..."
cd "$PROJECT_DIR"
npm install --silent 2>/dev/null

# ── Step 7: Initialize git ───────────────────────────────────────────────────
echo "7/7  Initializing git..."
git init -q
git add -A
git commit -q -m "Initial setup: base template + UI library (prefix: ${TABLE_PREFIX})"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Done! Project ready at:"
echo "  $PROJECT_DIR"
echo ""
echo "  Supabase:     shared instance (credentials from .env.local)"
echo "  Table prefix:  ${TABLE_PREFIX}"
echo "  Table name:    ${TABLE_PREFIX}_insurance_applications"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "  1. Open a Claude Code session in the project:"
echo ""
echo "     cd $PROJECT_DIR"
echo "     claude"
echo ""
echo "  2. Paste the trigger prompt to start the build."
echo ""
echo "  To clean up all demo runs:"
echo "     cd $SCRIPT_DIR && ./setup-demo.sh --clean"
echo ""
