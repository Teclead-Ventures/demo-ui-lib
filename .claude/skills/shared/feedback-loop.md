# Self-Improving Feedback Loop

Every skill in this system follows the same reflection and improvement cycle. This is inspired by [autoresearch](https://github.com/karpathy/autoresearch) — each execution makes the system smarter for the next one.

## The loop

```
Execute → Self-assess → Ask user → Apply improvements → Persist
   ↑                                                        │
   └────────────── next execution reads this ───────────────┘
```

Every skill run MUST end with steps 1-5 below. No exceptions — even failed runs produce valuable learnings.

---

## Step 1: Self-assessment (automatic, after every execution)

After completing (or failing) the main task, write a structured assessment:

```markdown
## Self-Assessment: [skill-name] — [product/task] — [date]

### Result: SUCCESS | PARTIAL | FAILED

### Metrics
- Duration: Xm
- Products built/researched: N
- TypeScript errors encountered: N
- Pricing accuracy: X% of calibration targets hit
- Playwright tests: X/Y passed

### What worked
- [specific thing that went well — be concrete, not vague]
- [pattern that should be repeated]

### What failed
- [specific failure] — ROOT CAUSE: [why] — SEVERITY: [high/medium/low]
- [each failure gets root cause analysis, not just symptoms]

### Improvements to apply
- [specific change to a specific file] — REASON: [why this helps]
- [each improvement is actionable — file path, what to change, why]

### Questions for the user
- [thing I'm unsure about and need human judgment on]
- [decision where I chose X but Y might be better — ask]
```

### What makes a GOOD self-assessment:
- **Concrete, not vague**: "BU occupation selector had 4 options, real ERGO has 200+" not "could improve UX"
- **Root cause, not symptom**: "Pricing was off because age curve quadratic was too steep" not "pricing was wrong"
- **Actionable improvements**: "Update products.md BU entry: change ageCurve.quadratic from -0.15 to -0.08" not "fix pricing"
- **Honest about uncertainty**: Flag things you're not sure about rather than guessing

---

## Step 2: Ask the user for feedback

Present the self-assessment and ask specific questions:

```
Here's what I built and what I think about it:
[self-assessment summary]

Questions for you:
1. [specific question about a decision you made]
2. [specific question about quality/accuracy]
3. Anything I missed or got wrong?
```

**If the user is away** (demo-factory autonomous mode): Skip the user question step. Write the self-assessment, apply obvious improvements automatically, and flag uncertain improvements for later review. Save everything to the feedback log.

---

## Step 3: Apply improvements

Based on the assessment + user feedback, apply changes to the relevant files:

### What can be improved automatically:

| Target | What changes | Example |
|--------|-------------|---------|
| `products.md` | Corrected base rates, age curves, field lists | "BU base rate Komfort: €2.54 → €2.31 based on market research" |
| `pricing-model.md` | Calibration table updates, new edge cases documented | "Added Kfz SF-Klasse interpolation formula" |
| `ticket-templates.md` | Better page type mappings, fixed patterns | "Summary page must include product-specific section" |
| `SKILL.md` (any skill) | Clearer instructions, fixed ambiguities | "Added: team member must update registry.ts" |
| `team-member-prompt.md` | Better agent instructions | "Added Unicode sed fix as mandatory Phase 3 step" |
| `learnings.md` | New entries from this run | Accumulated across all runs |
| `feedback-log.md` | Full run record | Source repo, persists across demo runs |

### What needs user approval:
- Changing the number of wizard steps for a product
- Removing or adding form fields
- Changing the tier structure (names, count)
- Any change that would affect the live demo

---

## Step 4: Persist to feedback log

Write the assessment + feedback + applied changes to TWO places:

1. **`/Users/malte/Desktop/Repositories/tlv/demo-ui-lib/tickets/feedback-log.md`** — source repo, persists across all demo runs
2. **`/Users/malte/Desktop/Repositories/tlv/demo-builds/learnings.md`** — accumulated lessons for the current factory run

Format for feedback-log.md:
```markdown
## Run: YYYY-MM-DD (product/task, skill-name)

### Self-Assessment
[the assessment from Step 1]

### User Feedback
[what the user said, or "User was away — autonomous mode"]

### Applied Improvements
- [x] [improvement 1 — checked when applied]
- [x] [improvement 2]
- [ ] [improvement 3 — deferred, needs user approval]

### Impact on next run
- [how this changes future behavior]
```

---

## Step 5: Verify improvements don't break existing products

After applying improvements to shared files (products.md, pricing-model.md):

1. **Pricing regression check**: For every product that has a calibration line, recalculate the price with the formula and verify it still hits the target within 5%
2. **Schema check**: Verify the entry still matches the format in `shared/product-schema.md`
3. **Cross-reference check**: If you changed a field name, make sure all references (ticket templates, team member prompt) are updated

---

## How each skill uses this

### tariff-designer
- After designing a tariff: self-assess the spec quality, ask user if the pricing feels right, capture feedback on tier descriptions and field choices
- Improvements go to: products.md (if the user corrected something that should be the new default)

### demo-factory
- After each product (Pass 2 complete): the team lead self-assesses, captures learnings
- After ALL products: comprehensive self-assessment, ask user for portfolio-level feedback
- Improvements go to: products.md, learnings.md, team-member-prompt.md, SKILL.md

### ergo-researcher
- After each product researched: self-assess confidence in findings, flag uncertain data
- After all research: comprehensive comparison of our assumptions vs reality
- Improvements go to: products.md (the main output), pricing-model.md (if formula needs changes)

### ergo-site-researcher
- After each page analyzed: self-assess component identification quality, style extraction accuracy
- After all pages: comprehensive catalog review — are there duplicates? missing components?
- Improvements go to: component catalog, BUILD_SPEC.md, style extraction methodology
- Key question: "Would a builder agent have enough info to recreate this page from my spec?"

---

## Cross-run improvement tracking

Over time, the system builds up a history in feedback-log.md:

```
Run 1 (Sterbegeld): Pricing off by 30% → fixed base rates
Run 2 (Sterbegeld): Theme CSS missing → added to Phase 0
Run 3 (Sterbegeld): Unicode escapes → added sed fix
Run 4 (Sterbegeld): Clean run, zero issues
Run 5 (Factory, 14 products): All succeeded, Reise still had Unicode issue → sed fix works
Run 6 (Researcher): Found ERGO uses different age bands for Zahnzusatz → updated products.md
Run 7 (Factory rebuild): Pricing now matches ERGO within 10% for all products
```

Each run starts by reading ALL previous entries. The system never makes the same mistake twice.

---

## Metrics to track across runs

| Metric | Where tracked | What it measures |
|--------|---------------|-----------------|
| Pricing accuracy | feedback-log.md | % of calibration targets hit within 5% |
| Build success rate | manifest.json | % of products that built without failure |
| Unicode escape rate | feedback-log.md | # of files that needed sed fix (should trend to 0) |
| Pass 1 → Pass 2 improvement | build-logs/ | What % of Pass 1 issues are fixed in Pass 2 |
| Agent iteration count | build-logs/ | How many compile/review/test loops per page (should trend to 1) |
| Market price alignment | products.md Source sections | How close our prices are to real ERGO prices |
| User satisfaction | feedback-log.md User Feedback sections | Qualitative trend |
