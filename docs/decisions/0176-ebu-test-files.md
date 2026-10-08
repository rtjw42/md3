# #176: EBU loudness test files

Approved 2026-10-08 by the maintainer after the auditor's cross-check (task B0.4.2). Summary row in DECISIONS.md §18.

## Problem

The official EBU loudness test set (`ebu-loudness-test-setv05.zip`, tech.ebu.ch) is covered by "Use of EBU audio test sequences" (EBU, July 2019, v1.0): use only "to assess the performance of audio equipment and systems within the frame of internal Research and Development operations"; no business, commercial or for-profit use; "You may not copy, modify, merge, publish, distribute, sublicense, and/or sell copies"; EBU may revoke the authorisation at any time; reports credit "© EBU". The files therefore can't be committed to md3's public repository or published through CI.

Tech 3341 (2023) Table 1 and Tech 3342 (2023) define the test cases. Only 3341 #7–#8 and 3342 #5–#6 are "authentic programme" recordings; every other case is described precisely enough to generate (sine tones with stated levels, durations, frequencies and phases). Cases 3341 #20–#23 use an anti-aliasing low-pass filter that Tech 3341 doesn't specify, so a generated version can't match EBU's files sample for sample.

## Decision

1. **Generated in code, run in CI:** Tech 3341 #1–#6 and #9–#23, Tech 3342 #1–#4, built from the published descriptions and cited in the code. For #20–#23 md3 uses its own anti-aliasing filter, documented next to the generator.
2. **Official EBU files stay on the maintainer's Mac:** downloaded by the maintainer, kept outside the repository, never committed, uploaded, cached or used in CI. `.gitignore` rules and a `tools/track.py check` rule (run by the pre-commit hook and CI) reject EBU test files.
3. **Agreement test (local run on the maintainer's Mac, in B3):**
   - Every generated case except 3341 #20–#23: md3's reading of the generated signal and of EBU's official file agree within **0.01 LU** (loudness, LRA) or **0.01 dB** (true peak), and both are within the Tech 3341 / 3342 tolerance. The largest sample difference between generated and official signals is reported for information; it doesn't have to be zero.
   - 3341 #20–#23: md3's reading of **EBU's official file** is within the Tech 3341 tolerance **+0.2 / −0.4 dB**. The generated-vs-official difference is reported for information only.
4. **Real programme recordings** (3341 #7–#8, 3342 #5–#6): tested only in the local run, against their Tech 3341 / 3342 expected values; the numbers go in the commit's `Evidence:` trailer.
5. **B3.2.3's finish line** (replaces "CI jobs green"): generated vectors pass in CI; the official EBU set, including 3341 #7–#8 and 3342 #5–#6, passes a local run on the maintainer's Mac, with the agreement test above, and the numbers in `Evidence:`; chunk-size bit-identity is green in CI.
6. **"EBU Mode" claim:** md3 claims "EBU Mode" compliance (Tech 3341) only on the basis of the full official EBU set passing in a local run on the maintainer's Mac, recorded with the date, md3 version and algorithm versions.
7. **Asking EBU (in parallel):** the maintainer asks EBU whether the official files may be used in public CI. Until a written answer allows it, points 2–5 stand; a permission would be recorded as a new decision.
8. **Credit:** reports and documentation that mention the official files credit "© EBU".

## Gain and cost

- Gain: md3 respects EBU's terms while still testing against the official files, and CI tests every case that can be generated.
- Cost: the four programme recordings and the agreement test are checked locally, not on every CI run; a regression in those cases is caught at the next local run (at least once per loudness-engine change in B3 and before each release).

## Test against the standard method

The official EBU set is the standard method. The agreement test (point 3) ties md3's generated signals to it.

## Sources

- EBU, "Use of EBU audio test sequences", v1.0, July 2019 (linked as "Terms of Use" from https://tech.ebu.ch/publications/ebu_loudness_test_set)
- EBU Tech 3341 (November 2023), Table 1; EBU Tech 3342 (November 2023), test signals table
