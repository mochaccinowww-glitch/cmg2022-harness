"""Portable evidence registry for local CMG studies. Python 3.10+, stdlib only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

VERSION = 1


def case_id(value):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", value):
        raise ValueError("Use a lowercase case ID with letters, digits, underscore or hyphen")
    if re.fullmatch(r"con|prn|aux|nul|com[1-9]|lpt[1-9]", value):
        raise ValueError("Reserved Windows device name")
    return value


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def directory(root, name):
    path = root / name
    if path.resolve() != path:
        raise ValueError(f"Linked location: {path}")
    return path


def snapshot(folder):
    records = {}
    if not folder.is_dir():
        raise ValueError(f"Missing case directory: {folder}")
    for path in sorted(folder.rglob("*")):
        if path.resolve() != path:
            raise ValueError(f"Linked artifact: {path}")
        if path.is_file():
            records[path.relative_to(folder).as_posix()] = digest(path)
    if not records:
        raise ValueError("Empty case directory")
    return records


def record_path(root, name):
    return directory(directory(root, "registry"), case_id(name) + ".json")


def read(root, name):
    data = json.loads(record_path(root, name).read_text(encoding="utf8"))
    if data["schema"] != VERSION or data["id"] != name:
        raise ValueError("Record identity or schema mismatch")
    if data["entry"] not in data["files"] or any(
            Path(p).is_absolute() or Path(p).drive or ".." in Path(p).parts
            for p in data["files"]):
        raise ValueError("Invalid case-relative manifest path")
    return data


def publish(path, data):
    """Publish a complete JSON record once; concurrent writers cannot overwrite it."""
    path.parent.mkdir(exist_ok=True, parents=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        tmp = Path(stream.name)
    try:
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")
        if os.name == "nt":
            os.rename(tmp, path)
        else:
            os.link(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def verify(root, name):
    data = read(root, name)
    actual = snapshot(directory(directory(root, "cases"), name))
    expected = data["files"]
    changed = sorted(k for k in expected.keys() | actual.keys() if actual.get(k) != expected.get(k))
    if changed:
        raise ValueError("Added, missing or modified files: " + ", ".join(changed))
    return dict(verified=name, files=len(actual), scope="SHA-256 and file membership")


def decision(root, args):
    folder = directory(directory(root, "decisions"), case_id(args.role))
    history = sorted(folder.glob("[0-9]" * 8 + ".json"))
    if args.command == "select":
        verify(root, case_id(args.id))
        if not args.reason.strip():
            raise ValueError("A selection reason is required")
        number = int(history[-1].stem) + 1 if history else 1
        if number > 99999999:
            raise ValueError("Decision sequence exhausted")
        record = dict(role=args.role, revision=number, case=args.id,
                      reason=args.reason, utc=datetime.now(timezone.utc).isoformat())
        if history:
            record["previous_case"] = json.loads(history[-1].read_text(encoding="utf8"))["case"]
        publish(folder / f"{number:08d}.json", record)
        return record
    if not history:
        raise ValueError("No selection for role " + args.role)
    record = json.loads(history[-1].read_text(encoding="utf8"))
    name = case_id(record["case"])
    checked = verify(root, name)
    entry = read(root, name)["entry"]
    return dict(**record, entry=str(root / "cases" / name / entry), verification=checked)


def execute(args):
    root = args.project.resolve()
    if args.command == "init":
        root.mkdir(parents=True, exist_ok=True)
        if any(root.iterdir()):
            raise ValueError("init expects an empty or new project directory")
        for name in ("cases", "registry", "decisions"):
            (root / name).mkdir()
        templates = Path(__file__).resolve().parent / "templates"
        for name in ("HANDOFF.md", "STUDY.md", "RESEARCH_LOG.md"):
            shutil.copyfile(templates / name, root / name)
        return dict(initialized=str(root), next="Define the question in STUDY.md")
    if args.command in ("select", "current"):
        return decision(root, args)
    name = case_id(args.id)
    cases = directory(root, "cases")
    folder = directory(cases, name)
    if args.command == "register":
        record = record_path(root, name)
        if record.exists():
            raise ValueError("ID already registered. Use a new revision.")
        if args.parent:
            read(root, args.parent)
        files = snapshot(folder)
        if args.entry not in files:
            raise ValueError("--entry must match a case-relative path (use /)")
        data = dict(schema=VERSION, id=name, parent=args.parent, entry=args.entry,
                    note=args.note, files=files)
        publish(record, data)
        return dict(registered=name, files=len(files))
    data = read(root, name)
    if args.command == "resolve":
        return dict(record=str(record_path(root, name)), entry=str(folder / data["entry"]),
                    exists=(folder / data["entry"]).is_file(), parent=data["parent"])
    return verify(root, name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="Initialize a new or empty study")
    for command in ("select", "current"):
        cmd = sub.add_parser(command)
        cmd.add_argument("role", help="Stable role, e.g. baseline or manuscript")
        if command == "select":
            cmd.add_argument("id")
            cmd.add_argument("--reason", required=True)
    for command in ("register", "resolve", "verify"):
        cmd = sub.add_parser(command)
        cmd.add_argument("id")
        if command == "register":
            cmd.add_argument("--entry", required=True)
            cmd.add_argument("--parent")
            cmd.add_argument("--note", required=True)
    try:
        print(json.dumps(execute(parser.parse_args()), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps(dict(error=str(exc)), ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
