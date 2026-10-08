# B8 Tempo and key
Milestone: M3.5 · Build order: §16 step 7 · Branch prefix: b8
Summary (written when the batch closes): —

## B8.1 Tempo
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B8.1.1 | Tempo analyser with its own onset front end | #107–#109, #115 | B7 | Synthetic tests pass | todo |

## B8.2 Key
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B8.2.1 | Key analyser on `SpectralFrame`; first check Faraldo's ECIR 2016 and AES 2017 papers and 2018 PhD thesis (and Sha'ath's thesis) for printed profile values, per #173 | #110, #111, #173 | B7 | Synthetic tests pass | todo |

## B8.3 Benchmark and display
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B8.3.1 | Local benchmark (datasets never in CI) | #113, #114 | B8.1.1, B8.2.1 | Figures published | todo |
| B8.3.2 | Set confidence thresholds, minimum capture lengths and the ship gate | #109, #111, #115, §15 | B8.3.1 | Values finalised | todo |
| B8.3.3 | Show tempo / key on the header line | §2.1 | B8.3.2 | "—" below threshold; tag `m3.5` | todo |

## Notes
- 2026-10-08 B8.2.1: key-profile values only from the publication that defines them, cited in the code; never from GPL, AGPL or unlicensed code (#173). Faraldo's and Sha'ath's profiles are in only if published that way or licensed by their authors.
