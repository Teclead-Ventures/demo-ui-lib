# Agent Contracts: Subagent Role Definitions

This document defines the exact communication contracts for all subagent roles used in the per-page feedback loop. Every page agent follows the same pipeline:

```
Page Agent (developer) → Reviewer Subagent → Page Agent fixes → Tester Subagent → Page Agent fixes → Loop
```

The page agent itself IS the developer. It retains full context across loop iterations. Reviewer and Tester are spawned as fresh subagents each time to ensure generator-evaluator separation.

---

## Role: Page Developer (the page agent itself)

**Purpose**: Implement a single wizard page component matching the ticket spec and reference screenshot.

**This is NOT a subagent** — it's the page agent itself. It:
- Reads its ticket file for full specifications
- Reads the reference screenshot for visual target
- Reads foundation code (context, wizard shell) for integration
- Writes the page component and any supporting files
- Orchestrates the review/test loop by spawning subagents
- Fixes issues reported by Reviewer and Tester

**Model**: opus

**File ownership**: Each page agent owns ONLY the files listed in its ticket. It must NOT modify:
- `src/app/wizard/page.tsx` (orchestrator assembles this in Phase 3)
- `src/lib/wizard/` (shared foundation)
- Any other page's files

**Loop orchestration logic**:
```
MAX_ITERATIONS = 3

for iteration in 1..MAX_ITERATIONS:
  1. Write/fix the page component code
  2. Run: npx tsc --noEmit (must pass before spawning reviewer)
  3. Spawn Reviewer subagent with code context
  4. If Reviewer returns STATUS: FAIL
     → Read CRITICAL issues, fix them, continue loop
  5. Spawn Tester subagent
  6. If Tester returns GATE_RESULT: FAIL
     → Read BLOCKING_ISSUES, fix them, continue loop
  7. If both PASS → break loop, report success

if still failing after MAX_ITERATIONS:
  → Report to orchestrator: ESCALATE with summary of persistent failures
```

---

## Role: Code Reviewer

**Purpose**: Review page component code for correctness, pattern adherence, and visual fidelity to reference screenshot.

**Context provided by page agent in spawn prompt**:
- The ticket file content (full spec)
- The reference screenshot path (agent should read it)
- The implemented file paths and their contents
- The foundation code paths (WizardContext, WizardShell, etc.)
- Which iteration this is and what was fixed since last review (if iteration > 1)

**Reads before starting**:
- The page component file(s)
- The reference screenshot (if available)
- The wizard context/state for correct field names
- The relevant UI component source in `src/components/ui/` (to verify correct API usage)

**Returns** (EXACTLY this format):
```
STATUS: PASS | FAIL

CHECKS:
[PASS] TypeScript compiles without errors
[PASS|FAIL] Component uses correct props from UI library API
[PASS|FAIL] State reads/writes use correct context fields and dispatch actions
[PASS|FAIL] Navigation (weiter/Zurück) targets correct step/subStep
[PASS|FAIL] German text matches reference screenshot exactly
[PASS|FAIL] Layout structure matches reference (element order, grouping, spacing)
[PASS|FAIL] All interactive elements are wired (onChange, onClick handlers)
[PASS|FAIL] No hardcoded values that should come from context
[PASS|FAIL] Accessibility basics (labels, aria attributes on interactive elements)

CRITICAL:
- <issue description> (file:line) — <why this must be fixed>
- ... (or "none")

WARNINGS:
- <issue description> (file:line) — <suggested improvement>
- ... (or "none")

VISUAL_FIDELITY: HIGH | MEDIUM | LOW | N/A
VISUAL_NOTES: <specific deviations from reference screenshot, or "matches well", or "no reference available">

CONFIDENCE: high | medium | low
```

**Fallback rule**: If the subagent returns a response that does not contain `STATUS: PASS` or `STATUS: FAIL`, treat it as `STATUS: FAIL` with CRITICAL: "Reviewer returned malformed response".

**Tools needed**: Read, Grep, Glob
**Model**: opus

**Done when**: All CHECKS evaluated, STATUS determined, structured result returned.

**Escalation**: If unable to read files or reference screenshot, return STATUS: BLOCKED with explanation.

---

## Role: Browser Tester (playwright-cli)

**Purpose**: Validate the page component by using the `playwright-cli` skill to interact with the live dev server in a headed browser visible on the user's desktop. Clicks through the wizard, fills forms, takes screenshots, and compares against reference.

**IMPORTANT**: This role uses the `playwright-cli` skill for browser interaction — NOT Playwright test files. The browser must be visible on the desktop (use `--headed` flag).

**Context provided by page agent in spawn prompt**:
- The ticket file content (navigation sequence + page-specific checks)
- The reference screenshot path
- The page's position in the wizard (which step/subStep)
- The dev server URL and port
- Which iteration this is and what was fixed since last test (if iteration > 1)

**Reads before starting**:
- The ticket file (for navigation sequence and check list)
- The page component file (to understand element structure for selectors)

**CRITICAL: Hidden input workaround**: UI components (Checkbox, RadioButton, SegmentedControl, InlineRadio) use CSS visually-hidden `<input>` elements. `getByRole('checkbox')` and `getByRole('radio')` resolve to the hidden input, which Playwright cannot click. Instead, click the parent `<label>` container — in snapshot output, look for the element with `[cursor=pointer]` that contains the checkbox/radio. Example: `playwright-cli click e178` (the label ref), NOT `playwright-cli click "getByRole('checkbox', { name: '...' })"`.

**Actions using playwright-cli**:
```bash
# 1. Open headed browser
playwright-cli open http://localhost:3000/wizard --headed

# 2. Take initial snapshot to understand page structure
playwright-cli snapshot

# 3. Navigate through wizard to reach target page
#    (follow the "Tester: Navigation Sequence" from the ticket)
#    Example: fill birth date, click weiter, etc.
playwright-cli fill <ref> "23"        # fill day field
playwright-cli fill <ref> "06"        # fill month field
playwright-cli fill <ref> "1982"      # fill year field
playwright-cli click <ref>            # click "weiter"

# 4. At target page: snapshot and verify elements
playwright-cli snapshot

# 5. Test interactions per the ticket's Page-Specific Checks
playwright-cli click <ref>            # test buttons
playwright-cli fill <ref> "value"     # test inputs
playwright-cli select <ref> "option"  # test dropdowns

# 6. Screenshot for visual comparison
playwright-cli screenshot --filename=<page-name>.png

# 7. Test navigation (forward + back)
playwright-cli click <weiter-ref>     # test forward
playwright-cli snapshot               # verify next page reached
playwright-cli click <zurück-ref>     # test back

# 8. Close browser
playwright-cli close
```

**Returns** (EXACTLY this format):
```
GATE: browser-validation
GATE_RESULT: PASS | FAIL

CHECKS:
[PASS|FAIL] Dev server accessible at expected URL
[PASS|FAIL] Page is reachable via wizard navigation (step X, subStep Y)
[PASS|FAIL] Heading text matches spec
[PASS|FAIL] All form elements render and are interactive
[PASS|FAIL] Forward navigation ("weiter") works correctly
[PASS|FAIL] Back navigation ("Zurück") works correctly (if applicable)
[PASS|FAIL] Form data persists in context (visible when navigating back)
[PASS|FAIL] No console errors or warnings
[PASS|FAIL] Visual layout matches reference screenshot

PASSED: X/Y
FAILED: X/Y

SCREENSHOT: <path to captured screenshot>

BLOCKING_ISSUES:
- <description> — <what the developer needs to fix>
- ... (or "none")

NON_BLOCKING:
- <minor visual differences, polish items>
- ... (or "none")

VISUAL_COMPARISON:
- Reference: <reference screenshot path, or "N/A">
- Actual: <captured screenshot path>
- Assessment: MATCH | CLOSE | DIVERGENT | N/A
- Differences: <specific differences noted, or "none significant">
```

**Fallback rule**: If the subagent returns a response that does not contain `GATE_RESULT: PASS` or `GATE_RESULT: FAIL`, treat it as `GATE_RESULT: FAIL` with BLOCKING_ISSUES: "Tester returned malformed response".

**Tools needed**: Bash (for playwright-cli commands), Read, Glob
**Model**: opus

**Done when**: All checks evaluated, screenshot captured, GATE_RESULT determined, browser closed.

**Escalation**: 
- If dev server won't start: return GATE_RESULT: BLOCKED
- If playwright-cli not available: return GATE_RESULT: BLOCKED
- If page is unreachable after correct navigation sequence: return GATE_RESULT: FAIL with details

---

## Role: Dashboard Developer (Phase 2, Agent H)

**Purpose**: Build the dashboard page that displays submitted insurance applications from Supabase with summary analytics.

**This is a page agent like the others** but builds `src/app/dashboard/page.tsx` instead of a wizard page.

**Owns files**:
- `src/app/dashboard/page.tsx`
- `src/app/dashboard/layout.tsx` (if needed)

**Follows the same loop**: develop → reviewer → tester (playwright-cli).

**Tester Navigation**: Simply navigates to `http://localhost:3000/dashboard` — no wizard steps needed.

---

## Role: Integration Verifier (Phase 3)

**Purpose**: After all page agents complete, verify the complete wizard + dashboard work end-to-end using playwright-cli in headed mode. This is the "live demo moment" — the audience sees Claude clicking through the entire application.

**Context provided by orchestrator**:
- List of all page files that were created
- The wizard state shape and step mapping
- The dev server URL
- The Supabase table name

**Actions using playwright-cli**:
```bash
# 1. Open headed browser
playwright-cli open http://localhost:3000/wizard --headed

# 2. Fill out the entire wizard form with realistic data
#    Navigate through all 7 pages, filling in:
#    - Birth date: 23.06.1982
#    - Insurance start: middle option
#    - Coverage: 8.000 €
#    - Plan: Komfort
#    - Dynamic: accept
#    - Personal: Max Mustermann, Musterstr. 1, 10115 Berlin
#    - Summary: check both checkboxes, submit

# 3. Verify success toast appears

# 4. Navigate to dashboard
playwright-cli goto http://localhost:3000/dashboard

# 5. Verify the submission appears in the table
playwright-cli snapshot
# Check that "Max Mustermann" or "Komfort" appears in the table

# 6. Screenshot the dashboard
playwright-cli screenshot --filename=integration-dashboard.png

# 7. Close browser
playwright-cli close
```

**Returns**:
```
GATE: integration
GATE_RESULT: PASS | FAIL

PHASE_CHECKS:
[PASS|FAIL] TypeScript compiles (zero errors)
[PASS|FAIL] Dev server starts clean (no console errors)
[PASS|FAIL] All 7 wizard pages render without errors
[PASS|FAIL] Forward navigation works through entire flow
[PASS|FAIL] Back navigation preserves entered data
[PASS|FAIL] Summary page displays all entered data correctly
[PASS|FAIL] Form submission succeeds (API returns 200)
[PASS|FAIL] Submission appears on dashboard
[PASS|FAIL] Dashboard stats update correctly
[PASS|FAIL] Stepper indicator correct at every step

PASSED: X/10
FAILED: X/10

BLOCKING_ISSUES:
- <issue> — <file:line> — <fix needed>

FULL_FLOW_SCREENSHOTS:
- wizard-complete.png
- dashboard-with-submission.png
```

**Tools needed**: Bash (playwright-cli), Read, Glob, Grep
**Model**: opus

**Done when**: Full flow tested, submission verified on dashboard, GATE_RESULT determined.

---

## Role: Production Verifier (Phase 4)

**Purpose**: After Vercel deployment, verify the production URL works end-to-end using playwright-cli.

**Actions**: Same as Integration Verifier but targeting the production URL instead of localhost.

**Returns**: Same format as Integration Verifier with `GATE: production` instead.
