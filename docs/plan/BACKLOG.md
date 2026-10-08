# Backlog

Follow-ups and bugs found along the way. One line each: what, where, why it matters. Triaged into a batch at each batch gate.

| ID | Found in | What | Why it matters | Status |
|---|---|---|---|---|
| X1 | B0.1.3 | B4.2.3 (and §16 steps 3 and 9) call for a self-hosted CI runner with audio, which security rule 4 forbids on this public repo | A self-hosted runner would let strangers' pull requests run code on the user's Mac. Proposed: run the capture end-to-end check locally on the user's Mac with a script, record the numbers as Evidence; decide at the B4 gate | todo |
| X2 | B0.1 review | `track.py check` requires a Task: trailer on every non-merge commit; commits made outside the hooks (Dependabot, GitHub web edits) have none | Once B0.5.3 enables Dependabot, its first merged PR would make check fail on main for good. Decide in B0.5.3: exempt bot-authored commits in check, or always merge them through a stage branch | todo |
