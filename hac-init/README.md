# hac-init

Bootstraps the `.hac/` (Human-Agent Context) directory in any project — the shared context layer that lets any human or agent understand a project's current state in under 30 seconds.

## How CLAUDE.md gets the HAC protocol

Claude needs the HAC protocol in `CLAUDE.md` to automatically read and update `.hac/` during sessions. There are two ways this happens:

- **Per-project (automatic):** When you run the `hac-init` skill on a project, Claude checks whether the HAC section is already present and adds it to the project's `CLAUDE.md` if not.
- **Global (manual, one-time):** To have HAC awareness in every project without relying on a project-level `CLAUDE.md`, copy the section below into your global `~/.claude/CLAUDE.md` once.

---

Add the following to your global `CLAUDE.md` file:

## HAC — Human-Agent Context (.hac/ directory)

Projects may have a `.hac/` directory — a shared context layer between the human and the agent. It solves the "where were we?" problem across sessions. This section defines the **protocol** for reading and maintaining `.hac/` during sessions. For file templates and bootstrapping, use the `hac-init` skill.

**Skip all of this for:** trivial bug fixes, formatting changes, single-file edits, or anything completable in one short session. Use judgment — if you wouldn't bother writing a plan on paper, don't bother with `.hac/`.

---

### Bootstrapping

If the user asks to "set up hac", "add .hac", "set up working memory", or you begin multi-session work on a project without a `.hac/` directory:

1. Use the `hac-init` skill. It owns the templates and the bootstrapping process.
2. If prior plan files exist elsewhere (e.g., `.claude/*.md`, `TODO.md`), offer to migrate them into `.hac/tasks/`.

### Session Start (multi-session tasks only)

- Read `.hac/status.md` overview table to understand what's active, blocked, and parked.
- Open the relevant task file linked from the table and read the session log.

### During Execution

- **New non-trivial work:** Create `.hac/tasks/<task-name>.md` using the task template from the `hac-init` skill. Add a row to the `status.md` overview table and the `README.md` master index.
- **Progress:** Update task file checklists as steps complete.
- **Session log:** Append to the session log at the end of a work block.
- **Discoveries:** Record in the Notes/Findings section of the task file.
- **Parked ideas:** When a useful idea surfaces but is out of scope for the current task, add it to the "Parked Ideas" table in `status.md` with a one-line description and the originating context. Don't create a task file for parked ideas.

### Design Decisions

- When making a strategic or architectural choice, append to `.hac/decisions.md`.
- Use the format: Context, Choice, Why, Rejected (what alternatives were ruled out and why).
- Add a row to the quick reference table at the top of `decisions.md` and the decisions table in `README.md`.
- Decisions are append-only. Never edit or remove past entries.

### Status Transitions

| From | To | Trigger |
|------|----|---------|
| 🟢 Active | 🟡 Review | Implementation complete, needs human eyes |
| 🟢 Active | 🔴 Blocked | External dependency or unresolved question blocks progress |
| 🟡 Review | ⚪ Done | Human approves |
| 🔴 Blocked | 🟢 Active | Blocker resolved |
| 🔵 Parked | 🟢 Active | Idea promoted — create a task file, remove from Parked Ideas table |
| Any | ⚪ Done | Move the row from `status.md` overview to `README.md` master index |

### Wrap-Up

- Update the task row in `status.md` overview table (status → ⚪, add date).
- Move the completed row to the `README.md` master index.
- Update the task file's metadata table status to `⚪ Done (YYYY-MM-DD)`.
- Append a final session log entry.
