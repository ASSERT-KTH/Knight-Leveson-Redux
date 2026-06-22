"""
Plot counts of pairwise phi correlations grouped into fixed ranges.

Reads `pairwise_table.csv` and counts version pairs by `phi_correlation`
using these ranges:

    <=0, (0,0.1], (0.1,0.2], ..., (0.9,1), =1

Usage:
    python -m analysis.plot_phi_buckets         --input results/main-spec-3/pairwise_table.csv
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def iter_phi_rows(input_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with input_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "phi_correlation" not in (reader.fieldnames or []):
            raise SystemExit("CSV is missing required column: phi_correlation")
        for row in reader:
            rows.append(row)
    return rows


BUCKET_ORDER = ["<=0"] + [f"({i/10:.1f},{(i+1)/10:.1f}]" for i in range(0, 9)] + ["(0.9,1)", "=1"]


def bucket_phi(value: float) -> str:
    if value <= 0:
        return "<=0"
    if value >= 1.0:
        return "=1"
    for hi in range(1, 10):
        upper = hi / 10
        if value <= upper:
            lower = (hi - 1) / 10
            return f"({lower:.1f},{upper:.1f}]"
    return "(0.9,1)"


def count_buckets(values: list[float]) -> Counter[str]:
    counts: Counter[str] = Counter({label: 0 for label in BUCKET_ORDER})
    for value in values:
        counts[bucket_phi(value)] += 1
    return counts


def _version_parts(version_id: str) -> list[str]:
    return version_id.split("__")


def _version_agent(version_id: str) -> str:
    parts = _version_parts(version_id)
    return parts[0] if parts else "unknown"


def _version_language(version_id: str) -> str:
    parts = _version_parts(version_id)
    if len(parts) >= 3 and parts[2].startswith("l_"):
        return parts[2][2:]
    return "unknown"


def language_pair_label(row: dict[str, str]) -> str:
    a = _version_language((row.get("version_i") or "").strip())
    b = _version_language((row.get("version_j") or "").strip())
    if not a or not b:
        return "unknown"
    x, y = sorted([a, b])
    return f"({x},{y})"


def agent_relation_label(row: dict[str, str]) -> str:
    a = _version_agent((row.get("version_i") or "").strip())
    b = _version_agent((row.get("version_j") or "").strip())
    if not a or not b:
        return "unknown"
    return "same-agent" if a == b else "cross-agent"


def count_buckets_stacked(rows: list[dict[str, str]], stack_by: str) -> tuple[dict[str, Counter[str]], list[str], dict[str, str], dict[str, str], str]:
    bucket_order = BUCKET_ORDER
    if stack_by == "language-pair":
        groups = ["(pascal,python)", "(pascal,rust)", "(python,rust)"]
        label_fn = language_pair_label
        colors = {
            "(pascal,python)": "#4c78a8",
            "(pascal,rust)": "#f58518",
            "(python,rust)": "#54a24b",
        }
        display_labels = {
            "(pascal,python)": "Pascal-Python",
            "(pascal,rust)": "Pascal-Rust",
            "(python,rust)": "Python-Rust",
        }
        title = "Cross-Language Pairwise Phi Distribution"
    elif stack_by == "agent-relation":
        groups = ["same-agent", "cross-agent"]
        label_fn = agent_relation_label
        colors = {
            "same-agent": "#4c78a8",
            "cross-agent": "#e45756",
        }
        display_labels = {
            "same-agent": "Same Agent",
            "cross-agent": "Cross Agent",
        }
        title = "Pairwise Phi Distribution by Agent Relation"
    else:
        raise ValueError(f"unknown stack mode: {stack_by!r}")

    counts_by_group: dict[str, Counter[str]] = {
        group: Counter({bucket: 0 for bucket in bucket_order}) for group in groups
    }
    for row in rows:
        raw = (row.get("phi_correlation") or "").strip()
        if not raw:
            continue
        group = label_fn(row)
        if group not in counts_by_group:
            continue
        counts_by_group[group][bucket_phi(float(raw))] += 1
    return counts_by_group, bucket_order, colors, display_labels, title


def plot_bucket_counts(counts: Counter[str], output_path: Path) -> None:
    labels = list(counts.keys())
    values = [counts[label] for label in labels]

    fig, ax = plt.subplots(figsize=(11, 5.2))
    bars = ax.bar(labels, values, color="#2f6c8f")
    ax.set_xlabel("Phi correlation range")
    ax.set_ylabel("Version-pair count")
    ax.set_title("Pairwise Phi Correlation Distribution")
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.tick_params(axis="x", rotation=35)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_bucket_counts_stacked(
    counts_by_group: dict[str, Counter[str]],
    bucket_order: list[str],
    colors: dict[str, str],
    display_labels: dict[str, str],
    title: str,
    legend_title: str,
    output_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(11, 5.2))
    groups = list(counts_by_group.keys())
    bottom = [0] * len(bucket_order)
    for group in groups:
        vals = [counts_by_group[group][bucket] for bucket in bucket_order]
        ax.bar(bucket_order, vals, bottom=bottom, color=colors[group], label=display_labels[group])
        bottom = [a + b for a, b in zip(bottom, vals)]

    ax.set_xlabel("Phi correlation range")
    ax.set_ylabel("Version-pair count")
    ax.set_title(title)
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.tick_params(axis="x", rotation=35)
    ax.legend(title=legend_title)
    for x, total in zip(range(len(bucket_order)), bottom):
        ax.text(x, total, str(total), ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument("--output", type=Path, default=None, help="Output path. Defaults to <input-dir>/phi_bucket_counts.pdf")
    parser.add_argument("--split-output", type=Path, default=None, help="Optional second output path; when provided, the same single-view chart is written there as well for compatibility with existing paper assets.")
    parser.add_argument(
        "--stack-by",
        choices=("none", "language-pair", "agent-relation"),
        default="none",
        help="Optional stacked view grouped by cross-language pair type or same-vs-cross agent relation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve() if args.output is not None else input_path.with_name("phi_bucket_counts.pdf")
    split_output_path = args.split_output.resolve() if args.split_output is not None else input_path.with_name("phi_bucket_counts_split_view.pdf")

    rows = iter_phi_rows(input_path)
    values = []
    for row in rows:
        raw = (row.get("phi_correlation") or "").strip()
        if raw:
            values.append(float(raw))
    if not values:
        raise SystemExit("No phi_correlation values found.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    split_output_path.parent.mkdir(parents=True, exist_ok=True)
    if args.stack_by != "none":
        counts_by_group, bucket_order, colors, display_labels, title = count_buckets_stacked(rows, args.stack_by)
        counts = Counter({bucket: sum(counts_by_group[group][bucket] for group in counts_by_group) for bucket in bucket_order})
        plot_bucket_counts(counts, output_path)
        legend_title = "Language pair" if args.stack_by == "language-pair" else "Agent relation"
        plot_bucket_counts_stacked(
            counts_by_group,
            bucket_order,
            colors,
            display_labels,
            title,
            legend_title,
            split_output_path,
        )
    else:
        counts = count_buckets(values)
        plot_bucket_counts(counts, output_path)
        plot_single_view(counts, split_output_path)

    print(f"Wrote {output_path}")
    print(f"Wrote {split_output_path}")
    print(f"Pairs with phi: {len(values)}")
    for label in counts:
        print(f"{label}: {counts[label]}")


if __name__ == "__main__":
    main()
