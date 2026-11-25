import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HandoffTest(unittest.TestCase):
    def test_selection_history_and_drift(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)

            def run(*args, ok=True):
                p = subprocess.run([sys.executable, str(ROOT / "harness.py"),
                                    "--project", work, *args], capture_output=True)
                self.assertEqual(p.returncode == 0, ok, p.stderr)
                return json.loads(p.stdout if ok else p.stderr)

            run("init")
            self.assertTrue((root / "STUDY.md").is_file())
            run("init", ok=False)
            run("current", "baseline", ok=False)
            for name, parent in [("base", []), ("variant", ["--parent", "base"])]:
                folder = root / "cases" / name
                folder.mkdir()
                (folder / "daily.csv").write_bytes((ROOT / "examples/offline/daily.csv").read_bytes())
                run("register", name, "--entry", "daily.csv", "--note", "fixture", *parent)
                run("select", "baseline", name, "--reason", "offline demonstration")
                self.assertTrue(Path(run("current", "baseline")["entry"]).samefile(folder / "daily.csv"))
            (folder / "daily.csv").write_text("changed")
            run("current", "baseline", ok=False)
            run("select", "baseline", "variant", "--reason", "drift", ok=False)
            back = run("select", "baseline", "base", "--reason", "verified fallback")
            self.assertEqual((back["previous_case"], back["revision"]), ("variant", 3))
            self.assertEqual(run("current", "baseline")["case"], "base")
