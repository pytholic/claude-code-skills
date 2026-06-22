---
name: pr-description
description: Generates a minimal, clear PR description from the current branch's diff and the repo's PR template. Use at the end of any task when the user wants to open a PR or needs a PR description written.
---

# PR Description

Generate a minimal, clear PR description using the repo's own PR template.

**Source-of-truth precedence: diff > commit messages > nothing. Never invent context.**

## Step 1: Find the Actual Branch Base

Do **not** assume the repo's default branch. Find the remote branch the current branch was most likely created from — the one with the fewest unique commits between it and HEAD.

```bash
CURRENT=$(git rev-parse --abbrev-ref HEAD)

BASE_REF=$(git for-each-ref --format='%(refname:short)' refs/remotes/origin/ \
  | grep -v 'HEAD$' \
  | grep -v "origin/${CURRENT}$" \
  | xargs -I{} sh -c 'printf "%d {}\n" $(git rev-list --count HEAD ^{})' \
  | sort -n \
  | head -1 \
  | awk '{print $2}')
```

`BASE_REF` is now the closest remote ancestor branch (e.g. `origin/develop`, `origin/main`, `origin/feature/parent`). Use it in all subsequent commands.

Guard: if `git log $BASE_REF..HEAD --oneline | wc -l` is zero, output "Branch is identical to $BASE_REF — nothing to describe." and stop.

## Step 2: Gather the Diff

Use `..` (two-dot) for log and `...` (three-dot) for diff — scopes to changes introduced by the current branch only.

1. Run `git diff --stat $BASE_REF...HEAD` to see file-level scope.
2. If the diff is **≤ 800 lines and ≤ 25 files**, run the full `git diff $BASE_REF...HEAD`.
   If larger, work from `--stat` + commit log + targeted reads of the most-changed files — do not ingest the full diff.
3. Run `git log --no-merges $BASE_REF..HEAD --oneline` for commit context. Treat these as hints only; the diff is authoritative.

## Step 3: Find the PR Template

Run:

```
find .github docs .gitlab . -maxdepth 2 \( -iname 'pull_request_template*' -o -iname 'PULL_REQUEST_TEMPLATE*' \) 2>/dev/null | head -5
```

- If one file found, use it.
- If multiple found, prefer `.github/PULL_REQUEST_TEMPLATE.md` or the most general one.
- If none found, use this fallback structure:
  ```
  ## What
  ## Why
  ## Notes
  ```

## Step 4: Write the Description

Fill in the template. Rules:

- **Minimal** — no padding, no restating what the code obviously does.
- **Preserve structure** — keep all headings, checkbox lines, and their labels exactly as they appear in the template. Never remove checkbox labels or descriptions.
- Strip only instructional HTML comments (`<!-- ... -->`). Everything else stays.
- For checkboxes (`- [ ]`): tick only those the diff clearly justifies; leave the rest unchecked. The label text after the checkbox is always preserved.
- If a section doesn't apply and it's the fallback structure, omit it. If it's a real template heading, keep the heading but leave the body blank.
- Do **not** mention Claude, AI, or this skill anywhere in the output.

**PR title:**
- Single commit on the branch → base the title on its subject line.
- Multiple commits → synthesize a title summarizing the overall change.
- Keep under 72 characters. Use imperative mood: "Add X", "Fix Y", "Refactor Z".

## Step 5: Output

Output the PR title as a plain line, then the full body in a single markdown code block:

```
**Title:** <title here>

**Body:**
```
<full template body, structure intact, HTML comments removed>
```
```

After the block, offer one line:

> To open the PR directly: `gh pr create --title "<title>" --body "$(cat <<'EOF' ... EOF)"`

No preamble, no explanation beyond that.
