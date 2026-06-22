from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def load_lic_failures(fault_events_path: Path, lic_number: int) -> dict[str, frozenset[int]]:
    failures: dict[str, set[int]] = collections.defaultdict(set)
    lic_index = lic_number - 1
    with fault_events_path.open(encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            diff = rec.get("diff", {})
            mismatches = diff.get("cmv_mismatch_indices", []) if isinstance(diff, dict) else []
            if lic_index in mismatches:
                failures[rec["version_id"]].add(int(rec["test_id"]))
    return {vid: frozenset(test_ids) for vid, test_ids in failures.items()}


def read_campaign_version_order(campaign_csv: Path) -> list[str]:
    seen = []
    seen_set = set()
    with campaign_csv.open(encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            version_id = line.split(",", 2)[1]
            if version_id not in seen_set:
                seen_set.add(version_id)
                seen.append(version_id)
    return seen


def build_groups(failures: dict[str, frozenset[int]], all_versions: list[str]) -> list[dict]:
    by_set: dict[frozenset[int], list[str]] = collections.defaultdict(list)
    for version_id in all_versions:
        by_set[failures.get(version_id, frozenset())].append(version_id)
    groups = []
    for failure_set, members in sorted(
        by_set.items(),
        key=lambda item: (0 if not item[0] else 1, -len(item[1]), len(item[0]), tuple(sorted(item[0]))),
    ):
        groups.append({"failure_set": failure_set, "members": members})
    return groups


def failing_groups(groups: list[dict]) -> list[dict]:
    out = []
    for idx, group in enumerate(groups, start=1):
        if not group["failure_set"]:
            continue
        out.append(
            {
                "name": f"Mode {len(out)+1}",
                "failure_set": set(group["failure_set"]),
                "members": group["members"],
            }
        )
    return out


def _count_regions_2(a: set[int], b: set[int]) -> dict[str, int]:
    return {
        "A": len(a - b),
        "B": len(b - a),
        "AB": len(a & b),
    }


def _count_regions_3(a: set[int], b: set[int], c: set[int]) -> dict[str, int]:
    ab = a & b
    ac = a & c
    bc = b & c
    abc = a & b & c
    return {
        "A": len(a - b - c),
        "B": len(b - a - c),
        "C": len(c - a - b),
        "AB": len(ab - c),
        "AC": len(ac - b),
        "BC": len(bc - a),
        "ABC": len(abc),
    }


def _label_for_group(group: dict) -> str:
    return f"{group['name']}\n({len(group['members'])} versions)"


def plot_venn_2(groups: list[dict], lic_number: int, output_path: Path) -> None:
    a, b = groups
    counts = _count_regions_2(a["failure_set"], b["failure_set"])

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.axis("off")

    circles = [
        Circle((0.42, 0.5), 0.26, color="#4e79a7", alpha=0.35),
        Circle((0.58, 0.5), 0.26, color="#e15759", alpha=0.35),
    ]
    for c in circles:
        ax.add_patch(c)

    ax.text(0.27, 0.78, _label_for_group(a), ha="center", va="center", fontsize=11)
    ax.text(0.73, 0.78, _label_for_group(b), ha="center", va="center", fontsize=11)

    ax.text(0.34, 0.50, str(counts["A"]), ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(0.66, 0.50, str(counts["B"]), ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(0.50, 0.50, str(counts["AB"]), ha="center", va="center", fontsize=16, fontweight="bold")

    ax.text(0.5, 0.10, "Each region shows the number of failing test cases.", ha="center", va="center", fontsize=10)
    ax.set_title(f"LIC-{lic_number} Failure-Mode Overlap", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_venn_3(groups: list[dict], lic_number: int, output_path: Path) -> None:
    a, b, c = groups
    counts = _count_regions_3(a["failure_set"], b["failure_set"], c["failure_set"])

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_aspect("equal")
    ax.axis("off")

    circles = [
        Circle((0.42, 0.60), 0.24, color="#4e79a7", alpha=0.35),
        Circle((0.58, 0.60), 0.24, color="#e15759", alpha=0.35),
        Circle((0.50, 0.42), 0.24, color="#59a14f", alpha=0.35),
    ]
    for circle in circles:
        ax.add_patch(circle)

    ax.text(0.25, 0.82, _label_for_group(a), ha="center", va="center", fontsize=11)
    ax.text(0.75, 0.82, _label_for_group(b), ha="center", va="center", fontsize=11)
    ax.text(0.50, 0.08, _label_for_group(c), ha="center", va="center", fontsize=11)

    ax.text(0.35, 0.62, str(counts["A"]), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.65, 0.62, str(counts["B"]), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.50, 0.30, str(counts["C"]), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.50, 0.66, str(counts["AB"]), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.43, 0.47, str(counts["AC"]), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.57, 0.47, str(counts["BC"]), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0.50, 0.52, str(counts["ABC"]), ha="center", va="center", fontsize=15, fontweight="bold")

    ax.text(0.5, -0.02, "Each region shows the number of failing test cases.", ha="center", va="center", fontsize=10)
    ax.set_title(f"LIC-{lic_number} Failure-Mode Overlap", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot Venn-style overlaps of LIC failure-mode test sets.")
    parser.add_argument("--fault-events", type=Path, required=True)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--lic", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.lic < 1 or args.lic > 15:
        raise SystemExit("--lic must be between 1 and 15.")

    campaign_dir = args.campaign if args.campaign.is_dir() else args.campaign.parent
    all_versions = read_campaign_version_order(campaign_dir / "campaign.csv")
    groups = build_groups(load_lic_failures(args.fault_events, args.lic), all_versions)
    nonempty = failing_groups(groups)

    if len(nonempty) == 2:
        plot_venn_2(nonempty, args.lic, args.output)
    elif len(nonempty) == 3:
        plot_venn_3(nonempty, args.lic, args.output)
    else:
        raise SystemExit(f"Expected 2 or 3 non-empty failure groups for LIC-{args.lic}; found {len(nonempty)}.")

    print(f"Wrote {args.output}")
    for group in nonempty:
        print(f"{group['name']}: versions={len(group['members'])}, failing_tests={len(group['failure_set'])}")


if __name__ == "__main__":
    main()
