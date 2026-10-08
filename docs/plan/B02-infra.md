# B2 Infrastructure
Milestone: — · Build order: §16 step 1 · Branch prefix: b2
Summary (written when the batch closes): —

## B2.1 Records and rings
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B2.1.1 | Record types | #103 | B1 | Every record in §3.4 defined with owner and version | todo |
| B2.1.2 | SPSC ring library | #147, #149 | B2.1.1 | Unit tests pass; TSan clean | todo |
| B2.1.3 | Ring stress test | #162 | B2.1.2 | 3.9 s stall → no loss; 4.5 s → gap recorded, grid intact | todo |

## B2.2 Coordinator
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B2.2.1 | Re-blocking into 100 ms `AnalysisBlock`s; gap zero-fill and flags | #80, V9, V10 | B2.1 | Chunking test passes with dummy modules | todo |
| B2.2.2 | FP environment on analysis threads | #82, V11, V16 | B2.2.1 | Set and verified per thread | todo |
| B2.2.3 | 20 ms polling, no timer when idle | #148, #51 | B2.2.1 | Timer only while a consumer is active | todo |
| B2.2.4 | Time budgets, stall marker, failure isolation | #146, #102 (8), V20 | B2.2.1 | Slow, blocked and NaN dummy modules handled as specified | todo |
| B2.2.5 | `checkpoint()` plumbing | #151 | B2.2.4 | Dummy checkpoints reach a stub journal every 30 s | todo |

## B2.3 Inputs and harnesses
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B2.3.1 | File-decoder input | #59 | B2.2.1 | Decodes WAV/AIFF/MP3/AAC into `AnalysisBlock`s | todo |
| B2.3.2 | Golden corpus | #106 b | B2.3.1 | Corpus and golden-hash store in the repo | todo |
| B2.3.3 | Disable-each, chunking and failure-injection harnesses | #106 a, c, d | B2.2.4, B2.3.2 | Harnesses pass with dummy modules | todo |
| B2.3.4 | ASan/UBSan CI job for the C modules | #106 e | B2.1.2 | CI job green | todo |
| B2.3.5 | Benchmark harness: results saved as a CI artifact on every merge to `main`, compared with the last run | #161, §6.1 | B2.1.2 | CI fails on a > 20% slowdown in any kernel | todo |
| B2.3.6 | Malformed-input tests for the file decoder (truncated, wrong header, huge sizes, zero length) | security rule 5 | B2.3.1 | No crash, no unbounded allocation; clean error for each | todo |

## Notes
