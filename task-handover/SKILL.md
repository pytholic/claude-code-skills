---
name: task-handover
description: Create a structured handover document so the next agent or engineer can resume work with zero prior context. Use this skill when a session is getting too long, the context window is under pressure, the user asks to "wrap up", "hand off", "create a summary for the next agent", or says "let's continue in a new chat". Also trigger proactively when a multi-subtask session has been running for a long time and meaningful progress has been made. Produces a single HANDOVER.md file — not a chat summary — that survives session boundaries and enables true cold-start resumption.
---

# Task Handover

Methodology for creating a self-contained handover document that lets the next agent or engineer resume immediately — no prior context required.

---

## Core Principle

**THE HANDOVER DOCUMENT MUST PASS THE COLD-START TEST.**

Before finalising, ask: *Could a completely fresh agent, with only this document and access to the codebase, pick up exactly where we left off and make the right next move?*

If the answer is no, the document is not done. A handover that requires the reader to reconstruct context is not a handover — it's a summary. These are different things.

---

## Triage Gate

Not every session needs a full handover document. Before starting, decide:

- **Short / single-task session** (one clear task, clean completion, no loose threads): A brief inline summary in chat is sufficient. No file needed.
- **Long / multi-subtask session** (multiple subtasks tackled, decisions made, work in progress, context window under pressure): Produce the full `HANDOVER.md` using the phased approach below.

When in doubt, write the full document — it costs minutes now and saves the next session hours.

---

## Phase 1: Verify State (Do Not Skip)

**Do not write the handover from conversational memory.** Agent memory degrades and drifts over long sessions — treat it as unreliable. You must verify the actual state of the codebase from the terminal before writing a single word.

```bash
# 1. What files are actually changed right now?
git status
git diff --stat

# 2. What is the exact test / lint state?
#    Run the project's fast test suite or linter if one exists.
#    Capture the result — pass/fail count, failing test names — for the handover.
```

Then reflect on the session narrative:
- What was the original goal, and what does "done" look like?
- What decisions were made and *why*? What alternatives were rejected?
- What approaches were tried and failed?
- What is the single most important thing the next agent must do first?
- What requires a human decision before work can continue?

Only after grounding in terminal output should you begin writing.

---

## Phase 2: Write the HANDOVER.md

Read [template.md](template.md) and fill out every section using verified state from Phase 1.

**Formatting rules:**
- Do not skip sections — use "N/A" with a brief reason if a section genuinely doesn't apply.
- **Strip all HTML comments** (`<!-- ... -->`) from the final output. The template uses them as authoring instructions — they must not appear in the written file.
- Write in plain, direct language. The reader has no session context.

**File placement — single source of truth:**
Always write to `.claude/HANDOVER.md`, overwriting any existing file. One file, always current — not a growing archive of `HANDOVER-v2.md` fragments. If the user explicitly asks to keep history, archive the previous version to `.claude/handover-archive/HANDOVER-<date>.md` first, then overwrite.

---

## Phase 3: Cold-Start Verification

Before writing the file, read the draft as if you are a fresh agent with no session memory. Check each of the following:

1. **Objective clarity** — Does it state what success looks like, not just what we're doing?
2. **Reproduction** — Can the environment be restored from the Environment section alone?
3. **Exact resume point** — Does the next agent know the *exact* next command or file to touch, with a line number if relevant?
4. **Decision rationale** — Is the *why* present for every decision? "Used X over Y because Z" — not just "used X".
5. **Dead ends documented** — Are failed approaches listed so the next agent doesn't repeat them?
6. **Open questions flagged** — Are human-decision-required blockers explicitly called out, not buried?
7. **No implicit context** — Is there anything that only makes sense if you were in this session?

If any check fails, revise before writing the file.

---

## Phase 4: Announce the Handover

After writing the file, respond to the user with three things:

1. **Confirmation** of where the file was written.
2. **Open questions** they need to resolve before the next session starts (if any).
3. **A copy-pasteable prompt block** — formatted exactly like this, ready to drop into a new chat:

---

> **Handover complete.** Close this chat and paste the following into your new session:
>
> ```
> Please read `.claude/HANDOVER.md` to get the full context of our current state.
> Once you've read it, acknowledge that you understand the objective, briefly state
> what you are going to do first, and wait for my confirmation before proceeding.
> ```

---

## Process Violations — Red Flags

Stop and correct if you catch yourself doing any of the following:

- Writing the handover from memory without first running `git status` or checking file contents
- Leaving `<!-- ... -->` comments in the final generated Markdown file
- Describing the next task vaguely ("continue implementing X") instead of specifically ("implement `refresh_token()` in `services/auth.py` at line 134, following the pattern of `create_token()` above it")
- Omitting failed approaches because "they didn't work so they don't matter" — they matter most
- Creating a new `HANDOVER-<topic>.md` instead of overwriting the single `.claude/HANDOVER.md`
- Skipping Phase 1 verification and writing from conversational memory

---

## Pre-Completion Checklist

- [ ] `git status` and `git diff --stat` run — handover reflects actual file state, not memory
- [ ] Test/lint state captured and recorded
- [ ] All template sections filled (or explicitly marked N/A)
- [ ] Every completed item references specific files or artefacts
- [ ] Every decision includes the *why* and rejected alternatives
- [ ] Dead ends documented with failure reasoning
- [ ] Next immediate task is specific enough to act on without clarification
- [ ] Open questions listed and flagged for human decision
- [ ] No HTML comments in the output file
- [ ] Written to `.claude/HANDOVER.md` (single file, overwritten)
- [ ] Cold-start verification passed
- [ ] Copy-pasteable resume prompt provided to user
