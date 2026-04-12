# Quality Gates: Per-Page and Integration

## Gate Composition

Each page goes through this gate sequence:

```
compile-gate → review-gate → browser-gate (playwright-cli) → (loop if FAIL) → merge-ready
```

After all pages merge:

```
integration-gate (playwright-cli, headed) → deploy-gate → production-gate (playwright-cli, headed) → done
```

---

## Gate: Compilation (Pre-Review)

```
GATE: compilation
WHEN: Before spawning Reviewer subagent
RUN: npx tsc --noEmit
PASS_CRITERIA: Exit code 0, zero TypeScript errors
BLOCKS: review-gate (never send uncompilable code to reviewer)
RETRY: Fix type errors inline, re-run
ESCALATE_AFTER: 3 failures — report to orchestrator with error log
```

---

## Gate: Code Review

```
GATE: code-review
WHEN: After compilation passes
RUN: Spawn Reviewer subagent (see agent-contracts.md → Code Reviewer)
PASS_CRITERIA: Reviewer returns STATUS: PASS
BLOCKS: browser-gate
RETRY_ON_FAIL:
  1. Read CRITICAL issues from reviewer response
  2. Fix each issue in the code
  3. Re-run compilation gate
  4. Re-spawn Reviewer with updated code + note of what was fixed
ESCALATE_AFTER: 3 FAIL results — report persistent review issues to orchestrator
MALFORMED_RESPONSE: If subagent returns neither PASS nor FAIL, treat as FAIL
CRITICAL_RULE: Never spawn the same agent instance for review — always a fresh subagent
```

---

## Gate: Browser Validation (playwright-cli)

```
GATE: browser-validation
WHEN: After code review passes
RUN: Spawn Tester subagent that uses playwright-cli skill (see agent-contracts.md → Browser Tester)
PASS_CRITERIA: Tester returns GATE_RESULT: PASS
BLOCKS: merge-ready status
IMPORTANT: Browser must be headed (--headed flag) so it's visible on desktop
RETRY_ON_FAIL:
  1. Read BLOCKING_ISSUES from tester response
  2. Fix each issue in the code
  3. Re-run compilation gate
  4. Re-spawn Reviewer with updated code (catches regressions from the fix)
  5. Re-spawn Tester with updated code + note of what was fixed
ESCALATE_AFTER: 3 FAIL results — report with screenshots and test output
MALFORMED_RESPONSE: If subagent returns neither PASS nor FAIL, treat as FAIL
CRITICAL_RULE: Tester must use playwright-cli commands, NOT write Playwright test files
```

---

## Gate: Integration (Phase 3)

```
GATE: integration
WHEN: After all page files are merged into the project
RUN: Spawn Integration Verifier subagent using playwright-cli (see agent-contracts.md → Integration Verifier)
PASS_CRITERIA: Verifier returns GATE_RESULT: PASS with ≥9/10 checks passing
BLOCKS: deploy-gate
IMPORTANT: This is the live demo moment — browser must be headed and visible
RETRY_ON_FAIL:
  1. Read BLOCKING_ISSUES
  2. Fix issues directly (orchestrator handles this)
  3. Re-spawn Integration Verifier
ESCALATE_AFTER: 3 FAIL results — present full report to user
```

---

## Gate: Deploy (Phase 4)

```
GATE: deploy
WHEN: After integration passes
RUN: Deploy to Vercel via MCP tool (mcp__claude_ai_Vercel__deploy_to_vercel)
PASS_CRITERIA: Deployment succeeds, production URL is accessible
BLOCKS: production-gate
RETRY_ON_FAIL: Check build logs via mcp__claude_ai_Vercel__get_deployment_build_logs, fix issues
ESCALATE_AFTER: 3 failures
```

---

## Gate: Production Verification (Phase 4)

```
GATE: production
WHEN: After deploy succeeds
RUN: Spawn Production Verifier using playwright-cli on the production URL
PASS_CRITERIA: Full flow works on production (same checks as integration)
BLOCKS: done
IMPORTANT: Browser headed — audience watches the live deployed app
RETRY_ON_FAIL: Usually indicates env var or Supabase config issue — check logs
ESCALATE_AFTER: 2 failures (production issues are usually config, not code)
```

---

## Escalation Protocol

When any gate escalates (consecutive failures at max):

```
ESCALATION_REPORT:
  GATE: <which gate failed>
  PAGE: <which page/ticket>
  ITERATION: <N> (max reached)
  PERSISTENT_ISSUE: <description of what keeps failing>
  ATTEMPTED_FIXES:
  - Iteration 1: <what was tried>
  - Iteration 2: <what was tried>
  - Iteration 3: <what was tried>
  ERROR_OUTPUT: <last error/test output>
  RECOMMENDATION: <what the developer agent thinks might work>
  ACTION_NEEDED: User must intervene or approve alternative approach
```

The orchestrator should:
1. NOT retry the same approach again
2. Present the escalation report to the user
3. Wait for user guidance before continuing
4. If user provides a fix direction, reset iteration count and continue

---

## Gate Ordering Rationale

```
compile → review → browser → integration → deploy → production
```

- **Compile first**: Catches 80% of issues for near-zero cost.
- **Review before browser**: Structural issues are cheaper to catch by reading code.
- **Browser after review**: Most expensive per-page gate — only run when code is structurally sound.
- **Integration after all pages**: Catches cross-page issues (shared state, navigation flow).
- **Deploy after integration**: Don't deploy broken code.
- **Production last**: Final validation that everything works in the real environment.
