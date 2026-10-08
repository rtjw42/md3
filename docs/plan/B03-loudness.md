# B3 Loudness engine
Milestone: — · Build order: §16 step 2 · Branch prefix: b3
Summary (written when the batch closes): —

## B3.1 Front end
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B3.1.1 | LoudnessFrontEnd: K-weighting per sample rate | #12 | B2 | Filter response matches BS.1770 at every supported rate | todo |
| B3.1.2 | `KWSubBlock` / `KWRecord` sub-block energies | #85, V5 | B3.1.1 | Record stored as its own versioned section | todo |

## B3.2 Loudness analyser
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B3.2.1 | Momentary, short-term, integrated with gating | #77, #78, #84 | B3.1 | Tech 3341 vectors within ±0.1 LU (#14) | todo |
| B3.2.2 | LRA | §4.3 | B3.2.1 | Tech 3342 vectors pass | todo |
| B3.2.3 | Programme vectors 3341 #7–8, 3342 #5–6; chunk-size bit-identity | §4.8 items 2–3, #176 | B3.2.2 | Generated vectors pass in CI; the official EBU set incl. 3341 #7–8 and 3342 #5–6 passes a local run on the maintainer's Mac with the #176 agreement test, numbers in Evidence; chunk-size bit-identity green in CI | todo |

## B3.3 True peak
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B3.3.1 | TruePeak analyser: oversampling designs, sample peak, FIR flush at `finish()` | #76, #76a, V1, V2 | B2 | Tech 3341 signals 15–23 pass | todo |
| B3.3.2 | #76 burst test against the real code | §4.8 item 1 | B3.3.1 | CI job green | todo |
| B3.3.3 | Clipped-master cross-check vs an ideal reference and libebur128 → finalise #76a (needs the user's masters) | #76a, §15 | B3.3.1 | Values finalised or changed via §18 | todo |

## B3.4 Derived and module checks
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B3.4.1 | Derived module: trim duration and PLR | #75, #79, V3, V17 | B3.2.1, B3.3.1 | Versioned `DerivedResult` | todo |
| B3.4.2 | Disable-each and failure injection with the real modules, incl. slow/blocked | #106, #146 | B3.4.1 | Other sections byte-identical | todo |
| B3.4.3 | CPU kernel bench | #161, §4.8 item 8 | B3.2.1, B3.3.1 | Figures recorded vs #161 | todo |

## Notes
- 2026-10-08 B3.3.1: "Tech 3341 signals 15–23 pass" means the Tech 3341 true-peak tolerance +0.2 / −0.4 dB (§4.3); signals are generated in CI (#176).
- 2026-10-08 B3: official EBU test files only on the maintainer's Mac, never committed or in CI; "EBU Mode" claimed only from a full local pass (#176).
