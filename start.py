"""Read-only first run. The packaged example needs no CMG installation."""
import csv
import json
from pathlib import Path
from types import SimpleNamespace
import sys

from harness import decision


def main():
    root = Path(__file__).resolve().parent / "examples" / "starter"
    selected = decision(root, SimpleNamespace(command="current", role="baseline"))
    with Path(selected["entry"]).open(encoding="utf8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    # The fixture records mean surface oil rate over each one-day interval.
    if [int(row["sim_day"]) for row in rows] != [1, 2, 3]:
        raise ValueError("The teaching example requires three consecutive daily averages")
    oil = sum(float(row["oil_sc_m3_d"]) for row in rows)
    print(json.dumps(dict(dataset="handmade teaching example", case=selected["case"],
                          verification=selected["verification"], days=len(rows),
                          cumulative_surface_oil_m3=round(oil, 6),
                          handoff=str(root / "HANDOFF.md")), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as exc:
        sys.exit(str(exc))
