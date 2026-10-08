# md3

A lightweight macOS menu bar app for accurate audio metering. Its main job is comparing the same song across sources (browser, Apple Music, Spotify and local files) with verified loudness, spectrum and stereo measurements, kept in a history for side-by-side comparison. It also hosts Audio Unit plugins to process a single app's audio.

md3 is for producers and mixing engineers, as a Mac-wide audio utility for everything outside the DAW: comparing a mix with references, comparing a release across platforms, and processing what you listen to.

## Status

**In development; nothing to install yet.** The design is complete and the build has started. Progress is tracked in the open:

- [STATUS](docs/STATUS.md): where the build is now, progress per batch
- [TIMELINE](docs/TIMELINE.md): every task commit, with its evidence
- [DECISIONS](docs/DECISIONS.md): the full specification and every design decision
- [Build plan](docs/plan/README.md): how the work is planned and tracked

## Planned for v1

- **Loudness:** integrated, short-term and momentary LUFS, loudness range and true peak, per ITU-R BS.1770 and EBU R128, checked in CI against the EBU Tech 3341 and 3342 test signals
- **Spectrum and stereo:** averaged spectrum, stereo width per frequency, correlation, balance, goniometer
- **History and Compare:** every measurement saved; up to four entries compared side by side, time-aligned and level-matched; JSON and CSV export
- **File analysis:** drop audio files in to measure them
- **Tempo and key** as rough estimates
- **Processing:** EQ and compressor using Apple's Audio Units, third-party AUv2 / AUv3 plugins, level-matched A/B

Bluetooth audio/video sync is planned for the first update after v1.

## Requirements

- macOS 14.2 or later (the first version with Core Audio process taps)
- Apple silicon

## License

[MIT](LICENSE)
