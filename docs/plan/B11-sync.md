# B11 Sync
Milestone: M4 → v1.1 · Build order: §16 step 9 · Branch prefix: b11
Summary (written when the batch closes): —

Not broken down until B10 is done (#166). Scope: the sync M0 checks (M0-2, M0-3, M0-4, M0-6, M0-7, M0-8, M0-12, M0-14), then the driver, engine, Calibrator and `sync` page (§5, #63, #66, #70, #130–#145). The driver runs inside macOS's audio system service, so it is md3's highest-risk code: plan a dedicated security review and fuzzing of every driver property and input before it ships.

## Notes
