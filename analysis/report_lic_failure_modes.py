"""
Per-LIC oracle-aware failure-mode table.

For each LIC, versions are grouped by the exact set of test cases on which that
LIC mismatched the oracle. The output is a table with one row per
(LIC, failure-mode) group, including the "Correct" group for versions that
never mismatched that LIC.

Usage:
    python -m analysis.report_lic_failure_modes \
        --fault-events results/main-spec-3/fault_events.jsonl \
        --output       results/main-spec-3/lic_failure_modes_table.md
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path


N_LICS = 15


def load_lic_failures(fault_events_path: Path, *, n_lics: int = N_LICS) -> dict[int, dict[str, frozenset[int]]]:
    """Return ``{lic_number: {version_id: frozenset(test_ids)}}``."""
    failures: dict[int, dict[str, set[int]]] = {
        lic: collections.defaultdict(set) for lic in range(1, n_lics + 1)
    }
    with fault_events_path.open(encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            diff = rec.get("diff", {})
            mismatches = diff.get("cmv_mismatch_indices", []) if isinstance(diff, dict) else []
            version_id = str(rec["version_id"])
            test_id = int(rec["test_id"])
            for idx in mismatches:
                lic = int(idx) + 1
                if 1 <= lic <= n_lics:
                    failures[lic][version_id].add(test_id)
    return {
        lic: {vid: frozenset(test_ids) for vid, test_ids in by_version.items()}
        for lic, by_version in failures.items()
    }


def short_label(version_id: str) -> str:
    parts = version_id.split("__")
    model = ""
    lang = ""
    for part in parts:
        if part.startswith("m_"):
            model = part[2:]
        elif part.startswith("l_"):
            lang = part[2:]
    return f"{model}-{lang}" if lang else model


def build_groups(
    failures: dict[str, frozenset[int]],
    all_versions: list[str],
) -> list[dict]:
    """Group versions by identical failing-test set."""
    by_set: dict[frozenset[int], list[str]] = collections.defaultdict(list)
    for version_id in all_versions:
        by_set[failures.get(version_id, frozenset())].append(version_id)

    groups = []
    for failure_set, members in sorted(
        by_set.items(),
        key=lambda item: (
            0 if not item[0] else 1,
            -len(item[1]),
            len(item[0]),
            tuple(sorted(item[0])),
        ),
    ):
        groups.append({"failure_set": failure_set, "members": members})
    return groups


def format_failure_set(failure_set: frozenset[int]) -> str:
    if not failure_set:
        return "∅"
    return ", ".join(str(test_id) for test_id in sorted(failure_set))


def format_failure_set_preview(failure_set: frozenset[int], *, limit: int) -> str:
    if not failure_set:
        return "∅"
    ordered = sorted(failure_set)
    shown = ordered[:limit]
    preview = ", ".join(str(test_id) for test_id in shown)
    extra = len(ordered) - len(shown)
    if extra > 0:
        preview += f", ... +{extra} more"
    return preview


def build_rows(
    failures_by_lic: dict[int, dict[str, frozenset[int]]],
    all_versions: list[str],
    *,
    max_members: int,
    max_tests: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for lic in range(1, N_LICS + 1):
        groups = build_groups(failures_by_lic.get(lic, {}), all_versions)
        failure_mode_num = 1
        for group in groups:
            failure_set = group["failure_set"]
            is_correct = not failure_set
            label = "Correct" if is_correct else f"Failure mode {failure_mode_num}"
            if not is_correct:
                failure_mode_num += 1

            members = group["members"]
            member_labels = [short_label(version_id) for version_id in members[:max_members]]
            extra = len(members) - len(member_labels)
            if extra > 0:
                member_labels.append(f"... +{extra} more")

            rows.append({
                "lic": lic,
                "mode": label,
                "is_correct": is_correct,
                "version_count": len(members),
                "failing_test_count": len(failure_set),
                "failing_tests": format_failure_set(failure_set),
                "failing_tests_preview": format_failure_set_preview(
                    failure_set,
                    limit=max_tests,
                ),
                "example_versions": ", ".join(member_labels),
            })
    return rows


def write_markdown(rows: list[dict[str, object]], output_path: Path) -> None:
    lines = [
        "# LIC Failure Modes",
        "",
        "| LIC | Mode | Versions | Failing Tests | Test IDs | Example Versions |",
        "| ---: | --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {lic} | {mode} | {version_count} | {failing_test_count} | {failing_tests_preview} | {example_versions} |".format(
                **row
            )
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_csv(rows: list[dict[str, object]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "lic",
                "mode",
                "is_correct",
                "version_count",
                "failing_test_count",
                "failing_tests",
                "failing_tests_preview",
                "example_versions",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fault-events",
        type=Path,
        default=Path("results/main-spec-3/fault_events.jsonl"),
    )
    parser.add_argument(
        "--campaign",
        type=Path,
        default=Path("results/main-spec-3"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/main-spec-3/lic_failure_modes_table.md"),
    )
    parser.add_argument(
        "--max-members",
        type=int,
        default=5,
        help="How many example versions to list per row before truncating.",
    )
    parser.add_argument(
        "--max-tests",
        type=int,
        default=12,
        help="How many failing test IDs to show per Markdown row before truncating.",
    )
    args = parser.parse_args()

    failures_by_lic = load_lic_failures(args.fault_events)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from analysis.analyze_results import analysis_version_ids, read_campaign_version_order

    campaign_dir = args.campaign if args.campaign.is_dir() else args.campaign.parent
    campaign_csv = campaign_dir / "campaign.csv"
    all_versions = analysis_version_ids(
        campaign_csv,
        read_campaign_version_order(campaign_csv),
    )
    rows = build_rows(
        failures_by_lic,
        all_versions,
        max_members=args.max_members,
        max_tests=args.max_tests,
    )

    for lic in range(1, N_LICS + 1):
        lic_rows = [row for row in rows if row["lic"] == lic]
        failing_modes = sum(1 for row in lic_rows if not row["is_correct"])
        correct_count = next(
            (int(row["version_count"]) for row in lic_rows if row["is_correct"]),
            0,
        )
        print(
            f"LIC {lic:2d}: {failing_modes:2d} failure modes, "
            f"{correct_count:3d} versions fully correct on this LIC"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.suffix.lower() == ".csv":
        write_csv(rows, args.output)
    else:
        write_markdown(rows, args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
