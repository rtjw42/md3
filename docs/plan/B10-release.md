# B10 Release
Milestone: M7 → v1 · Build order: §16 step 10 · Branch prefix: b10
Summary (written when the batch closes): —

## B10.1 App behaviour
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B10.1.1 | Prefs window (look prefs, hotkeys, retention N) | #170, #34, #25, #22 | B9 | Every pref works | todo |
| B10.1.2 | Onboarding, launch at login, standard behaviour | #36, #35, §7 | B10.1.1 | 3-step onboarding; accessibility labels | todo |
| B10.1.3 | "Copy diagnostics" (versions, settings, recent log lines; no audio, no titles, no paths) | §7 no telemetry, security rule 7 | B9 | Output reviewed: nothing private included | todo |

## B10.2 Normalisation preview
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B10.2.1 | Normalisation preview with editable platform levels, defaults checked against platform docs | #167 | B9 | Off by default; numbers only | todo |

## B10.3 Release pipeline
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B10.3.1 | Sparkle updates with EdDSA-signed updates and an HTTPS-only feed (the user creates the key, MAINTAINER-SETUP later steps) | #37 | B9 | Daily check, prompt before install; an update with a bad signature is rejected | todo |
| B10.3.2 | Release pipeline: `.dmg`, Homebrew tap, Sparkle feed on Pages, Actions on tags | #43 | B10.3.1 | A tag produces a release | todo |
| B10.3.3 | Compliance report; build-from-source guide | #46, §9 | B9 | Published in docs | todo |
| B10.3.4 | Release hardening: hardened runtime, minimal entitlements and usage strings; SHA-256 checksums and GitHub build attestations on every release; signing and notarization steps run only in the `release` environment | #172, security rules 1, 8 | B10.3.2 | `codesign -d --entitlements` shows only the approved set; checksums and attestations published | todo |

## B10.4 Ship
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B10.4.1 | 10-minute performance run at shipping QoS | §6.1, #161 | B10.1, B10.2, B10.3 | All §6.1 targets met | todo |
| B10.4.2 | Test matrix on macOS 14.x, 15.x, 26.x, 27.x | §12 | B10.4.1 | Results recorded | todo |
| B10.4.3 | Unsigned developer preview release, with release notes drafted from the batch summaries | #172 | B10.4.2 | `v0.x.0-preview` on GitHub with checksums | todo |
| B10.4.4 | Developer account (user buys), signed and notarised 1.0 | #172 | B10.4.3 | `v1.0.0` released | todo |

## Notes
