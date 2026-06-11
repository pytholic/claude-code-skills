---
name: goal-workflow
description: Implement a spec fully, verify each requirement with parallel agents, and produce a report. Use whenever the user runs /goal-workflow, mentions "implement spec", "verify against spec", or wants to go from requirements to verified implementation in one shot. Even if the request seems simple, invoke this skill — it handles both small and large specs.
---

You are running the goal-workflow skill. Your job: implement a spec fully, verify each requirement, report results.

## Step 1 — Get the spec

Check `args` (the text after `/goal-workflow`):
- **File path** (starts with `/`, `./`, `~/`, or ends with `.md`/`.txt`/`.yaml` etc.) → read the file
- **Inline text** → use it directly
- **Nothing** → ask: "Paste your spec or give me a file path."

## Step 2 — Set the goal

Parse the spec into a numbered list of discrete, verifiable requirements. State out loud:

> **Goal:** Implement all N requirements below. Done when every item is verified complete.
> 1. …
> 2. …

If the spec is ambiguous on any point, ask before starting — not mid-implementation.

## Step 3 — Implement

Work through each requirement in order. Check it off as you go. Keep changes focused; don't add anything not in the spec.

## Step 4 — Verify with a workflow

After implementation, use the `Workflow` tool to verify in parallel. One agent per requirement:

```js
export const meta = {
  name: 'spec-verify',
  description: 'Verify each spec requirement against the implementation',
  phases: [{ title: 'Verify' }],
}

const REQS = args  // array of requirement strings passed via args

const VERDICT = {
  type: 'object',
  properties: {
    satisfied: { type: 'boolean' },
    evidence: { type: 'string' },
  },
  required: ['satisfied', 'evidence'],
}

const results = await parallel(REQS.map((req, i) => () =>
  agent(
    `Requirement: "${req}"\n\nCheck whether this requirement is fully satisfied in the current code/output. Be concrete — cite file names, function names, or output values as evidence.`,
    { label: `verify:${i}`, phase: 'Verify', schema: VERDICT }
  ).then(v => ({ req, ...v }))
))

return results.filter(Boolean)
```

Pass `args` as the array of requirement strings.

## Step 5 — Report

Print a markdown table:

```
## Implementation Report

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | …           | ✅     | …        |
| 2 | …           | ❌     | …        |

**Result: X / Y requirements satisfied.**
```

If anything failed, list what's missing and ask: "Fix the gaps, or done for now?"
