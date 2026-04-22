---
name: systematic-debugging
description: Language-agnostic, four-phase debugging methodology with root cause analysis. Use when investigating bugs, fixing test failures, diagnosing unexpected behavior, or troubleshooting any runtime/logic error. Trigger this skill whenever the user says "debug", "fix this bug", "why is this failing", "unexpected behavior", "broken", "not working", or presents a stack trace / error log. Emphasizes NO FIXES WITHOUT ROOT CAUSE FIRST.
---

# Systematic Debugging

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Never apply symptom-focused patches that mask underlying problems. For example, adding `if x is None: return` at the crash site instead of tracing where the missing data originated is a process violation.

## Triage Gate

Not every bug needs the full four-phase framework. Before entering the phases, perform a quick triage:

- **Trivial bug** (typo, wrong variable name, off-by-one that is immediately obvious from the error): Fix it directly, add a brief note explaining the cause, and move on. No hypothesis template needed.
- **Non-trivial bug** (root cause is not immediately obvious, involves data flow across multiple functions/modules, or has failed one fix attempt already): Enter the full four-phase framework below.

When in doubt, default to the full framework — it costs minutes but saves hours.

## Cross-Skill Integration

This is a methodology skill. The steps below involve writing tests, implementing code, and reviewing changes. For each of these activities, check whether a relevant skill exists in the current project and apply it. If no matching skill is found, follow the inline guidance provided.

1. **Writing Reproduction Tests**: Look for any skill related to testing conventions, test authoring, or test structure. Apply its rules when writing the failing test case. If none exists: write a minimal, isolated test that fails on the current bug and passes on the correct behavior. Prefer parameterized tests for boundary conditions. Name tests descriptively so the failure message explains the bug.

2. **Implementing the Fix**: Look for any skill related to the language or framework being used (e.g., a Python development skill, a TypeScript conventions skill, etc.). Apply its style rules, typing expectations, and structural constraints when writing the fix. If none exists: follow the project's established conventions — use explicit types, keep functions focused and short, apply SOLID principles, and match the existing code style.

3. **Verifying the Fix**: Look for any skill related to code review, PR review, or change validation. Apply its checklist to your own changes before declaring the bug fixed. If none exists: re-read your own diff critically — check for unhandled edge cases, regressions in adjacent behavior, style violations, and missing test coverage for the fix.

## The Four-Phase Framework

### Phase 1: Reproduce & Trace

**Goal**: Confirm the bug exists and narrow down where the invalid state originates.

1. **Read every word of the error message.** Extract: the exception type, the failing line, and any chained/cause exceptions.
2. **Reproduce the issue.** Create a minimal failing test case. If you cannot reproduce it, you cannot verify a fix — do not proceed until reproduction is achieved.
3. **Trace data flow backward.** Do NOT stop at the crash site. Work backward through the call chain using these concrete steps:
   - Read the stack trace bottom-to-top, opening each frame's source.
   - Identify the first frame where the data is already invalid.
   - Add targeted logging/print statements at function boundaries around that frame.
   - Inspect input arguments and return values at each boundary until you find where valid data becomes invalid.
4. **Collect evidence.** Record specific observations: exact variable values, log lines, timestamps, or conditions that trigger vs. don't trigger the bug. You will need these in Phase 2.

### Phase 2: Hypothesis (MANDATORY — Do Not Skip)

Before writing ANY fix, pause and state your hypothesis explicitly.

Read the [template.md](template.md) file in this directory and fill out every field. The template includes:

- **Symptom**: Where and how the error manifests.
- **Evidence**: Specific observations (variable values, log output, stack frames) that point to the root cause.
- **Root Cause**: The exact logical flaw, broken assumption, or data corruption causing the issue.
- **Proposed Fix**: How to fix the problem at its origin, not at the crash site.

**Do not proceed to Phase 3 until the hypothesis is written and the Evidence field contains at least one concrete observation.**

### Phase 3: Implementation & Verification

1. **Implement a single, targeted fix** that addresses the root cause from your hypothesis. Do not bundle unrelated refactors or "while I'm here" changes.
2. **Follow project conventions.** Apply the relevant language/framework skill or fall back to the project's existing style.
3. **Run the reproduction test.** It must now pass.
4. **Run the full test suite.** Ensure zero regressions. If new tests fail, determine whether they are pre-existing flaky tests or genuine regressions from your change before proceeding.

### Phase 4: Stop Rules (CRITICAL)

**Single failure**: If your fix doesn't resolve the reproduction test, return to Phase 2. Re-examine your evidence, invalidate the current hypothesis, and form a new one.

**Three consecutive failures**: STOP ENTIRELY. Three failed hypotheses in a row indicate one of:
- An incorrect mental model of the system
- An architectural/design flaw beyond a single bug fix
- Missing context (undocumented side effects, external dependencies, race conditions)

When you hit this threshold, do not attempt another patch. Instead, fill out the [escalation_template.md](escalation_template.md) and surface it to the user for discussion.

## Process Violations — Red Flags

Stop immediately if you catch yourself doing any of the following:

- Skipping the hypothesis template ("I'll just try this real quick")
- Catching broad exceptions to silence an error instead of fixing its source
- Patching the crash site without knowing where the invalid data entered the flow
- Saying "one more attempt" after multiple failures without revisiting your mental model
- Bundling cosmetic or unrelated changes into a bug-fix commit

## Pre-Completion Checklist

Before declaring a bug fixed, verify both process compliance and correctness:

**Process compliance:**
- [ ] Reproduction test was created before any fix was attempted
- [ ] Hypothesis template was filled out with concrete evidence
- [ ] No more than one logical change was made per fix attempt

**Correctness:**
- [ ] Root cause was fixed at its origin, not patched at the symptom
- [ ] Reproduction test now passes
- [ ] Full test suite passes with no new failures
- [ ] Self-review of the diff was performed (or a code review skill was applied)