"""
Plot pairwise phi bucket counts split by same-agent vs cross-agent pairs.

The left panel shows the full phi bucket distribution and the right panel zooms
into the high-correlation mass near phi = 1. Counts are stacked by whether the
two versions in the pair come from the same coding agent or from different
agents.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


FULL_BUCKETS = ["<=0"] + [f"({i/10:.1f},{(i+1)/10:.1f}]" for i in range(0, 9)] + ["(0.9,1]"]
ZOOM_BUCKETS = ["(0.9,0.99]", "(0.99,0.999]", "(0.999,1)", "=1"]
GROUPS = ["same-agent", "cross-agent"]
COLORS = {
    "same-agent": "#4c78a8",
    "cross-agent": "#f58518",
}


def bucket_phi(value: float) -> str:
    if value <= 0:
        return "<=0"
    for hi in range(1, 10):
        upper = hi / 10
        if value <= upper:
            lower = (hi - 1) / 10
            return f"({lower:.1f},{upper:.1f}]"
    return "(0.9,1]"


def bucket_phi_zoom(value: float) -> str | None:
    if value <= 0.9:
        return None
    if value <= 0.99:
        return "(0.9,0.99]"
    if value <= 0.999:
        return "(0.99,0.999]"
    if value < 1.0:
        return "(0.999,1)"
    return "=1"


def load_agent_by_version(meta_path: Path) -> dict[str, str]:
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return {row["version_id"]: row["agent"] for row in meta}


def count_buckets(pairwise_path: Path, meta_path: Path) -> tuple[dict[str, Counter[str]], dict[str, Counter[str]]]:
    agent_by_version = load_agent_by_version(meta_path)
    full = {group: Counter({bucket: 0 for bucket in FULL_BUCKETS}) for group in GROUPS}
    zoom = {group: Counter({bucket: 0 for bucket in ZOOM_BUCKETS}) for group in GROUPS}

    with pairwise_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw_phi = (row.get("phi_correlation") or "").strip()
            if not raw_phi:
                continue
            vi = row["version_i"]
            vj = row["version_j"]
            ai = agent_by_version[vi]
            aj = agent_by_version[vj]
            group = "same-agent" if ai == aj else "cross-agent"

            phi = float(raw_phi)
            full[group][bucket_phi(phi)] += 1
            zoom_bucket = bucket_phi_zoom(phi)
            if zoom_bucket is not None:
                zoom[group][zoom_bucket] += 1

    return full, zoom


def annotate_stacked(ax, totals: list[int], fontsize: int = 8) -> None:
    for idx, total in enumerate(totals):
        ax.text(idx, total, str(total), ha="center", va="bottom", fontsize=fontsize)


def plot_split_view(
    full_counts: dict[str, Counter[str]],
    zoom_counts: dict[str, Counter[str]],
    output_path: Path,
) -> None:
    fig, (ax_left, ax_right) = plt.subplots(
        1,
        2,
        figsize=(13, 5),
        gridspec_kw={"width_ratios": [3, 2]},
    )

    left_bottom = [0] * len(FULL_BUCKETS)
    for group in GROUPS:
        vals = [full_counts[group][bucket] for bucket in FULL_BUCKETS]
        ax_left.bar(FULL_BUCKETS, vals, bottom=left_bottom, color=COLORS[group], label=group)
        left_bottom = [a + b for a, b in zip(left_bottom, vals)]
    ax_left.set_xlabel("Phi correlation range")
    ax_left.set_ylabel("Version-pair count")
    ax_left.set_title("Full Range")
    ax_left.set_axisbelow(True)
    ax_left.grid(axis="y", linestyle="--", alpha=0.35)
    ax_left.tick_params(axis="x", rotation=35)
    ax_left.text(0.01, 0.99, "(a)", transform=ax_left.transAxes, ha="left", va="top", fontsize=12, fontweight="bold")
    annotate_stacked(ax_left, left_bottom)

    right_bottom = [0] * len(ZOOM_BUCKETS)
    for group in GROUPS:
        vals = [zoom_counts[group][bucket] for bucket in ZOOM_BUCKETS]
        ax_right.bar(ZOOM_BUCKETS, vals, bottom=right_bottom, color=COLORS[group], label=group)
        right_bottom = [a + b for a, b in zip(right_bottom, vals)]
    ax_right.set_xlabel("Phi correlation range near 1")
    ax_right.set_ylabel("Version-pair count")
    ax_right.set_title("High-Correlation Zoom")
    ax_right.set_axisbelow(True)
    ax_right.grid(axis="y", linestyle="--", alpha=0.35)
    ax_right.tick_params(axis="x", rotation=20)
    ax_right.text(0.01, 0.99, "(b)", transform=ax_right.transAxes, ha="left", va="top", fontsize=12, fontweight="bold")
    annotate_stacked(ax_right, right_bottom)

    handles, labels = ax_left.get_legend_handles_labels()
    ax_left.legend(handles, labels, title="Pair type")
    fig.suptitle("Cross-Agent Pairwise Phi Distribution", y=1.02)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairwise", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument("--meta", type=Path, required=True, help="Path to versions_meta.json")
    parser.add_argument("--output", type=Path, required=True, help="Output PDF path")
    args = parser.parse_args()

    full_counts, zoom_counts = count_buckets(args.pairwise, args.meta)
    plot_split_view(full_counts, zoom_counts, args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
