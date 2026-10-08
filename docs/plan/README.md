# md3 build plan and tracking

How md3's build is planned and tracked. The full rules are in `docs/AGENT_PROMPT.md`; this page is the short version for anyone, human or agent.

## Structure

- **Batch** (`B3`): a milestone-sized block of work, following the build order in DECISIONS.md §16. One file per batch: `B00-kickoff.md` … `B11-sync.md`.
- **Stage** (`B3.2`): an ordered step inside a batch that ends with something working and tested. One branch and one pull request per stage.
- **Task** (`B3.2.1`): one unit of work, done in one or a few commits.

IDs never change and are never reused. A task added later takes the next free number in its stage; a split task becomes `B3.2.1a`, `B3.2.1b`. Follow-ups found along the way get backlog IDs `X1`, `X2`, … in `BACKLOG.md`.

## One source of truth per fact

| Fact | Lives in |
|---|---|
| Decisions (the spec) | `docs/DECISIONS.md`; build-phase changes in §18 |
| Task status | the batch files (Status column only) |
| Commits, dates, push and merge state | git |
| Current position and timeline | `docs/STATUS.md`, `docs/TIMELINE.md`: **generated** by `tools/track.py sync`, never edited by hand |
| Where work stopped | `HANDOFF.md`: rewritten (never appended) at every pause |

## Batch files

Each stage has a table: `ID | Task | Decisions | Depends on | Done when | Status`.

- **Status** is one of `todo` · `doing` · `review` · `blocked: <reason>` · `done` · `dropped: <reason>`. Only one task is `doing` at a time.
- **Depends on** lists task IDs, stage IDs (every task in the stage done) or batch IDs (every task in the batch done), or `—`.
- **Done when** is a testable criterion, taken from DECISIONS.md wherever one exists.
- Only the Status column changes, unless the user approves a change to the scope.
- **Notes** hold dated one-line findings. Anything longer goes in the commit body.

## Commit messages

```
B3.2.1: Add BS.1770 gating and integrated loudness

Why: <one or two lines>.

Task: B3.2.1
Decisions: #77, #78, #84
Evidence: Tech 3341 #1–#6 within ±0.03 LU; chunking test bit-identical
```

- Subject: imperative, ≤ 72 characters, starts with the task ID. It becomes the timeline's "what was done" line.
- `Task:` is required: a task ID, an X ID, or `meta` (tracking and housekeeping only).
- `Evidence:` is required on the commit that makes a task `done`.
- `Decisions:` lists every decision ID the commit implements or touches.
- No AI attribution of any kind; the hooks and CI reject it.

## Tools and hooks

`python3 tools/track.py check | sync | report | next`. The git hooks in `.githooks/` run `sync` and `check` before every commit and validate the message. Enable them once per clone:

```
git config core.hooksPath .githooks
```

If a generated file has a merge conflict, run `tools/track.py sync` instead of merging it by hand.

## Branches

One branch per stage (`b3.2-loudness-analyser`), from `main`. Push after every finished task. `main` changes only through a pull request, merged with a merge commit (never squash) after CI and review pass.
