# B5 Storage, history, Compare basics
Milestone: — · Build order: §16 step 4 · Branch prefix: b5
Summary (written when the batch closes): —

## B5.1 Database
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B5.1.1 | GRDB schema, binary array container, migrator | #150 | B4 | Round-trip bit-exact; migration test | todo |
| B5.1.2 | Fuzz tests for the binary container reader and the JSON import (libFuzzer or a seeded random-mutation harness in CI) | #150, #152, security rule 5 | B5.1.1 | 10-minute fuzz run in CI with no crash or sanitizer report | todo |

## B5.2 Safety
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B5.2.1 | Recovery journal | #151 | B5.1.1 | `kill -9` test passes | todo |
| B5.2.2 | DB robustness and rolling backups | #164 | B5.1.1 | Corrupt / newer / missing tests pass | todo |

## B5.3 History
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B5.3.1 | History view in the dropdown; grouping | #22, #23 | B5.1.1 | Entries grouped by "artist — title" | todo |
| B5.3.2 | Retention: last N + up to 20 saved | #25 | B5.3.1 | Auto-delete respects saved entries | todo |
| B5.3.3 | Export / import JSON and CSV | #152 | B5.1.2 | Export → import identical | todo |

## B5.4 Compare basics
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B5.4.1 | Time alignment → finalise #75 values on real cross-source captures | #75, §15 | B5.3.1 | Alignment tests pass; values finalised | todo |
| B5.4.2 | Level-match toggle; version labels | #92, V13, rule 5 | B5.4.1 | Differences labelled, never silently overlaid | todo |

## Notes
