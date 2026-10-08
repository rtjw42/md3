# M0 results

Results of the checks in DECISIONS.md §14. Each row records what was checked, against which primary source, and the outcome. Prototype results (M0-1 … M0-16) are added in batch B1.

## DOC: document checks (B0.4.2, 2026-10-08)

| # | Claim (where) | Primary source | Result |
|---|---|---|---|
| 1 | Integrated gating keeps blocks with loudness **strictly above** each gate: `> −70 LUFS` and `> relative − 10 LU` (§4.4 #84 reproduction; #77) | ITU-R BS.1770-5 (11/2023), Annex 1 eq. (3)–(7): "J_g = {j : l_j > Γ}"; relative gate Γr = (loudness after Γa) − 10 | ✅ Confirmed. Note: LRA uses `>=` (row 2), so the two gates differ on purpose; implement each as its standard says. |
| 2 | Block indexing: 400 ms blocks, 75% overlap, j = 0, 1, 2, …; incomplete blocks at the end are dropped (#84) | BS.1770-5 Annex 1: "Tg = 400 ms, to the nearest sample", overlap 75%, j ∈ {0, 1, 2, …, (T − Tg)/(Tg·step)}, "Incomplete gating blocks at the end of the measurement interval are not used." | ✅ Confirmed. |
| 3 | LRA: both gates `>=`; relative gate −20 LU from the mean power of the absolute-gated values; percentile index `round((n−1)·p/100 + 1)`; short-term rate ≥ 10 Hz (#78) | EBU Tech 3342 V4 (November 2023) §5 MATLAB: `ShortTermLoudness >= ABS_THRES`, `stl_absgated_vec >= stl_integrated + REL_THRES` (REL_THRES = −20), `stl_sorted_vec(round((n-1)*PRC_LOW/100 + 1))`; "a rate of at least 10 Hz" | ✅ Confirmed verbatim. The same code comment asks for ≥ 1.5 s of trailing silence in file-based measurement; #84 already rejects padding on purpose and documents why. |
| 4 | MATLAB `round` rounds halves away from zero; Swift `.rounded()` matches; `rint` does not (#78) | MathWorks `round` reference: "rounds away from zero to the nearest integer with larger magnitude". Swift, run here (Swift 6.4): `2.5.rounded()` = 3, `(-2.5).rounded()` = −3, `rint(2.5)` = 2, `rint(0.5)` = 0 | ✅ Confirmed. |
| 5 | ffmpeg / libebur128 read mono files 3.01 LU lower unless told the file is dual-mono (#83) | ffmpeg `libavfilter/f_ebur128.c`: option `dualmono` "treat mono input files as dual-mono", default 0; `panlaw` default −3.01029995663978, subtracted from I, M, S and LRA when `dualmono` is set on 1-channel input. libebur128 `ebur128.h`: `EBUR128_DUAL_MONO` "a channel that is counted twice"; channel 0 defaults to `EBUR128_LEFT` (counted once) | ✅ Confirmed. |
| 6 | AAC / MP3 priming counts (no number is stated in DECISIONS.md; relevant to #75 trim and the B2.3.1 file decoder) | Apple TN2258: AAC "priming value is currently fixed at 2112 samples", remainder < 1024; ExtAudioFile and movie playback remove priming and remainder automatically; AudioQueue does not. LAME tech FAQ: encoder delay "The default right now is 576"; "All decoders I have tested introduce a delay of 528 samples" | ✅ Facts recorded; no spec text to correct. **Build note (B2.3.1, B2.3.6):** decode through ExtAudioFile / AVAudioFile and test that AAC priming is removed and whether LAME gapless info (encoder delay + padding) is honoured for MP3; otherwise a file's first ~1,100 samples are silence and its duration is ~0.02–0.05 s long. |
| 7 | Hann window scalloping loss ≈ 1.42 dB (spectrum, §4.5; #86 says band power removes it) | Computed here: N = 8192 Hann, response at half a bin vs at the bin centre = −1.424 dB; matches the standard table value (Harris 1978, 1.42 dB) | ✅ Confirmed. |
| 8 | ITU-R BT.1359 detection thresholds ≈ +45 / −125 ms; EBU R37 tolerance +40 / −60 ms (§5.1) | BT.1359-1 (11/1998): "detectability thresholds are about +45 ms to –125 ms and acceptability thresholds are about +90 ms to –185 ms", positive = sound advanced. EBU R37 (2007) Table 1: sound before picture ≤ 40 ms, sound after picture ≤ 60 ms | ✅ Confirmed (sync is after v1, #166). |
| 9 | Goniometer orientation matches Logic's MultiMeter: mono vertical, L-only upper-left, anti-phase horizontal (#100) | Apple, MultiMeter Goniometer guide: L and R on the X/Y inputs "rotating the display by 45°"; centre line labelled "M for mid/mono"; phase problems show as "trace cancelations along the center line" | ⚠️ **Partly confirmed:** mono is vertical. Apple doesn't document which diagonal an L-only signal takes. **Open:** a hands-on check in Logic with an L-only test tone, done with the user in B6.3.2. #100's formula puts L-only upper-left, the usual convention. |
| 10 | GRDB's migrator is fit for #150 / #164 (versioned migrations; detect a DB written by a newer md3) | GRDB `DatabaseMigrator.swift`: migrations run in a transaction and abort on error; applied migrations recorded in `grdb_migrations`; `hasBeenSuperseded(_:)` "indicating whether the database refers to unregistered migrations … likely been migrated by a more recent migrator"; deferred foreign-key checks before commit | ✅ Confirmed. **Build note (B5.1.1, B5.2.2):** use `hasBeenSuperseded` for #164's "newer md3" case; never enable `eraseDatabaseOnSchemaChange` outside `#if DEBUG` (it wipes the database and is not debug-only in GRDB). |
| 11 | Faraldo's EDM key profiles: values and licence (#111) | Author's repository `angelfaraldo/edmkey` (`templates.py` holds `edma`, `edmm` and others): **no licence** (GitHub API: none; no notice in the file). Essentia, which also ships them, is AGPL-3 | ❌ **Licence not cleared.** Code with no licence is all rights reserved; AGPL can't be shipped inside MIT md3. **Fixed by #173 (approved, option A):** #111 amended. Not yet checked: whether Faraldo's ECIR 2016 / AES 2017 papers or 2018 thesis print the values (B8.2.1). |
| 12 | Korzeniowski & Widmer 2017 weighted key score ~74.3 on GiantSteps Key (§4.7 table, "via a secondary source") | Primary: Korzeniowski & Widmer, "End-to-End Musical Key Estimation Using a Convolutional Neural Network", EUSIPCO 2017 (arXiv 1706.02921), Table I, GS test set, CK1 (trained on GiantSteps MTG): weighted 74.3, correct 67.9, fifth 6.8, relative 7.1, parallel 4.3, other 13.9 | ✅ Confirmed from the primary source; the §4.7 table now cites it directly. |
| 13 | GiantSteps / Ballroom licence terms (#114) | GiantSteps key, tempo and MTG-key repositories: **no licence** (GitHub API: none); audio is Beatport preview MP3s fetched by a script; key labels come from forum corrections. Ballroom (ISMIR 2004 contest, from ballroomdancers.com): no terms published upstream; the mirdata loader labels it CC BY-NC-SA 4.0 (secondary) | ✅ #114's rule holds (fetch locally, never commit, never use as CI artifacts). Extended to the annotation files by #175 (approved 2026-10-08). |

### Proposal #173 (from B0.4.2): key-profile sources — approved 2026-10-08, option A (DECISIONS.md §18)

Problem: #111 chooses among Krumhansl–Kessler, Temperley, Sha'ath and Faraldo profiles, but doesn't say where the numbers come from. Faraldo's are only available as unlicensed code or inside AGPL Essentia. Sha'ath's reference implementation (libKeyFinder) is GPL-3.

Options:
- **A (recommended):** take every profile's 24 values only from the published paper or thesis that defines it, cited in the code, never copied from GPL/AGPL/unlicensed code. A profile whose values aren't printed in a publication is left out, unless its author grants a licence. Gain: clean MIT licensing, no change to the method. Cost: Faraldo's (and possibly Sha'ath's) profiles may drop out of the candidate set, which can cost some EDM key accuracy.
- B: ask Faraldo (and Sha'ath) for an explicit permissive licence for the profile values. Gain: keeps all candidates. Cost: depends on a reply; may not come.
- C: use only Krumhansl–Kessler and Temperley (both published). Gain: simplest. Cost: the weakest EDM candidates only.

Test against the standard method: the B8.3.1 benchmark compares the chosen set with Krumhansl–Kessler alone (the standard baseline) on GiantSteps Key with the MIREX weighted score.

Recommendation: A, with B tried in parallel. Licensing is cleared before any profile enters the code, and the benchmark shows what dropping a profile costs.

### Sources

- ITU-R BS.1770-5 (11/2023): https://www.itu.int/rec/R-REC-BS.1770
- EBU Tech 3342 (2023): https://tech.ebu.ch/docs/tech/tech3342.pdf
- MathWorks `round`: https://www.mathworks.com/help/matlab/ref/double.round.html
- ffmpeg `f_ebur128.c`: https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_ebur128.c
- libebur128 `ebur128.h`: https://github.com/jiixyj/libebur128/blob/master/ebur128/ebur128.h
- Apple TN2258, AAC audio encoder delay: https://developer.apple.com/library/archive/technotes/tn2258/_index.html
- LAME technical FAQ: https://lame.sourceforge.io/tech-FAQ.txt
- ITU-R BT.1359-1: https://www.itu.int/rec/R-REC-BT.1359
- EBU R37: https://tech.ebu.ch/docs/r/r037.pdf
- Apple, MultiMeter Goniometer controls: https://support.apple.com/guide/final-cut-pro-logic-effects/lgex039cc291/mac
- GRDB `DatabaseMigrator.swift`: https://github.com/groue/GRDB.swift/blob/master/GRDB/Migration/DatabaseMigrator.swift
- Faraldo, edmkey: https://github.com/angelfaraldo/edmkey
- Essentia licensing: https://essentia.upf.edu/licensing_information.html
- Korzeniowski & Widmer 2017: https://arxiv.org/abs/1706.02921
- GiantSteps key dataset: https://github.com/GiantSteps/giantsteps-key-dataset
- Ballroom (mirdata loader): https://mirdata.readthedocs.io/en/stable/_modules/mirdata/datasets/ballroom.html
