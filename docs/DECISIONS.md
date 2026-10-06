# md3 — Decision Document

> Status: **pre-build / design**. Last updated: 2026-10-06.
>
> Legend: **✅ Decided** · **🟡 Open** (has a recommendation, awaiting your call) · **⛔ Superseded**
>
> Open items keep the numbering used during design discussions (`#1`–`#73`) so they can be referenced quickly ("accept all except #12, #40").

---

## 0. The app

**md3** is a lightweight macOS menu bar app for accurate audio metering and processing of a single app's audio. Its core job is **comparing the same song across sources** — browser, Apple Music, Spotify and local files — with verified loudness, spectrum and stereo measurements, stored in a history stack for side-by-side comparison. It also hosts Audio Unit plugins for per-app processing and fixes **Bluetooth audio/video sync** system-wide.

**Principles**

1. **Accurate.** Every measurement is verified against published standards or reference implementations in CI (§4).
2. **Better than the free option.** Every feature must have a concrete edge over free tools (§11), or it doesn't ship.
3. **Lightweight.** Near-zero idle cost, small binary, minimal dependencies (§6).
4. **Out of the way.** Menu bar first, minimal, dark, monospaced. Displays data; doesn't lecture (no advice text, no platform-target tables).
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
| D10 | **No streaming-platform target tables and no advice or warning text.** The app displays measurements only. |
| D11 | **Stereo: phase and width**, similar to Logic's Mastering Assistant. **Width is shown as a spectrum** (width per frequency band). |
| D12 | **UI:** fully **monospaced**, **dark only**, terminal/coder look, minimal. |
| D13 | Dropdown **pages switched with ‹ › chevrons**; the user can set the **default page**. |
| D14 | Pages include **lufs, spec, stereo, comp, eq** (comp = compressor). |
| D15 | **History and prefs** are reached from the **bottom bar** of the dropdown. |
| D16 | **Audio plugin hosting is a must-have.** |
| D17 | **Presets** must be quick to use from within the dropdown. |
| D18 | **Bluetooth audio/video sync is a core feature.** |
| D19 | Every feature must be **accurate** and an **improvement over free apps**. |
| D20 | **Performance** is a requirement: light and efficient (§6). |
| D21 | Will eventually be **released as open source**. |
| D22 | Main use case: **comparing levels across platforms** (browser, Apple Music, Spotify, mp3/file). |

---

## 2. Product & UI

### 2.1 Layout (proposed)

```
 menu bar:   ●-14.1                     (● while recording; --.- before any measurement)

┌──────────────────────────────────────────────────────────┐
│ src: spotify ▾   "Title" — Artist   128bpm Amin  [● 03:41]│  header (always visible)
│ preset: [flat] [bass mono] [night] [+]              A/B  │  chain presets (always visible)
│──────────────────────────────────────────────────────────│
│ ‹  LUFS · spec · stereo · eq · comp · fx · sync  ›       │  chevron pages
│                                                          │
│                     (page content)                       │
│                                                          │
│──────────────────────────────────────────────────────────│
│ src:spotify vol:100% norm:off 48k pre lat:0ms  sync:off  │  status line
│ [history]  [prefs]                              [pin]    │  bottom bar
└──────────────────────────────────────────────────────────┘
```

### 2.2 Pages

| Page | Content |
|---|---|
| `lufs` | Integrated (large), short-term, momentary, true peak, LRA, PLR, short-term history graph |
| `spec` | Live spectrum + averaged spectrum for the current measurement, peak hold |
| `stereo` | Width spectrum (per band: width = bar height, correlation = colour), goniometer, correlation, balance |
| `eq` | Plugin slot pre-loaded with Apple `AUNBandEQ`, drawn as a native EQ curve/band list (see #72) |
| `comp` | Plugin slot pre-loaded with Apple `AUDynamicsProcessor`, with a gain-reduction meter (see #72) |
| `fx` | Additional AU plugin slots (proposed, #2) |
| `sync` | Bluetooth AV sync: device, measured vs reported latency, total latency X, drift graph, calibrate/nudge controls (proposed, #70) |

### 2.3 Open UI decisions 🟡

| # | Question | Recommendation |
|---|---|---|
| 1 | Final page list and order | `lufs · spec · stereo · eq · comp · fx · sync`. Header, chain presets, status line and bottom bar stay visible on every page. |
| 22 | Where do History / Compare / Prefs open? | `[history]` replaces the page area inside the dropdown, and Compare opens from History in the same place. `[prefs]` opens a standard settings window (also ⌘,). |
| 27 | Font | SF Mono by default (built in, nothing to bundle). Prefs can choose any installed monospaced font. |
| 28 | Colours | Background `#0B0B0C`, text `#C8C8C8`, dim text `#5A5A5A`, one accent (default phosphor green `#7CFC9A`, user-selectable). Amber/red only near and over 0 dBFS. |
| 29 | Dropdown size | Fixed **600 × 380 pt**; every page is designed to fit. |
| 30 | Page navigation | Chevrons, ←/→, number keys, trackpad swipe, wrapping at the ends. Prefs: default page or "remember last page", and hiding unused pages. |
| 31 | Menu bar format | `-14.1` in monospaced digits, `●-14.1` while recording, `--.-` before any measurement. Prefs can switch to live short-term or true peak. |
| 33 | Terminal-style details | Labels like `[● rec 03:41]`, `src:spotify`; right-aligned numbers; bars drawn with block characters `▁▂▃▄▅▆▇█`; no rounded corners or shadows; 1-px dividers. |
| 48 | Preset placement | Chain presets always visible under the header; page presets on each processing page. |

---

## 3. Audio architecture

### 3.1 Signal flow

```
Tap mode (metering only, no driver, zero added latency):
  App ──► device (unchanged)
   └─► process tap ──► ring buffer ──► analysis (LUFS/TP every sample; FFT/stereo only when visible)

Driver mode (sync and/or processing):
  Player ──► md3 virtual device (reports fixed latency X) ──► md3 engine
     │                                                           │
     │     process tap (per-app meters, pre/post)                ▼
     └─ delays its video by X           eq ─► comp ─► fx slots ─► padding delay ─► real output (e.g. AirPods)
```

### 3.2 Sources 🟡

| # | Question | Recommendation |
|---|---|---|
| 18 | Source list | Only apps with audio activity, currently-playing first, with icons. Helper processes grouped under their parent app (all Chrome helpers → "Chrome"). |
| 19 | Include a "system (all)" source? | Yes, as one option in the same single-select list. |
| 20 | Startup | Remember the last source. If that app isn't running, show it greyed out and capture it automatically once it starts. |
| 21 | Track titles for browsers | Manual title entry. Automatic titles for Spotify and Music via AppleScript. No Accessibility permission. |
| 17 | App volume / normalization info | Read via AppleScript for Spotify and Music; `vol:? norm:?` otherwise. Display and record only. |

### 3.3 Processing & plugins 🟡

| # | Question | Recommendation |
|---|---|---|
| 72 | eq/comp: built-in DSP or plugin loader? *(was "3a")* | **Each processing page is a plugin slot pre-loaded with Apple's built-in Audio Unit** (`AUNBandEQ`, `AUDynamicsProcessor`; also `AUPeakLimiter`, `AUMultibandCompressor`, `AUSampleDelay` available), drawn in md3's own UI, with `[swap ▾]` to replace it with any third-party AU. No EQ/comp code written from scratch. |
| ⛔ 2 | ~~Built-in EQ/comp processors~~ | Superseded by #72. Still open: whether there's an **`fx` page** with up to 8 extra AU slots. Recommendation: yes. |
| 1 (A) | Plugin formats | AUv3 + AUv2 only. VST3 later (its SDK is now MIT). No CLAP in v1. |
| 3 | Chain order | Fixed `source → eq → comp → fx → delay → output`, each stage bypassable. Reordering later. |
| 4 | Plugin UIs | The plugin's own editor in a separate floating window; a generic parameter list if the plugin has no editor. |
| 5 | Meter tap point | Before processing by default, with a pre/post toggle. Each history entry records which was used and the chain state. |
| 6 | Mute the original only when processing | Yes. All stages bypassed = pure listening, zero latency. |
| 7 | Latency display | Show total chain latency in the status line. In driver mode it's absorbed into X (§5). |
| 8 | Crash safety | AUv3 plugins run out of process. If md3 dies, macOS removes its tap and the original audio returns (verify in M0). A watchdog bypasses the chain if the processing thread stalls. |
| 9 | Presets | Named chain presets, with optional auto-load per source app / per output device. Plugins keep their own presets. |
| 10 | Level-matched A/B | Yes: one-button bypass with loudness compensation based on measured LUFS. |
| 11 | Output device | Follow the system default; can be fixed to a specific device in prefs. |
| 49 | Factory presets | `flat`, `mono`, `bass mono` (<120 Hz summed), `night`, `voice`, `loud match`, `bt sync`. All built from Apple AUs. |
| 50 | `loud match` preset (auto-gain to a LUFS target) | Yes. Directly supports comparing sources. |

---

## 4. Measurement & accuracy

### 4.1 Measurement set

Integrated / short-term / momentary LUFS, LRA, true peak (4× oversampled), PLR, spectrum (live + averaged), width spectrum, correlation, goniometer, balance, key and BPM (#73), loudness curve over time.

### 4.2 Open measurement decisions 🟡

| # | Question | Recommendation |
|---|---|---|
| 12 | Standard | ITU-R BS.1770-5 / EBU R128. K-weighting recalculated per sample rate. |
| 13 | Controls | Start/Stop + Reset, no pause. Stop always saves; Reset discards. |
| 14 | Accuracy bar | ±0.1 LU against the EBU compliance set, checked in CI. |
| 15 | Spectrum defaults | 8192-point FFT, 75% overlap, +4.5 dB/oct tilt, 1/6-octave smoothing, 20 Hz–20 kHz, −90 to 0 dB. All adjustable. |
| 16 | Width spectrum definition | Per 1/3-octave band: width = side / (mid + side) energy (bar height); correlation per band (bar colour). Live plus per-measurement average. |
| 45 | Accept the accuracy targets below? | Yes. |
| 46 | Publish a compliance report in the docs? | Yes. |
| 73 | Key / BPM: v1 or later? *(was "3c")* | Written in-house (the existing libraries are GPL/AGPL). Calculated during measurements and file analysis, shown on the track line, stored in history. Milestone after M3. |

### 4.3 Verification references

| Feature | Reference | Pass target |
|---|---|---|
| M / S / I LUFS | ITU-R BS.1770-5, EBU Tech 3341, ITU-R BS.2217 | ±0.1 LU |
| LRA | EBU Tech 3342 | ±1 LU (spec); target ±0.1 |
| True peak | EBU Tech 3341 true-peak cases | +0.2 / −0.4 dB (spec); target ±0.1 |
| PLR | Derived from TP and integrated | Same as its inputs |
| All loudness | Cross-check against libebur128 (MIT) on a real-music library | ≤0.05 LU |
| Spectrum | Generated sines, white/pink noise | Frequency within one FFT bin; level ±0.1 dB; correct slope |
| Correlation / width | Mono, left-only, polarity-flipped, uncorrelated noise | ±0.01 |
| Width spectrum | Band-limited versions of the signals above | ±2% within the band, no leakage into neighbours |
| Goniometer | Orientation of Logic's MultiMeter | Matches |
| BPM | GiantSteps Tempo, Ballroom (MIREX metrics) | ≥85% exact; ≥95% allowing half/double |
| Key | GiantSteps Key (MIREX weighted) | ≥70% weighted; labelled as an estimate in the UI |
| Sample rates | 44.1 / 48 / 88.2 / 96 / 192 kHz | Same targets |
| Capture path end to end | Play a file in Music vs analyse the same file directly | ≤0.05 LU |

**Known limits:** resampling when the file and device rates differ (true peak can shift by about 0.1–0.3 dB; each entry records the device rate); lossy encoding on streaming services (a real difference in the audio, not an error); app volume and normalization (recorded, not corrected).

---

## 5. Bluetooth audio/video sync

### 5.1 Approach

- **Problem:** Bluetooth audio arrives 150–300 ms late. Players delay their video by the latency macOS reports, but Bluetooth devices often report it wrongly, md3's processing adds unreported latency, and latency drifts during playback.
- **Fix: driver mode.** md3 installs a virtual output device (an AudioServerPlugIn, not a kernel extension) that reports a **fixed total latency X** = measured Bluetooth latency + chain latency + a safety margin. The md3 engine adds whatever **padding delay** is needed so sound always reaches your ears exactly X ms later. Changing the chain changes only the padding, never X, so players never need to resync.
- **Calibration:** automatic, by playing a test sweep and recording it with the **Mac's built-in mic** (never the headset's mic, which switches the headset into call mode), about ±5 ms. Manual visual flash/click alignment as a fallback, plus ±5 ms nudges. **Saved per device** and applied automatically when it connects.
- **Target:** within ±20 ms (inside EBU R37's +40 / −60 ms tolerance; ITU-R BT.1359 detection thresholds are about +45 / −125 ms).
- **Drift:** continuous monitoring with gradual speed correction; prompts to recalibrate when latency moves by more than 10 ms.
- **Failsafe:** the driver watches for md3's heartbeat. If md3 is gone, the virtual device marks itself unavailable so macOS falls back to the real device. md3 also restores the original device when it quits normally.
- **Licensing:** built on **libASPL (MIT)**. No code from BlackHole (GPL-3) or Background Music (GPL-2).
- **Known limits:** games and other interactive apps can't delay their video; some players read latency only at playback start; a few apps ignore device latency entirely.

### 5.2 Open sync decisions 🟡

| # | Question | Recommendation |
|---|---|---|
| 47 | Delay only vs full driver mode | ⛔ Resolved by D18: full driver mode is required. |
| 63 | Driver mode in v1 | Yes, after M0 shows the main players honour the reported latency. |
| 64 | Calibration methods | Automatic via mic as the main method; manual visual fallback; nudges. Mic permission requested only when calibrating. |
| 65 | Default safety margin in X | 20 ms, adjustable. |
| 66 | Take over the system output automatically | Only while sync or processing is on; otherwise return to the real device. |
| 67 | Clock drift correction | Start with Apple's built-in aggregate-device drift correction in M0; replace with md3's own gradual correction if measurements show it isn't good enough. |
| 68 | Recalibration prompt threshold | Latency moves by >10 ms for >5 s. |
| 69 | Driver build | libASPL, MIT, signed `.pkg` installer, heartbeat failsafe. |
| 70 | Sync UI | A `sync` page; the status line always shows `sync: airpods 186ms ✓`. |
| — | Audio delay (sync offset) | A positive delay of 0–2000 ms with ±1 / ±10 ms nudges, saved per app and per device. Covers the reverse case (video later than audio, e.g. a TV with display lag). Decided as a feature (answer to "3b"); details still open. |

### 5.3 M0 verification matrix (must pass before building on it)

Safari, Chrome, Firefox, QuickTime, the TV app, Music (video), IINA and VLC: does each honour the virtual device's reported latency, at playback start and after a change? Does the heartbeat failsafe return audio to the real device when md3 is killed? Is Apple's drift correction good enough?

---

## 6. Performance 🟡

### 6.1 Targets (Apple Silicon)

| State | CPU | RAM |
|---|---|---|
| Idle (not measuring, dropdown closed) | ~0% | <30 MB |
| Measuring, dropdown closed | <1% | <40 MB |
| Measuring, dropdown open | <4% | <60 MB |
| Apple-AU processing | <3% plus plugins | — |
| App size <10 MB · launch to menu bar <200 ms · Energy Impact "Low" | | |

### 6.2 Open performance decisions

| # | Question | Recommendation |
|---|---|---|
| 51 | When the tap runs | Only while measuring, while the dropdown is open, or while processing; stop 2 s after none apply. |
| 52 | Audio thread rules | No allocation, locks, logging, or runtime reference counting in the audio callback. Real-time code in a small C/C++ module. Debug builds fail loudly when the rules are broken. |
| 53 | Split analysis by need | LUFS/TP on every sample; FFT, width spectrum and goniometer only while visible; history's averaged spectrum at 4096 points in the background. |
| 54 | Frame rate | 30 fps (60 optional), following the display refresh, drawing nothing while hidden. |
| 55 | Menu bar update rate | 2 Hz, and only when the text changes. |
| 32 / 56 | Drawing | SwiftUI for static layout only. Meters drawn as Core Animation layers with geometry reused. Metal only if profiling requires it. |
| 57 | Point limits | Goniometer ≤2,000 points per frame; spectrum ≈256 log-spaced points. |
| 58 | Database writes | One write at Stop, on a background thread. Loudness curve at 10 values a second (about 30 KB per entry). |
| 59 | File analysis | Low-priority background thread, processed in chunks, with progress and cancel. |
| 60 | Power awareness | In Low Power Mode or under thermal pressure: 15 fps and pause the background spectrum. LUFS never reduced. |
| 61 | Preventing slowdowns | A CI performance test (10-minute run within the targets) plus Instruments profiling before each release. |
| 62 | Plugin loading | Load when a slot is enabled; keep bypassed plugins loaded; reuse loaded plugins across preset changes. |

---

## 7. System behaviour 🟡

| # | Question | Recommendation |
|---|---|---|
| 34 | Default hotkeys | Only start/stop is bound (⌃⌥Space). Everything else, including presets 1–4, is assignable but unbound. |
| 35 | Login / Dock | Launch at login off by default and offered during onboarding. No Dock icon (`LSUIElement`). |
| 36 | Onboarding | 3 steps: System Audio Recording permission; optional Automation permission (Spotify/Music); launch at login. The driver and mic are requested only when you first use sync or processing. |
| 37 | Updates | Sparkle, daily check, prompt before installing. |
| 38 | Language | English only in v1; all text prepared for translation. |
| — | Other standard behaviour | `SMAppService` login item; single instance; recovery from sleep/wake and device changes; a source app quitting ends the measurement and saves it as "interrupted"; respects Reduce Motion / Increase Contrast; VoiceOver labels; no telemetry. |

---

## 8. History & Compare 🟡

**Each entry stores:** source app, track title/artist, start time, duration, device and sample rate, app volume/normalization (when known), pre/post tap point and chain state, I / max ST / max M LUFS, TP, LRA, PLR, width and correlation, averaged spectrum, averaged width spectrum, loudness curve, key/BPM, and notes.

**Files:** drag-and-drop files are analysed faster than real time and saved as "File" entries (the unencoded reference).

| # | Question | Recommendation |
|---|---|---|
| 23 | Grouping | Normalized "artist — title"; drag entries between groups, or rename. |
| 24 | Compare | Up to 4 entries, one marked as reference with differences shown relative to it. Table, plus overlays (spectrum with a level-matched toggle, width spectrum, time-aligned loudness curves). |
| 25 | Retention | Keep forever, delete manually. Export CSV/JSON, import JSON. |
| 26 | Storage | SQLite via GRDB. Spectra and curves stored as compact binary data. |
| — | Leading/trailing silence | Trimmed automatically from each entry. |

---

## 9. Open source & release 🟡

| # | Question | Recommendation |
|---|---|---|
| ✅ 39 | Name | **md3** (D1). Still to check availability on GitHub and Homebrew. |
| 40 | License | **MIT**. GPL-3.0 only if stopping closed-source forks matters more than adoption. |
| 41 | Apple Developer account | Not needed while building. Required ($99/yr) before the first public release, for signing and notarization (the app **and** the driver `.pkg`). |
| 42 | Dependencies | Sparkle, KeyboardShortcuts, GRDB, libASPL. All MIT. DSP written on Accelerate. |
| 43 | Distribution | GitHub Releases (notarized `.dmg` + driver `.pkg`), a Homebrew tap (`brew install --cask <user>/tap/md3`), a Sparkle feed on GitHub Pages, and GitHub Actions to build, sign, notarize, and publish on version tags. |
| — | Repo basics | LICENSE, README, CONTRIBUTING, CHANGELOG, issue templates, the compliance report, a build-from-source guide. |
| — | Mac App Store | Not targeted (the sandbox conflicts with process taps, AppleScript control of other apps, and the driver). |

---

## 10. Milestones 🟡 (#44, revised by #71)

| Milestone | Scope |
|---|---|
| **M0** | Prototypes: (a) process taps + source switching + mute/replace; (b) virtual device latency reporting across the §5.3 player matrix, heartbeat failsafe, drift. **Go/no-go for driver mode.** |
| **M1** | LUFS/TP engine + test suite, menu bar app, start/stop, dropdown shell with chevron pages. |
| **M2** | `spec` and `stereo` pages (width spectrum, goniometer, correlation). |
| **M3** | History, Compare, file analysis, CSV/JSON export. |
| **M3.5** | Key/BPM (#73). |
| **M4** | Driver mode + `sync` page + calibration. |
| **M5** | Processing chain: `eq` / `comp` slots with Apple AUs, presets, A/B, `loud match`. |
| **M6** | `fx` slots / third-party AU hosting and editor windows. |
| **M7** | Prefs, onboarding, Sparkle, signing/notarization, release pipeline, compliance report. |

---

## 11. Edge over free tools (the feature bar)

| Feature | What free tools usually offer | md3 |
|---|---|---|
| LUFS | A single integrated number, often not verified | Verified against EBU/ITU test sets with a published report; per-app capture; history grouped by track |
| Comparing sources | Nothing, or manual notes | Grouped stack, a reference entry, time-aligned overlays, recorded app volume and normalization |
| Spectrum | Live display only | Per-measurement average, overlays, level-matched comparison |
| Stereo | Correlation and goniometer | Width spectrum, saved and compared between entries |
| EQ / comp | System-wide EQ only | Per-app chains, AU hosting, presets auto-loaded per app/device, level-matched A/B |
| Bluetooth sync | A manual offset inside one player | System-wide, mic auto-calibration, per-device memory, fixed latency total, drift monitoring |
| Key / BPM | A separate app | Saved with the loudness entry, accuracy measured against public datasets |

---

## 12. Risks & unknowns

| Risk | Mitigation |
|---|---|
| Players don't honour the virtual device's latency | M0 matrix gates driver mode; document which players are supported |
| Heartbeat failsafe doesn't return audio to the real device | Also restore on quit; a small helper as backup; verify in M0 |
| Apple aggregate-device drift correction too poor | md3's own gradual correction (#67) |
| Bluetooth latency varies between connections or codecs | Per-device calibration + drift monitor + recalibrate prompt |
| Process tap API differences between 14.2 and 27 | Test matrix on 14.x, 15.x, 26.x and 27.x |
| AUv2 plugin crashes take down md3 | Prefer AUv3 (out of process); watchdog; the tap disappears with the process |
| Driver install friction / trust | Signed and notarized `.pkg`; metering works without the driver; clean uninstall |
| Key/BPM accuracy below targets | Labelled as an estimate; half/double tempo toggle; ship after M3 only if targets are met |

---

## 13. How to close the open items

Reply with overrides by number (e.g. "accept all except #29, #40 → GPL"). Every 🟡 item without an override becomes ✅ with its recommendation, and this document gets updated accordingly.
