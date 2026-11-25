# CMG 2022 Research Harness

A local project starter and an optional agent skill for reproducible reservoir simulation studies. It links each delivery to a case, its parent, input/output files, and the reason a researcher selected it. Python 3.10+ and the standard library are sufficient for the offline example. A licensed CMG installation is needed for actual simulations.

## Open and start

Extract the archive, open the folder containing AGENTS.md in Codex, and type **start**. The local instructions activate the bundled skill. Or run `python start.py` for a read-only verification of the pre-registered fixture and a three-day total of 12.6 m³. Read examples/starter/HANDOFF.md for the reasoning and limits.

## Create a separate practice study

Extract the repository and run these commands in PowerShell from its root:

```powershell
python harness.py --project demo init
New-Item -ItemType Directory demo/cases/tutorial-r1
Copy-Item examples/offline/daily.csv demo/cases/tutorial-r1/
python harness.py --project demo register tutorial-r1 --entry daily.csv --note "Synthetic offline fixture"
python harness.py --project demo select baseline tutorial-r1 --reason "Walkthrough data only"
python harness.py --project demo current baseline
```

The last command returns the selected case, entry path, reason and checksum verification. Change the case file and run it again: drift produces an error. Derive a new case under a new ID and register it with `--parent tutorial-r1`. Select that ID to advance a role. Select a previous ID with a reason to roll back. Decisions are append-only under normal CLI use. Real projects can use separate roles for baseline, fluid model or report.

## Working with an agent

Copy the entire `skills/cmg2022-harness` directory into your project's `.agents/skills/`, or give the agent the path to its SKILL.md. The skill works with another registry as well. A starting prompt:

> Read the CMG harness skill. Identify the selected baseline and verify the files. Design a paired production-control test. State the hypothesis, actual injection and production quantities we must compare, and which native outputs support a conclusion. Stop after the design review.

Write the question in STUDY.md, keep the case-specific evidence in REVIEW.md, and record the next decision in HANDOFF.md. Check solver version, actual controls, output coverage, material balance and interpretation separately. Figures derived from multiple runs should identify the reference cases, equations and source fields. A successful checksum verifies file identity. The user reviews physical validity and scope of inference.

This community package includes no solver, credentials, proprietary example decks, field observations or CMG output. Its native-software notes cover WinProp, GEM, Results and CMOST; other simulators need their own local checks. Run `python -m unittest discover -s tests -v` to test the registry. See the [architecture](ARCHITECTURE.md), [Chinese walkthrough](START_HERE.md) and [MIT license](LICENSE).
