# B8 Tempo and key
Milestone: M3.5 · Build order: §16 step 7 · Branch prefix: b8
Summary (written when the batch closes): —

## B8.1 Tempo
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B8.1.1 | Tempo analyser with its own onset front end | #107, #108, #109, #115 | B7 | Synthetic tests pass | todo |

## B8.2 Key
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B8.2.1 | Key analyser on `SpectralFrame` | #110, #111 | B7 | Synthetic tests pass | todo |

## B8.3 Benchmark and display
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B8.3.1 | Local benchmark (datasets never in CI) | #113, #114 | B8.1.1, B8.2.1 | Figures published | todo |
| B8.3.2 | Set confidence thresholds, minimum capture lengths and the ship gate | #109, #111, #115, §15 | B8.3.1 | Values finalised | todo |
| B8.3.3 | Show tempo / key on the header line | §2.1 | B8.3.2 | "—" below threshold; tag `m3.5` | todo |

## Notes
