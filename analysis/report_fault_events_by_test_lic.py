#!/usr/bin/env python3
"""
Summarize fault_events.jsonl by (test_id, LIC) and by (agent, model).

Each line is one failing (version_id, test_id) run. CMV indices in the diff are
0-based; this script maps them to 1-based spec LIC numbers (index + 1).

``version_id`` follows ``{agent}__m_{model_slug}__l_{language}__run{NNN}`` (see
``pipeline/naming.version_json_filename``). Agent/model are parsed from that
string so aggregation matches how versions are named on disk.

Fault rows for versions with no usable build (same ``versions/index.json`` rule as
``analyze_results``) are skipped entirely.

Usage:
    python -m analysis.report_fault_events_by_test_lic \\
        --input results/main-spec-2/fault_events.jsonl

    python -m analysis.report_fault_events_by_test_lic --input path.jsonl --csv out.csv \\
        --csv-agent-model agent_model.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

_VERSION_TAIL = re.compile(r"__l_[a-z0-9._+-]+__run\d+$", re.IGNORECASE)


def agent_model_from_version_id(version_id: str) -> tuple[str, str]:
    """
    Split version_id into (agent, model_slug).

    Uses the suffix ``__l_<lang>__runNNN`` so model_slug may contain ``__``
    (e.g. OpenRouter slashes slugged as ``__``).
    """
    m = _VERSION_TAIL.search(version_id)
    if not m:
        return ("?", "?")
    prefix = version_id[: m.start()]
    if "__m_" not in prefix:
        return ("?", "?")
    agent, model = prefix.split("__m_", 1)
    return agent, model


def _version_ids_to_skip_from_index(index_json: Path) -> set[str]:
    """Same exclusion list as ``analysis.analyze_results`` (must stay in sync)."""
    if not index_json.is_file():
        return set()
    raw = json.loads(index_json.read_text(encoding="utf-8"))
    rows = raw if isinstance(raw, list) else raw.get("versions", raw.get("admitted", []))
    return {
        str(r["version_id"])
        for r in rows
        if isinstance(r, dict) and r.get("build_status") == "api_unavailable"
    }


def iter_fault_events(path: Path):
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {e}") from e


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--input",
        type=Path,
        default=Path("results/main-spec-2/fault_events.jsonl"),
        help="Path to fault_events.jsonl",
    )
    p.add_argument(
        "--top-pairs",
        type=int,
        default=500,
        help="Print this many (test_id, LIC) pairs by descending count (0 = all)",
    )
    p.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="Write full (test_id, lic, count) table to this CSV file",
    )
    p.add_argument(
        "--top-agent-model",
        type=int,
        default=30,
        help="Print this many (agent, model) pairs by descending fault-row count (0 = all)",
    )
    p.add_argument(
        "--top-agent-model-lic",
        type=int,
        default=70,
        help="Print this many (agent, model, lic) triples by count (0 = all)",
    )
    p.add_argument(
        "--csv-agent-model",
        type=Path,
        default=None,
        help="Write (agent, model, fault_row_count) CSV",
    )
    p.add_argument(
        "--csv-agent-model-lic",
        type=Path,
        default=None,
        help="Write (agent, model, lic, count) CSV — one row per fault row per LIC bit",
    )
    args = p.parse_args()

    if not args.input.is_file():
        sys.exit(f"not a file: {args.input}")

    skip_versions = _version_ids_to_skip_from_index(
        args.input.resolve().parent / "versions" / "index.json",
    )

    pair_counts: Counter[tuple[int, int]] = Counter()
    by_lic: Counter[int] = Counter()
    by_test: Counter[int] = Counter()
    by_agent_model: Counter[tuple[str, str]] = Counter()
    by_agent_model_lic: Counter[tuple[str, str, int]] = Counter()
    n_lines = 0

    for rec in iter_fault_events(args.input):
        version_id = str(rec.get("version_id", ""))
        if version_id in skip_versions:
            continue
        n_lines += 1
        test_id = int(rec["test_id"])
        agent, model = agent_model_from_version_id(version_id)
        by_agent_model[(agent, model)] += 1

        indices = rec.get("diff", {}).get("cmv_mismatch_indices") or []
        for idx in indices:
            lic = int(idx) + 1
            pair_counts[(test_id, lic)] += 1
            by_lic[lic] += 1
            by_test[test_id] += 1
            by_agent_model_lic[(agent, model, lic)] += 1

    print(f"file: {args.input.resolve()}")
    print(f"fault rows: {n_lines}")
    print(f"distinct (test_id, LIC) pairs: {len(pair_counts)}")
    print()

    print("by LIC (how many fault rows mention that LIC in cmv_mismatch_indices):")
    for lic in sorted(by_lic):
        print(f"  LIC {lic:2d}: {by_lic[lic]}")
    print()

    print("top test_ids by fault row count:")
    for tid, c in by_test.most_common(15):
        print(f"  test_id {tid}: {c}")
    print()

    pairs_sorted = pair_counts.most_common()
    if args.top_pairs > 0:
        pairs_sorted = pairs_sorted[: args.top_pairs]
    print(f"top (test_id, LIC) pairs by count (showing {len(pairs_sorted)}):")
    for (tid, lic), c in pairs_sorted:
        print(f"  test_id {tid:6d}  LIC {lic:2d}:  {c}")
    print()

    am_sorted = by_agent_model.most_common()
    if args.top_agent_model > 0:
        am_sorted = am_sorted[: args.top_agent_model]
    print(
        f"by agent/model (fault rows per version stem; showing {len(am_sorted)} of {len(by_agent_model)}):"
    )
    for (agent, model), c in am_sorted:
        print(f"  {agent:12s}  {model:48s}  {c}")
    print()

    aml_sorted = by_agent_model_lic.most_common()
    if args.top_agent_model_lic > 0:
        aml_sorted = aml_sorted[: args.top_agent_model_lic]
    print(
        f"by agent/model/LIC (one count per failing LIC bit per fault row; "
        f"showing {len(aml_sorted)} of {len(by_agent_model_lic)}):"
    )
    for (agent, model, lic), c in aml_sorted:
        print(f"  {agent:12s}  {model:40s}  LIC {lic:2d}  {c}")

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["test_id", "lic", "count"])
            for (tid, lic), c in sorted(
                pair_counts.items(), key=lambda x: (-x[1], x[0][0], x[0][1])
            ):
                w.writerow([tid, lic, c])
        print()
        print(f"wrote {args.csv} ({len(pair_counts)} rows)")

    if args.csv_agent_model:
        args.csv_agent_model.parent.mkdir(parents=True, exist_ok=True)
        with args.csv_agent_model.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["agent", "model", "fault_row_count"])
            for (agent, model), c in sorted(
                by_agent_model.items(), key=lambda x: (-x[1], x[0][0], x[0][1])
            ):
                w.writerow([agent, model, c])
        print()
        print(f"wrote {args.csv_agent_model} ({len(by_agent_model)} rows)")

    if args.csv_agent_model_lic:
        args.csv_agent_model_lic.parent.mkdir(parents=True, exist_ok=True)
        with args.csv_agent_model_lic.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["agent", "model", "lic", "count"])
            for (agent, model, lic), c in sorted(
                by_agent_model_lic.items(),
                key=lambda x: (-x[1], x[0][0], x[0][1], x[0][2]),
            ):
                w.writerow([agent, model, lic, c])
        print()
        print(f"wrote {args.csv_agent_model_lic} ({len(by_agent_model_lic)} rows)")


if __name__ == "__main__":
    main()
