"""Unit tests for tools/track.py. Run: python3 -m unittest discover -s tools"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import track  # noqa: E402

DECISIONS = """\
# Test decisions

## 4. Measurement

### 4.3 Verification

| # | Decision |
|---|---|
| ✅ 1 | First decision, see D1 and V1. |
| ~~⛔ 2~~ | Superseded by #3. |
| ✅ 3 | Third, checked by M0-1. |
| ✅ 32 / 56 | Combined row. |

The log starts at #173 (mentioned, not defined).

#### #76a ✅ Lettered decision defined by a heading
"""

BATCH = """\
# B0 Test batch
Milestone: — · Build order: — · Branch prefix: b0
Summary (written when the batch closes): —

## B0.1 First stage
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.1.1 | Do one | #1, D1 | — | One done | {s1} |
| B0.1.2 | Do two | #3, V1, M0-1, §4.3 | B0.1.1 | Two done | {s2} |

## B0.2 Second stage
| ID | Task | Decisions | Depends on | Done when | Status |
|---|---|---|---|---|---|
| B0.2.1 | Do three | #76a, #32/56 | B0.1 | Three done | {s3} |

## Notes
- a note
"""

BACKLOG = """\
# Backlog

| ID | Found in | What | Why it matters | Status |
|---|---|---|---|---|
| X1 | B0.1.1 | something | reasons | todo |
"""


def msg(subject: str, task: str | None = None, evidence: str | None = None, body: str = "Why: test.") -> str:
    trailers = []
    if task:
        trailers.append(f"Task: {task}")
    if evidence:
        trailers.append(f"Evidence: {evidence}")
    parts = [subject, body]
    if trailers:
        parts.append("\n".join(trailers))
    return "\n\n".join(parts) + "\n"


class Repo:
    """A throwaway git repo with an md3-shaped plan."""

    def __init__(self, path: Path):
        self.root = path
        self.git("init", "-q", "-b", "main")
        (path / "docs/plan").mkdir(parents=True)
        (path / "docs/DECISIONS.md").write_text(DECISIONS)
        (path / "docs/plan/BACKLOG.md").write_text(BACKLOG)
        self.statuses("todo", "todo", "todo")
        self.commit_all(msg("Initial import"))  # before kickoff: no trailers needed

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True, text=True
        ).stdout

    def statuses(self, s1: str, s2: str, s3: str) -> None:
        (self.root / "docs/plan/B00-test.md").write_text(BATCH.format(s1=s1, s2=s2, s3=s3))

    def commit_all(self, message: str, sync: bool = False) -> None:
        if sync:  # what the pre-commit hook does
            track.sync(self.root)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)

    def errors(self) -> list[str]:
        return track.check(self.root)

    def good_history(self) -> None:
        self.statuses("doing", "todo", "todo")
        self.commit_all(msg("B0.1.1: Start one", "B0.1.1"), sync=True)
        self.statuses("done", "todo", "todo")
        self.commit_all(msg("B0.1.1: Finish one", "B0.1.1", "it works"), sync=True)


class TrackTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Hermetic git: ignore the developer's global and system config.
        cls.home = tempfile.TemporaryDirectory()
        env = {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "HOME": cls.home.name,
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
        }
        cls.env = mock.patch.dict(os.environ, env)
        cls.env.start()

    @classmethod
    def tearDownClass(cls):
        cls.env.stop()
        cls.home.cleanup()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Repo(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def assertProblem(self, fragment: str):
        errors = self.repo.errors()
        self.assertTrue(any(fragment in e for e in errors), f"expected '{fragment}' in {errors}")


class CleanRepo(TrackTestCase):
    def test_clean_history_passes(self):
        self.repo.good_history()
        self.assertEqual(self.repo.errors(), [])

    def test_pre_commit_state_passes(self):
        # Hook ran sync, commit not yet made: generated at HEAD.
        self.repo.good_history()
        track.sync(self.repo.root)
        self.assertEqual(self.repo.errors(), [])

    def test_meta_and_backlog_tasks_allowed(self):
        self.repo.good_history()
        self.repo.commit_all(msg("meta: Tidy", "meta"), sync=True)
        self.repo.commit_all(msg("X1: Fix thing", "X1"), sync=True)
        self.assertEqual(self.repo.errors(), [])

    def test_merge_commit_without_hook_passes(self):
        self.repo.good_history()
        self.repo.git("checkout", "-q", "-b", "b0.1-stage")
        self.repo.statuses("done", "done", "todo")
        self.repo.commit_all(msg("B0.1.2: Do two", "B0.1.2", "two works"), sync=True)
        self.repo.git("checkout", "-q", "main")
        self.repo.git("merge", "-q", "--no-ff", "-m", "Merge pull request #1 from b0.1-stage", "b0.1-stage")
        self.assertEqual(self.repo.errors(), [])

    def test_push_columns_ignored(self):
        self.repo.good_history()
        f = self.repo.root / track.TIMELINE
        f.write_text(f.read_text().replace("| · | · |\n", "| ✓ | ✓ (PR #9) |\n"))
        self.assertEqual(self.repo.errors(), [])

    def test_mentioning_tooling_files_is_not_attribution(self):
        self.repo.good_history()
        self.repo.commit_all(
            msg("meta: Update CLAUDE.md", "meta", body="Touches CLAUDE.md and .claude/settings.json."), sync=True
        )
        self.assertEqual(self.repo.errors(), [])


class Violations(TrackTestCase):
    def test_duplicate_id(self):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("| B0.2.1 |", "| B0.1.1 |"))
        self.assertProblem("duplicate task ID B0.1.1")

    def test_malformed_id(self):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("| B0.2.1 |", "| B0.1.9 |"))
        self.assertProblem("malformed task ID 'B0.1.9'")

    def test_malformed_stage_heading(self):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("## B0.2 Second", "## B1.2 Second"))
        self.assertProblem("malformed stage heading")

    def test_invalid_status(self):
        self.repo.statuses("finished", "todo", "todo")
        self.assertProblem("invalid status 'finished'")

    def test_two_doing(self):
        self.repo.statuses("doing", "doing", "todo")
        self.assertProblem("more than one task is doing")

    def test_blocked_without_reason(self):
        self.repo.statuses("blocked:", "todo", "todo")
        self.assertProblem("invalid status 'blocked:'")

    def test_dropped_without_reason(self):
        self.repo.statuses("todo", "dropped", "todo")
        self.assertProblem("invalid status 'dropped'")

    def test_done_without_commit(self):
        self.repo.good_history()
        self.repo.statuses("done", "done", "todo")
        self.assertProblem("B0.1.2 is done but no commit has 'Task: B0.1.2'")

    def test_done_without_evidence(self):
        self.repo.statuses("done", "todo", "todo")
        self.repo.commit_all(msg("B0.1.1: Finish one", "B0.1.1"), sync=True)
        self.assertProblem("B0.1.1 is done but none of its commits has an Evidence: trailer")

    def test_missing_task_trailer_after_kickoff(self):
        self.repo.good_history()
        self.repo.commit_all(msg("Sneaky change"), sync=True)
        self.assertProblem("missing Task: trailer")

    def test_unknown_task_trailer(self):
        self.repo.good_history()
        self.repo.commit_all(msg("B9.9.9: Nope", "B9.9.9"), sync=True)
        self.assertProblem("Task: B9.9.9 is not a task ID")

    def test_unknown_backlog_id(self):
        self.repo.good_history()
        self.repo.commit_all(msg("X7: Nope", "X7"), sync=True)
        self.assertProblem("Task: X7 is not a task ID")

    def test_unknown_decision(self):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("#76a", "#999"))
        self.assertProblem("cites #999")

    def test_unknown_section_and_check_id(self):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("§4.3", "§9.9").replace("M0-1", "M0-42"))
        self.assertProblem("cites §9.9")
        self.assertProblem("cites M0-42")

    def test_unknown_dependency(self):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("| B0.1 | Three", "| B0.7 | Three"))
        self.assertProblem("depends on unknown 'B0.7'")

    def test_generated_files_missing(self):
        self.assertProblem("STATUS.md missing")

    def test_generated_files_stale_content(self):
        self.repo.good_history()
        self.repo.statuses("done", "doing", "todo")  # changed without sync
        self.assertProblem("STATUS.md does not match")

    def test_generated_files_hand_edited(self):
        self.repo.good_history()
        f = self.repo.root / track.TIMELINE
        f.write_text(f.read_text().replace("Start one", "Start one, edited"))
        self.assertProblem("TIMELINE.md does not match")

    def test_generated_files_too_old(self):
        self.repo.good_history()
        self.repo.commit_all(msg("meta: One", "meta"))  # no sync
        self.repo.commit_all(msg("meta: Two", "meta"))  # no sync
        self.assertProblem("which is stale")


class ReviewFixes(TrackTestCase):
    def cite(self, ref: str):
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text().replace("#76a, #32/56", ref))

    def test_mentioned_but_undefined_decision_rejected(self):
        self.cite("#173")
        self.assertProblem("cites #173, not found")

    def test_superseded_decision_rejected(self):
        self.cite("#2")
        self.assertProblem("cites #2, which is superseded")

    def test_heading_defined_decision_accepted(self):
        self.cite("#76a")
        self.assertFalse(any("#76a" in e for e in self.repo.errors()))

    def test_wrapped_and_lowercase_trailers(self):
        text = "S\n\nbody\n\ntask: B0.1.1\nEvidence: first line\n  continued here\n"
        self.assertEqual(
            track.parse_trailers(text), {"Task": "B0.1.1", "Evidence": "first line continued here"}
        )

    def test_subject_prefix_checked_in_history(self):
        self.repo.good_history()
        self.repo.commit_all(msg("Untagged subject", "B0.1.1"), sync=True)
        self.assertProblem("subject must start with 'B0.1.1: '")

    def test_merge_after_main_moved_on(self):
        self.repo.good_history()
        self.repo.git("checkout", "-q", "-b", "stage-a")
        self.repo.statuses("done", "done", "todo")
        self.repo.commit_all(msg("B0.1.2: Do two", "B0.1.2", "two works"), sync=True)
        self.repo.git("checkout", "-q", "main")
        self.repo.git("checkout", "-q", "-b", "stage-b")
        self.repo.commit_all(msg("X1: Fix thing", "X1"), sync=True)
        self.repo.git("checkout", "-q", "main")
        self.repo.git("merge", "-q", "--no-ff", "-m", "Merge pull request #2 from stage-b", "stage-b")
        self.repo.git("merge", "-q", "--no-ff", "-m", "Merge pull request #3 from stage-a", "stage-a")
        errors = self.repo.errors()
        self.assertFalse(any("stale" in e for e in errors), errors)

    def test_amend_gives_actionable_error(self):
        self.repo.good_history()
        track.sync(self.repo.root)
        self.repo.git("add", "-A")
        self.repo.git("commit", "-q", "--amend", "--no-edit")
        self.assertProblem("after an amend or rebase")

    def test_bad_banner_hash_rejected(self):
        self.repo.good_history()
        f = self.repo.root / track.STATUS
        lines = f.read_text().splitlines(keepends=True)
        lines[0] = track.GENERATED_MARK + "--output=/tmp/x -->\n"
        f.write_text("".join(lines))
        self.assertProblem("STATUS.md has a malformed generated banner")

    def test_shallow_clone_reported(self):
        self.repo.good_history()
        clone = Path(self.tmp.name) / "shallow"
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", f"file://{self.repo.root}", str(clone)], check=True
        )
        errors = track.check(clone)
        self.assertTrue(any("shallow clone" in e for e in errors), errors)

    def test_sync_refuses_symlinked_output(self):
        self.repo.good_history()
        target = Path(self.tmp.name) / "outside.txt"
        target.write_text("keep me\n")
        f = self.repo.root / track.STATUS
        f.unlink()
        f.symlink_to(target)
        with self.assertRaises(track.TrackError):
            track.sync(self.repo.root)
        self.assertEqual(target.read_text(), "keep me\n")
        self.assertProblem("is a symlink")


class Attribution(TrackTestCase):
    CASES = [
        "Co-Authored-By: Claude <noreply@anthropic.com>",
        "co-authored-by: Someone <a@b.c>",
        "Generated with some tool",
        "generated by a bot",
        "Written by claude",
        "Thanks Anthropic",
        "\U0001F916 done",
    ]

    def test_each_pattern_is_rejected(self):
        for i, line in enumerate(self.CASES):
            with self.subTest(line=line):
                self.repo.commit_all(msg(f"Pre-kickoff {i}", body=line))
                self.assertProblem("AI attribution")
                self.repo.git("reset", "-q", "--hard", "HEAD~1")

    def test_attribution_hit_helper(self):
        self.assertIsNone(track.attribution_hit("See CLAUDE.md and .claude/agents/x.md"))
        self.assertEqual(track.attribution_hit("see claude.md"), "claude")


class CommitMessage(TrackTestCase):
    """The commit-msg hook: track.py msg <file>."""

    def problems(self, text: str) -> list[str]:
        return track.check_message(self.repo.root, text)

    def assertRejected(self, text: str, fragment: str):
        errors = self.problems(text)
        self.assertTrue(any(fragment in e for e in errors), f"expected '{fragment}' in {errors}")

    def test_good_message(self):
        self.assertEqual(self.problems(msg("B0.1.1: Start one", "B0.1.1")), [])
        self.assertEqual(self.problems(msg("Tidy the plan", "meta")), [])
        self.assertEqual(self.problems(msg("X1: Fix thing", "X1")), [])

    def test_no_trailers_rejected(self):
        self.assertRejected("B0.1.1: Start one\n\nWhy: x.\n", "missing Task: trailer")

    def test_unknown_task_rejected(self):
        self.assertRejected(msg("B7.1.1: Nope", "B7.1.1"), "not a task ID")

    def test_subject_must_start_with_task_id(self):
        self.assertRejected(msg("Start one", "B0.1.1"), "subject must start with 'B0.1.1: '")

    def test_subject_length(self):
        self.assertRejected(msg("B0.1.1: " + "x" * 70, "B0.1.1"), "subject is 78 characters")

    def test_attribution_rejected(self):
        self.assertRejected(
            msg("B0.1.1: Start one", "B0.1.1", body="Co-Authored-By: Claude <noreply@anthropic.com>"),
            "AI attribution",
        )

    def test_comments_ignored(self):
        text = msg("B0.1.1: Start one", "B0.1.1") + "# Please enter the commit message\n# Claude\n"
        self.assertEqual(self.problems(text), [])

    def test_done_needs_evidence(self):
        self.repo.statuses("done", "todo", "todo")
        self.assertRejected(msg("B0.1.1: Finish one", "B0.1.1"), "needs an Evidence: trailer")
        self.assertEqual(self.problems(msg("B0.1.1: Finish one", "B0.1.1", "works")), [])

    def test_done_with_earlier_evidence_ok(self):
        self.repo.good_history()
        self.assertEqual(self.problems(msg("B0.1.1: Fix typo", "B0.1.1")), [])

    def test_cli_exit_codes(self):
        f = self.repo.root / "MSG"
        f.write_text("Nope\n")
        self.assertEqual(track.main(["msg", str(f), "--root", str(self.repo.root)]), 1)
        f.write_text(msg("B0.1.1: Start one", "B0.1.1"))
        self.assertEqual(track.main(["msg", str(f), "--root", str(self.repo.root)]), 0)


class PreCommitMode(TrackTestCase):
    def test_done_task_allowed_before_its_commit_exists(self):
        self.repo.good_history()
        self.repo.statuses("done", "done", "todo")
        track.sync(self.repo.root)
        self.assertEqual(track.check(self.repo.root, pre_commit=True), [])
        self.assertTrue(any("B0.1.2 is done" in e for e in track.check(self.repo.root)))


class NextAndReport(TrackTestCase):
    def test_next_respects_dependencies(self):
        plan = track.parse_plan(self.repo.root)
        self.assertEqual(track.next_task(plan).id, "B0.1.1")
        self.repo.statuses("done", "todo", "todo")
        self.assertEqual(track.next_task(track.parse_plan(self.repo.root)).id, "B0.1.2")
        self.repo.statuses("done", "dropped: not needed", "todo")
        self.assertEqual(track.next_task(track.parse_plan(self.repo.root)).id, "B0.2.1")

    def test_next_none_when_blocked(self):
        self.repo.statuses("blocked: waiting", "todo", "todo")
        self.assertIsNone(track.next_task(track.parse_plan(self.repo.root)))

    def test_report_runs_without_remote(self):
        self.repo.good_history()
        out = track.report(self.repo.root, fetch=False)
        self.assertIn("# md3 status", out)
        self.assertIn("B0.1.1", out)

    def test_status_shows_position_and_blockers(self):
        self.repo.statuses("done", "blocked: needs masters", "todo")
        text = track.gen_status(track.parse_plan(self.repo.root), [], None, None)
        self.assertIn("B0.1.2 Do two: needs masters", text)
        self.assertIn("1 / 3 tasks", text)

    def test_next_cross_check(self):
        def line():
            text = track.gen_status(track.parse_plan(self.repo.root), [], None, None)
            return next(l for l in text.splitlines() if l.startswith("- Next cross-check:"))

        self.assertIn("at the end of B0 Test batch", line())
        self.repo.statuses("done", "done", "dropped: not needed")
        self.assertIn("due now: B0 Test batch is done", line())
        p = self.repo.root / "docs/plan/B00-test.md"
        p.write_text(p.read_text() + "- 2026-10-08 Cross-check B0: skipped by user\n")
        self.assertIn("none", line())

    def test_second_opinion_batches(self):
        self.assertEqual(track.SECOND_OPINION, {"B1", "B3"})

    def test_trailers_only_from_last_paragraph(self):
        self.assertEqual(track.parse_trailers("S\n\nTask: B0.1.1 in body text\n\nWhy: x"), {"Why": "x"})
        self.assertEqual(track.parse_trailers("S\n\nbody\n\nTask: B0.1.1\nnot a trailer"), {})
        self.assertEqual(track.parse_trailers("Task: B0.1.1"), {})


if __name__ == "__main__":
    unittest.main()
