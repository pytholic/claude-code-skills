---
name: explain-code
description: Explains code with analogies, diagrams, and step-by-step walkthroughs. Use when the user asks "how does this work?", requests a walkthrough of a function/module/codebase, is onboarding to unfamiliar code, or needs a concept clarified. Match depth to the question — short for quick questions, layered for deep dives.
---

# Explain Code

Goal: build the reader's mental model fast. Prefer clarity over exhaustiveness.

## Match depth to the question

- **Quick question** ("what does this line do?") → one or two sentences, no ceremony.
- **Function/component walkthrough** → analogy + short flow diagram + step-by-step + gotcha.
- **System / architecture** → layer it: high-level picture first, then zoom into components on request.

Don't over-explain. If the user already understands half of it, skip to the part they don't.

## When you do a full explanation

1. **Analogy** — Compare to something familiar. For technical users, use a programming analogy (e.g., "like a reducer but over a stream"). For less-technical readers, use everyday analogies.
2. **Diagram** — Show flow, structure, or relationships. ASCII or mermaid is usually enough and stays inline with the explanation.
3. **Walkthrough** — Step through the code in execution order. Reference file paths with `file:line` so the user can jump.
4. **Gotcha** — Call out a non-obvious behavior, common mistake, or subtle invariant. This is usually the highest-value part.

## Style

- Conversational, not textbook.
- Concrete over abstract — name the actual variables, functions, files.
- Pair a tricky concept with a second analogy from a different domain if the first might not land.
- If something is genuinely confusing *in the code itself* (not just to the reader), say so — don't pretend it's elegant.

## What to avoid

- Narrating what's obvious from variable names.
- Paraphrasing each line in prose ("this line sets x to 5"). Explain the *why*, not the *what*.
- Dumping everything at once — layer it. Offer to go deeper rather than forcing it.
