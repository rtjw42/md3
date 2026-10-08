# Backlog

Follow-ups and bugs found along the way. One line each: what, where, why it matters. Triaged into a batch at each batch gate.

| ID | Found in | What | Why it matters | Status |
|---|---|---|---|---|
| X1 | B0.1.3 | B4.2.3 (and §16 steps 3 and 9) call for a self-hosted CI runner with audio, which security rule 4 forbids on this public repo | A self-hosted runner would let strangers' pull requests run code on the user's Mac. Proposed: run the capture end-to-end check locally on the user's Mac with a script, record the numbers as Evidence; decide at the B4 gate | todo |
| X2 | B0.1 review | `track.py check` requires a Task: trailer on every non-merge commit; commits made outside the hooks (Dependabot, GitHub web edits) have none | Once B0.5.3 enables Dependabot, its first merged PR would make check fail on main for good. Dependabot is already enabled on the repo, so this is handled in B0.3.3, when packages and workflows first appear | moved to B0.3.3 |
| X3 | B0.2 review | The B0 hands-on check in docs/CROSS_CHECK.md expects a green CI badge on the README, but no task adds one | The user's end-of-B0 check would fail. Proposed: add the badge in B0.3.3 when CI exists | todo |
