# B9 Processing
Milestone: M5, M6 · Build order: §16 step 8 · Branch prefix: b9
Summary (written when the batch closes): —

## B9.1 Engine
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B9.1.1 | Engine topology: tap with mute, aggregate device, I/O proc | #116, #126, #127 | B8 | Audio passes through unchanged | todo |
| B9.1.2 | Stage order, gain stage, limiter rule, pass-through Sync output stage | #117, V18 | B9.1.1 | Impulse position constant across bypasses | todo |
| B9.1.3 | Utility stage incl. bass mono | #118 | B9.1.2 | #118 tests pass | todo |
| B9.1.4 | Latency, processing on/off, post tap point, meter toggle | #119, #120, #128, #5 | B9.1.2 | Pre tap → analyser sections bit-identical regardless of chain | todo |

## B9.2 Apple AU pages
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B9.2.1 | `eq` and `comp` slots with Apple AUs, drawn from the parameter tree | #153 | B9.1 | Pages work at all three sizes | todo |

## B9.3 A/B, loud match, presets
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B9.3.1 | Private meters, `PreStream` / `ChainOutStream`, level-matched A/B | #121, #121a, #149 | B9.1 | #121 tests pass | todo |
| B9.3.2 | Loud match → real-track parameter check | #122b, §15 | B9.3.1 | Parameters finalised | todo |
| B9.3.3 | Factory and chain presets, switching, auto-load | #123, #124, #157, #48 | B9.2.1 | Presets on eq/comp/fx only; tag `m5` | todo |

## B9.4 Third-party plugins
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B9.4.1 | AUv2/AUv3 hosting per the M0-5 result; loading rules; if plugins load in process, propose the library-validation entitlement trade-off as a §18 decision | #155, #158, security rule 8 | B9.3 | Plugins load per spec under the hardened runtime | todo |
| B9.4.2 | `fx` slots and editor windows | #154, #156 | B9.4.1 | 8 slots; generic list when no editor | todo |
| B9.4.3 | Stage failure isolation, watchdog, safe mode | #125 | B9.4.1 | Injection tests pass; original audio back ≤ 500 ms | todo |
| B9.4.4 | Full #129 test suite | #129 | B9.4.3 | CI green; tag `m6` | todo |

## Notes
