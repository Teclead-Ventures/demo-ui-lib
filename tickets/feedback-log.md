# Demo Run Feedback Log

This file is read at the start of every execution and written to at the end.
Each run adds a section. The orchestrator must read ALL previous entries before starting
and apply the lessons learned.

---

## Pre-Run Feedback (added manually before first run completed)

### MUST FIX for next run: Dynamic pricing calculation

The current plan uses hardcoded static prices in `planData.ts`. This is unrealistic — the price should change based on the user's age, coverage amount, and plan tier.

**Create** `src/lib/data/pricing.ts` with:
```typescript
const BASE_RATE = { grundschutz: 2.80, komfort: 3.45, premium: 4.25 };
const AGE_FACTOR = (age: number) => 1 + (age - 40) * 0.022;
const PAYMENT_YEARS = (age: number) => 85 - age;

export function calculateMonthlyPrice(
  age: number,
  coverageAmount: number,
  plan: "grundschutz" | "komfort" | "premium"
): number {
  const units = coverageAmount / 1000;
  return Math.round(units * BASE_RATE[plan] * AGE_FACTOR(age) * 100) / 100;
}

export function calculatePaymentDuration(age: number): number {
  return PAYMENT_YEARS(age);
}
```

**Unit tests** (Vitest) for this module — at minimum:
- 40-year-old, 8.000€, all 3 plans → verify Grundschutz < Komfort < Premium
- 60-year-old same coverage → verify higher price than 40-year-old
- Edge cases: age 40 (minimum), age 85 (maximum)
- Payment duration: age 44 → 41 years, age 60 → 25 years

**Impact on tickets:**
- Phase 1: Create `pricing.ts` + unit tests in foundation (so all worktrees inherit it)
- Ticket 05 (plan selection): Use `calculateMonthlyPrice()` instead of static `planData.monthlyPrice`
- Ticket 06 (dynamic adjustment): Display calculated price in summary bar
- Ticket 08 (summary): Show calculated price, not looked up from static data
- `planData.ts` still exists for benefit descriptions, but prices come from `pricing.ts`

### Priority: HIGH — this makes the demo significantly more impressive (prices react to user input)

---

<!-- Entries are added below by the orchestrator after each run -->

## Run: 2026-04-11 (ergo-demo, prefix run_20260411_1706)

### Result: SUCCESS (with post-deploy styling fix)

### Phase Results
- Phase 0 (Setup): PASS — Supabase table created, env vars set
- Phase 1 (Foundation): PASS — TariffContext, planData, wizard routing, SSR-safe Toast
- Phase 2 (Parallel): PASS — 8/8 agents succeeded on first attempt, all tsc clean
- Phase 3 (Integration): PASS — Full wizard walkthrough + submit + dashboard verification
- Phase 4 (Deploy): PASS — Vercel deploy + production walkthrough with different data
- Phase 5 (Retrospective): Styling fix applied post-deploy

### Critical Issues Found

1. **THEME CSS NOT IMPORTED (P0)** — All UI components rendered without colors because `globals.css` didn't import `theme.css`. The CSS custom properties (`--color-primary`, `--color-border`, etc.) were all undefined.
   - **Fix applied**: Added `@import "../../src/lib/theme/theme.css"` to globals.css
   - **Fix applied to EXECUTE.md**: Added step 7 in Phase 1 to explicitly import theme CSS

2. **Unicode escapes rendered literally** — Agents used `\u20AC` in JSX props which rendered as literal text instead of €.
   - **Fix applied**: Replaced with actual € character
   - **Fix applied to EXECUTE.md**: Added critical rule about using actual Unicode characters

3. **Supabase project ID mismatch** — The .env.local hardcoded a project ID not accessible via MCP. Had to switch to accessible project.

4. **Broken .bin symlinks** — `npx tsc` and `npx next` failed because .bin symlinks were stale.
   - **Fix applied to EXECUTE.md**: Added fallback path `node_modules/typescript/bin/tsc`

5. **ToastProvider SSR crash** — `document.body` in `createPortal` crashed during SSR. Fixed with `useEffect` mount guard.

### What Went Well
- All 8 parallel agents compiled cleanly on first attempt
- WizardContext/WizardShell infrastructure worked well for all pages
- Dashboard correctly showed aggregations
- Production deployment worked end-to-end

### User Feedback
- "The styling is completely shit" — theme CSS was missing, all colors were absent
- Applied theme CSS import fix, redeployed, styling now matches reference screenshots

### Applied Fixes
- [x] EXECUTE.md: Added step 7 (import theme.css) in Phase 1
- [x] EXECUTE.md: Added Unicode character rule + tsc fallback path in Critical Rules
- [x] Dynamic pricing �� implemented in run_20260411_1744
- [x] SegmentedControl/Checkbox playwright workaround — documented in run_20260411_1744

## Run: 2026-04-11 (tariff-wizard, prefix run_20260411_1744)

### Result: SUCCESS (clean, no post-deploy fixes needed)

### Phase Results
- Phase 0 (Setup): PASS — Supabase table created (switched to accessible project proactively), env vars set
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts (dynamic!), planData, wizard routing, theme CSS import, Toast SSR fix
- Phase 2 (Parallel): PASS — 8/8 agents succeeded, all tsc clean. One minor \u20AC fix in SummaryPage
- Phase 3 (Integration): PASS — Full wizard walkthrough with playwright-cli, submit to Supabase, dashboard shows submission
- Phase 4 (Deploy): PASS — Vercel deploy to https://demo-run-202604111744.vercel.app, production walkthrough with different data (Erika Musterfrau, Premium, 15k), both submissions visible on dashboard

### Improvements Applied from Previous Run
- [x] Theme CSS imported in globals.css from Phase 1 (no styling issues this time)
- [x] ToastProvider SSR crash prevented with mount guard
- [x] Dynamic pricing module created (pricing.ts) — prices react to age/coverage/plan
- [x] Used `npm rebuild` to fix broken .bin symlinks proactively

### Issues Found This Run

1. **SummaryPage used \u20AC escape** — Despite explicit Unicode rule in prompt, one agent still used `\u20AC`
   - ROOT_CAUSE: The rule was in the prompt but not emphatic enough
   - FIX: Add to each page agent prompt: "CRITICAL: Use € not \\u20AC, use ü not \\u00FC — JS unicode escapes render as literal text in JSX"

2. **Playwright can't click hidden checkbox/radio inputs** — SegmentedControl, RadioButton, and Checkbox components use CSS-hidden `<input>` elements. `getByRole('checkbox')` and `getByRole('radio')` resolve to the hidden input which Playwright can't click.
   - ROOT_CAUSE: Standard a11y pattern of visually hiding the native input
   - FIX: Document in agent-contracts.md Browser Tester section: "Click the parent `<label>` element (use snapshot refs for the cursor=pointer container), NOT the radio/checkbox role directly"

3. **Supabase project ID still wrong in base template** — Same issue as previous run
   - ROOT_CAUSE: .env.local in base template has inaccessible project ID
   - FIX: Update base template .env.local with accessible project (zdklkvkutlmhlclcgtek)

4. **dynamicAdjustment schema mismatch** — Ticket 01 foundation spec lists 3 values ("none" | "standard" | "custom") but SQL CHECK only allows 2 ("none" | "standard") and TariffFormData only uses 2
   - FIX: Update ticket 01 to specify only "none" | "standard"

### What Went Well
- All 8 parallel agents compiled on first attempt (zero tsc failures)
- Dynamic pricing makes the demo dramatically more impressive
- Theme CSS import worked perfectly (learned from previous run)
- Stepper, navigation, back-button data persistence all work
- Dashboard shows correct aggregations for multiple submissions
- Production deployment succeeded on first try

### User Feedback
- User approved, no issues reported

### User Feedback (post-run)

1. **Dashboard styling too basic** — The dashboard is functional but visually plain. Needs better visual hierarchy, card styling, spacing, and polish to match the quality of the wizard pages. Consider subtle gradients, better typography, hover states, and a more professional data visualization for the plan distribution.

2. **No form validations** — The wizard has zero validation:
   - Age validation missing: user can enter any birth year, but policy requires age 40-85
   - Personal data fields have no required-field validation (can submit empty name, address, etc.)
   - No inline error messages shown when fields are invalid
   - "weiter" button should be disabled or show errors when required fields are empty

3. **No wizard step tracking/analytics** — There's no way to know where users drop off in the funnel. Need a tracking approach that records which steps users reach and when, to analyze conversion and abandonment patterns.

### Applied Fixes
- [x] feedback-log.md: Added this entry
- [x] EXECUTE.md: Added playwright-cli label click workaround documentation
- [x] agent-contracts.md: Added Browser Tester note about clicking labels not inputs
- [x] Ticket 01: Fixed dynamicAdjustment to "none" | "standard" only
- [x] All page tickets: Reinforced Unicode character rule
- [x] next-demo-base/.env.local: Fixed Supabase project ID to accessible project
- [x] Dashboard styling improvements — ticket 11 written
- [x] Form validations (age 40-85, required fields) — ticket 12 written
- [x] Wizard step tracking/analytics — ticket 13 written (full architecture)
- [x] EXECUTE.md updated with new Phase 1 steps (pricing, validation, tracking, track API route)

## Run: 2026-04-11 (tariff-wizard, prefix run_20260411_1845)

### Result: SUCCESS (clean run, funnel dashboard added post-deploy)

### Phase Results
- Phase 0 (Setup): PASS — Both Supabase tables created on first try (insurance_applications + wizard_tracking_events)
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts, validation.ts, WizardTrackingProvider, /api/track, theme CSS, Toast SSR fix. tsc clean.
- Phase 2 (Parallel): PASS — 8/8 agents succeeded on first attempt, all tsc clean, no escalations
- Phase 3 (Integration): PASS — Full playwright-cli walkthrough, submit to Supabase, dashboard shows submission with correct stats
- Phase 4 (Deploy): PASS — Vercel deploy to https://demo-run-202604111845.vercel.app, production walkthrough with different data (Erika Musterfrau, Premium, 15k), both submissions visible

### Improvements Applied from Previous Runs
- [x] Theme CSS imported in globals.css from Phase 1
- [x] Toast SSR crash prevented with mount guard
- [x] Dynamic pricing module in foundation
- [x] Form validations: age 40-85 on BirthDatePage, required fields on PersonalDataPage
- [x] Wizard step tracking: WizardTrackingProvider + /api/track route
- [x] Dashboard styling: gradient header, stat cards with accents, plan badges, zebra striping

### Issues Found This Run

1. **Dashboard agent used HTML entities** — Despite the Unicode rule, the dashboard agent used `&uuml;`, `&Oslash;`, `\u20AC`, `\u2014` etc. in server component JSX
   - ROOT_CAUSE: Server components DO render HTML entities correctly (unlike client components), so this isn't a bug — but it's inconsistent with the rule
   - FIX: Reinforce in dashboard agent prompt: use actual Unicode even in server components for consistency

2. **Funnel analytics not built by dashboard agent** — Ticket 13 specified the tracking infrastructure but never told the dashboard agent to visualize it. Had to add funnel section manually after user noticed.
   - ROOT_CAUSE: Ticket 13 only described backend (provider + API route + table) but not the dashboard UI. Ticket 10 didn't reference ticket 13.
   - FIX: Added "Dashboard: Funnel Analytics Section" to ticket 13 with full spec. Updated ticket 10 to require reading ticket 13 and building the funnel. Dashboard agent now queries both tables.

3. **Worktree dirs accidentally committed** — `.claude/worktrees/` dirs were included in `git add -A`
   - ROOT_CAUSE: No .gitignore rule for worktree directories
   - FIX: Add `.claude/worktrees/` to .gitignore in setup-demo.sh

4. **Some agents used relative imports, others used @/ aliases** — Cosmetic inconsistency
   - ROOT_CAUSE: Agent prompts didn't specify import style
   - FIX: Add to agent spawn template: "Use @/ path aliases for all imports (e.g. @/lib/wizard/TariffContext, @/components/ui/Button/Button)"

### What Went Well
- All 8 parallel agents compiled on first attempt — zero failures or escalations
- Age validation working correctly (weiter disabled until valid age 40-85)
- Personal data required field validation with blur-triggered errors
- Dynamic pricing reactive to all inputs (age × coverage × plan)
- Playwright checkbox/radio label click workaround worked perfectly
- Production deployment succeeded first try
- Wizard step tracking events captured correctly (verified in Supabase)

### User Feedback
- "did you implement tracking?" — tracking infrastructure was built but no dashboard visualization
- "but you didn't build a dashboard for it?" — correct, ticket gap identified and fixed
- Applied funnel analytics section to dashboard, redeployed

### Applied Fixes
- [x] Ticket 13: Added "Dashboard: Funnel Analytics Section" with full UI spec for funnel visualization
- [x] Ticket 10: Updated to require reading ticket 13 and building funnel section, added funnel tester checks
- [x] Add `.claude/worktrees/` to .gitignore in setup-demo.sh
- [x] Add @/ import alias rule to agent spawn template in EXECUTE.md

## Run: 2026-04-11 (tariff-wizard, prefix run_20260411_1921)

### Result: SUCCESS (clean run, zero issues)

### Phase Results
- Phase 0 (Setup): PASS — Supabase tables created, .gitignore updated, theme CSS imported, Toast SSR fixed, npm rebuild
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts, validation.ts, WizardTrackingProvider, /api/track, wizard routing. tsc clean.
- Phase 2 (Parallel): PASS — 8/8 agents succeeded on first attempt, all tsc clean, zero escalations
- Phase 3 (Integration): PASS — Full wizard walkthrough with playwright-cli (headed). Submit to Supabase. Dashboard shows submission + funnel analytics.
- Phase 4 (Deploy): PASS — Vercel deploy to https://demo-run-202604111921.vercel.app. Production walkthrough with different data (Erika Musterfrau, Premium, 15k). Both submissions visible on dashboard.

### Improvements Applied from Previous Runs
- [x] All previous fixes applied proactively (theme CSS, Toast SSR, dynamic pricing, validations, tracking, funnel dashboard, Unicode rule, @/ imports, .gitignore worktrees)
- [x] npm rebuild done proactively in Phase 0 (fixed broken .bin symlinks before they could cause issues)
- [x] Excluded *.test.tsx from tsconfig (pre-existing Button.test.tsx was causing tsc failures)

### Issues Found This Run

1. **tsconfig.json doesn't exclude test files** — Pre-existing `Button.test.tsx` causes `tsc --noEmit` to fail with missing `@testing-library/react` types
   - ROOT_CAUSE: Base template includes a test file but doesn't have test deps or tsconfig exclusion
   - FIX: Added Step 5 to Phase 0 in EXECUTE.md: exclude `**/*.test.tsx` and `**/*.test.ts` from tsconfig

2. **Broken .bin symlinks** — `npx tsc` and `npx next` fail because `.bin` symlinks are stale after setup-demo.sh copies
   - ROOT_CAUSE: setup-demo.sh copies node_modules but symlinks point to wrong paths
   - FIX: Added `npm rebuild` as explicit Step 5 in Phase 0

### What Went Well
- Cleanest run yet — zero agent failures, zero post-deploy fixes needed
- All proactive fixes from previous runs paid off (no theme issues, no SSR crashes, no Unicode escapes)
- Dashboard funnel analytics rendered correctly with real tracking data
- Both production submissions verified with different personas
- Dynamic pricing correctly calculated for different ages (1982 vs 1975)

### User Feedback
- No issues reported. Clean run.

### Applied Fixes
- [x] EXECUTE.md: Added Step 5 to Phase 0 (npm rebuild + tsconfig test exclusion)

## Run: 2026-04-12 (tierkranken-v1, prefix run_20260412_1023)

### Result: SUCCESS (clean run, zero post-deploy fixes needed)

### Product: Tierkrankenversicherung (Pet Health Insurance)
### Pass: 1

### Phase Results
- Phase 0 (Setup): PASS — Supabase tables created (insurance_applications + wizard_tracking_events), .gitignore updated, theme CSS imported, Toast SSR fixed, npm rebuild, tsconfig test exclusion
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts with species multiplier, planData, validation.ts, WizardTrackingProvider, /api/track, /api/submit, all 6 page components, dashboard. tsc clean.
- Phase 2 (Parallel): N/A — built inline (no worktree agents for this run, single-agent execution)
- Phase 3 (Integration): PASS — Full playwright-cli walkthrough with dog data (Bello/Labrador/3/Komfort/5k). Submit to Supabase. Dashboard shows submission + funnel.
- Phase 4 (Deploy): PASS — GitHub repo created (teclead-ventures/tierkranken-v1), Vercel deploy to https://tierkranken-v1.vercel.app. Production walkthrough with cat data (Luna/Maine Coon/5/Premium/3k). Both submissions visible on dashboard.

### Pricing Calibration
- Dog age 3, 5k budget, Komfort: 35,00 EUR/month (matches calibration target)
- Cat age 5, 3k budget, Komfort: 19,38 EUR/month (0.75x species multiplier applied correctly)
- Cat age 5, 3k budget, Premium: 23,85 EUR/month (correct tier differentiation)

### Key Observations
1. **Species multiplier works correctly** — Katze prices are 75% of Hund prices as expected
2. **Conditional chip recommendation** shows when chipNumber is empty (Luna test), hidden when filled (Bello test)
3. **Dynamic breed lists** switch correctly between Hund and Katze breeds
4. **6 pages (no dynamic adjustment)** is the correct count for tierkranken — no 7th page needed
5. **Funnel analytics** show 2 sessions started, 2 completed, 100% rate with per-step dwell times
6. **All German text** renders correctly with actual Unicode (Schäferhund, Französische, München, etc.)

### What Went Well
- Zero TypeScript errors throughout the entire build
- All learnings from previous runs applied proactively (theme CSS, Toast SSR, npm rebuild, tsconfig, Unicode, @/ imports)
- Dynamic pricing reactive to species, age, coverage, and plan
- Dashboard includes both submission stats AND wizard funnel analytics
- Full tier comparison table in "Alle Leistungen" section
- Conditional recommendation note on summary page adds product-specific value
- Production deployment succeeded on first try with all env vars
- Both test personas (Bello/Hund + Luna/Katze) visible on production dashboard

### Tierkranken-Specific Learnings
- Pet age range 0-10 is much narrower than person products, but the quadratic age curve (0.90) creates meaningful price differentiation
- Breed selection needs dynamic filtering per animal type — reset breed on type switch
- "laufend" (ongoing) payment display for pet insurance vs year-count for person products
- Dashboard columns (Tiername, Tierart) are product-specific — not just Name/Tarif

## Run: 2026-04-12 (haftpflicht-v2, prefix run_20260412_1145)

### Result: SUCCESS (clean run, zero post-deploy fixes needed)

### Product: Privathaftpflichtversicherung (Personal Liability Insurance)
### Pass: 2 (improvement build)

### Phase Results
- Phase 0 (Setup): PASS — Supabase tables created, npm rebuild, tsconfig test exclusion, theme CSS imported, Toast SSR fixed
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts (flat-rate), planData with deductibleAmount, WizardTrackingProvider, /api/track. tsc clean.
- Phase 2 (Pages): PASS — All 5 wizard pages built inline with v2 improvements. tsc clean.
- Phase 3 (Integration): PASS — Full playwright-cli walkthrough with both test data sets. Supabase submissions verified. Dashboard shows funnel + submissions.
- Phase 4 (Deploy): PASS — GitHub repo (teclead-ventures/haftpflicht-v2), Vercel deploy to https://haftpflicht-v2.vercel.app. Production walkthrough with both personas, all 4 submissions visible.

### v2 Improvements Applied
1. **Coverage slider "Mio. €" format** — Slider labels show "1 Mio. €" / "50 Mio. €", value display shows "10 Mio. €" not "10000000"
2. **Selbstbeteiligung prominence** — Prominent colored badges on plan selection: green "Keine Selbstbeteiligung" for Komfort/Premium, orange "Selbstbeteiligung: 150 €" for Grundschutz
3. **Real-world haftpflicht scenarios** — 3 examples below coverage slider: laptop damage, key loss, parquet scratch
4. **Family status detailed descriptions** — Description card changes dynamically: "Einzelperson", "Familienschutz", "Alleinerziehend" with detailed text
5. **Summary Selbstbeteiligung badge** — Green/orange badge replicated on summary page for at-a-glance confirmation

### Pricing Calibration
- Single, Komfort: 6,00 EUR/month (matches calibration target: 5.00 * 1.0 * 1.20 = 6.00)
- Familie, Premium: 9,96 EUR/month (6.15 * 1.35 * 1.20 = 9.963 → 9,96)
- Familie, Komfort: 8,10 EUR/month (5.00 * 1.35 * 1.20 = 8.10)

### What Went Well
- Zero TypeScript errors, zero post-deploy fixes needed
- All proactive learnings from previous runs applied (theme CSS, Toast SSR, npm rebuild, tsconfig, Unicode, @/ imports)
- v1 code provided excellent foundation — v2 improvements were surgical and targeted
- Selbstbeteiligung badges are visually prominent and change instantly when switching plans
- Real-world scenarios make the product tangible and relatable
- Family status descriptions provide clear guidance for each selection
- Flat-rate pricing correctly ignores coverage amount (only family status + plan tier matter)
- Production deployment succeeded on first try with all env vars
- Both test personas verified on production dashboard

### v2-Specific Learnings
- Having v1 as reference makes Pass 2 dramatically faster — mostly targeted improvements
- planData.deductibleAmount (numeric) is cleaner than parsing the string for badge logic
- Coverage display format ("Mio. €") should be the default for products with million-range values
- Selbstbeteiligung is a strong differentiator and deserves visual prominence in plan comparison

## Run: 2026-04-12 (kfz-v2, prefix run_20260412_1416)

### Result: SUCCESS (clean run, zero post-deploy fixes needed)

### Product: Kfz-Versicherung (Motor Insurance)
### Pass: 2 (improvement build)

### Phase Results
- Phase 0 (Setup): PASS — Supabase tables created (insurance_applications + wizard_tracking_events), .gitignore updated, theme CSS imported, Toast SSR fixed, npm rebuild, tsconfig test exclusion
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts with SF-Klasse multipliers + age U-curve, planData with sublabels/deductibles, validation.ts, WizardTrackingProvider, /api/track, all 6 page components, dashboard. tsc clean.
- Phase 2 (Pages): PASS — All 6 wizard pages built inline (single-agent execution). tsc clean.
- Phase 3 (Integration): PASS — Full playwright-cli walkthrough (headed) with test data set 1 (Max Mustermann, Mittelklasse, SF 10, Komfort). Submit to Supabase. Dashboard shows submission + funnel.
- Phase 4 (Deploy): PASS — GitHub repo (teclead-ventures/kfz-v2), Vercel deploy to https://kfz-v2.vercel.app. Production walkthrough with test data set 2 (Erika Musterfrau, SUV, SF 20, Premium). Both submissions visible on production dashboard.

### v2 Improvements Applied
1. **SF-Klasse discount clarity** — Full SF scale with 9 color-coded levels (red surcharge, gray reference, green discount). Current SF badge updates dynamically. All percentages match spec.
2. **Haftpflicht/Teilkasko/Vollkasko distinction** — SegmentedControl labels show "Grundschutz (Haftpflicht)", "Komfort (+ Teilkasko)", "Premium (+ Vollkasko)". Subtitle explains mandatory vs optional coverage.
3. **SB badges** — Prominent colored badges: Grundschutz "Keine SB (nur Haftpflicht)" blue, Komfort "SB: 150 €" orange, Premium "Keine SB" green. Visible on both PlanSelection and Summary pages.
4. **Young driver surcharge explanation** — Age-based Alert after birth date entry: <25 orange warning, 25-40 green note, >40 no note. Tested with age 35 (green) and age 50 (none).
5. **Vehicle type context** — Alert shows Typklasse info after selecting vehicle type. Tested with Mittelklasse (14-18) and SUV (18-23).

### Pricing Calibration
- 35yo, SF 10, Komfort: 65,00 EUR/month (matches calibration target exactly)
- 50yo, SF 20, Premium: 50,04 EUR/month (correct: lower due to 30% SF discount)
- U-curve verified: young drivers pay more, mid-age cheapest, slight rise for elderly

### What Went Well
- Zero TypeScript errors throughout the entire build
- All proactive learnings applied (theme CSS, Toast SSR, npm rebuild, tsconfig, Unicode, @/ imports)
- All 5 v2 improvements implemented correctly and verified with playwright-cli
- Dynamic pricing with SF multiplier interpolation works smoothly
- Production deployment succeeded on first try with all env vars
- Both test personas visible on production dashboard with correct data
- SF discount scale provides clear transparency to the user
- Comparison table in plan selection shows all benefits side by side

### Kfz-Specific Learnings
- SF-Klasse slider needs explicit number input (spinbutton) for precise selection
- U-curve age factor works well for Kfz — young drivers see meaningful surcharges
- Flat-rate pricing (coverageUnit=1) simplifies the pricing display vs coverage-based products
- Vehicle type → Typklasse info is purely informational but adds domain credibility
- SB badges are the strongest visual differentiator between plan tiers for motor insurance

## Run: 2026-04-12 (berufsunfaehigkeit-v1, prefix run_20260412_1448)

### Result: SUCCESS (clean run, zero post-deploy fixes needed)

### Product: Berufsunfähigkeitsversicherung (Disability Insurance / BU)
### Pass: 1

### Phase Results
- Phase 0 (Setup): PASS — Supabase tables created (insurance_applications + wizard_tracking_events), .gitignore updated, theme CSS imported, Toast SSR fixed, npm rebuild, tsconfig test exclusion
- Phase 1 (Foundation): PASS — TariffContext, pricing.ts with occupation risk multiplier, planData with 3 tiers, validation.ts, WizardTrackingProvider, /api/track, /api/submit, wizard routing. tsc clean.
- Phase 2 (Pages): PASS — All 7 wizard pages built inline (single-agent execution). tsc clean. All pages: Occupation, BirthDate, IncomeCoverage, PlanSelection, HealthQuestions, PersonalData, Summary. Plus Dashboard with funnel.
- Phase 3 (Integration): PASS — Full playwright-cli walkthrough with test data set 1 (Max Mustermann, Bürotätigkeit, Komfort, 2k). Submit to Supabase. Dashboard shows submission + funnel.
- Phase 4 (Deploy): PASS — GitHub repo (teclead-ventures/berufsunfaehigkeit-v1), Vercel deploy to https://berufsunfaehigkeit-v1.vercel.app. Production walkthrough with test data set 2 (Erika Musterfrau, Handwerk, Premium, 1.5k). Both submissions visible on production dashboard.

### Pricing Calibration
- 30yo, Bürotätigkeit (1.0x), 2k coverage, Komfort: 55,04 EUR/month (matches calibration target ~55/month)
- 46yo, Handwerk (1.4x), 1.5k coverage, Premium: higher price as expected (older + risk class + premium tier)

### Key Observations
1. **75% income cap works correctly** — Slider max updates dynamically when income changes, coverage auto-adjusts
2. **Occupation risk badges** provide clear visual feedback of risk class impact with color coding
3. **4 summary sections** (Tarifdaten, Tarif, Gesundheit, Persönliche Daten) with edit links work correctly
4. **Waiting period badges** change per plan tier (6mo/3mo/none) with color differentiation
5. **Tier comparison table** expandable with checkmarks/dashes per benefit per tier
6. **Dynamic pricing** reacts to age, coverage, occupation, and plan in real-time
7. **Funnel analytics** show per-step dwell times and completion rate on dashboard
8. **All German text** renders correctly with actual Unicode (Bürotätigkeit, Berufsunfähigkeit, München, etc.)

### What Went Well
- Zero TypeScript errors throughout the entire build
- All proactive learnings from previous runs applied (theme CSS, Toast SSR, npm rebuild, tsconfig, Unicode, @/ imports)
- 75% income cap is the standout BU-specific feature — updates slider max dynamically
- Risk class badges with color coding add domain credibility
- Pricing calibration accurate (55,04 EUR for reference customer)
- Production deployment succeeded on first try with all env vars
- Both test personas visible on production dashboard with correct data

### BU-Specific Learnings
- Occupation risk class multiplier is the primary price differentiator (more so than age for BU)
- 75% income cap requires careful UX — must show the rule prominently AND auto-adjust
- Health questions simplified to 2 yes/no — this is realistic for a demo but a real BU app needs extensive underwriting
- No dynamic adjustment page needed (unlike Sterbegeld) — 7 pages not 8
- Separate health questions section in summary adds transparency

### Applied Fixes
- [x] All previous run fixes applied proactively

## Run: 2026-04-12 (ergo-researcher, Zahnzusatz — Mode A single-product iteration)

### Result: SUCCESS

### Self-Assessment

**Metrics**:
- Duration: ~45 min
- Products researched: 1 (Zahnzusatz)
- Data points: 28 (10 calculator-verified, 18 from Beitragstabelle)
- Pricing accuracy: 100% match between calculator and official Beitragstabelle
- R² (polynomial fit to band midpoints): 0.9974

**What worked**:
- Beitragstabelle shortcut: The ergo.de product page has a "Zur Beitragstabelle" button that opens a dialog with all tariff prices by age band — this is far more efficient than scraping the calculator for each data point
- Verification approach: Using the calculator to spot-check 10 data points against the Beitragstabelle confirmed 100% accuracy
- Full wizard flow: Navigating through all steps (initial-selection → birth date → weiter → insurance-beginning) to reach the price display

**What failed**:
- Initial scraping approach tried to extract price after birth date entry without clicking "weiter" — missed the critical step that advances to the price display page — ROOT CAUSE: SPA wizard doesn't show price until you navigate past the birth date step — SEVERITY: high (wasted ~10 min)
- Background run-code script for bulk collection failed silently when browser session was closed — ROOT CAUSE: closing browser terminates the script without error capture — SEVERITY: low (Beitragstabelle shortcut made this unnecessary)
- `#ppzApp` selector needed instead of `main` — two main elements on page — ROOT CAUSE: ERGO wraps calculator in nested main elements — SEVERITY: low

**Improvements applied**:
- [x] products.md: Complete rewrite of Zahnzusatz entry (flat rate, no coverage slider, age bands, correct tiers, no waiting period)
- [x] pricing-model.md: Updated age curve table, added Zahnzusatz to flat-rate products, added age-band pricing documentation, updated calibration table
- [x] ergo-product-urls.md: Marked Zahnzusatz as CONFIRMED with specific calculator URLs
- [x] ticket-templates.md: Updated Zahnzusatz wizardSteps to match real ERGO flow

### Key Structural Findings
1. ERGO Zahnzusatz is a FLAT-RATE product — no coverage slider at all
2. Tariff tiers are reimbursement percentages (DS75/DS90/DS100), not benefit tiers
3. Pricing uses 6 discrete age bands, not a continuous polynomial
4. No waiting period, no dental status field, no missing teeth field
5. First 6 months at 50% premium (Startbeitrag)
6. Our previous model was off by +429% at age 20 and −40% at age 60

### User Feedback
- "yes update everything so the implementation plan is closer to reality of ergo"
- Applied all changes to products.md, pricing-model.md, ticket-templates.md, ergo-product-urls.md

### Impact on next run
- Always check Beitragstabelle first before scraping calculator
- Navigate through ALL wizard steps to reach price display
- Use `#ppzApp` selector for ERGO calculator content extraction
- Expect structural differences from our assumptions — ERGO products may not match our model architecture

## Run: 2026-04-13 (ergo-researcher, Batch: Sterbegeld + Risikoleben + Hausrat — Mode B-lite parallel)

### Result: SUCCESS (all 3 products)

### Self-Assessment

**Metrics**:
- Duration: ~87 min total (3 agents in parallel)
- Products researched: 3 (Sterbegeld, Risikoleben, Hausrat)
- Data points: 258 total (160 + 75 + 23)
- Agent durations: Sterbegeld ~87min, Risikoleben ~52min, Hausrat ~42min
- Coverage linearity R²: Sterbegeld 0.978-0.997, Hausrat 0.998
- Age curve fit: Sterbegeld cubic R²=0.990-0.997, Risikoleben cubic R²=0.995
- Confidence: HIGH for all 3 products

**What worked**:
- **Parallel execution**: All 3 agents ran concurrently in worktrees with separate playwright sessions (-s=sterbegeld, -s=risikoleben, -s=hausrat). No session conflicts.
- **Zahnzusatz learnings applied**: Full wizard navigation, cookie dismissal, and 5-second wait patterns all worked across all 3 products. The methodology transfer was smooth.
- **Data quality**: 258 data points total with high R² values. Each agent systematically varied the relevant dimensions.
- **Structural discovery**: Each product revealed structural differences from our assumptions — the research is producing genuinely new information, not just validating prices.

**What failed / was suboptimal**:
- **No Beitragstabelle found** for any of the 3 products — the Zahnzusatz shortcut was unique to that product. All 3 required full calculator scraping. — ROOT CAUSE: Beitragstabelle appears to be a Zahnzusatz-specific feature, not a common pattern — SEVERITY: low (methodology still worked, just slower)
- **Sterbegeld agent was slowest** (87 min vs 42-52 min for others) — it collected the most data points (160) by varying many coverage amounts. — ROOT CAUSE: Sampled too many coverage variations for a product where coverage scaling is linear — SEVERITY: low (data quality is great, but 50 points would have been sufficient)
- **Hausrat had fewest data points** (23) but the model is well-determined because the pricing dimensions (m², region, floor, building type, age) are mostly independent multipliers — SEVERITY: none (23 is enough for this model type)
- **Risikoleben quadratic R²=0.958** — confirms the polynomial model is inadequate for exponential mortality curves. Cubic R²=0.995 is better but lookup table is the right approach. — ROOT CAUSE: Our pricing-model.md assumes all products use a quadratic age curve — SEVERITY: high (Risikoleben needs a lookup table, not polynomial)

**Improvements applied**:
- [x] products.md: Sterbegeld — corrected payment duration (90−age), coverage step (€500), default (€7k), base rates (age-dependent lookup table), Aufbauzeit per tier, fixed fee component
- [x] products.md: Risikoleben — complete rewrite with lookup table, 3 smoker classes, age-dependent smoker multipliers, employment/occupation fields, add-ons, term scaling
- [x] products.md: Hausrat — complete rewrite: 2 tiers (Smart/Best), additive tier model, per-m² pricing, ZIP-specific regional multipliers, floor/building type factors, under-36 Startbonus, add-on modules
- [x] pricing-model.md: Added lookup table pricing section, additive tier model section, per-m² coverage model section. Updated age curve table and calibration table for all 3 products.
- [x] ergo-product-urls.md: All 3 URLs confirmed with calculator details

### Comparison: Our Assumptions vs ERGO Reality

| Product | Our calibration | ERGO actual | Delta | Key structural difference |
|---------|----------------|-------------|-------|--------------------------|
| Sterbegeld | €30/mo (44yo, 8k, Komfort) | €27.45/mo | −8.5% | Payment 90−age (not 85), coverage step €500, age-dependent tier multipliers |
| Risikoleben | €12/mo (35yo, NS, 200k, Komfort) | €9.54/mo | −20% | Exponential age curve, 3 smoker classes, age-dependent smoker multiplier 1.87-3.92× |
| Hausrat | €8/mo (50k, Zone 3, Komfort) | €12.40 (80m², München, Best) | Model mismatch | Only 2 tiers, additive not multiplicative, per-m² pricing, ZIP-specific |

### Questions for the user
1. Risikoleben needs a lookup table — our polynomial formula can't model it. Should we extend pricing.ts with a lookup table interpolation function?
2. Hausrat has only 2 tiers. Should we keep our 3-tier demo structure (adding a synthetic Premium) or match ERGO's 2-tier model?
3. The additive tier model for Hausrat (Best = Smart + €3.39 fixed) is fundamentally different from our multiplicative model. Should we add a separate pricing function for property products?

### User Feedback
- Risikoleben: approved lookup table approach (Template B)
- Hausrat: approved 2-tier model, no synthetic Premium
- Property pricing: approved separate Template C for additive tier models

### Applied Improvements (post-user-feedback)
- [x] pricing-model.md: 3 pricing templates (A=polynomial, B=lookup, C=property) with full TypeScript implementations
- [x] pricing-model.md: Risikoleben lookup table with age-dependent smoker multipliers and term scaling
- [x] pricing-model.md: Hausrat Template C with additive tiers, per-m² rate, ZIP/floor/building/age factors
- [x] SKILL.md: Added "Accumulated learnings" section with 7 structural patterns and pricing model selection guide
- [x] SKILL.md: Updated timing estimates from actual batch run data
- [x] SKILL.md: Rate limiting updated — 3 concurrent sessions worked fine, no cross-session coordination needed
- [x] researcher-prompt.md: Phase C now does multi-model fitting (quadratic/cubic/exponential/piecewise), checks tier relationship type, tests risk multiplier age-dependency, checks for fixed fees
- [x] product-schema.md: Updated for 2-tier products, 3 pricing templates, expanded validation checklist
- [x] ergo-product-urls.md: 3 URLs confirmed with calculator details

### Impact on next run
- Beitragstabelle is Zahnzusatz-specific — still check (10-second effort), but plan for calculator scraping
- For products with exponential age curves (potentially Pflege), plan for lookup table (Template B) from the start
- Property products (Wohngebäude) may use additive tier models and per-m² pricing like Hausrat — verify with Template C
- Check for fixed fee components in every product (Sterbegeld had ~€1.80/month)
- Check if risk class multipliers are age-dependent (Risikoleben smoker was 1.87-3.92×)
- 50 data points is enough for most products; property products need ~25 with ZIP/factor variations
- fit_pricing.py should always try multiple models and auto-select based on R²

### Next batch proposal
**Batch 3: Rechtsschutz, Unfall, Pflegezusatz**

| Product | Why this order | Expected model | Key question |
|---------|---------------|----------------|-------------|
| Rechtsschutz | Liability product, likely flat age curve + fixed pricing. Should be straightforward (Template A). Good to confirm our Rechtsschutz assumptions quickly. | Template A (polynomial, mild age curve) | Does it have legal area checkboxes that affect pricing? |
| Unfall | Person product with moderate age curve. Tests whether our 0.85/0.10/0.15 age curve is accurate. Also has occupation risk classes — test if multipliers are constant or age-dependent. | Template A (likely) or B (if steep) | Are occupation multipliers age-dependent like Risikoleben smoker? |
| Pflegezusatz | Steep age curve (0.50/0.25/0.65) — may need Template B like Risikoleben. Important to test because care insurance pricing is notoriously complex. | Template A or B | Is the age curve polynomial or does it need a lookup table? |

**Methodology adjustments for batch 3:**
- Each agent's fit_pricing.py should try quadratic, cubic, exponential, AND piecewise from the start
- Check tier relationship type (multiplicative vs additive) for every product
- Sample risk class multipliers at 3+ ages to detect age-dependency early
- Target 50 data points per product (not 160)
