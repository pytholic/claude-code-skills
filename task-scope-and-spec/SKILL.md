---
name: task-scope-and-spec
description: >
  Scope a loose engineering task into a tight, testable spec list. Use when the user
  gives background for a piece of work and wants the requirements narrowed down before
  implementation. Trigger phrases include: "scope this", "what are the specs", "what's
  involved", "what would it take", "what's left for this task", "port this to", "bring
  this logic to", and "spec this ticket/issue". This skill defines WHAT must be true
  when the work is done — it does not produce an implementation plan, task ordering, or
  execution steps. For sequencing the specs into ordered, verifiable tasks, use
  planning-and-task-decomposition instead.
---

# task-scope-and-spec

## Purpose

Turn loose task context — a description, ticket, link, branch, diff, or existing code —
into a small, accurate spec list. Gather the relevant context, judge what the change
touches, and report only what changes what must be built, finished, or decided.

The output is a decision aid, not a design doc.

## Core principle

**Narrow, don't expand.** Investigate broadly, report tightly. If a detail does not
change the implementation target or acceptance criteria, leave it out. The failure mode
to avoid is a comprehensive, low-signal architecture summary.

## Triage Gate

Before investigating, judge how much context-gathering the task actually needs. The
expensive step is investigation (step 2) — skip it when it would tell you nothing new.

- **Self-contained** (a clear ticket or description that already states the requirements,
  with no codebase claim to verify): go straight to the spec list from the given text.
  Do not open files speculatively.
- **Code-grounded** (references a branch, diff, PR, "what's left", porting to a module, or
  any spec that depends on the current state of the code): run the full workflow below —
  here the investigation *is* the value.

When in doubt, do a shallow investigation first; expand only if what you find changes the
specs.

## Workflow (internal — do not narrate)

### 1. Resolve inputs
Identify what context the task references (description, ticket, PR/diff, branch,
file path, pasted notes, existing code) and gather what's reachable using whatever tools
are available. Stay tool-agnostic — don't assume or require a specific one. If a
referenced source can't be reached, note it briefly in the output and proceed; only stall
if the missing source would materially change the specs.

### 2. Investigate
Read enough to understand affected modules, current vs. desired behavior, data
shapes/contracts, callers and downstream consumers, existing tests, and similar
implementations.

### 3. Classify task shape
- **New work** — specs are what must be built.
- **In-progress work** — specs are what's left to satisfy.
- **Porting work** — specs are the delta. Compare explicitly:
  source behavior → target current state → what's missing in target →
  what must adapt because the target differs (contracts, deps, tests).
- **Unclear/stale work** — specs are what can be inferred, plus the mismatch.

### 4. Judge blast radius
Exactly one of *local* (one module), *cross-cutting* (several modules/contracts/tests),
or *structural* (shared interfaces, data flow, persistence, architecture boundary).

### 5. Reconcile intent vs. reality
Tag each requirement's basis: **observed** (in the context), **implied** (a reasonable
inference), or **needs decision**. Never present an inference as fact, and never invent a
requirement the context doesn't support. Surface a mismatch only when it changes the
specs — e.g. the ask is already done, the ticket is stale, or the code implies extra work.

## Output contract

Return only this structure, one screen or less:

```markdown
**Goal:** <one sentence>

**Scope:** <local | cross-cutting | structural> — <one sentence on what it touches>

**Specs:**
- <concrete, testable requirement — what must be true when done>
- ...

**Note:**
- <only if stated intent and observed context diverge>

**Needs a decision:**
- <only if a real blocker remains, phrased as a question>
```

Omit `Note` and `Needs a decision` when not needed.

Specs should: state observable behavior, name contracts only when necessary, include
compatibility/test expectations only when they define required confidence, and stay free
of implementation steps unless the step *is* the requirement.

Aim for 3–8 specs. Split the task when it exceeds ~10 specs **or** when specs span
unrelated goals — group by user-visible outcome or contract boundary, and say so.

## Anti-patterns (do not)

- No preamble, "here's what I found", or restating the user's background.
- No generic checklists, vague engineering advice, or architecture essays.
- No implementation plan unless explicitly requested.
- No speculative nice-to-haves or duplicate restatements of one requirement.
- No tool names unless the user supplied them or the source itself matters.

## Clarifying questions

Ask at most one, and only if the answer would materially change the specs. If enough
context exists for a useful partial spec, produce that instead of asking.
