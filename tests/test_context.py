import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "harness.py"


class ContextTest(unittest.TestCase):
    def test_feedback_resume_and_stale_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def run(*args, ok=True):
                result = subprocess.run([sys.executable, str(CLI), "--project", tmp, *args],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode == 0, ok, result.stderr)
                return json.loads(result.stdout if ok else result.stderr)

            run("init")
            self.assertEqual(run("context")["topics"], {})
            self.assertFalse((root / "context").exists())
            case = root / "cases" / "trial"
            case.mkdir()
            (case / "record.txt").write_text("offline")
            run("register", "trial", "--entry", "record.txt", "--note", "offline")
            run("select", "baseline", "trial", "--reason", "example")
            args = ("--kind", "feedback", "--summary", "Use fitted anchor",
                    "--next", "Review table", "--case", "trial", "--evidence", "STUDY.md")
            first = run("checkpoint", "fluid", "--base", "0", *args)
            self.assertEqual(run("checkpoint", "fluid", "--base", "0", *args), first)
            correction = ("--kind", "decision", "--summary", "Use laboratory anchor",
                          "--next", "Recalculate")
            run("checkpoint", "fluid", "--base", "0", *correction, ok=False)
            run("checkpoint", "fluid", "--base", "1", *correction)
            run("checkpoint", "other", "--base", "0", *correction, "--evidence", "../x", ok=False)
            self.assertEqual(run("context", "fluid")["revision"], 2)
            self.assertEqual(run("context", "fluid", "--history")[0], first)
            summary = run("context")
            self.assertEqual(summary["topics"]["fluid"]["next"], "Recalculate")
            self.assertEqual(summary["roles"], {"baseline": "trial"})
            self.assertEqual(summary["cases"], ["trial"])
