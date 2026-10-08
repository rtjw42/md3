# B0 Build-phase kickoff
Milestone: — · Build order: — · Branch prefix: b0
Summary (written when the batch closes): —

## B0.1 Go-ahead and trackers
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.1.1 | Confirm with the user that the decision phase is over and repo changes are allowed | — | — | User says yes | done |
| B0.1.2 | Commit the build prompt, `docs/MAINTAINER-SETUP.md`, `docs/CROSS_CHECK.md`, `CLAUDE.md`, `.claude/settings.json` and `.claude/agents/md3-reviewer.md` (none loosened); set the DECISIONS.md status line to "build phase"; add an empty §18 | — | B0.1.1 | Committed (the hooks don't exist yet) | done |
| B0.1.3 | `docs/plan/`: README, batch files B00–B11 seeded from the plan, BACKLOG, HANDOFF | — | B0.1.2 | Every planned task is in a batch file | done |
| B0.1.4 | `tools/track.py` (check, sync, report, next) with its own unit tests; `check` also fails on AI attribution in any commit message (security rule 10) | — | B0.1.3 | Tests pass; `check` fails on each rule violation in a fixture | doing |
| B0.1.5 | Git hooks (`.githooks/`), STATUS.md and TIMELINE.md generated for the first time; ask the user to run `git config core.hooksPath .githooks` | — | B0.1.4 | A commit without trailers is rejected; the timeline lists B0.1's commits | todo |

## B0.2 Repo basics
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.2.1 | LICENSE (MIT), README (links to DECISIONS, STATUS, TIMELINE), CHANGELOG in Keep a Changelog format with semantic versions | #40, §9 | B0.1 | Files present | todo |
| B0.2.2 | CONTRIBUTING (incl. hook setup and the commit format), issue templates, Swift/Xcode `.gitignore` | §9 | B0.2.1 | Files present | todo |

## B0.3 Project skeleton and CI
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.3.1 | Xcode app target: LSUIElement, macOS 14.2 minimum, Apple Silicon only | D2, D3, #35, §6.1 | B0.2 | Empty app builds and shows a menu bar item | todo |
| B0.3.2 | Swift package for modules, C target for real-time code, test targets; exact dependency versions, `Package.resolved` committed | D2, #42, #52, #102 | B0.3.1 | `swift test` runs a placeholder test in each target | todo |
| B0.3.3 | CI (GitHub Actions, macOS runner, one pinned Xcode version): build, unit tests and `track.py check` on every push and PR; Actions pinned to full commit SHAs; `permissions: contents: read` | §4.8, security rule 4 | B0.3.2 | CI green on main; a PR with stale tracking files fails; user asked to add CI as a required check and set up CodeQL | todo |

## B0.4 Evidence carried over
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.4.1 | Commit the simulation scripts under `tools/` with a README (ask the user where they are) | §4.8 | B0.1 | Each script runs and reproduces its recorded numbers | todo |
| B0.4.2 | Document checks (§14 DOC row): read the primary sources, record the findings | §14 | B0.1 | Each claim confirmed, or a fix proposed | todo |

## B0.5 Security and quality baseline
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.5.1 | gitleaks in the pre-commit hook and as a CI job, with a project config; CI job that checks every commit message on the branch and the PR title and body for AI attribution | security rules 1–2, 9a | B0.3.3 | A planted fake key is blocked locally and in CI; a test PR with an AI co-author line fails CI | todo |
| B0.5.2 | Formatting and linting: swift-format (or SwiftLint) for Swift, clang-format and clang-tidy for C; warnings as errors; Swift 6 strict concurrency checking | #52 | B0.3.3 | CI fails on a lint error or warning; codebase clean | todo |
| B0.5.3 | Dependabot config for GitHub Actions and Swift packages (weekly, grouped); CI workflow audit (SHA pins, minimal permissions, no `pull_request_target`) | security rules 3–4 | B0.3.3 | Dependabot config valid; audit checklist in the PR | todo |
| B0.5.4 | PR template (task IDs, evidence, decisions touched, modularity statement, review counts), CODEOWNERS, SECURITY.md, CODE_OF_CONDUCT.md | §9 | B0.2.2 | Files present; the next PR uses the template | todo |
| B0.5.5 | `docs/ARCHITECTURE.md`: one-page module and record diagram built from §3.4, linked from README | #102, #103, #104 | B0.2.1 | Matches §3.4; the user can follow it | todo |
| B0.5.6 | Logging wrapper over `os_log` with private-by-default fields, and a short logging policy in CONTRIBUTING | security rule 7 | B0.3.2 | Unit test: private fields redacted in a captured log | todo |
| B0.5.7 | Confirm with the user that the open items in `docs/MAINTAINER-SETUP.md` are done (required CI check, CodeQL, hooks path, gitleaks installed) | — | B0.5.1 | User confirms; any skipped step is listed in HANDOFF as a known gap | todo |

## Notes
- 2026-10-08 B0.1.1: user confirmed the decision phase is over and repo changes are allowed.
