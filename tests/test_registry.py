from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RegistryTest(unittest.TestCase):
    def test_roundtrip_and_drift(self):
        with tempfile.TemporaryDirectory() as work:
            def cli(*args, ok=True):
                result = subprocess.run([sys.executable, str(ROOT / "harness.py"),
                                         "--project", work, *args], capture_output=True)
                self.assertEqual(result.returncode == 0, ok, result.stderr)
                return json.loads(result.stdout if ok else result.stderr)

            for name in ("base", "child"):
                folder = Path(work, "cases", name)
                folder.mkdir(parents=True)
                (folder / "daily.csv").write_bytes((ROOT / "examples/offline/daily.csv").read_bytes())
            register = ["--entry", "daily.csv", "--note", "fixture"]
            cli("register", "base", *register)
            cli("register", "base", *register, ok=False)
            cli("register", "child", *register, "--parent", "base")
            self.assertEqual(cli("resolve", "child")["parent"], "base")
            self.assertEqual(cli("verify", "child")["files"], 1)
            (folder / "daily.csv").write_text("changed")
            cli("verify", "child", ok=False)
            (folder / "daily.csv").unlink()
            (folder / "extra.txt").touch()
            cli("verify", "child", ok=False)
            cli("verify", "base")
            cli("resolve", "../outside", ok=False)
