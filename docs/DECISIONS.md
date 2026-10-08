# md3 — Decision Document

> Status: **build phase** (started 2026-10-08). Design review complete; every open item decided 2026-10-08 (§17); build-phase changes are logged in §18. Last updated: 2026-10-08.
>
> Legend: **✅ Decided** · **🟡 Open** (has a recommendation, awaiting your call) · **⛔ Superseded**
>
> Numbering: `D1`–`D22` are the founding decisions; `#1`–`#73` come from the first design pass; `#74`–`#164` come from the seven-part design review of 2026-10-06; `#165`–`#172` come from the open-items session of 2026-10-08. Superseded items stay in place, struck through, with a pointer to the decision that replaces them, so each decision is stated once in its final form. Consolidated lists: M0 checklist §14, provisional values §15, build order §16, **decision log §17** (every item closed on 2026-10-08, with the old recommendation next to your decision).

---

## 0. The app

**md3** is a lightweight macOS menu bar app for accurate audio metering and processing of a single app's audio. Its core job is **comparing the same song across sources** — browser, Apple Music, Spotify and local files — with verified loudness, spectrum and stereo measurements, stored in a history stack for side-by-side comparison. It also hosts Audio Unit plugins for per-app processing (EQ, compressor, plugins for listening). **Bluetooth audio/video sync** is planned for the first update after v1 (#166).

**Who it's for (#165):** producers and mixing engineers, as a Mac-wide audio utility for everything *outside* the DAW: comparing a mix with references, comparing a release across platforms, and processing what you listen to. A DAW works as a source but isn't a design focus (the DAW has its own meters).

**Principles**

1. **Accurate.** Every measurement is verified against published standards or reference implementations in CI (§4).
2. **Better than the free option.** Every feature must have a concrete edge over free tools (§11), or it doesn't ship.
3. **Lightweight.** Near-zero idle cost, small binary, minimal dependencies (§6).
4. **Out of the way.** Menu bar first, minimal, dark or cream (#168), monospaced. Displays data; doesn't lecture (no advice text, no platform-target tables).
5. **Open-source ready.** Clean licensing from day one.

---

## 1. Decided ✅

| ID | Decision |
|---|---|
| D1 | App name: **md3**. |
| D2 | **macOS only.** Native Swift (C/C++ only for real-time audio code and the driver). |
| D3 | **Minimum macOS 14.2** (the oldest version with Core Audio process taps), chosen for inclusivity. Developed on macOS 27; newer APIs only with availability checks. |
| D4 | Audio capture via **Core Audio process taps**, **one source app at a time**. No per-tab or per-window capture (macOS doesn't separate audio that way). |
| D5 | **Menu bar app.** The menu bar shows the **integrated LUFS** number; clicking opens a **wide-ish dropdown**. |
| D6 | The dropdown can be **pinned** to float above all windows (all Spaces, over full-screen apps). |
| D7 | Standard menu bar app behaviour: no Dock icon, runs in the background, launch at login, single instance, hotkeys, auto-updates, and so on (§7). |
| D8 | **Manual Start/Stop** for measurements. No automatic song splitting. Track metadata is used only to label entries. |
| D9 | **History stack**, grouped by track, with a **Compare** view across sources (browser / Apple Music / Spotify / file). |
| D10 | **No advice or warning text.** The app displays measurements only. *Amended by #167:* an optional, numbers-only normalisation preview per platform (off by default). |
| D11 | **Stereo: phase and width**, similar to Logic's Mastering Assistant. **Width is shown as a spectrum** (width per frequency band). |
| D12 | **UI:** fully **monospaced**, terminal/coder look, minimal. *Amended by #168:* dark and cream themes (was dark only). |
| D13 | Dropdown **pages switched with ‹ › chevrons**; the user can set the **default page**. |
| D14 | Pages include **lufs, spec, stereo, comp, eq** (comp = compressor). Final list: #1. |
| D15 | **History and prefs** are reached from the **bottom bar** of the dropdown. |
| D16 | **Audio plugin hosting is a must-have.** |
| D17 | **Presets** must be quick to use from within the dropdown. |
| D18 | **Bluetooth audio/video sync** is wanted, but *amended by #166:* planned for the first update after v1, not v1. |
| D19 | Every feature must be **accurate** and an **improvement over free apps**. |
| D20 | **Performance** is a requirement: light and efficient (§6). |
| D21 | Will eventually be **released as open source**. |
| D22 | Main use case: **comparing levels across platforms** (browser, Apple Music, Spotify, mp3/file). |

---

## 2. Product & UI

### 2.1 Layout (decided 2026-10-08: #1, #29, #48, #171)

```
 menu bar:   -14.1                      (●-14.1 while recording; --.- before any measurement)

╭──────────────────────────────── 720 × 320 pt (default size, #169) ──────────────────────╮
│ src:spotify ▾   "Title" — Artist   128bpm Amin                       [● rec 03:41]       │  header
│ ‹  lufs · spec · stereo · compare · eq · comp · fx  ›                                    │  page tabs
│──────────────────────────────────────────────────────────────────────────────────────────│
│                                                                                          │
│                              (page content, ~250 pt tall)                                │
│                                                                                          │
│──────────────────────────────────────────────────────────────────────────────────────────│
│ spotify 100% norm:off 48k pre                                          ⌂  ⚙  ⊼          │  one bottom line: status + icons
╰──────────────────────────────────────────────────────────────────────────────────────────╯
 Frame: standard macOS popover (rounded corners, arrow); inside: square, 1 px dividers (#171).
 Chain presets and A/B appear only on eq / comp / fx (#48).
```

### 2.2 Pages

| Page | Content |
|---|---|
| `lufs` | Integrated (large), short-term, momentary, true peak, LRA, PLR, short-term history graph. Pref: integrated only, or all values (#170) |
| `spec` | Live spectrum + averaged spectrum for the current measurement, peak hold |
| `stereo` | Width spectrum (per band: width = bar height, correlation = colour), goniometer, correlation, balance |
| `eq` | Plugin slot pre-loaded with Apple `AUNBandEQ`, drawn as a native EQ curve/band list (#153); chain presets and A/B (#48) |
| `comp` | Plugin slot pre-loaded with Apple `AUDynamicsProcessor`, with a gain-reduction meter (#153); chain presets and A/B (#48) |
| `fx` | Up to 8 additional AU plugin slots (#154); chain presets and A/B (#48) |
| `compare` | Up to 4 entries, one reference: table and overlay graph side by side (#24) |
| `sync` | **After v1 (#166).** Bluetooth AV sync: device, measured vs reported latency, total latency X, clock-lock state, calibration age and spread, calibrate/nudge controls (#70, #131–#141) |

### 2.3 UI decisions ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ✅ 1 | Final page list and order | **Decided 2026-10-08 (§17):** `lufs · spec · stereo · compare · eq · comp · fx` (compare added; `sync` page only after v1). Page order is changeable in Prefs (#170). Header, page tabs and the bottom line stay visible on every page. |
| ✅ 22 | Where do History / Compare / Prefs open? | **Decided 2026-10-08 (§17):** History and Compare open inside the dropdown (Compare is also a page, #1). Prefs open a separate standard Settings window (⌘,). |
| ✅ 27 | Font | **Decided 2026-10-08 (§17):** SF Mono, **fixed** (not user-selectable). |
| ✅ 28 | Colours | **Decided 2026-10-08 (§17):** Dark: background `#0B0B0C`, text `#C8C8C8`, dim `#5A5A5A`, accent phosphor green `#7CFC9A`. Cream: see #168. Amber/red only near and over 0 dBFS. Accent and text colour user-changeable (#170). |
| ✅ 29 | Dropdown size | **Decided 2026-10-08 (§17):** Wide-ish and as short as possible: **720 × 320 pt** by default; size presets in #169. Three fixed lines: header, page tabs, one bottom line (short status + icon buttons for history, prefs, pin). Compare shows its table and graph side by side. |
| ✅ 30 | Page navigation | **Decided 2026-10-08 (§17):** Chevrons, ←/→, number keys, trackpad swipe, wrapping at the ends. Prefs: default page or "remember last page". No page hiding. |
| ✅ 31 | Menu bar format | **Decided 2026-10-08 (§17):** `-14.1` in monospaced digits, `●-14.1` while recording, `--.-` before any measurement. Prefs can switch to live short-term or true peak (#170). |
| ✅ 33 | Terminal-style details | **Decided 2026-10-08 (§17):** Labels like `[● rec 03:41]`, `src:spotify`; right-aligned numbers; bars and meters drawn with block characters `▁▂▃▄▅▆▇█`; **overlaid curves (Compare, loudness over time) drawn as 1 px lines**; square inside with 1 px dividers, no shadows. Outer frame: #171. |
| ✅ 48 | Preset placement | **Decided 2026-10-08 (§17):** Chain presets and A/B appear **only on the processing pages** (eq / comp / fx), not on every page; page presets on each processing page. |
| ✅ 168 | Themes (amends D12) | **Dark and cream.** Follows the macOS light/dark setting; Prefs can force either. Cream: background `#FAF7F0`, text `#2B2A26`, dim `#8C877C`, accent teal green `#1F6F66`; near-0 dB colour a darker amber. Dark keeps phosphor green `#7CFC9A`. If the user changes the accent, md3 derives a readable shade per theme. |
| ✅ 169 | Size presets | Compact 640 × 280 · **Default 720 × 320** · Large 880 × 400. Every page is designed and tested at all three. No free resizing. |
| ✅ 170 | Look preferences | Size preset (#169); accent and text colour; page order; menu-bar number (integrated / short-term / true peak); default page or remember last; `lufs` page shows **integrated only** or **all values**. Not included: font choice, page hiding. |
| ✅ 171 | Frame | Standard macOS popover frame (≈10 px corners and the arrow). Everything inside stays square with 1 px dividers (amends #33's "no rounded corners" for the outer frame only). |

---

## 3. Audio architecture

### 3.1 Signal flow

```
Tap mode (metering; no driver, nothing added to the app's audio path):
  App ──► device (unchanged)
   └─► process tap ─► CaptureStream ring (#147) ─► Coordinator: 100 ms AnalysisBlocks (#80)
         ─► providers (LoudnessFrontEnd, SpectralFrontEnd) ─► analysers ─► *Live records / *Result sections

Processing (tap mode, #116):
  App ─► tap (mute-when-tapped) ─► eq ─► comp ─► fx[0..7] ─► utility ─► gain stage ─► limiter ─► Sync output stage ─► device
          │ PreStream (#121)                        │ ChainOutStream (#121a)        │ ProcessedStream (#128, "post" metering)

Driver mode (sync, §5.4):
  Player ─► md3 virtual device (reports fixed latency X; clock follows the real device, #136)
          ─► VirtualInput ─► same chain as above ─► Sync output stage (padding, AV offset) ─► real output (e.g. AirPods)
  Player delays its video by X.
```

Module ownership and records: §3.4. All stored analysis runs whenever a measurement runs; only live-only work depends on visibility (#53, V8).

### 3.2 Sources ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ✅ 18 | Source list | **Decided 2026-10-08 (§17):** Only apps with audio activity, currently-playing first, with icons. Helper processes grouped under their parent app (all Chrome helpers → "Chrome"). |
| ✅ 19 | Include a "system (all)" source? | **Decided 2026-10-08 (§17):** Yes, as one option in the same single-select list, for measuring and processing. Entries captured from it are labelled `system` in History and Compare. |
| ✅ 20 | Startup | **Decided 2026-10-08 (§17):** Remember the last source. If that app isn't running, show it greyed out and attach automatically once it starts. Never starts measuring by itself. |
| ✅ 21 | Track titles for browsers | **Decided 2026-10-08 (§17):** Automatic titles for Spotify and Music via AppleScript. Browsers: the title is **suggested** from the front tab (cleaned up, e.g. " - YouTube" removed) and confirmed or edited at Stop. No Accessibility permission. Browser tab reading is `[MEM]` (M0-13). |
| ✅ 17 | App volume / normalization info | **Decided 2026-10-08 (§17):** App volume read via AppleScript for Spotify and Music where possible; normalisation shown as `on / off / ?` with a one-click manual toggle (whether the apps expose it is `[MEM]`, M0-13). Both stored per entry. Display and record only; nothing is corrected. |

### 3.3 Processing & plugins ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ⛔ 72 | ~~eq/comp: built-in DSP or plugin loader?~~ | Closed by #153 (§3.6). |
| ⛔ 2 | ~~Built-in EQ/comp processors; `fx` page~~ | Superseded by #72 / #153; the `fx` page is closed by #154. |
| ⛔ 1 (A) | ~~Plugin formats~~ | Closed by #155 (§3.6). |
| ⛔ 3 | ~~Chain order~~ | Refined by #117 (§3.5). |
| ⛔ 4 | ~~Plugin UIs~~ | Closed by #156 (§3.6). |
| ✅ 5 | Meter tap point | **Decided 2026-10-08 (§17):** Before processing by default, with a pre/post toggle. Mechanics decided in #128 (`ProcessedStream`); `EntryHeader` records the tap point and a `ChainState` snapshot. |
| ⛔ 6 | ~~Mute the original only when processing~~ | Refined by #120 (§3.5). |
| ⛔ 7 | ~~Latency display~~ | Refined by #119 (§3.5). |
| ⛔ 8 | ~~Crash safety~~ | Refined by #125 (§3.5); the "original audio returns when md3 dies" check stays in M0. |
| ⛔ 9 | ~~Presets~~ | Closed by #157 (§3.6). |
| ⛔ 10 | ~~Level-matched A/B~~ | Refined by #121 (§3.5). |
| ⛔ 11 | ~~Output device~~ | Refined by #126 (§3.5). |
| ⛔ 49 | ~~Factory presets~~ | Refined by #123 (§3.5): `bt sync` removed from processing presets. |
| ⛔ 50 | ~~`loud match` preset~~ | Refined by #122 (§3.5). |

### 3.4 Modularity rule and module map (2026-10-06)

**Goal:** a bug in one feature can be fixed and shipped, and every other feature produces exactly the same results as before. Applies to all parts; re-checked after Parts 5–6 in §3.6 (#159).

| # | Decision |
|---|---|
| ✅ 102 | **Modularity rule.** <br>(1) Each analyser (loudness, true peak, spectrum, stereo, tempo, key) is a separate module with one interface: `init(sampleRate, channelLayout)`, `process(fixedSizeBlock)`, `finish() → result`, and optionally `checkpoint() → partialResult` (#151). Providers and the Derived module use the same interface. No analyser calls another or reads another's internal state. <br>(2) True peak is split out of `loudness_process` into its own analyser. <br>(3) Shared front ends are explicit, named **providers**, each with its own owner, version and tests. Consumers depend on a provider, never on each other. <br>(4) Cross-analyser dependencies are inputs supplied by the **coordinator**, not internal calls; every one is listed in #104. <br>(5) Each history entry stores each analyser's (and provider's) result in its own section, with a schema version and an algorithm version. Compare labels any version difference and never silently overlays. <br>(6) Any analyser can be disabled; disabling or removing one leaves every other output bit-identical. <br>(7) Capture, analysis, storage and display communicate only through the named records in #103. <br>(8) **Runtime failure isolation:** if an analyser returns an error, or its result contains NaN or infinity, **or exceeds its time budget (#146)**, the Coordinator stores the entry with that section marked `failed` (cause recorded) and every other section intact. One analyser failing never fails the entry or stops the others. A failed provider marks all its consumers `failed` (V20). <br>(9) **Shared code libraries** (#160): pure code shared by several modules is allowed if each module creates its own instances with no shared state; a library has its own version, and a library change bumps the algorithm version of every module that links it. |
| ✅ 103 | **Modules and records** (tables below). |
| ✅ 104 | **Dependency table** (below): the complete list of cross-module inputs. |
| ✅ 105 | **Violations found in #74–#101, and the smallest fix for each** (below; V1–V14 approved). |
| ✅ 106 | **Modularity tests** (build phase): <br>(a) *Disable-each:* for a fixed corpus, run all modules, then run again with each analyser disabled in turn; every other section must be byte-identical. <br>(b) *Version discipline:* golden hashes per section. If a section's bytes change, its algorithm version must have changed, and no other section may change. A provider version bump lists its consumers, whose versions bump with it. <br>(c) *Chunking:* the #80 test, now run per module. <br>(d) *Failure injection:* inject a failure (error return, NaN, ±infinity) into each analyser in turn; the entry is stored with that section `failed`, and every other section is byte-identical to the normal run. Also inject a **deliberately slow analyser** (disabled under #146, others byte-identical) and a **blocked analyser** (stall detected and recorded, entry recovered from the last checkpoint, #146 / #151). <br>(e) *Memory safety:* CI runs the C modules under AddressSanitizer and UndefinedBehaviorSanitizer, because modules in one process can't be fully isolated from a memory bug. |

**Modules (#103)**

| Module | Kind | Owns decisions | Reads | Writes |
|---|---|---|---|---|
| Capture | I/O | #51, #52, #80, #147 (ring, overflow, gaps), #81 (tap type), #5 / #128 (tap point), #163 (lifecycle events) | process tap / file decoder | `CaptureStream`, `SourceAudio` |
| Coordinator | orchestration | #80 / V9 (re-blocking), #82 / V16 (FP environment on its threads), #74 / #83 (input conditioning), #53 / #60 / #161 (scheduling), #59 / #146 (threads, workers, time budgets, stall detection), #148 (polling), #151 (checkpoint calls), #163 | `CaptureStream`, `ProcessedStream`, every `*Result` / checkpoint | `AnalysisBlock`, `EntryHeader`; supplies #104 inputs |
| Derived | module (V17) | #75 (silence-trim duration), #79 (PLR) | `KWRecord`, `TruePeakResult`, `LoudnessResult` (supplied by the Coordinator) | `DerivedResult` (`derived.trim`, `derived.plr`, each versioned) |
| LoudnessFrontEnd | provider | #12 (K-weighting per rate), #85 (sub-block energies) | `AnalysisBlock` | `KWSubBlock` (live), `KWRecord` (stored section) |
| SpectralFrontEnd | provider | #89 (frames: 683 ms Hann, 87.5%, edge-padded), #86 (band table, bin weights), #98 (band record) | `AnalysisBlock` | `SpectralFrame` (live: X_L, X_R, per-1/24-band P_L/P_R/C), `BandRecord` (stored section: totals) |
| Loudness | analyser | #77, #78, #84 (complete blocks), M / S / I / LRA | `KWSubBlock` | `LoudnessLive`, `LoudnessResult` |
| TruePeak | analyser | #76, #76a, #84 (FIR zero-flush), sample peak | `AnalysisBlock` | `TruePeakLive`, `TruePeakResult` |
| Spectrum | analyser | #87 (tilt is display-side), #88 (its own private 171 ms live front end), #90, #91 | `SpectralFrame`, `BandRecord`, active time (#104) | `SpectrumLive`, `SpectrumResult` |
| Stereo | analyser | #94–#97, #99 (time-domain broadband meter), #100 (scope points) | `SpectralFrame`, `BandRecord`, `AnalysisBlock` (broadband) | `StereoLive`, `ScopeLive`, `StereoResult` |
| Tempo | analyser | #107–#109, #115 (own private onset front end) | `AnalysisBlock` | `TempoResult` |
| Key | analyser | #107, #110, #111, #115 | `SpectralFrame` | `KeyResult` |
| Storage | persistence | #150 (layout), #151 (recovery journal), #152 (export/import), #164 (DB robustness) | `EntryHeader`, all stored sections, `Checkpoint`s | history DB, `RecoveryJournal` |
| Display / Compare | UI | #87, #92, #95, #100 drawing, #75 alignment, #54–#57 | `*Live`, stored sections | — |
| Processing | engine | #116–#129, #149, #153–#158 | `SourceAudio`, `SyncOutput`, `ChainConfig`; its own private loudness meters (#121) | processed audio, `PreStream`, `ChainOutStream`, `ProcessedStream`, `ChainState`, `ChainLatency` |
| Sync | engine + driver (§5.4) | #130–#145; #63, #66, #70 | `ChainLatency`, real device I/O timestamps, device events, virtual device properties | `SyncOutput`, `SyncStatus`, `DeviceCalibration`, `SyncConfig`, `DriverProperties` |

**Records (#103)**

| Record | Owner | Content | Lifetime |
|---|---|---|---|
| `CaptureStream` | Capture | raw float32 samples, overflow counts | ring (transient) |
| `AnalysisBlock` | Coordinator | fixed 100 ms block per channel (64-byte aligned), block index, flags (gap / zero-filled count, dual-mono, layout) | transient |
| `KWSubBlock` / `KWRecord` | LoudnessFrontEnd | weighted channel-sum energy per 100 ms (#85) | live / stored |
| `SpectralFrame` / `BandRecord` | SpectralFrontEnd | per frame: X_L, X_R and band sums; stored: per-1/24-band totals of P_L, P_R, C (#98) | live / stored |
| `<Analyser>Live` | each analyser | current values for display and menu bar | transient |
| `<Analyser>Result` | each analyser | `finish()` output = its history section | stored |
| `EntryHeader` | Coordinator | source, track, times, device rate, layout, tap point, chain state, gaps, duration, status and interruption reason (#163), every section's versions | stored |
| `DerivedResult` | Derived | trim duration (#75) and PLR (#79), with the source sections' versions | stored |
| `Checkpoint` | each module that implements `checkpoint()` | partial result at a checkpoint (#151) | journal |
| `RecoveryJournal` | Storage | checkpoints + `EntryHeader` draft, appended every 30 s (#151) | file, deleted after a clean Stop |
| `SourceAudio` | Capture | tap audio delivered inside the I/O callback (#116) | transient |
| `PreStream`, `ChainOutStream`, `ProcessedStream` | Processing | SPSC rings: pre-chain audio (#121); after utility, before gain stage and limiter (#121a); post-chain, pre-sync-delay audio for measurement (#128) | transient |
| `ChainConfig` | Processing | slots, plugins, parameters, presets | stored (prefs) |
| `ChainState` | Processing | bypass flags, A/B gain, loud-match gain and mode, failed stages; snapshot copied into `EntryHeader` | live |
| `ChainLatency` | Processing | stage latencies + I/O latency (#119) | live |
| `SyncOutput` | Sync | parameters of the Sync-owned output stage hosted at the end of the chain: padding, AV offset, fallback output gain (#117, #131, #140, #144; renamed from `SyncDelay` by V18) | live |
| `SyncStatus` | Sync | device, X, measured vs reported latency, lock state, calibration age and spread | live |
| `DeviceCalibration` | Sync (SyncStore) | per device: measurement history, applied value, method, self-check residual, version (#138) | stored |
| `SyncConfig` | Sync | X, margin, headroom, nudges, AV offsets per app/device (#131, #135, #140) | stored |
| `DriverProperties` | Sync (driver) | custom properties on the virtual device: X, clock-steering parameters, failsafe state, mirrored volume/mute (#136, #141, #144); transport per the #130 M0 result | live |
| `VirtualInput` | Sync (driver) | the virtual device's loopback input stream (transport (a), #130) | transient |

**Dependency table (#104)**

| Consumer | Provider | What is passed | When |
|---|---|---|---|
| Loudness | LoudnessFrontEnd | `KWSubBlock` | every 100 ms |
| Spectrum (#90) | LoudnessFrontEnd, via Coordinator | active time = count of `KWSubBlock` ≥ −70 LUFS × 100 ms | at `finish()` |
| Spectrum (#89, #91) | SpectralFrontEnd | `SpectralFrame`, `BandRecord` | per frame / at finish |
| Stereo (#97, #98) | SpectralFrontEnd | `SpectralFrame`, `BandRecord` | per frame / at finish |
| TruePeak, Stereo broadband, LoudnessFrontEnd, SpectralFrontEnd | Coordinator | `AnalysisBlock` | every 100 ms |
| Derived: trim duration (#75) | LoudnessFrontEnd, via Coordinator | `KWRecord` | at finish |
| Compare alignment (#75) | Storage | both entries' `KWRecord` (+ its version) | at view time |
| Compare level-match (#92, spectrum overlays) | Storage | both entries' `LoudnessResult.I` (+ its version) | at view time |
| Derived: PLR (#79) | TruePeak + Loudness, via Coordinator | `TruePeakResult.max`, `LoudnessResult.I` | at finish |
| Storage journal (#151) | every module with `checkpoint()`, via Coordinator | `Checkpoint` | every 30 s |
| Menu bar (#31) | Display | `LoudnessLive` (or `TruePeakLive`) | 2 Hz |
| Coordinator (post tap point, #128) | Processing | `ProcessedStream` | live, when tap point = post |
| Processing private meters (#121, #122b; inside one module) | Processing | `PreStream`, `ChainOutStream` | every block, on the control thread |
| Processing: hosted Sync output stage (#117) | Sync | `SyncOutput` | on change |
| Sync (#119 → §5) | Processing | `ChainLatency` | on change |
| Capture, in driver mode (`SourceAudio`) | Sync driver | `VirtualInput` | every I/O cycle |
| Sync engine (volume/mute forwarding, #144) | Sync driver | `DriverProperties.volume` / `mute` | on change |
| Key (#110) | SpectralFrontEnd | `SpectralFrame` (mid = (X_L + X_R)/2) | per frame |

**Violations in #74–#101 and smallest fixes (#105, approved; V15–V22 from the Part 7 re-check are in §3.6)**

| V | Where | Violation | Smallest fix | Cost |
|---|---|---|---|---|
| V1 | #80 / §1.7 module shape | `loudness_process` does K-weighting, gating *and* true peak | Split: LoudnessFrontEnd (provider) + Loudness (analyser) + TruePeak (analyser) | none |
| V2 | #84 | the true-peak FIR flush is part of the loudness end-of-measurement rule | Move it to `TruePeak.finish()` | none |
| V3 | #79 | PLR combines two analysers' results | `DerivedResult` computed by the Coordinator at finish, storing both source versions | none |
| V4 | #90 | Spectrum needs loudness sub-blocks for active time | Read them from LoudnessFrontEnd via the Coordinator, never from Loudness. The provider runs whenever any enabled consumer needs it, so disabling Loudness leaves Spectrum unchanged | none |
| V5 | #85 | the stored sub-block record had no owner | `KWRecord`, owned and versioned by LoudnessFrontEnd, stored as its own section | a few bytes |
| V6 | #75 | trim and alignment had no stated owner, and no version check | Duration: Coordinator → `EntryHeader`. Alignment: Compare. Both record the `KWRecord` version used | none |
| V7 | #88 | live-spectrum hop = fs / display fps couples analysis to display settings (30 / 60 / 15 fps, #60) | Fixed hop = round(fs/30) whatever the display rate; display samples the latest `SpectrumLive` | at 60 fps updates stay at 30/s, masked by Slow smoothing; at 15 fps ~30 FFTs/s of 8k per channel keep running while visible (estimate <0.1% CPU) |
| V8 | #53 / #60 | Low Power Mode "pauses the background spectrum", so stored results depend on power state | Never pause stored analysis; power state only changes display rate and live-only work | #89 frames keep running: ~12 FFTs/s of 32k per channel (estimate <0.2% CPU) |
| V9 | #80 | re-blocking inside `loudness_process`, so each analyser would re-block on its own | Coordinator re-blocks once into `AnalysisBlock`; every module gets identical blocks | one copy of ~384 KB/s at 48 kHz stereo (negligible) |
| V10 | #80 | gaps (ring overflow) handling was undefined per analyser | Coordinator zero-fills lost samples (keeping the 100 ms grid) and flags the block; `EntryHeader` records the gap | none |
| V11 | #82 | FTZ was set "on whichever thread runs the filters" | FP environment set by the owner of each thread (Coordinator for analysis threads; see V16 for Processing and Sync), identical in live, offline and CI; modules must not change it | none |
| V12 | #86 / #91 / #98 | band table used by both Spectrum and Stereo had no owner | Owned and versioned by SpectralFrontEnd | none |
| V13 | #92 | level-match reads another analyser's result | Allowed only in Compare (view time). If either `LoudnessResult` is missing, the toggle is disabled; if versions differ, it's labelled | none |
| V14 | rule (6) | bit-identity can be broken by buffer alignment or shared FFT setups `[MEM: whether vDSP takes alignment-dependent code paths is unverified]` | 64-byte-aligned buffers everywhere; each module creates its own read-only FFT setups; no multithreaded reductions inside a module | memory only |

**Compare with differing versions (rule 5):**
- Every Compare table row and overlay shows the section versions when they differ between entries, e.g. `spec v2 ≠ v3`.
- Overlays are drawn only with that label visible.
- File entries can be re-analysed to the current version.
- When only a derivation changed, the stored provider record can be re-derived: W/ρ from `BandRecord`, alignment from `KWRecord`.

**Ownership of every decision:** Parts 5–7 list module, reads and writes per decision (§3.5, §5.4, §3.6).

**Cost of the rule:** no accuracy cost. CPU cost only from V7 / V8, estimated <0.3% of one core combined (unprofiled); the always-on DSP as a whole was measured at ≈0.27% of an M2 performance core (#161).

### 3.5 Processing chain (design review Part 5, 2026-10-06)

| # | Decision | Module | Reads | Writes |
|---|---|---|---|---|
| ✅ 116 | **Engine topology.** Tap-mode processing: a process tap on the source app with mute-when-tapped feeds an aggregate device (tap + the app's output device, one clock). One I/O proc: input = tap, output = device; the render chain runs on the I/O thread (the #80 exception). Driver mode replaces the tap with the virtual device (§5). | Processing (chain), Capture (tap) | `SourceAudio` | `PreStream`, `ChainOutStream`, `ProcessedStream`, `ChainState`, `ChainLatency` |
| ✅ 117 | **Stage order (refines #3):** eq → comp → fx[0..7] → utility → **gain stage (loud-match gain + A/B compensation gain)** → **limiter** → **Sync output stage** (padding, AV offset, fallback volume gain; `SyncOutput`, V18) → output. Every stage bypassable. **The limiter is active whenever any stage or gain in the chain can boost:** any third-party plugin enabled (its gain can't be known), or any md3 gain > 0 dB. It's off only when the chain is entirely bypassed or contains only md3/Apple stages with no positive gain. Limiter = AUPeakLimiter at −1 dBFS (sample-peak `[MEM]`); its latency is included in #119. The Sync output stage is owned by Sync and hosted here; with the driver absent it is a pass-through. | Processing; Sync owns its output stage | `SyncOutput` | — |
| ✅ 118 | **Utility stage (in-house, small):** gain, per-channel polarity, L/R swap, mono (M only), width (S gain), and **bass mono = LR4 high-pass on S plus the matching LR4 all-pass on M** (fc default 120 Hz). Separation −80 dB at 1 kHz, zero latency (a side-only high-pass gives −15 dB). Exception to #72's "no DSP from scratch", limited to matrix / gain / 2nd-order sections. Tests: offline scipy reference within 1e-6; mono-sum magnitude flat ±0.001 dB; separation ≤ −60 dB from 5·fc up (≈ −30 dB at 2·fc; `p5f_sim.py`, corrected 2026-10-07). | Processing | `ChainConfig` | — |
| ✅ 119 | **Latency:** each stage's reported latency (`[MEM]` AUAudioUnit.latency / kAudioUnitProperty_Latency). Bypassing a stage keeps its latency (compensating delay), so bypass and A/B never move audio in time. `ChainLatency` = stage latencies + I/O latency (buffers + safety offsets), sent to Sync and shown in the status line. In tap mode a lip-sync offset of about the I/O latency remains; in driver mode it's absorbed into X. | Processing | stage reports, device latency | `ChainLatency` |
| ✅ 120 | **Processing on/off (#6):** with every stage off, md3 unmutes the original and drops its path (zero latency); the switch has a discontinuity of about the I/O latency. A/B never uses this path. | Processing, Capture | `ChainConfig` | `ChainState` |
| ✅ 121 | **Level-matched A/B:** Processing owns private pre- and post-chain loudness meters (LoudnessFrontEnd code, its own instances), with no dependency on the Loudness analyser. **They don't run on the I/O thread.** They read the pre-chain audio from `PreStream` and the post-chain audio from `ChainOutStream` (#121a), and run K-weighting, gating and gain calculation on a control thread. Only the resulting gain goes to the I/O thread, atomically. Compensation on the processed side = I_pre − I_post since the last chain change (BS.1770 gating), using the short-term difference for the first 3 s; 50 ms gain ramps; clamped ±24 dB. **Added delay in the gain response:** ring transit + ~10 ms polling, ≤ ~20 ms. Including the 100 ms sub-block granularity, a new gain reaches the audio 1–2 sub-blocks after the audio it was measured on. **Tests (re-run with 0/1/2 sub-blocks of delay, `p5d_sim.py` / `p5e_sim.py`):** pure +6 dB chain → −6.000 dB at 3 s (error 0.000) at all delays; EQ chain on pink noise → compensated I − input I = −0.001 LU and worst short-term mismatch 0.055 LU at all delays. All three #121 tests pass. *Known behaviour (not a delay effect):* on music, a frequency-dependent chain makes the compensation wander, because the integrated difference depends on content; 0.26–0.29 LU integrated difference after 3 s in the simulation, for delays 0–2. | Processing | `PreStream`, `ChainOutStream` | `ChainState.abGain` |
| ✅ 121a | **Post-meter tap point:** `ChainOutStream`, an SPSC ring taken after the utility stage and before the gain stage and limiter. The A/B and loud-match post meters read it, so they never measure their own gain (reading `ProcessedStream` would create a feedback loop). `ProcessedStream` stays the post tap point for measurement (#128). Cost: one extra copy per block. | Processing | — | `ChainOutStream` |
| ⛔ 122a | **Considered and deferred (not in v1): known-track static gain** from a stored measurement. Reasons: wrong-match risk (a different master of the same title, changed source normalisation or app volume), and it would create a Storage → Processing dependency. | — | — | — |
| ✅ 122b | **`loud match`, live estimator (v1):** gain = target − integrated-since-segment-start (reset on track change, source change, or manually); up 0.5 dB/s, down 10 dB/s; ceiling: momentary output ≤ target + 6 LU; max boost +6 dB; no boost for the first 10 s; followed by the #117 limiter. **These parameters are provisional;** a build-phase check on real tracks confirms them. Default target −16 LUFS, user-set. With the control-thread meters (#121), the ceiling acts 1–2 sub-blocks late; simulated overshoot rises from +5.6 to +6.0 LU short-term and from +7.0 to +8.1 LU momentary (`p5d_sim.py`). **Status-line wording carries the known limits:** `loud: live ~±2 LU` (accuracy after long quiet intros) and the fact that dynamics change, e.g. `loud: live, adjusts dynamics`; exact wording in UI design. | Processing | `PreStream`, `ChainOutStream` | `ChainState.loudGain` |
| ✅ 123 | **Factory presets:** `flat`; `mono`, `bass mono` (#118); `night` (AUMultibandCompressor or AUDynamicsProcessor + limiter); `voice` (AUNBandEQ + AUDynamicsProcessor); `loud match` (#122b). **`bt sync` removed**: sync state belongs to Sync. Parameter values for night/voice are a listening task. | Processing | `ChainConfig` | `ChainConfig` |
| ✅ 124 | **Preset switching:** parameter-only changes applied directly (md3-owned parameters ramp over 20 ms). Switching plugins crossfades old and new chains over 50 ms (briefly 2× CPU). Loaded plugins reused (#62). | Processing | `ChainConfig` | `ChainState` |
| ✅ 125 | **Render-chain failure isolation:** <br>• A stage that returns an error, outputs NaN/±infinity, or overruns its budget (> 50% of the buffer period in 3 of the last 20 callbacks, provisional, §15) is auto-bypassed (latency-compensated, 20 ms crossfade) and flagged; the others continue. A final guard replaces NaN/infinity with 0 before the device. <br>• **Engine watchdog:** a thread independent of the I/O thread polls an atomic render counter every 50 ms. If no buffer has been rendered for **200 ms** while processing is active and the device reports running, it **removes the muting tap**, so the original audio returns. It's suppressed during deliberate reconfiguration (device change, sample-rate change). 200 ms ≈ 19 buffers at 512 frames / 48 kHz; target for audible original audio ≤ 500 ms including tap teardown (teardown time measured in M0). Not covered: a hang of the whole md3 process (every thread); documented, with an external helper as a possible later addition. **Failure-injection test:** block the render callback; the original audio is back within 500 ms (measured by loopback), and no other module's output changes. <br>• **Out-of-process plugin hosting (M0 check, §14):** can third-party AUv2 and AUv3 load out of process on Apple Silicon, and at what latency and CPU cost per plugin? `[MEM: believed to be a host instantiation option; unverified]`. **If it works:** third-party plugins load out of process by default, so a plugin crash loses only that plugin (auto-bypassed and flagged); Apple's built-in units and the utility stage stay in process. **Fallback if it doesn't:** in-process hosting with the watchdog. If md3 crashes, the tap disappears and the original audio returns (M0 check). On the next launch after an unclean exit (a "clean exit" flag plus a record of which plugin slots were active), md3 starts in **safe mode**: the third-party plugins that were active are disabled, and the user can re-enable them one at a time. Recording which plugin was rendering on every callback would cost too much. | Processing | render counter, device state | `ChainState.failedStages`, watchdog events |
| ✅ 126 | **Output device and clocks:** processing outputs to the device the source app plays to (same clock). If the user fixes another device, an aggregate device with drift correction is used (quality measured in M0 with #67). | Processing, Capture | device list | — |
| ✅ 127 | **"system (all)" processing:** global tap excluding md3's own process (no feedback). | Capture | — | `SourceAudio` |
| ✅ 128 | **Post tap point:** Processing writes the post-chain, pre-sync-delay signal to `ProcessedStream`; the Coordinator consumes it when the tap point is "post". md3 never taps its own device output. `EntryHeader` records the tap point and a `ChainState` snapshot. | Processing → Coordinator | `ProcessedStream` | `AnalysisBlock` |
| ✅ 129 | **Tests:** <br>• Impulse through every bypass combination: output position constant. <br>• #121 / #122b / #118 tests. <br>• Stage failure injection (NaN AU, slow AU): bypassed within N callbacks, other stages bit-identical. <br>• #125 watchdog test. <br>• Tap point "pre": all analyser sections bit-identical regardless of chain state. | Processing | — | — |

**Evidence:** scripts `p5_sim.py`, `p5b_sim.py`, `p5c_sim.py` (bass mono variants, loud-match variants), and `p5d_sim.py`, `p5e_sim.py` (control-thread delay). Tables in the review status document §11.

### 3.6 Real-time architecture (design review Part 7, 2026-10-06)

| # | Decision | Module | Reads | Writes |
|---|---|---|---|---|
| ✅ 146 | **Thread model:** I/O thread(s) (real-time; Capture / Processing); one **analysis thread** (Coordinator: providers then analysers in a fixed order, deterministic); **control thread** (Processing meters, A/B, loud match; Sync's DLL updates with separate state); **watchdog thread** (#125, and the analysis-stall check below); **storage writer** (background); **file-analysis workers** (#59, one Coordinator + module set per job, no shared instances, V19); **Calibrator** (Sync, own mic I/O, V22); **main/UI**. Analysis and control at QoS *utility*; results don't depend on QoS or core type. <br>**Analyser time budget:** the Coordinator times every provider and analyser call per 100 ms block. A module that takes more than **5 ms for a block in 10 of the last 50 blocks** (provisional, §15; ~30× the measured cost of the largest kernel) is disabled for the rest of that entry, and its section is marked `failed` with the cause; consumers of a disabled provider are marked `failed` too (V20). The others continue on the same blocks, so their outputs are unchanged. <br>**Analysis-thread stall:** before each module call the Coordinator writes the module's id to an atomic "current module" marker and bumps a progress counter. If the watchdog sees no progress for **2 s** while blocks are pending (provisional), it records "analysis stalled in *module*" in the entry. The ring (#147, ≥ 4 s) absorbs the stall. If the stall outlasts the ring, the entry ends as interrupted and is saved from the last checkpoint (#151), and the stalled module starts disabled in the next measurement until md3 restarts. **Tests (in #106 (d) and #162):** a deliberately slow analyser is disabled and every other section is byte-identical to the normal run; a blocked analyser is detected within 2 s and the entry is recovered with the cause recorded. | Coordinator, watchdog | timing, progress counter | section status, `EntryHeader` |
| ✅ 147 | **Capture ring (closes #80 sizing / overflow):** SPSC, lock-free, capacity = next power of two ≥ 4 s of frames (262,144 frames at 44.1/48 kHz; 524,288 at 88.2/96; 1,048,576 at 192); interleaved float32 (2 MiB stereo at 48 kHz, 8 MiB at 192 kHz); C11 acquire/release indices on separate cache lines. Overflow: the producer never blocks; it drops the whole callback block and adds to an atomic `droppedFrames` with the first dropped sample time. Gaps are also detected from tap sample-time discontinuities. The consumer zero-fills both, keeps the 100 ms grid, flags the `AnalysisBlock`, and `EntryHeader` records "gapped (x ms lost)". | Capture → Coordinator | `CaptureStream` | `AnalysisBlock` |
| ✅ 148 | **Polling:** the analysis thread wakes on a **20 ms** timer with 5 ms leeway, only while a consumer is active; no timer when idle (#51). | Coordinator | — | — |
| ✅ 149 | **Processing rings:** `PreStream` and `ChainOutStream` hold 1 s (65,536 frames at 48 kHz); overflow → the private meters hold their last gain and mark it stale. `ProcessedStream` is on the measurement path and follows #147 exactly. | Processing | — | rings |
| ✅ 150 | **Storage layout (closes #85 / #98 storage; refines #26, #58):** SQLite via GRDB. `entries` (typed columns: source app, artist, title, group, start, duration, device rate, tap point, status, interruption reason, lost ms; plus `header` JSON with the `ChainState` snapshot and every section's versions); `sections` (entry_id, kind, schema_version, algorithm_version, status ok / failed / absent, payload; key (entry_id, kind)); `groups` (#23). Small results as JSON; arrays in a binary container (16-byte header: magic `MD3A`, kind u16, schema u16, dtype u8, little-endian flag, count u32, reserved; then little-endian data). `KWRecord` float32 at 10 Hz = 40 B/s; `BandRecord` 3 × ~240 float32 = 2.9 KB; a typical 3-minute entry ≈ 12 KB. I, LRA and true peak stay as computed live (double) in their own sections. Migrations via GRDB's migrator. One write at Stop (#58) plus the journal (#151). | Storage | sections, `EntryHeader` | DB |
| ✅ 151 | **Crash-safe recording, through the module interface** (extends #13): every 30 s the Coordinator calls `checkpoint()` on each module that implements it and passes the returned partial results to Storage, which appends them with the `EntryHeader` draft to the `RecoveryJournal`. **Storage journals only what modules return; it never reads module state.** After a crash, the next launch offers an "interrupted (recovered)" entry built from the last checkpoint; a module without `checkpoint()` is marked `absent` in it. The journal is deleted after a clean Stop. Expected implementers in v1: LoudnessFrontEnd (`KWRecord` so far), Loudness (M/S/I/LRA so far), TruePeak (max so far), SpectralFrontEnd (`BandRecord` totals), Spectrum and Stereo (partial results); Tempo and Key optional. **Test:** `kill -9` mid-measurement → the recovered sections equal each module's own checkpoint output byte for byte, and modules without `checkpoint()` are `absent`. | Coordinator, Storage, every module | `Checkpoint`s | `RecoveryJournal` → entry |
| ✅ 152 | **Export/import (refines #25):** JSON per entry with header and sections, each carrying schema and algorithm versions and status; CSV summary export. Import validates versions; imported entries keep their versions, so Compare labels any difference. | Storage | DB | files |
| ✅ 153 | **Closes #72:** each processing page is a plugin slot pre-loaded with an Apple AU (AUNBandEQ, AUDynamicsProcessor; AUPeakLimiter and AUMultibandCompressor available), drawn by md3 from the AU parameter tree, with `[swap ▾]` to any AU. A third-party AU gets a generic parameter list and its own editor (#156). | Processing, Display | `ChainConfig`, AU parameter tree | `ChainConfig` |
| ✅ 154 | **Closes #2:** `fx` page with up to 8 slots (fx[0..7], #117). | Processing | `ChainConfig` | — |
| ✅ 155 | **Closes #1(A):** AUv3 + AUv2 in v1; VST3 later; no CLAP. AUv2 loading follows the #125 out-of-process M0 result and the safe-mode fallback. | Processing | — | — |
| ✅ 156 | **Closes #4:** plugin editors in separate floating windows; a generic parameter list when a plugin has none. Editors reach plugins only through the AU parameter tree / state API. | Display, Processing | AU views | — |
| ✅ 157 | **Closes #9:** named chain presets storing each slot's full AU state plus md3 parameters, never Sync state (#123). Auto-load precedence: app + device > app > device > last used. Plugins keep their own presets. | Processing | `ChainConfig` | `ChainConfig` |
| ✅ 158 | **Closes #62:** load a plugin when its slot is enabled; keep bypassed plugins loaded; reuse loaded plugins across preset changes (#124). | Processing | — | — |
| ✅ 159 | **Modularity re-check after Parts 5–6:** violations V15–V22 and fixes (table below). | — | — | — |
| ✅ 160 | **Shared code libraries:** recorded as rule (9) of #102. | all | — | — |
| ✅ 161 | **CPU budget (#61, §6.1):** measured always-on DSP kernels (Accelerate, Apple M2, 30 s stereo): true peak at the #76a size 0.15% of a performance core (0.41% efficiency core); K-weighting 0.03 (0.09); FFT 32768 hop 4096 0.07 (0.22); tempo FFT 0.02 (0.06); total ≈ 0.27% (≈ 0.78%) while measuring with the dropdown closed; live spectrum 0.05 (0.12) when visible. Not included: band mapping, chroma, gating, ring copies, wake-ups, I/O thread, drawing, SQLite. The target is measured at the shipping QoS with everything included. If over budget, mitigations in order, none changing stored results: the exact #76 skip bound; dropping live-only work while hidden; profiling fixes. Never: reduce stored-analysis accuracy, decimate, or pause stored analysis. | Coordinator | — | — |
| ✅ 162 | **Tests (Part 7):** ring stress (analysis stall 3.9 s → no loss; 4.5 s → gap recorded, zero-filled, grid intact) and ThreadSanitizer on all rings; 4 files analysed concurrently vs sequentially → byte-identical; storage round-trip bit-exact, export → import identical, migration test; #151 recovery test; #146 slow and blocked analyser tests; #163 and #164 tests; §6 10-minute performance run at shipping QoS. | all | — | — |
| ✅ 163 | **Lifecycle events during a measurement** *(coverage check)*: (1) output device, sample-rate or format change; (2) system sleep; (3) the source app quitting or its tap becoming invalid (permission revoked, process replaced). **In every case the entry ends and is saved as `interrupted` with the reason** (`device changed`, `rate changed`, `format changed`, `sleep`, `source quit`, `tap invalid`), via each module's `finish()` where possible, otherwise from the last checkpoint (#151). **Audio is never resampled to continue an entry**: analysers are initialised for one sample rate and layout per entry (#102). md3 does not start a new entry by itself (D8); the status line offers Start. For sleep: md3 finishes the entry on the will-sleep notification `[MEM]`; on wake it re-establishes taps, the processing chain and the clock lock without measuring. Previously only §7 mentioned "recovery from sleep/wake and device changes" and the source-app-quit case. **Tests:** each event injected during a measurement → one `interrupted` entry with the right reason, no resampled data, other state intact. | Capture, Coordinator | device / workspace / tap notifications | `EntryHeader.status`, entry |
| ✅ 164 | **History database robustness** *(coverage check; not covered before)*: <br>• **Unreadable or corrupt** (open or `PRAGMA integrity_check` fails): move it aside as `history-unreadable-<timestamp>.sqlite` (never deleted), start a fresh DB, and show a one-line notice. <br>• **Written by a newer md3** (schema version above the known one): open **read-only**, show history, and save new entries as #152 JSON files in a `pending/` folder. They're auto-imported when the DB is writable by this version or a newer one. <br>• **Rolling backup:** at launch, at most weekly, copy the DB with SQLite's online backup API; keep the last 4. <br>**Tests:** corrupt file, newer schema, and missing file → no data deleted; pending entries imported later byte-identical to direct saves. | Storage | DB file | DB, `pending/`, backups |

**#159 — violations V15–V22 and fixes (approved)**

| V | Where | Violation | Fix | Cost |
|---|---|---|---|---|
| V15 | #121 | Processing's private meters reuse LoudnessFrontEnd code | Rule (9) of #102 | none |
| V16 | #82 / V11 | Processing (I/O + control threads) and the Calibrator also run DSP | Each module sets the FP environment on the threads it owns; the I/O thread sets it at the start of every callback (cheap, idempotent; whether the HAL resets it is an M0 item) | negligible |
| V17 | #75, #79 | Trim and PLR were unversioned algorithms inside the Coordinator | The **Derived** module, with versions `derived.trim` / `derived.plr` | none |
| V18 | #144 | The volume fallback gain is Sync logic inside Processing's render chain | One Sync-owned output stage hosted at the end of the chain; `SyncDelay` renamed `SyncOutput` {padding, avOffset, outputGain} | none |
| V19 | #59 | Concurrent file analysis could share provider instances | One Coordinator + module set per job; #162 concurrency test | memory per job |
| V20 | rule (8) | Provider failure undefined | A failed provider marks every consumer `failed`, with the cause | none |
| V21 | rule (5) | Compare with `failed` / `absent` / recovered sections | Labelled like version differences; never silently overlaid or left blank | none |
| V22 | #130 / #132 | The Calibrator opens the built-in mic outside Capture | Allowed: Sync owns its mic I/O and never touches `CaptureStream`; calibration asks the user to pause playback (the sweep shares the output device; the global tap excludes md3, #127) | none |

---

## 4. Measurement & accuracy

### 4.1 Measurement set

Integrated / short-term / momentary LUFS, LRA, true peak (8× / 4× / 2× oversampled to ~384 kHz, #76 / #76a), sample peak, PLR, spectrum (live + averaged), width spectrum, correlation, goniometer, balance, tempo and key (#107–#115), loudness curve over time (#85).

### 4.2 Measurement decisions ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ✅ 12 | Standard | **Decided 2026-10-08 (§17):** ITU-R BS.1770-5 / EBU R128. K-weighting recalculated per sample rate (settled in substance by the design review). |
| ✅ 13 | Controls | **Decided 2026-10-08 (§17):** Start/Stop + Reset, **no pause**. Stop always saves; Reset discards. Extended by #151 (crash recovery) and #163 (interruptions). |
| ✅ 14 | Accuracy bar | **Decided 2026-10-08 (§17):** ±0.1 LU against the EBU compliance set, checked in CI. |
| ⛔ 15 | ~~Spectrum defaults~~ | Superseded by #86–#89 (§4.5). Kept from the original: 1/6-octave default smoothing, 20 Hz–20 kHz, −90 to 0 dB, all adjustable. |
| ⛔ 16 | ~~Width spectrum definition~~ | Superseded by #94–#98 (§4.6). The definition is kept: width = side / (mid + side) energy per 1/3-octave band (bar height), correlation per band (bar colour), live plus per-measurement. |
| ✅ 45 | Accept the accuracy targets below? | **Decided 2026-10-08 (§17):** Yes, as rewritten by #76, #93, #101, #113. |
| ✅ 46 | Publish a compliance report in the docs? | **Decided 2026-10-08 (§17):** Yes; CI output structured for it from build step 2, published at release. |
| ✅ 167 | Normalisation preview (amends D10) | Optional, **off by default**, numbers only, no advice: e.g. `spotify −14: −4.9 dB · apple −16: −6.9 dB`. Platform reference levels are editable in Prefs because they change; the shipped defaults are checked against each platform's documentation before release (`[MEM]`). |
| ⛔ 73 | ~~Key / BPM: v1 or later?~~ | Superseded by #107–#115 (§4.7). Kept: written in-house; calculated during measurements and file analysis; shown on the track line; stored in history; milestone after M3. |

### 4.3 Verification references

| Feature | Reference | Pass target |
|---|---|---|
| M / S / I LUFS | ITU-R BS.1770-5, EBU Tech 3341, ITU-R BS.2217 | ±0.1 LU |
| LRA | EBU Tech 3342 | ±1 LU (spec); target ±0.1 |
| True peak | EBU Tech 3341 Table 1, signals 15–23 (tolerance is Tech 3341's; the under-read itself is described in BS.1770 Annex 2, Appendix 1) | +0.2 / −0.4 dB (spec); target ±0.1 dB for content up to 20 kHz (#76) |
| PLR | Derived from TP and integrated | Same as its inputs |
| All loudness | Cross-check against libebur128 (MIT) on a real-music library | ≤0.05 LU |
| Spectrum | Per #93: sines at IEC band centres; deterministic multisines; 0 dBFS 50 Hz leakage sine; random noise as sanity check only | Sines ±0.1 dB from 150 Hz (live) / 40 Hz (averaged), maximum in the correct band; slope flat / +3.01 dB/oct ±0.05 dB; leakage < −90 dB from 200 Hz; noise within 4.34/√(B·T) dB |
| Correlation / width | Per #101: deterministic mono, polarity flip, quadrature pair (R = Hilbert(L)), panned mono R = g·L, left-only; broadband correlation and balance with tones and pans | ±0.01 per band 40 Hz–16 kHz (averaged); left-only: W = 0.5, ρ undefined; independent noise only as a sanity check |
| Width spectrum | Per #101: one band anti-phase, all others mono (S2 method) | ±0.02 band independence from 200 Hz on #89 frames |
| Goniometer | Per #100: mono, L-only, R-only, anti-phase cases; cross-checked against Logic's MultiMeter | Orientation as defined in #100 |
| BPM | GiantSteps Tempo (current annotations), Ballroom, plus a non-EDM set (MIREX metrics, #114) | Provisional expectations (#113), not pass marks: GiantSteps Acc1 ≥60% / Acc2 ≥88%; Ballroom Acc1 ≥65% / Acc2 ≥95%. Ship gate set from the first measured benchmark |
| Key | GiantSteps Key (MIREX weighted, #114) | Provisional expectation (#113): weighted ≥60%; labelled as an estimate in the UI; ship gate set from the first measured benchmark |
| Sample rates | 44.1 / 48 / 88.2 / 96 / 192 kHz | Same targets |
| Capture path end to end | Play a file in Music vs analyse the same file directly | ≤0.05 LU |

**Known limits:** resampling when the file and device rates differ (true peak can shift by about 0.1–0.3 dB; each entry records the device rate); lossy encoding on streaming services (a real difference in the audio, not an error); app volume and normalization (recorded, not corrected).

### 4.4 Loudness engine ✅ (design review Parts 1 & 1b, 2026-10-06)

| # | Decision |
|---|---|
| 74 | **Mono files** are analysed as dual-mono stereo, matching how players output them. |
| 75 | **Silence trim** (first and last 100 ms sub-block ≥ −70 LUFS momentary; computed by the Derived module, V17) sets **reported duration only**, never overlay alignment. **Overlays are aligned** by normalised cross-correlation of momentary loudness: momentary is rebuilt from 4 stored sub-blocks (#85), converted to dB and **clamped at −70 LUFS**; mean removed; computed only over each entry's trimmed span, normalised over the overlap at each lag; ≥50% overlap required; correlation peak refined parabolically. Silence inside the span stays at the clamp (silence lining up with silence counts as alignment evidence). **Fallback:** if the peak correlation is <0.8, or >50% of the overlap is at the floor, align by trim points and mark the overlay "unaligned". |
| 76 | **True peak:** fixed ~384 kHz effective rate: 8× at 44.1/48 kHz, 4× at 88.2/96 kHz, 2× at 192 kHz. Polyphase FIR, **32 taps per phase**, equiripple (Parks-McClellan) design: passband edge 20 / 40 / 80 kHz respectively, stopband edge at fs − passband edge, stop:pass weight 2:1. **Parabolic refinement at every local maximum** of the oversampled signal, not only at the largest sample. Target: **±0.1 dB for content up to 20 kHz** (simulated worst case at 44.1 kHz: −0.008 / +0.069 dB). Above 20 kHz the FIR transition band dominates the error (−0.34 dB at 20.5 kHz, −1.3 dB at 21 kHz). *Deferred optimisation, only if profiling calls for it:* for max-hold, skip interpolation for any window where max\|x\| × (largest phase L1 norm) × 9/8 < current peak. This is exact, **valid only when the parabola is fitted on \|y\| (all three points non-negative)**; with signed fits the factor is 5/4. Measured margin: a window must sit 9.20 dB (44.1k) / 8.22 dB (96k) / 7.05 dB (192k) below the held peak to be skipped, so expect little gain on loud masters. Max-hold only: not usable for a true-peak-over-time curve. **Build-phase test (added 2026-10-06):** cross-check true peak on several hard-clipped / heavily limited 44.1 kHz masters against an ideal band-limited reference (offline FFT or long-sinc interpolation) and against libebur128, and report the differences. libebur128 is a comparison point, not ground truth: its own interpolator has its own error. If the gap on real material exceeds 0.1 dB, revisit the passband edge. **The 44.1 / 48 kHz designs are amended by #76a (provisional) below.** |
| 77 | **Integrated gating** uses an exact list of block energies (no histogram). |
| 78 | **LRA percentile:** nearest rank on the sorted gated short-term values, 1-based index `round((n−1)·p/100 + 1)`, rounding halves away from zero (MATLAB `round`; Swift `.rounded()`, never `rint`). Both gates use `>=`; the relative gate (−20 LU) is taken from the mean power of the absolute-gated values; short-term rate ≥10 Hz. Verified verbatim against the Tech 3342 (2023) §5 MATLAB code; pinned in tests against the Tech 3342 reference values. |
| 79 | **PLR** = ungated whole-measurement true-peak max of both channels − I; computed by the Derived module (V17). |
| 80 | **Capture thread rule:** the metering capture callback does no DSP; it only copies samples into the lock-free SPSC ring (#147) and counts overflows. The Coordinator re-blocks the stream once into fixed 100 ms `AnalysisBlock`s aligned to the sub-block grid (V9), so every provider and analyser runs on identical block boundaries however the input arrives; vectorised reductions change their last bits with block length, which is why this matters. The same path serves live and offline file analysis. App Nap is disabled while measuring; polling every 20 ms (#148); gaps per #147. Exception: when processing, the render chain runs in the I/O callback (#116). Thread model: #146. Chunk-size bit-identical test: #106 (c). |
| 81 | **Tap type:** stereo-mixdown process taps in v1. "system (all)" = stereo mixdown of all processes except md3, before device volume. Surround channel weights apply only to file analysis; 5.x file entries are labelled as not directly comparable with stereo playback. M0 verifies the `CATapDescription` API and tap behaviour when the output device changes. |
| 82 | **Flush-to-zero** on every thread that runs DSP (analysis, file-analysis workers, CI, Processing's I/O and control threads, the Calibrator), set by each thread's owning module (V11, V16). Without it the 38 Hz high-pass state reaches the denormal range after ~3 s of digital silence. Kept even though v1 is Apple Silicon only (§6). |
| 83 | **Dual-mono label:** "File" readings of mono files are marked `dual-mono` in the UI and in exports (`channel_mode: "dual-mono"`). ffmpeg/libebur128 report 3.01 LU lower unless told the file is dual-mono. |
| 84 | **End of measurement:** integrated loudness uses complete 400 ms blocks only, and LRA complete 3 s short-term windows only, in both live and file paths; the trailing partial block is dropped. True peak: at Stop or end of file, `TruePeak.finish()` flushes the polyphase FIR with zeros for its own length (V2). **That is the only flush; no silence padding.** The Tech 3342 §5 comment asking for ≥1.5 s of trailing silence in file-based measurements describes the reference function's input, for meters whose short-term value lags the audio. md3's windows end at the current tick, so there is nothing to compensate. Measured: padding shifts I by up to −0.033 LU on the Tech 3341 vectors and leaves LRA unchanged on the Tech 3342 vectors (table below). |
| 85 | **History storage:** store (as `KWRecord`, owned by LoudnessFrontEnd, layout #150) the 100 ms sub-block energy (weighted channel sum, linear, float32; digital silence = 0) at 10 Hz instead of the short-term curve. Momentary and short-term are rebuilt from it; #75 alignment uses it. |

#### #76 reproduction

- **Environment:** Python 3.13.1, numpy 2.2.4, scipy 1.16.1. Script `tp_table76.py` (to be committed under `tools/`, §4.8); run `python3 tp_table76.py`.
- **Filter design:** `scipy.signal.remez(numtaps=L·32, bands=[0, fp, fs−fp, L·fs/2], desired=[1, 0], weight=[1, 2], fs=L·fs)`, then scaled so Σh = L. The near-ideal reference row uses `scipy.signal.firwin(L·128, fs/2, window=('kaiser', 8), fs=L·fs)`.
- **Estimator:** zero-stuff by L, convolve with h, apply a parabola at every local maximum of \|y\| (fitted on sign-adjusted values s·y, which equals \|y\| here because the neighbours of a peak share its sign at these rates), take the max.
- **Test signal:** Gaussian bursts of N = 2048 samples. Frequency f ~ U(1 kHz, fmax). Length in cycles c ∈ {1, 1.5, 2, 3, 6}, with σ = c/(2f). Centre t0 = N/(2·fs) + U(0, 1/fs). Phase ~ U(0, 2π). Band-limited by FFT brickwall at fmax, normalised to 0.5 peak.
- **Reference:** exact band-limited peak via 256× FFT zero-padding interpolation. Error = 20·log10(estimate / reference).
- **RNG and trials:** `numpy.random.default_rng(7)`, one generator shared by all cases, run in the table order below.

| fs | Factor | Taps/phase | Passband | Content ≤ | Trials | Error (dB) |
|---|---|---|---|---|---|---|
| 44.1k | 8× | 128 (Kaiser β=8, near-ideal) | — | 20 kHz | 1500 | −0.002 / +0.001 |
| 44.1k | 8× | 32 | 20k | 20 kHz | 4000 | **−0.008 / +0.069** |
| 44.1k | 8× | 32 | 20k | 21 kHz | 2000 | −0.405 / +0.068 |
| 48k | 8× | 32 | 20k | 20 kHz | 3000 | −0.002 / +0.001 |
| 96k | 4× | 32 | 40k | 40 kHz | 1500 | −0.026 / +0.003 |
| 192k | 2× | 32 | 80k | 80 kHz | 1500 | −0.327 / +0.008 |
| 192k | 2× | 32 | 80k | 20 kHz | 1500 | −0.001 / +0.001 |

The 44.1k / 32-tap filter has passband ripple +0.042 dB and stopband −58.1 dB. The +0.069 dB worst case is that ripple; 40 taps per phase would cut it to ~+0.02 dB for 25% more CPU (not adopted). Without refinement, even the near-ideal filter under-reads by up to −0.106 dB, so the parabola is required. Refining only the largest sample leaves −0.065 dB.

#### #84 reproduction

- **Environment:** same as #76. Script `pad_test.py`; run `python3 pad_test.py`. Deterministic, no RNG.
- **Signals:** 48 kHz, 1 kHz sine starting at phase 0, sample counts `round(duration·fs)`, identical in both channels. 3341 #6 in channel order L, R, C, Ls, Rs with weights 1, 1, 1, 1.41, 1.41.
- **Processing:** K-weighting per #12 (libebur128's formulas: BS.1770 prototype parameters, bilinear transform at fs) via `scipy.signal.lfilter` (float64). Complete 4800-sample sub-blocks only. 400 ms blocks = mean of 4 consecutive sub-blocks. Short-term = mean of 30.
- **Gates:** integrated uses > −70 LUFS and > (relative − 10 LU). LRA follows #78.
- **Padded variant:** append 72,000 zero samples (1.5 s) before analysis.

| Vector | Expected | Complete blocks | Padded 1.5 s | Δ |
|---|---|---|---|---|
| 3341 #1 | I −23.0 | −22.993 | −23.026 | −0.033 |
| 3341 #2 | I −33.0 | −32.993 | −33.026 | −0.033 |
| 3341 #3 | I −23.0 | −23.014 | −23.014 | 0.000 |
| 3341 #4 | I −23.0 | −23.014 | −23.014 | 0.000 |
| 3341 #5 | I −23.0 | −22.979 | −22.995 | −0.016 |
| 3341 #6 | I −23.0 | −23.016 | −23.049 | −0.033 |
| 3342 #1 | LRA 10 | 10.000 | 10.000 | 0.000 |
| 3342 #2 | LRA 5 | 5.000 | 5.000 | 0.000 |
| 3342 #3 | LRA 20 | 20.000 | 20.000 | 0.000 |
| 3342 #4 | LRA 15 | 15.000 | 15.000 | 0.000 |

Not yet run: the downloadable authentic-programme vectors (3341 #7–8, 3342 #5–6).

#### #76a ✅ Provisional amendment: per-rate passband edge (adopted 2026-10-06; the build-phase real-master test decides whether it stays, and CPU is profiled then)

**Synthetic clipped masters.** Signal: `music(fs, 8, 2)` from `p2b_sim.py`, low-passed with an 8th-order zero-phase Butterworth at 16 or 19 kHz, padded with 1 s of silence each side, normalised to a 1.0 peak. Then three treatments: hard clip +6 dB (`clip(2v)`), hard clip +12 dB (`clip(4v)`), and a tanh limiter +12 dB (`tanh(4v)/tanh(4)`). The energy above 20 kHz ends up 31–43 dB below the total.

**Method.** Reference = ideal true peak via 32× FFT interpolation of the whole signal. Estimator = `upfirdn` + parabola on \|y\| at every local maximum.

**Finding:** the current design reaches **−0.116 dB at 44.1 kHz and −0.146 dB at 48 kHz** on the +12 dB clips. The cause is content between 20 kHz and Nyquist, which a 20 kHz passband attenuates. Moving the *stopband* edge to 22.05 kHz with the same ripple (T = 64) does not help (−0.20 dB worst), so it isn't images. Widening the *passband* does help:

| fs | Design (pass edge / taps per phase / cost) | Passband ripple | Clean bursts ≤20 kHz | Worst on clipped masters |
|---|---|---|---|---|
| 44.1k | 20 kHz / 32 / 1× (current) | +0.042 | −0.008 / +0.068 | 0.116 |
| 44.1k | **21 kHz / 64 / 2×** | +0.036 | +0.001 / +0.052 | **0.088** |
| 44.1k | 21.5 kHz / 128 / 4× | +0.028 | — | 0.030 |
| 48k | 20 kHz / 32 / 1× (current) | +0.001 | −0.002 / +0.001 | 0.146 |
| 48k | **22 kHz / 48 / 1.5×** | +0.007 | −0.002 / +0.012 | **0.076** |
| 48k | 22.5 kHz / 64 / 2× | +0.007 | −0.003 / +0.010 | 0.090 |

**Adopted (provisional):** 44.1 kHz → 21 kHz passband, 64 taps per phase; 48 kHz → 22 kHz, 48 taps per phase. Stopband edge stays at fs − passband edge, weight 2:1.

**88.2 / 96 / 192 kHz: the current designs stand** (script `p2g_sim.py`). Same synthetic clipped masters, generated at the native rate and low-passed at 20 or 40 kHz (an 8th-order zero-phase Butterworth); reference = 16× FFT ideal true peak; worst error over six treatments (+6 / +12 dB hard clip, +12 dB tanh, each at both low-pass settings):

| fs | Design | Clean bursts ≤20 kHz | Worst on clipped |
|---|---|---|---|
| 88.2k | **4× / 40 kHz / 32 (current)** | −0.006 / +0.050 | **0.079** |
| 88.2k | 4× / 42 kHz / 48 | −0.002 / +0.139 | 0.104 |
| 96k | **4× / 40 kHz / 32 (current)** | −0.002 / +0.001 | **0.083** |
| 96k | 4× / 44 kHz / 32 | −0.009 / +0.082 | 0.070 |
| 96k | 4× / 45 kHz / 48 | −0.002 / +0.043 | 0.053 |
| 192k | **2× / 80 kHz / 32 (current)** | −0.001 / +0.001 | **0.078** |
| 192k | 2× / 88 kHz / 48 | −0.000 / +0.007 | 0.065 |
| 192k | 2× / 90 kHz / 64 | −0.001 / +0.006 | 0.061 |

All current designs are already under 0.1 dB, and widening gains at most ~0.03 dB.
- **Gain:** at 44.1/48 kHz, worst case on synthetic heavy clipping drops from 0.12–0.15 dB to under 0.09 dB, and the clean ≤20 kHz target still holds.
- **Cost:** ~45M (44.1k) / ~37M (48k) multiply-adds per second instead of ~23M (estimate, not profiled).
- **Test:** the build-phase real-master cross-check in #76 decides between this and the current design. Scripts `p2c_sim.py`–`p2f_sim.py`.

**Correction to an earlier claim:** it was suggested that passing images (stopband at 24.1 kHz) caused the over-reads. The 22.05 kHz stopband test rules that out.

### 4.5 Spectrum (design review Parts 2 & 2b, 2026-10-06)

| # | Decision |
|---|---|
| ✅ 86 | **What is measured:** IEC 61260-1 base-10 fractional-octave **band power**. Power-normalised window (one-sided bin power × 2/(N·Σw²)); bins split at band edges by how much of each bin falls in the band; dB relative to a full-scale sine (full-scale sine = 0 dB). By Parseval's theorem a sine's band power doesn't depend on its sub-bin position, so scalloping disappears. Pink noise reads flat, white +3.01 dB/oct. |
| ✅ 87 | **Tilt** is display only (stored data and Compare tables untilted). UI label **"4.5 dB/oct"**. It is *applied as +1.5 dB/oct on band levels*, pivot 1 kHz, because band power over a constant relative bandwidth already contains +3.01 dB/oct compared with a per-Hz spectrum. |
| ✅ 88 | **Live spectrum:** Hann, fixed 171 ms window (8192 at 44.1/48k, 16384 at 88.2/96k, 32768 at 192k). Hop = round(fs/30) whatever the display rate (V7); the display samples the latest `SpectrumLive`. 256 display points = 1/6-oct-wide band powers at log-spaced centres; options 1/3, 1/6, 1/12. Exponential power averaging, default **Slow (1 s)**, option Fast (125 ms) (time constants borrowed from IEC 61672). Peak hold 2 s, then falls at 20 dB/s, click resets. Channels: mean of L and R power by default; L/R/M/S selectable. Accurate to ±0.1 dB from 150 Hz; the curve is drawn dimmed below that. |
| ✅ 89 | **Averaged spectrum** (per measurement, stored): Welch, Hann, 683 ms window (32768 at 48k, scaled with fs), power averaging (not dB averaging), **87.5% overlap**. **Zero-padded frames at the capture edges:** the frame grid starts N − hop before the first sample and runs N past the last, zero-filled, so every captured sample gets full weight. Cost: ~12 FFTs/s per channel at 48k (estimate). |
| ✅ 90 | **Normalisation:** averaged spectrum = total accumulated band energy ÷ active time. No relative gate, no loudness-bin histogram, no per-frame storage. **Active time = count of 100 ms sub-blocks (#85) at or above −70 LUFS, × 100 ms.** (Overlapping 400 ms blocks were rejected: they over-count by up to 3 blocks at each edge; evidence below.) **Gain:** silence before, after or between parts doesn't change the spectrum. **Cost:** none beyond #85 / #89. **Tests:** (a) the sum of band energies over *all* bins (including the residual below 20 Hz and above 20 kHz) equals Σx² over the capture; (b) the same file with 0, 5 and 30 s of digital silence added at arbitrary offsets matches within 10·log10(1 + 0.2 s / T) dB, where T is the music duration (the bound from one sub-block at each edge; 0.01 dB needs T ≳ 90 s). Depends on #89's overlap and edge padding. |
| ✅ 91 | **Storage:** 1/24-oct IEC base-10 band powers, linear float32, 20 Hz–20 kHz (~240 values, ~1 KB). The same bands at every sample rate; nests exactly into 1/6 bands. Individual 1/24 values below ~150 Hz are resolution-limited. *(Amended by #98: stored as L, R and cross-spectrum.)* |
| ✅ 92 | **Compare overlays:** the level-matched toggle shifts curves by (I_ref − I_entry), consistent with the A/B level matching of #121. Adds a Δ curve (entry − reference per band). |
| ✅ 93 | **Spectrum tests** (replace the §4.3 row): <br>• Sines at IEC band centres ±0.1 dB from 150 Hz (live) / 40 Hz (averaged) at all rates, maximum in the correct band. <br>• Deterministic multisines with equal power per band / per Hz read flat / +3.01 dB/oct within ±0.05 dB. <br>• A 0 dBFS 50 Hz sine stays below −90 dB from 200 Hz up. <br>• Random noise only as a sanity check, tolerance std ≈ 4.34/√(B·T) dB. |

#### Part 2 evidence (sine accuracy, leakage, noise spread)

Script `spec_sim.py`, `default_rng(11)`, 48 kHz. Sine at band centre, worst of 3 phases, 1/6-oct: ±0.1 dB from **150 Hz** (8192 Hann), 75 Hz (16384), **38 Hz** (32768). Blackman-Harris 4 is worse at the low end (211 / 106 / 47 Hz) but leaks less (−94 vs −61 dB one octave above a 0 dBFS 50 Hz sine; Hann reaches −92 dB at 200 Hz). Band-level std for white noise: 0.11–0.15 dB at 31.5 Hz over 180 s.

**dB-averaging bias** (1/6-oct, white noise, 32768 Hann): −1.28 / −0.51 / −0.05 / −0.01 dB at 31.5 Hz / 100 Hz / 1 kHz / 10 kHz. The single-bin theoretical value is −2.51 dB.

#### #89 evidence: overlap vs frame-grid offset

Script `p2b_sim.py` / `p2c_sim.py`, 48 kHz, N = 32768, Hann.
- **Signal:** `music(48000, 40, 1)`, a synthetic transient-heavy track: 55 Hz decaying kicks every 0.5 s, 6 noise hits/s, a low-passed bass bed and four sustained tones.
- **Setup:** placed with at least N of silence each side and shifted by the offsets shown. Worst per-band difference relative to offset 0.

| Overlap | w² overlap-sum (min/max) | Offsets | Worst, 1/24-oct | Worst, 1/6-oct |
|---|---|---|---|---|
| 50% | 0.500 | 0, N/8, N/4, 3N/8 | 1.623 dB | 1.027 dB |
| 75% | 1.000 | 0, N/8, N/4, 3N/8 | 0.066 dB | 0.015 dB |
| 75% | 1.000 | 0 … 15N/16 in N/16 steps | 0.098 dB | 0.019 dB |
| **87.5%** | 1.000 | 0 … 15N/16 in N/16 steps | **0.003 dB** | **0.0005 dB** |

At 75%, w² sums to a constant (COLA), so the energy summed over *all* bins doesn't depend on the frame grid. That's necessary but not sufficient per band: each bin's accumulated energy is a time-sampled row of the spectrogram, and at hop N/4 a measurable residual remains. At N/8 it's negligible. *(This explanation is the author's interpretation; the numbers are simulated.)*

#### #90 evidence: active-time definitions

Script `p2c_sim.py`. 87.5% overlap with edge padding. Six variants of the same music with digital silence added: leading 5.012 / 30.008 s, trailing 5.037 / 30.012 s, and both 5.005 + 30.031 / 30.060 + 5.000 s. Worst 1/24-oct difference relative to the no-silence version:

| Music duration | Band energy alone | Reviewer: 400 ms blocks × 100 ms | **100 ms sub-blocks** | T_eff = E_K / P_I (considered) |
|---|---|---|---|---|
| 40 s | 0.005 dB | 0.080 dB | **0.015 dB** | 0.050 dB |
| 180 s | 0.003 dB | 0.019 dB | **0.004 dB** | 0.009 dB |

- With the block definition, active time was 39.7 s for the bare file and 40.0–40.4 s with silence added. Blocks that straddle an edge pass the −70 LUFS gate as soon as they contain a few milliseconds of music.
- Without edge padding (75%), the bare file differed by **6.83 dB** in some bands: its first and last frames are under-weighted.
- With 50% overlap plus edge padding (block definition) the difference was 0.79 dB.
- **Test (a) check:** summed over all bins, energy / Σx² = 1.000000000. Over 20 Hz–20 kHz bands only, it's 0.9188 (−0.37 dB) for this signal, so test (a) has to include the out-of-range residual.

### 4.6 Stereo (design review Part 3, 2026-10-06)

**Maths.** Per band, P_L = Σ\|X_L\|², P_R = Σ\|X_R\|², C = Σ Re(X_L·X_R*). Then:
- width W = ½ − C/(P_L + P_R)
- correlation ρ = C/√(P_L·P_R)
- balance 10·log10(P_R/P_L)
- W = ½·(1 − ρ·b), with b = 2√(P_L·P_R)/(P_L + P_R); any two of the three determine the third.

**W is the fraction of average channel energy that cancels in a (L+R)/2 mono fold-down:** 0 = no loss, 0.5 = −3 dB, 1 = full cancellation.

| # | Decision |
|---|---|
| ✅ 94 | **Per-band quantities from cross-spectra:** accumulate P_L, P_R and C = Re Σ X_L·X_R* per band; derive W, ρ and balance from the accumulated sums, never by averaging ratios. Re, not coherence: a delay between channels lowers ρ, matching what happens to the mono sum. |
| ✅ 95 | **Width spectrum display:** bar height = W (0–1, marks at 0 / 0.5 / 1), colour = ρ (continuous; negative values a distinct hue). Inspect shows W, ρ, balance and mono fold-down loss 10·log10(1 − W) per band, as data. |
| ✅ 96 | **Edge cases:** ρ undefined (no colour, `null` in exports) when min(P_L, P_R) < max(P_L, P_R)·10⁻⁶ (one channel >60 dB down) or band total < −90 dB re full scale; below −90 dB, W is also not drawn. **The 60 dB and −90 dB thresholds are provisional;** a build-phase check on real material confirms or adjusts them. |
| ✅ 97 | **Bands and frames:** IEC base-10 1/3-oct, computed from the #89 frames (683 ms Hann, 87.5% overlap) for both live and per-measurement, so no extra FFTs. Live: exponential smoothing of the three band sums, Slow τ = 1 s; ~11.7 updates/s at 48 kHz, interpolated for display. Per measurement: totals over the capture (silence adds zero to all three sums, so no gating). Bands stay independent (±0.02) from ~126–200 Hz, versus ~800 Hz with 171 ms frames. |
| ✅ 98 | **Storage (amends #91):** store P_L, P_R and C per 1/24-oct band (3 × ~240 float32 ≈ 2.9 KB) instead of the single (P_L + P_R)/2 array. The #91 spectrum, the L/R/M/S spectra and W/ρ/balance at any band resolution are derived. 1/24 nests exactly into 1/3. |
| ✅ 99 | **Broadband meters:** the standard time-domain correlation meter, ΣL·R/√(ΣL²·ΣR²), with exponential averaging (Slow 1 s default, Fast option); per measurement, totals over the capture. **Broadband balance = 10·log10(ΣR²/ΣL²) from the unweighted powers the same meter accumulates.** No K-weighting, no change to #85, and no dependency of stereo on the loudness engine. |
| ✅ 100 | **Goniometer:** x = (R − L)/√2, y = (L + R)/√2 (mono vertical, L-only upper-left, anti-phase horizontal). Fixed log-radial scale −40 … 0 dBFS, angle preserved; auto-gain optional. Every sample drawn up to 2,000 per frame; above that, every k-th sample. Phosphor-style decay. Orientation to be checked against Logic's MultiMeter. |
| ✅ 101 | **Stereo tests:** deterministic cases (mono, flip, quadrature, panned R = g·L with W = ½ − g/(1 + g²) and ρ = 1, left-only with ρ undefined) ±0.01 per band, 40 Hz–16 kHz, averaged; band independence ±0.02 from 200 Hz on #89 frames; independent noise only as a sanity check; broadband correlation and balance with tones and pans; goniometer orientation cases. |

**Evidence** (scripts `p3_sim.py`, `p3b_sim.py`, `default_rng(21)`, 48 kHz):
- **S1:** the deterministic cases are exact (0.0000 error). Independent 30 s noise is off by 0.019 (W) and 0.038 (ρ), which is estimator noise.
- **S2:** band independence ±0.02 holds from 794 Hz with 8192 frames and from 126 Hz with 32768 frames (200 Hz with an inner-half-band test signal).
- **S3:** live std(ρ) for independent noise with Slow smoothing is 0.12 / 0.09 / 0.03 / 0.013 at 31.5 Hz / 100 Hz / 1 kHz / 10 kHz. Per-measurement values (60 s) are ≤0.017.

### 4.7 Tempo and key (design review Part 4, 2026-10-06)

| # | Decision |
|---|---|
| ✅ 107 | **Two analysers, Tempo and Key**, with separate versions. |
| ✅ 108 | **Tempo front end (private to Tempo):** mono (L+R)/2. STFT Hann, ~43 ms window (2048 at 44.1/48k, scaled with fs). Hop = fs/100, so the frame rate is 100 Hz at every supported rate. log(1 + λ·\|X\|) compression. Semitone-spaced filterbank 30 Hz–16 kHz. Half-wave-rectified spectral flux with local-mean subtraction → onset-strength envelope. |
| ✅ 109 | **Global tempo:** autocorrelation of the onset envelope over 8 s windows, averaged over the capture. Harmonic enhancement (ACF at 2× and 4× lag, weights tuned on dev data). Log-Gaussian prior (mode 120 BPM, σ = 1 octave). Search 40–240 BPM, parabolic peak refinement. Best and second-best candidates plus a confidence (peak ratio) are stored; the half/double toggle switches to the stored candidate. No genre-specific range restriction. **Shows "—" when confidence is below a threshold**, as key does in #111. The threshold is provisional and set from the first benchmark run. |
| ✅ 110 | **Key front end: reuses SpectralFrontEnd frames** (683 ms Hann, 87.5%, mid = (X_L + X_R)/2). Tuning-adjusted semitone bands C2 (65 Hz)–C7 (2.1 kHz) using the #86 fractional bin weights; log compression; energy-accumulated mean chroma over the capture; global tuning offset (±50 cents) from a spectral-peak deviation histogram. **Gain:** no extra FFTs. **Cost:** coupled to the provider version; poor semitone resolution below C2. **Test:** compare against a dedicated constant-Q chroma front end on the same datasets; keep the shared frames only if within 1 percentage point of weighted score. |
| ✅ 111 | **Key decision:** correlate mean chroma with 24 rotated profiles. The set is chosen on dev data from profiles whose values are printed in the publication that defines them, cited in the code (#173): Krumhansl–Kessler and Temperley; Sha'ath's and Faraldo's EDM profiles only if their values are published that way or their authors grant a licence (multi-profile variant optional). Output: key, runner-up, confidence (correlation margin), tuning. "—" below a provisional confidence threshold (set from the first benchmark). Always labelled as an estimate. |
| ⛔ 112 | **Considered and deferred (not in v1): a small neural network** for tempo and/or key (Core ML / BNNS). Gain: about +10–15 percentage points on GiantSteps. Reasons for deferring: training-data licensing (GiantSteps audio comes from Beatport previews and is likely not redistributable); model size against the 10 MB app budget; an ML toolchain; genre-overfitting risk; harder bit-identity across OS versions; and it conflicts with the in-house DSP direction of #73. |
| ✅ 113 | **Classical methods with revised targets. The numbers are provisional expectations, not pass marks:** tempo GiantSteps Acc1 ≥60% / Acc2 ≥88%; Ballroom Acc1 ≥65% / Acc2 ≥95%; key GiantSteps weighted ≥60%. The first benchmark runs in the build phase; md3's measured figures are published, and the §12 ship gate is set from them. *Note:* under the current GiantSteps annotations, Percival & Tzanetakis already reach 95.6% Acc2 and Gkiokas et al. 92.2% (Böck & Davies 2020, Table 1), so 88% is a low expectation for Acc2. The figure stays as approved; the benchmark will set the real one. |
| ✅ 114 | **Evaluation protocol:** MIREX metrics (Acc1/Acc2 ±4%; weighted key: 1 correct / 0.5 fifth / 0.3 relative / 0.2 parallel). Test sets: GiantSteps Tempo (664 tracks, current annotations), GiantSteps Key (604), Ballroom, plus at least one non-EDM set (GTZAN, Hainsworth or ACM Mirum). Tune only on separate dev sets (e.g. GiantSteps MTG). Dataset audio and annotations are fetched locally under each dataset's terms, never committed or used as CI artifacts; only md3's aggregate scores are published (#175). Licence terms checked 2026-10-08: no licence on the GiantSteps repositories; no terms published for Ballroom. |
| ✅ 115 | **Integration:** front ends run live during a measurement and in file analysis; estimates at `finish()` only in v1. Minimum capture: 15 s for tempo, 30 s for key, else "—". Sections `TempoResult {bpm, alt_bpm, confidence}` and `KeyResult {key, alt_key, confidence, tuning_cents}`, each versioned. **Deterministic unit tests:** synthetic drum patterns at 60 / 87.5 / 120 / 128 / 140 / 174 / 200 BPM, with and without swing, at every sample rate, within ±0.5%. Shepard-tone I–IV–V–I cadences in all 24 keys, in tune and at ±30 cents, all correct. A single repeated note gives "—". |

**Published benchmarks** (Acc1 / Acc2 in %; key = MIREX weighted). Annotation versions differ between sources and change results a lot:

| Source | GiantSteps Tempo | Ballroom | GiantSteps Key |
|---|---|---|---|
| Böck & Davies, ISMIR 2020, Table 1 (current annotations, unseen test data) | Non-neural: Percival & Tzanetakis 50.6 / 95.6; Gkiokas et al. 72.1 / 92.2. Neural: Böck et al. 76.4 / 95.8; Schreiber & Müller 82.1 / 97.1; Foroughmand & Peeters 83.6 / 97.9; **Böck & Davies 87.0 / 96.5** | — | — |
| Schreiber & Müller, ISMIR 2018, Table 1 | schr 63.1 / 88.7; böck 58.9 / 86.4; CNN 73.0 / 89.3 | 64.6 / 97.0; 84.0 / 98.7; 92.0 / 98.4 | — |
| Knees et al., ISMIR 2015, Tables 4–5 (original annotations) | Percival 51.4 / 88.4; Böck (50–240 BPM) 56.3 / 88.3; Böck (95–190 BPM) 76.5 / 86.6 | — | Essentia 44.85; QM 52.90; KeyFinder 59.30; Mixed-In-Key 74.60; Rekordbox 79.55 |
| Korzeniowski & Widmer, EUSIPCO 2017, Table I (CK1, trained on GiantSteps MTG) | — | — | 74.3 (CNN) |

**Modules and records:**
- Tempo reads `AnalysisBlock` and writes `TempoResult`.
- Key reads `SpectralFrame` and writes `KeyResult`.
- Neither depends on Loudness, Spectrum or Stereo.

### 4.8 Build-phase handoff (not done during the decision phase)

When the build phase starts (scripts are kept in the review status document's appendix until then):

1. Commit the simulation scripts (`tp_table76.py`, `pad_test.py`, `spec_sim.py`, `p2b_sim.py`–`p2g_sim.py`, `p3_sim.py`, `p3b_sim.py`, `p5_sim.py`–`p5e_sim.py`, `p6_sim.py`–`p6c_sim.py`) under `tools/` with a README giving the commands above.
2. CI's first jobs:
   1. The #76 burst test, run against md3's real true-peak code (not the Python model).
   2. The Tech 3341 and 3342 vectors that can be generated from their published descriptions; the official EBU files, including the programme vectors 3341 #7–8 and 3342 #5–6, run only locally on the maintainer's Mac (#176).
   3. The #80 test: feeding a file in random chunk sizes gives bit-identical results to feeding it in one go.
   4. The #76 clipped-master cross-check (ideal reference and libebur128) on real hard-clipped / limited 44.1 kHz masters.
   5. The #93 spectrum tests and the #90 tests (a) and (b).
   6. The #101 stereo tests, and the #96 threshold check on real material.
   7. The #106 modularity tests (disable-each bit-identity; version discipline).
   8. CPU profile of the #76a designs.
   9. #106 (d) failure injection and (e) ASan/UBSan runs of the C modules.
   10. First Tempo/Key benchmark (#113, #114): publish md3's measured figures, set the provisional "—" confidence thresholds (#109, #111) and the ship gate from them.
   11. Part 5 tests (#129), the #125 watchdog failure-injection test, and the #122b real-track parameter check.
   12. Part 6 tests (#143) on a dedicated runner with the driver installed; every other job runs without the driver.
   13. Part 7 tests (#162), including #146 slow/blocked analysers, #151 recovery, #163 lifecycle events and #164 database robustness.

The order in which these come online is §16.

---

## 5. Bluetooth audio/video sync

### 5.1 Approach

- **Problem:** Bluetooth audio arrives 150–300 ms late. Players delay their video by the latency macOS reports, but Bluetooth devices often report it wrongly, md3's processing adds unreported latency, and latency drifts during playback.
- **Fix: driver mode.** md3 installs a virtual output device (an AudioServerPlugIn, not a kernel extension; optional install) that reports a **fixed total latency X**, defined in #131 (measured output latency + engine latency + chain headroom + margin). The Sync output stage adds whatever **padding** is needed so sound reaches the ears exactly X later; chain changes alter only the padding, so players never need to resync. Design: §5.4.
- **Calibration:** automatic, with a 1 s sweep recorded by the **Mac's built-in mic** selected explicitly (never the headset's mic, which switches the headset into call mode); manual flash/click fallback and ±1 / ±10 ms nudges; **saved per device** (#132–#135, #138). The measurement itself is accurate to ~0.1 ms; the end-to-end budget is #142.
- **Target:** within ±20 ms, provisional until M0 measures Bluetooth variability (#142) (inside EBU R37's +40 / −60 ms tolerance; ITU-R BT.1359 detection thresholds are about +45 / −125 ms).
- **Clock and drift:** clock follow, no resampling (#136); recalibration prompts on observable events (#137).
- **Failsafe:** heartbeat → the virtual device becomes unavailable within 200 ms and is never offered without md3 (#141); md3 restores the original device on quit (#66).
- **Licensing:** built on **libASPL (MIT)**. No code from BlackHole (GPL-3) or Background Music (GPL-2).
- **Known limits:** games and other interactive apps can't delay their video; some players read latency only at playback start; a few apps ignore device latency entirely.

### 5.2 Sync decisions ✅ (closed 2026-10-08; sync itself is after v1, #166)

| # | Question | Recommendation |
|---|---|---|
| 47 | Delay only vs full driver mode | ⛔ Resolved by D18: full driver mode is required. |
| ✅ 63 | Driver mode (when sync is built, #166) | **Decided 2026-10-08 (§17):** Driver mode ships if **at least 5 of the 8 M0-2 players pass AND Safari or Chrome is one of them**. Otherwise sync falls back to the AV offset only (#140). |
| ⛔ 64 | ~~Calibration methods~~ | Refined by #132–#135 (§5.4). |
| ⛔ 65 | ~~Default safety margin in X~~ | Kept at 20 ms; refined by #131 (§5.4). |
| ✅ 66 | Take over the system output automatically | **Decided 2026-10-08 (§17):** Automatically, **only while sync is on** (processing no longer needs the virtual device, #116); back to the real device when sync turns off or md3 quits. |
| ⛔ 67 | ~~Clock drift correction~~ | Fallback for #136 (§5.4): Apple's aggregate-device drift correction, used if clock follow fails in M0. |
| ⛔ 68 | ~~Recalibration prompt threshold~~ | Replaced by #137 (§5.4): the latency move isn't observable without the mic. |
| ⛔ 69 | ~~Driver build~~ | Refined by #130 and #141 (§5.4): libASPL, MIT, signed `.pkg`, optional install, minimal driver. |
| ✅ 70 | Sync UI | **Decided 2026-10-08 (§17):** Deferred with sync (#166). When built: a `sync` page; the status line shows `sync: airpods 186ms ✓`. |
| ⛔ — | ~~Audio delay (sync offset)~~ | Refined by #140 (§5.4). |

### 5.3 M0 verification matrix

Consolidated with every other M0 check in **§14** (the player latency matrix is item M0-2).

### 5.4 Sync design (design review Part 6, 2026-10-06)

| # | Decision | Module | Reads | Writes |
|---|---|---|---|---|
| ✅ 130 | **Sync module structure.** `SyncDriver` (AudioServerPlugIn, libASPL, in coreaudiod); `SyncEngine` (in md3: steering, padding, volume forwarding, prompts); `Calibrator` (own mic capture and sweep analysis; shares no state with the analysers); `SyncStore`. <br>**Driver minimalism:** a driver bug can break all system audio, so the driver contains **no DSP, no allocation on the I/O path, and no logic beyond passing audio, reporting latency, and its failsafe**. Everything else lives in `SyncEngine`. The driver has its own version. **md3 works fully with the driver not installed; sync is an optional install.** <br>**Driver–app transport (M0 comparison):** <br>(a) *Standard route:* the virtual device loops its output to an input stream (`VirtualInput`) that the engine reads as an ordinary input device; options go through custom device properties (`DriverProperties`). <br>(b) *Custom shared memory* between engine and driver. `[MEM: AudioServerPlugIns run sandboxed in coreaudiod; unverified]`. <br>**Prefer (a)** unless M0 shows it can't carry the clock steering and heartbeat. Under (a), the heartbeat is the engine's read activity on `VirtualInput` (I/O started / reads arriving), plus a counter property the engine sets at ≥ 5 Hz. (b) would gain about one I/O buffer of latency, direct control of ring sizing, and arbitrary high-rate data. It would cost sandbox exceptions or entitlements, a larger security surface, and custom synchronisation code in the driver, which works against minimalism. **Not recommended unless (a) fails.** | Sync | — | — | 
| ✅ 131 | **Latency model and X (refines #65):** A_out = *measured* latency from the engine's output I/O time to sound at the transducer (#132); the Bluetooth device's reported latency is not used for timing. X = A_out + L_engine + H_chain + margin; H_chain = max(current `ChainLatency`, 30 ms headroom); margin 20 ms. Padding P = X − (L_engine + L_chain + A_out) ≥ 0. X is recomputed only on device change or recalibration; if chain latency exceeds the headroom, X grows and status shows "players may need restart". | Sync | `DeviceCalibration`, `ChainLatency` | `SyncConfig.X`, `SyncOutput` |
| ✅ 132 | **Calibration measurement (refines #64):** <br>• **Input is always the Mac's built-in microphone, selected explicitly by device** (built-in transport type `[MEM]`), never the system default input and never the headset's own mic (opening it would switch the headset to its call profile and change the latency). **No built-in mic, or unavailable** (e.g. Mac mini, Mac Studio, Mac Pro): go straight to the manual method (#135). <br>• **Sweep:** exponential sine sweep **1 s, 300 Hz–12 kHz** (adopted: accuracy equivalent to 5 s, 20 Hz–20 kHz in every simulated case, `p6c_sim.py`), Farina inverse filter, −20 dBFS with fades. <br>• **Detection:** first arrival = first local peak above −12 dB of the maximum, searched only within [max − 50 ms, max]; parabolic refinement. The 2nd/3rd-harmonic responses land 188 / 298 ms before the linear one, outside the window. <br>• **Time base:** t_out = host time of the first sweep sample at the engine's output I/O; t_in = input I/O host time minus the input path's reported latency; 0.3 m acoustic distance (0.9 ms) subtracted. <br>• **5 repeats,** median, spread ≤ 3 ms or repeat/warn. **Total: 2.0 s per repeat, 10 s for 5 repeats** (5 s sweep would be 30 s), plus the one-off #133 self-check (2 s). | Sync (Calibrator) | built-in mic, output I/O timestamps | `DeviceCalibration` |
| ✅ 133 | **Input-latency self-check:** once per Mac and OS version, built-in speaker → built-in mic, compared with the two reported latencies; residual ≤ 2 ms passes, otherwise stored as an input correction. A consistency check, not proof; validated in M0 against an electrical loopback through an audio interface with known latency. | Sync (Calibrator) | built-in devices | `DeviceCalibration.inputCorrection` |
| ✅ 134 | **Procedure:** earbuds out of the ear, 5–10 cm from the mic; over-ear headphones off the head, cups facing the mic; speakers in place. Level capped; hearing-safety instruction first; mic permission at the first calibration only. **M0 check:** do AirPods and similar earbuds with ear detection keep playing md3's test signal when out of the ear? **Fallback if they don't:** (1) ask the user to turn off automatic ear detection for the calibration, with a reminder to turn it back on afterwards; (2) if that isn't possible on the device, use the manual method (#135). | Sync | — | — |
| ✅ 135 | **Manual fallback and nudges:** flash + click pattern with adjustable offset; nudges ±1 / ±10 ms on top of the calibration; manual results labelled lower confidence. | Sync | user input | `DeviceCalibration` (manual), `SyncConfig.nudge` |
| ✅ 136 | **Clock follow** (#67 is the fallback): the virtual device's zero timestamps are steered to the real output device's rate, estimated by a 2nd-order DLL (Adriaensen 2005) on its I/O timestamps (1 Hz for initial lock, narrowing to 0.1 Hz). Apps render at the real device's rate: no resampler, bit-transparent. Simulated: max 78 µs time error over 1 h at +40 ppm, against 144 ms uncorrected. **Carried under transport (a):** the engine sets a custom property at ≤ 10 Hz holding {rate scalar (double), reference host time, reference sample time}; the driver's zero-timestamp callback computes from the latest values with pure arithmetic, no allocation, no locks beyond an atomic swap of the parameter set. Whether the HAL accepts steered timestamps smoothly is an M0 check. Test: 1 h ring-fill within ±1 buffer + bit-transparency null test, against #67. | Sync (engine computes, driver applies) | real device I/O timestamps | `DriverProperties.clock` |
| ✅ 137 | **Recalibration prompts (replaces #68)** on observable events only: reconnect (if this device's past calibrations spread > 10 ms), reported-latency change > 10 ms, format/rate change, ring-fill excursion > 10 ms. Acoustic latency changes are not observable without the mic. Status: "calibrated N days ago, spread ±x ms". | Sync | device events | `SyncStatus` |
| ✅ 138 | **Per-device memory:** `DeviceCalibration` by device UID (+ codec if exposed), with history; applied value = median of the last 3 valid measurements; cross-session spread shown. | Sync (SyncStore) | — | `DeviceCalibration` |
| ✅ 139 | **Delay changes:** 20 ms crossfade between old and new read positions; no time-stretching; no continuous speed correction (clock follow). | Sync (output stage hosted in Processing) | `SyncConfig` | `SyncOutput` |
| ✅ 140 | **AV offset** (video later than audio): extra audio delay 0–2000 ms, **not** reported to players, added to padding only (Sync output stage), per app and per device. | Sync | `SyncConfig.avOffset` | `SyncOutput` |
| ✅ 141 | **Failsafe (refines #69):** heartbeat (see #130); stale > 200 ms → the virtual device marks itself not alive / unavailable, so macOS falls back to the real device; md3 restores the original device on a normal quit (#66). **Not selectable without md3:** when md3 isn't running (or the engine is disconnected), the virtual device isn't offered as an output at all, either by not publishing the device object or by marking it hidden / not default-capable (`[MEM]`; which mechanism works with macOS's output picker is an M0 check). So the user can never be left on a dead device after a crash, a quit, or a login without md3. Test: `kill -STOP` md3 → audio returns to the real device within the measured limit; reboot without md3 → virtual device absent from the output list. | Sync (driver) | heartbeat | device availability |
| ✅ 142 | **Error budget** for ±20 ms: measurement ≤ 0.1 ms; reflection error removed by first arrival; input report ±2 ms (#133); acoustic distance ±0.5 ms; clock follow < 0.1 ms; Bluetooth variability across reconnects and within a session, and player adherence: **unknown, measured in M0**. The ±20 ms target stays provisional until then; the §5.1 "±5 ms" applies to the measurement, not end to end. | Sync | — | — |
| ✅ 143 | **Tests:** <br>• Software loopback with known delay (±0.5 ms); acoustic test with a wired reference (±2 ms). <br>• Heartbeat kill test; reboot-without-md3 test (#141); 1 h clock-lock test. <br>• Padding crossfade without clicks; AV offset by loopback timestamps. <br>• Modularity: enabling, disabling or failing Sync leaves every analyser section bit-identical. <br>• **Every non-sync feature passes its tests with the driver absent.** | Sync | — | — |
| ✅ 144 | **Volume and mute forwarding** *(coverage gap; approved, using the Sync-owned output stage of V18)*: the virtual device publishes standard volume and mute controls, so the volume keys and menu-bar volume work when it's the default output. The driver only stores the values (no DSP, #130). The engine observes them and forwards them to the real device's hardware volume/mute when it has one (keeps headset-side volume and full resolution). Otherwise it applies the volume as a digital gain in the Sync output stage (`SyncOutput.outputGain`). Measurement is unaffected: taps are pre-device-volume (#81). **Test:** volume keys change the real device's volume within one step; mute silences within 50 ms; analyser sections unchanged by volume. | Sync | `DriverProperties.volume` / `mute` | real device volume / `SyncOutput.outputGain` |
| ✅ 145 | **Format following** *(coverage gap; approved)*: the virtual device's nominal sample rate follows the real output device's current rate (its available-rates list mirrors the real device), stereo, float32. The engine never resamples. When the real device changes rate, the engine sets the virtual device's rate (apps get the standard rate-change notification) and re-locks the clock (#136); a short glitch is acceptable. **Test:** real-device rate changes 44.1 → 48 → 96 kHz with playback running: the virtual device follows each, and audio is bit-transparent after re-lock. | Sync | real device format | virtual device format |

**Evidence:** `p6_sim.py` (pickers), `p6b_sim.py` (DLL), `p6c_sim.py` (sweep length/range). Tables in the review status document §12.

---

## 6. Performance

### 6.1 Targets (Apple Silicon)

**v1 supports Apple Silicon only; Intel Macs are not supported.** Flush-to-zero stays on regardless (#82). Measured DSP cost and the budget rule: #161.

| State | CPU | RAM |
|---|---|---|
| Idle (not measuring, dropdown closed) | ~0% | <30 MB |
| Measuring, dropdown closed | <1% | <40 MB |
| Measuring, dropdown open | <4% | <60 MB |
| Apple-AU processing | <3% plus plugins | — |
| App size <10 MB · launch to menu bar <200 ms · Energy Impact "Low" | | |

### 6.2 Performance decisions ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ✅ 51 | When the tap runs | **Decided 2026-10-08 (§17):** Only while measuring, while the dropdown is open, or while processing; stop 2 s after none apply. |
| ✅ 52 | Audio thread rules | **Decided 2026-10-08 (§17):** (settled in substance by the review) No allocation, locks, logging, or runtime reference counting in the audio callback. Real-time code in a small C/C++ module. Debug builds fail loudly when the rules are broken. |
| ✅ 53 | Split analysis by need | **Decided 2026-10-08 (§17):** (settled in substance by the review) Stored analysis (all providers and analysers) runs for the whole measurement and is never paused (V8). Live-only work (the #88 live spectrum, goniometer, live width display) runs only while visible. |
| ✅ 54 | Frame rate | **Decided 2026-10-08 (§17):** 30 fps (60 optional), following the display refresh, drawing nothing while hidden. |
| ✅ 55 | Menu bar update rate | **Decided 2026-10-08 (§17):** 2 Hz, and only when the text changes. |
| ✅ 32 / 56 | Drawing | **Decided 2026-10-08 (§17):** SwiftUI for static layout only. Meters drawn as Core Animation layers with geometry reused. Metal only if profiling requires it. |
| ✅ 57 | Point limits | **Decided 2026-10-08 (§17):** (settled in substance by the review) Goniometer ≤2,000 points per frame; spectrum ≈256 log-spaced points. |
| ⛔ 58 | ~~Database writes~~ | Refined by #150 (one write at Stop) and #151 (30 s recovery journal). |
| ✅ 59 | File analysis | **Decided 2026-10-08 (§17):** (settled in substance by the review) Low-priority background workers, processed in chunks, with progress and cancel; one Coordinator + module set per job (#146, V19). |
| ✅ 60 | Power awareness | **Decided 2026-10-08 (§17):** (settled in substance by the review) In Low Power Mode or under thermal pressure: 15 fps and reduced live-only work. Stored analysis is never reduced or paused (V8, #161). |
| ✅ 61 | Preventing slowdowns | **Decided 2026-10-08 (§17):** (settled in substance by the review) A CI performance test (10-minute run within the targets, at shipping QoS) plus Instruments profiling before each release; budget rule #161. |
| ⛔ 62 | ~~Plugin loading~~ | Closed by #158 (§3.6). |

---

## 7. System behaviour ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ✅ 34 | Default hotkeys | **Decided 2026-10-08 (§17):** **None bound.** Every action (start/stop, reset, A/B, open dropdown, presets 1–4) is assignable in Prefs, so nothing clashes with DAW shortcuts. |
| ✅ 35 | Login / Dock | **Decided 2026-10-08 (§17):** Launch at login **on by default** (turn off in Prefs or during setup). No Dock icon (`LSUIElement`). |
| ✅ 36 | Onboarding | **Decided 2026-10-08 (§17):** 3 steps: (1) System Audio Recording permission; (2) optional Automation permission (Spotify, Music, browsers for titles); (3) "launch at login is on" with an off switch. The driver and mic are requested only when sync exists and is first used (#166). |
| ✅ 37 | Updates | **Decided 2026-10-08 (§17):** Sparkle, daily check, prompt before installing. |
| ✅ 38 | Language | **Decided 2026-10-08 (§17):** English only in v1; all text prepared for translation. |
| ✅ — | Other standard behaviour | **Decided 2026-10-08 (§17):** `SMAppService` login item; single instance; recovery from sleep/wake and device changes (#163); respects Reduce Motion / Increase Contrast; VoiceOver labels; **no telemetry**. |

---

## 8. History & Compare ✅ (closed 2026-10-08)

**Each entry stores** an `EntryHeader` (source app, track title/artist, start time, duration, device and sample rate, app volume/normalization when known, tap point, chain state, status, notes) and one versioned section per module: loudness (I, max ST, max M, LRA), true peak, derived (trim, PLR), `KWRecord` (loudness curve), `BandRecord`, spectrum, stereo, tempo, key. Layout: #150.

**Files:** drag-and-drop files are analysed faster than real time and saved as "File" entries (the unencoded reference).

| # | Question | Recommendation |
|---|---|---|
| ✅ 23 | Grouping | **Decided 2026-10-08 (§17):** Normalized "artist — title"; drag entries between groups, or rename. |
| ✅ 24 | Compare | **Decided 2026-10-08 (§17):** Up to 4 entries, one marked as reference (★) with differences shown relative to it. Table plus overlays (loudness curve time-aligned by #75, spectrum with a level-matched toggle, width spectrum), side by side. Also reachable as the `compare` page (#1). |
| ✅ 25 | Retention | **Decided 2026-10-08 (§17):** History keeps the **last N** entries (Prefs, **default 10**); older ones are deleted automatically. In addition, up to **20 entries can be saved**: saved entries never auto-delete and don't count toward N. Export/import #152; robustness #164. |
| ⛔ 26 | ~~Storage~~ | Refined by #150. |
| ⛔ — | ~~Leading/trailing silence trimmed from each entry~~ | Replaced by #75: silence trim sets the reported duration only; no data is cut. |

---

## 9. Open source & release ✅ (closed 2026-10-08)

| # | Question | Recommendation |
|---|---|---|
| ✅ 39 | Name | **md3** (D1). Still to check availability on GitHub and Homebrew. |
| ✅ 40 | License | **Decided 2026-10-08 (§17):** **MIT**. |
| ✅ 41 | Apple Developer account | **Decided 2026-10-08 (§17):** Not bought yet: code first. See #172. |
| ✅ 42 | Dependencies | **Decided 2026-10-08 (§17):** Sparkle, KeyboardShortcuts, GRDB in v1; libASPL only when sync is built (#166). All MIT. DSP written on Accelerate. |
| ✅ 43 | Distribution | **Decided 2026-10-08 (§17):** Open-source download on GitHub Releases (`.dmg`; the driver `.pkg` only once sync exists), a Homebrew tap, a Sparkle feed on GitHub Pages, and GitHub Actions to build and publish on version tags. Signing per #172. |
| ✅ — | Repo basics | **Decided 2026-10-08 (§17):** LICENSE (MIT), README, CONTRIBUTING, CHANGELOG, issue templates, the compliance report, a build-from-source guide. |
| ✅ — | Mac App Store | **Decided 2026-10-08 (§17):** Not targeted (the sandbox conflicts with process taps, AppleScript control of other apps, and the driver). |
| ✅ 172 | Release signing | Early GitHub releases are **unsigned "developer preview" builds** with install instructions (System Settings → Privacy & Security → Open Anyway). The $99/yr Apple Developer account is bought before the first public 1.0, so 1.0 is signed and notarized. Known cost of unsigned previews (`[MEM]`): the Gatekeeper step on first launch, and the System Audio Recording permission may need re-granting after updates. |

---

## 10. Milestones ✅ (#44, decided 2026-10-08: Processing before Sync, Sync after v1)

| Milestone | Scope |
|---|---|
| **M0** | Prototypes for the v1 checks in §14: process taps, source switching and mute/replace; out-of-process AU hosting; AU facts; lifecycle notifications; aggregate drift; AppleScript metadata; FP environment and alignment. The sync checks (M0-2, -3, -4, -6, -7, -8, -12, -14) are postponed to the start of M4 (#166). |
| **M1** | LUFS/TP engine + test suite, menu bar app, start/stop, dropdown shell with chevron pages. |
| **M2** | `spec` and `stereo` pages (width spectrum, goniometer, correlation). |
| **M3** | History, Compare (incl. the `compare` page), file analysis, CSV/JSON export. |
| **M3.5** | Tempo / key (#107–#115). |
| **M5** | Processing chain: `eq` / `comp` slots with Apple AUs, presets, A/B, `loud match`. |
| **M6** | `fx` slots / third-party AU hosting and editor windows. |
| **M7** | Prefs, onboarding, Sparkle, release pipeline, compliance report → **v1** (unsigned previews first; 1.0 signed, #172). |
| **M4** | **After v1 (v1.1, #166):** sync M0 checks, then driver mode (#63 rule) + `sync` page + calibration. |

---

## 11. Edge over free tools (the feature bar)

| Feature | What free tools usually offer | md3 |
|---|---|---|
| LUFS | A single integrated number, often not verified | Verified against EBU/ITU test sets with a published report; per-app capture; history grouped by track |
| Comparing sources | Nothing, or manual notes | Grouped stack, a reference entry, time-aligned overlays, recorded app volume and normalization |
| Spectrum | Live display only | Per-measurement average, overlays, level-matched comparison |
| Stereo | Correlation and goniometer | Width spectrum, saved and compared between entries |
| EQ / comp | System-wide EQ only | Per-app chains, AU hosting, presets auto-loaded per app/device, level-matched A/B |
| Bluetooth sync (after v1, #166) | A manual offset inside one player | System-wide, mic auto-calibration, per-device memory, fixed latency total, clock follow without resampling |
| Key / BPM | A separate app | Saved with the loudness entry, accuracy measured against public datasets |

---

## 12. Risks & unknowns

| Risk | Mitigation |
|---|---|
| Players don't honour the virtual device's latency | M0 matrix gates driver mode; document which players are supported |
| Heartbeat failsafe doesn't return audio to the real device | Also restore on quit; a small helper as backup; verify in M0 |
| Clock follow rejected by the HAL (M0) | Apple aggregate-device drift correction as the fallback (#67, #136) |
| Bluetooth latency varies between connections or codecs | Per-device calibration history and spread (#138), event-based recalibration prompts (#137), M0 measurement (#142) |
| Process tap API differences between 14.2 and 27 | Test matrix on 14.x, 15.x, 26.x and 27.x |
| Third-party plugin crashes take down md3 | Out-of-process hosting if M0 allows; otherwise watchdog + safe mode (#125) |
| Driver install friction / trust (after v1) | Signed and notarized `.pkg`; metering works without the driver; clean uninstall |
| Unsigned preview builds put users off (#172) | Clear install instructions; label as developer preview; sign and notarize from 1.0 |
| Tempo/key accuracy below expectations | Labelled as an estimate; "—" below confidence thresholds; half/double toggle; ship gate set from the first measured benchmark (#113) |

---

## 13. How to close the open items

**Closed 2026-10-08.** Every open item was decided in a question-by-question session; §17 lists each one with the old recommendation and the decision. New open questions get the next free number (#173 onwards).

---

## 14. M0 checklist (every `[MEM]` claim and M0 check, ordered by how many decisions it can change)

**Since #166:** M0-2, M0-3, M0-4, M0-6, M0-7, M0-8, M0-12 and M0-14 are sync checks and are **postponed to the start of M4 (after v1)**. All other checks run in M0.

| ID | What is checked | Experiment | Pass criterion | Fallback if it fails | Decisions that depend on it |
|---|---|---|---|---|---|
| M0-1 | **Process taps:** `CATapDescription` stereo-mixdown, global-excluding and mute-when-tapped variants; tap point (after app volume, before device volume); behaviour on output-device change; DRM playback (Music, Safari video); original audio returns when md3 dies; tap teardown time; tap-invalidation events | Prototype tapping Music playing a reference file at known app volume; switch devices; play protected content; `kill -9`; time teardown | Captured audio within ≤0.05 LU of the file; mute-when-tapped silences the original; original back ≤1 s after a crash; teardown ≤300 ms (keeps #125 ≤500 ms) | No mute-when-tapped → processing only in driver mode; DRM silenced → those sources documented as unsupported; device change kills the tap → already handled by #163 | D4, #5, #8, #17, #81, #116, #120, #125, #126, #127, #128, #163 |
| M0-2 | **Player latency matrix:** Safari, Chrome, Firefox, QuickTime, TV, Music (video), IINA, VLC honour the virtual device's reported latency, at start and after a change | Virtual device reporting X; AV offset measured with a flash/click clip and a camera or loopback | Each player within ±10 ms of X at playback start; behaviour after a change documented | Unsupported players listed; driver mode is go only if ≥ 5 of 8 pass **and** Safari or Chrome is among them (#63); otherwise sync falls back to the AV offset only (#140) | D18, #63, #131, #140, #142 |
| M0-3 | **Driver transport** (a) loopback input + custom properties vs (b) shared memory; whether AudioServerPlugIns are sandboxed | libASPL prototype; custom property set at 10 Hz; heartbeat from read activity | Steering parameters delivered within 20 ms without glitches; heartbeat loss detected within 200 ms | (b) shared memory, with the costs stated in #130 | #130, #136, #141, #144 |
| M0-4 | **Clock follow:** the HAL accepts steered zero timestamps; the real Bluetooth device's drift against the host clock | 1 h playback logging ring fill; null test; compared with Apple aggregate drift correction | Ring fill within ±1 buffer over 1 h; no HAL overloads; bit-transparent | Apple aggregate drift correction (#67) | #136, #139, #145, #67 |
| M0-5 | **Out-of-process AU hosting** of third-party AUv2 and AUv3 on Apple Silicon: added latency and CPU per plugin; crash isolation | Host 3 AUv2 + 3 AUv3 out of process; kill the plugin host process | md3 survives a plugin crash; added latency ≤ 1 buffer; CPU overhead small enough for §6.1 (figure set from the measurement) | In-process hosting + watchdog + safe mode (#125) | #125, #129, #155, #1(A) |
| M0-6 | **Bluetooth latency variability:** across 20 reconnects, within a session (every 10 min for 1 h), across codecs and several headset models | Calibrator prototype (#132) | Spread ≤ 10 ms → the ±20 ms target holds | Always prompt on reconnect (#137); widen the target | #131, #137, #138, #142 |
| M0-7 | **Device visibility and failsafe:** which mechanism (not publishing the device vs hidden / not default-capable) keeps the virtual device out of the output picker without md3; fallback time after `kill -STOP` / `kill -9`; restore on quit | Driver prototype; reboot without md3 | Absent from the picker without md3; audio on the real device ≤ 500 ms after a kill | The other mechanism; else md3 restores the device at launch and the installer warns | #66, #130, #141 |
| M0-8 | **Built-in mic:** input latency report vs an electrical loopback through an interface with known latency; explicit selection by built-in transport type; raw input without voice processing; headset profile unchanged | Calibrator prototype + audio interface | Residual ≤ 2 ms; the headset never switches profile | A stored correction per Mac model; no raw input → manual method | #132, #133 |
| M0-9 | **AU facts:** reported latency (`AUAudioUnit.latency` / `kAudioUnitProperty_Latency`) for Apple and sample third-party units; AUPeakLimiter is sample-peak and its latency; AUNBandEQ / AUDynamicsProcessor parameter IDs; no M/S filtering among Apple units | Impulse through each unit; parameter-tree dump | Measured latency = reported ± 1 sample | md3 measures each stage's latency with an impulse at load instead of trusting the report | #117, #118, #119, #153 |
| M0-10 | **Lifecycle notifications:** will-sleep leaves time for `finish()`; device / rate / format change and tap-invalidation notifications arrive before data is lost | Prototype with forced sleep and device changes | Each event observed in time; the entry finishes via `finish()` | Finish from the last checkpoint (#151) | #151, #163 |
| M0-11 | **Aggregate-device drift correction** when processing outputs to a different device | 1 h playback, artefact and drift measurement | No audible artefacts; no drift | Processing output restricted to the source app's device | #126, #67 |
| M0-12 | **Volume keys** reach a virtual device's volume control; forwarding to Bluetooth hardware volume | Driver prototype | Keys work; the real device follows within one step | Digital gain in the Sync output stage only | #144 |
| M0-13 | **AppleScript metadata:** Spotify / Music track changes, app volume, normalisation; Safari / Chrome front-tab title (#21) | Script prototype | Track change detected within 1 s; values readable | Manual titles; loud match reset manually only | #17, #21, #122b |
| M0-14 | **Ear detection:** earbuds out of the ear keep playing md3's test signal | Calibrator prototype with AirPods and two other models | Sweep played and recorded | #134 procedure (disable ear detection) or manual (#135) | #134 |
| M0-15 | **FP environment on the HAL I/O thread** (is FPCR reset between callbacks?) | Denormal timing test in the callback | FTZ set at callback start is effective | None needed: it's set every callback | #82, V16 |
| M0-16 | **vDSP and buffer alignment:** different results for different alignments? | Kernels on 16- vs 64-byte-aligned and offset buffers, bit comparison | Identical, or identical once aligned per V14 | V14 already mandates 64-byte alignment | #106, V14 |
| DOC | **Document checks (no prototype):** BS.1770-5 gate operator and block indexing; MATLAB `round` semantics; ffmpeg `dualmono` / libebur128 dual-mono; AAC / MP3 priming counts; Hann scalloping figure; BT.1359 thresholds; Logic MultiMeter orientation; GRDB migrator details; Faraldo profile values and licence; Korzeniowski weighted score; GiantSteps / Ballroom licences | Read the primary sources | Matches the claim | Correct the affected decision text | #75, #77, #78, #83, #100, #111, #113, #114, #135, #150 |

## 15. Provisional values (how and when each is finalised)

| Value | Decision | How it is finalised | When (step in §16) |
|---|---|---|---|
| True-peak designs: 44.1 kHz 21 kHz / 64 taps; 48 kHz 22 kHz / 48; 88.2–192 kHz unchanged | #76a | Real hard-clipped / limited masters against an ideal reference and libebur128; CPU profile | Step 2 |
| Alignment: peak correlation ≥ 0.8, ≤ 50% of overlap at the floor, ≥ 50% overlap | #75 | Real cross-source captures (streaming vs file) | Step 4 |
| ρ undefined beyond 60 dB imbalance; −90 dB band floor | #96 | Real material | Step 5 |
| Peak hold 2 s / 20 dB/s; goniometer −40 … 0 dBFS; live stereo update rate | #88, #100, #97 | UX review | Step 5 |
| Tempo and key "—" confidence thresholds | #109, #111 | First benchmark | Step 7 |
| Expectations 60 / 88 / 65 / 95 / 60 and the ship gate | #113 | First benchmark, published | Step 7 |
| Minimum capture 15 s (tempo) / 30 s (key) | #115 | Benchmark accuracy vs excerpt length | Step 7 |
| Bass-mono default 120 Hz, LR4 | #118 | Listening (user-adjustable anyway) | Step 8 |
| A/B: ±24 dB clamp, 50 ms ramps, short-term for the first 3 s | #121 | #121 tests + listening | Step 8 |
| Loud match: up 0.5 dB/s, down 10 dB/s, +6 LU ceiling, +6 dB max boost, 10 s wait, −16 LUFS default | #122b | Real-track check | Step 8 |
| Ramps 20 ms (parameters), 50 ms (chain crossfade) | #124 | Listening | Step 8 |
| Stage budget > 50% of the buffer period in 3 of 20 callbacks; watchdog 200 ms with 50 ms polling; ≤ 500 ms to audible original audio | #125 | Failure-injection tests; M0-1 teardown time | M0, step 8 |
| Headroom 30 ms; margin 20 ms | #131 | M0-2, M0-6 | M0, step 9 |
| −12 dB first-arrival threshold, 50 ms window, spread ≤ 3 ms, 5 repeats, 0.3 m, −20 dBFS sweep | #132 | M0-8 + acoustic tests | M0, step 9 |
| Self-check residual ≤ 2 ms | #133 | M0-8 | M0 |
| DLL 1 Hz → 0.1 Hz | #136 | M0-4 | M0 |
| Prompt triggers 10 ms; median of the last 3 calibrations | #137, #138 | M0-6 | M0, step 9 |
| Crossfade 20 ms | #139 | Listening | Step 9 |
| Heartbeat 200 ms | #141 | M0-7 | M0 |
| ±20 ms end-to-end target | #142, §5.1 | M0-2, M0-6 | M0 |
| Analyser budget 5 ms per block in 10 of 50 blocks; stall 2 s | #146 | Profiling + failure-injection tests | Steps 1–2 |
| Rings: capture ≥ 4 s, meters 1 s | #147, #149 | Ring stress tests | Step 1 |
| Polling 20 ms | #148 | Energy Impact measurement | Step 3 |
| Journal interval 30 s | #151 | Recovery test and write volume | Step 4 |
| Backups weekly, keep 4 | #164 | UX review | Step 4 |
| CPU < 1% measuring with the dropdown closed, and the other §6.1 targets | §6.1, #161 | 10-minute run at shipping QoS | Step 10 |

## 16. Build order (respects #104; no code is written during the decision phase)

| Step | Build | Needs | CI jobs that come online |
|---|---|---|---|
| 0 | **M0 prototypes** (throwaway, outside the product code) | — | none; results recorded against §14, go/no-go for driver mode |
| 1 | **Infrastructure:** record types, SPSC ring library (#147, #149), Coordinator skeleton (re-blocking, FP environment, scheduling, time budgets, stall marker, failure isolation, `checkpoint()` plumbing), file-decoder input, golden corpus and test harnesses | — | unit tests; ThreadSanitizer on rings; ASan/UBSan (#106 e); ring stress (#162); disable-each, failure-injection and chunking harnesses with dummy modules (#106 a, c, d); `tools/` scripts committed (§4.8 item 1) |
| 2 | **LoudnessFrontEnd → Loudness, TruePeak; Derived** | 1 | Tech 3341 / 3342 generated vectors in CI, official EBU files incl. programme in a local run (§4.8 item 2, #176); chunk-size bit-identity (item 3); #76 burst test (item 1); clipped masters → finalise #76a (item 4); libebur128 cross-check; CPU kernel bench (item 8); disable-each and failure injection with real modules, incl. slow/blocked analysers (items 7, 9, #146) |
| 3 | **Capture** (taps, lifecycle events), live records, menu bar, dropdown shell (M1) | 1, 2 | #163 lifecycle tests (simulated events); capture-path end-to-end ≤0.05 LU (self-hosted runner with audio); polling energy check (#148) |
| 4 | **Storage**, history, Compare basics (#150–#152, #164; #75 alignment; #92) | 2 | storage round-trip, migration, export/import, #151 recovery (`kill -9`), #164 robustness, alignment tests, Compare version labelling (rule 5) |
| 5 | **SpectralFrontEnd → Spectrum** (incl. #88 live front end), **Stereo** (incl. goniometer) (M2) | 1, 4 | #93; #90 (a), (b); #101; #96 real-material check; version-discipline test across providers (#106 b) |
| 6 | **File-analysis workers**, full Compare (M3) | 4, 5 | concurrency identity test (#162); Compare overlays with failed/absent/recovered sections (V21) |
| 7 | **Tempo, Key** (M3.5) | 5 (Key uses SpectralFrontEnd) | synthetic unit tests (#115); local benchmark (#113, #114; datasets never in CI) → thresholds and ship gate |
| 8 | **Processing** (M5, M6): render chain, utility, gain stage, limiter, Apple AUs; then A/B, loud match, presets; then third-party AU hosting per M0-5 and editors; watchdog. The Sync output stage exists as a pass-through | 1, 3 | #129; #118; #121; #122b real-track check; #125 watchdog injection; "pre tap point → analyser sections bit-identical regardless of chain" |
| 9 | **Sync** (M4, **after v1**, #166; built after step 10 ships v1): driver (separate target, own version), engine, Calibrator, store; clock follow; #144, #145 | 8 (the Sync output stage is hosted in the chain; driver mode feeds the chain) | #143 on a dedicated runner with the driver installed; every other job keeps running without the driver ("non-sync features pass with the driver absent") |
| 10 | **Prefs, onboarding, Sparkle, release pipeline, compliance report** (M7 → v1; unsigned previews, signed 1.0 per #172) | all | §6 10-minute performance run at shipping QoS (#161); build / sign / notarise jobs |

**Note on milestones:** decided 2026-10-08 (§9.3 of the review report): Processing before Sync, and Sync after v1 (#166). Step numbers are kept for reference; the build order is 0–8, then 10 (v1), then 9 (v1.1). The Sync output stage stays a pass-through until step 9.

---

## 17. Decision log — open items closed 2026-10-08

Every item that was still 🟡 on 2026-10-07 was decided by you, question by question. **Rounds:** R1 = plan and release · R2 = producer focus · R3 = UI and everyday use · R4 = confirm-batches (with discussion where you asked for it). "As recommended" means you accepted the recommendation unchanged; **bold** marks a decision that differs from it.

### New decisions

| # | Decision | Round |
|---|---|---|
| ✅ 165 | **Audience and v1 jobs.** md3 is a Mac-wide audio utility for producers and mixing engineers, for everything outside the DAW. v1 core jobs: (1) mix vs reference tracks, (2) the same track across platforms vs the master (D22), (3) processing for listening (EQ, compressor e.g. for movies, plugins), (4) tempo/key as rough estimates. A DAW works as a source but gets no special design or testing. | R2 |
| ✅ 166 | **Bluetooth sync after v1** (amends D18). v1 = measurement, Compare, processing. Sync is the first big update (M4 / v1.1). Its M0 checks (M0-2, -3, -4, -6, -7, -8, -12, -14) move to the start of M4. #63, #66 and #70 are decided now and apply when sync is built. | R2 |
| ✅ 167 | Optional normalisation preview (amends D10), §4.2. | R2 |
| ✅ 168 | Dark and cream themes (amends D12), §2.3. | R4 |
| ✅ 169 | Size presets, §2.3. | R3 |
| ✅ 170 | Look preferences, §2.3. | R3 |
| ✅ 171 | macOS popover frame, square inside, §2.3. | R3 |
| ✅ 172 | Unsigned developer previews, signed 1.0, §9. | R4 |

### Items that were open

| # | Topic | Previous recommendation | Your decision | Round |
|---|---|---|---|---|
| 63 | Driver mode go rule | Yes, if "the main players" pass M0-2 | **≥ 5 of 8 players pass, and Safari or Chrome is one of them** (applies when sync is built) | R1 |
| §9.3 | Build order | Processing before Sync | As recommended; **and Sync after v1** (#166) | R1, R2 |
| 66 | Output takeover | While sync or processing is on | **Only while sync is on**, automatic | R1 |
| 40 | Licence | MIT | As recommended | R1 |
| 41 | Developer account | Before the first release | **Not yet; unsigned previews first, buy before 1.0** (#172) | R1, R4 |
| 44 | Milestones | Align with the build order | Rewritten: M5, M6, M7 (v1), then M4 sync (v1.1) | R4 |
| 70 | Sync UI | `sync` page + status text | Deferred with sync | R4 |
| 42 | Dependencies | Sparkle, KeyboardShortcuts, GRDB, libASPL | As recommended; libASPL only with sync | R4 |
| 43 | Distribution | GitHub, Homebrew, Sparkle, Actions | As recommended (open-source download on GitHub); driver `.pkg` only with sync | R4 |
| — | Repo basics; App Store | Yes; not targeted | As recommended | R4 |
| D10 | No platform tables | (founding) | **Amended: optional normalisation preview** (#167) | R2 |
| 24 | Compare | Up to 4 entries, one reference | As recommended; table and graph side by side | R2 |
| 5 | Meter tap point | Before processing, toggle | As recommended | R2 |
| 29 | Dropdown size | 600 × 380 | **720 × 320**, wide-ish and as short as possible; presets #169 | R3 |
| 1 | Pages | `lufs · spec · stereo · eq · comp · fx · sync` | **`lufs · spec · stereo · compare · eq · comp · fx`** | R3 |
| 22 | History / Compare / Prefs | Inside dropdown; Prefs window | As recommended | R3 |
| 33 | Terminal details | No rounded corners anywhere | Blocks for bars; **1 px lines for overlays; macOS popover frame outside** (#171) | R3, R4 |
| — | Bottom bar | Status line + button row (2 lines) | **One line: short status + icon buttons** | R3 |
| 48 | Preset placement | Chain presets always visible | **Only on eq / comp / fx** | R3 |
| 27 | Font | SF Mono, user-selectable | **SF Mono, fixed** | R3 |
| 30 | Navigation | Chevrons, keys, swipe; default page; hide pages | As recommended, **without page hiding** | R3 |
| 13 | Controls | Start/Stop + Reset, no pause | As recommended | R3 |
| 19 | "System (all)" | Yes | As recommended; entries labelled `system` | R3 |
| 21 | Browser titles | Manual entry | **Suggested from the front tab, you confirm** | R3 |
| 35 | Launch at login | Off by default | **On by default** | R3 |
| 25 | Retention | Keep forever | **Keep the last N (default 10); up to 20 saved entries never auto-delete** | R3 |
| 18 | Source list | Playing apps only | As recommended | R4 |
| 20 | Startup source | Remember last, wait | As recommended | R4 |
| 17 | App volume / normalisation | Read via AppleScript | As recommended; normalisation as a manual toggle where it can't be read | R4 |
| 45, 46 | Accuracy targets; compliance report | Yes; yes | As recommended | R4 |
| 12, 14 | Standard; ±0.1 LU | (settled by the review) | Marked ✅ | R4 |
| 51, 54, 55, 32/56 | Capture, frame rate, menu-bar rate, drawing | As listed in §6.2 | As recommended | R4 |
| 52, 53, 57, 59, 60, 61 | Engineering rules | (settled by the review) | Marked ✅ | R4 |
| 28 | Colours | Phosphor green, dark only | As recommended for dark; **cream theme added** (#168) | R4 |
| 31 | Menu bar format | `-14.1` | As recommended | R4 |
| 34 | Hotkeys | Only Start/Stop bound | **None bound** | R4 |
| 36 | Onboarding | 3 steps; driver/mic at first sync or processing | Driver/mic only with sync; launch-at-login step shows "on" | R4 |
| 37 | Updates | Daily check, prompt | As recommended | R4 |
| 38 | Language | English, translation-ready | As recommended | R4 |
| — | Other standard behaviour | Single instance, accessibility, no telemetry | As recommended | R4 |
| 23 | Grouping | "artist — title" | As recommended | R4 |
| D12 | Dark only | (founding) | **Amended: dark + cream**, follows macOS, overridable (#168) | R4 |
| D18 | Sync is core | (founding) | **Amended: after v1** (#166) | R2 |

**Unchanged by this session:** every design-review decision #74–#164, except where a row above says otherwise. The #118 test criterion was corrected separately on 2026-10-07 (2·fc → 5·fc).

---

## 18. Build-phase decision log

Every decision made or changed during the build phase gets one row here, numbered from #173. A row states the old text, the new decision and why. Reasoning or evidence longer than three lines goes in `docs/decisions/<number>-<slug>.md`, linked from the row. A decision that replaces an earlier one is struck through in place with a pointer to its new number.

| # | Date | Task | Old text | New decision | Why |
|---|---|---|---|---|---|
| ✅ 173 | 2026-10-08 | B0.4.2 | #111: "The set is chosen on dev data from Krumhansl–Kessler, Temperley, Sha'ath and Faraldo's EDM profiles" | **Key-profile sources.** Key-profile values come only from the publication that defines them, cited in the code; never copied from GPL, AGPL or unlicensed code. A profile whose values aren't published is left out unless its author grants a licence (#111 amended). | Faraldo's profile values have so far been found only in unlicensed code (`angelfaraldo/edmkey`) and in AGPL Essentia; his publications (ECIR 2016, AES 2017, 2018 thesis) haven't been checked for printed values yet (B8.2.1). The maintainer never uses unlicensed or incompatibly licensed material. Evidence: docs/M0-RESULTS.md, DOC row 11 |
| ✅ 174 | 2026-10-08 | B0.4.2 | — (new) | **Sourcing rule.** No third-party code, constants, tables, test files or data enter the repository, CI output (artifacts, caches, logs), release assets or the app bundle unless their licence is compatible with MIT. Published values may be used when taken from the publication that defines them and cited. Anything unclear is checked and noted before use. This doesn't replace security rule 3: every new dependency still needs the maintainer's approval. | Generalises #173 after the DOC checks found unlicensed and AGPL sources for data md3 planned to use. Evidence: docs/M0-RESULTS.md |
| ✅ 175 | 2026-10-08 | B0.4.2 | #114: "Dataset audio is fetched locally under each dataset's terms, never committed or used as CI artifacts; licence terms to be checked." | **Dataset labels kept local.** Dataset audio **and annotations** are fetched locally, never committed or used as CI artifacts; only md3's aggregate scores are published (#114 amended). | The GiantSteps key, tempo and MTG-key repositories have no licence; Ballroom publishes no terms. Evidence: docs/M0-RESULTS.md, DOC row 13 |
| ✅ 176 | 2026-10-08 | B0.4.2 | §4.8 item 2: "The Tech 3341 and 3342 vectors, including the downloaded programme vectors 3341 #7–8 and 3342 #5–6" (in CI); B3.2.3 done when "CI jobs green" | **EBU test files.** Generated in code and run in CI: 3341 #1–6, #9–23 and 3342 #1–4. Official EBU files stay on the maintainer's Mac, are never committed or uploaded (`.gitignore` + `track.py check`), and pass a local run with an agreement test: generated vs official within 0.01 LU / 0.01 dB, except 3341 #20–23, where md3's reading of EBU's file must be within +0.2 / −0.4 dB and the difference is informational. **B3.2.3 finish line:** generated vectors pass in CI; the official set incl. 3341 #7–8 and 3342 #5–6 passes the local run, numbers in Evidence; chunk-size bit-identity green in CI. md3 claims "EBU Mode" only from the full official set passing locally. EBU is asked about CI use in parallel. Details: [docs/decisions/0176-ebu-test-files.md](decisions/0176-ebu-test-files.md) | EBU's terms (July 2019) allow internal R&D use only and forbid copying or distributing the files. |
