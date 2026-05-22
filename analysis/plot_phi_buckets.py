"""
Plot counts of pairwise phi correlations grouped into fixed ranges.

Reads `pairwise_table.csv` and counts version pairs by `phi_correlation`
using these ranges:

    <=0, (0,0.1], (0.1,0.2], ..., (0.9,1]

Usage:
    python -m analysis.plot_phi_buckets \
        --input results/main-spec-3/pairwise_table.csv
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


def iter_phi_values(input_path: Path) -> list[float]:
    values: list[float] = []
    for row in iter_phi_rows(input_path):
        raw = (row.get("phi_correlation") or "").strip()
        if not raw:
            continue
        values.append(float(raw))
    return values


def bucket_phi(value: float) -> str:
    if value <= 0:
        return "<=0"
    for hi in range(1, 10):
        upper = hi / 10
        if value <= upper:
            lower = (hi - 1) / 10
            return f"({lower:.1f},{upper:.1f}]"
    return "(0.9,1]"


def count_buckets(values: list[float]) -> Counter[str]:
    order = ["<=0"] + [f"({i/10:.1f},{(i+1)/10:.1f}]" for i in range(0, 9)] + ["(0.9,1]"]
    counts: Counter[str] = Counter({label: 0 for label in order})
    for value in values:
        counts[bucket_phi(value)] += 1
    return counts


def count_zoom_buckets(values: list[float]) -> Counter[str]:
    order = ["(0.9,0.99]", "(0.99,0.999]", "(0.999,1)", "=1"]
    counts: Counter[str] = Counter({label: 0 for label in order})
    for value in values:
        if value <= 0.9:
            continue
        if value <= 0.99:
            counts["(0.9,0.99]"] += 1
        elif value <= 0.999:
            counts["(0.99,0.999]"] += 1
        elif value < 1.0:
            counts["(0.999,1)"] += 1
        else:
            counts["=1"] += 1
    return counts


def language_pair_label(row: dict[str, str]) -> str:
    a = (row.get("language_i") or "").strip()
    b = (row.get("language_j") or "").strip()
    if not a or not b:
        return "unknown"
    x, y = sorted([a, b])
    return f"({x},{y})"


def count_buckets_stacked_by_language_pair(rows: list[dict[str, str]]) -> tuple[dict[str, Counter[str]], list[str]]:
    groups = ["(pascal,python)", "(pascal,rust)", "(python,rust)"]
    bucket_order = ["<=0"] + [f"({i/10:.1f},{(i+1)/10:.1f}]" for i in range(0, 9)] + ["(0.9,1]"]
    counts_by_group: dict[str, Counter[str]] = {
        group: Counter({bucket: 0 for bucket in bucket_order}) for group in groups
    }
    for row in rows:
        raw = (row.get("phi_correlation") or "").strip()
        if not raw:
            continue
        group = language_pair_label(row)
        if group not in counts_by_group:
            continue
        counts_by_group[group][bucket_phi(float(raw))] += 1
    return counts_by_group, bucket_order


def count_zoom_buckets_stacked_by_language_pair(rows: list[dict[str, str]]) -> tuple[dict[str, Counter[str]], list[str]]:
    groups = ["(pascal,python)", "(pascal,rust)", "(python,rust)"]
    bucket_order = ["(0.9,0.99]", "(0.99,0.999]", "(0.999,1)", "=1"]
    counts_by_group: dict[str, Counter[str]] = {
        group: Counter({bucket: 0 for bucket in bucket_order}) for group in groups
    }
    for row in rows:
        raw = (row.get("phi_correlation") or "").strip()
        if not raw:
            continue
        value = float(raw)
        group = language_pair_label(row)
        if group not in counts_by_group or value <= 0.9:
            continue
        if value <= 0.99:
            counts_by_group[group]["(0.9,0.99]"] += 1
        elif value <= 0.999:
            counts_by_group[group]["(0.99,0.999]"] += 1
        elif value < 1.0:
            counts_by_group[group]["(0.999,1)"] += 1
        else:
            counts_by_group[group]["=1"] += 1
    return counts_by_group, bucket_order


def plot_bucket_counts(counts: Counter[str], output_path: Path) -> None:
    labels = list(counts.keys())
    values = [counts[label] for label in labels]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(labels, values, color="#2f6c8f")
    ax.set_xlabel("Phi correlation range")
    ax.set_ylabel("Version-pair count")
    ax.set_title("Pairwise Phi Correlation Distribution")
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_split_view(counts: Counter[str], zoom_counts: Counter[str], output_path: Path) -> None:
    fig, (ax_left, ax_right) = plt.subplots(
        1,
        2,
        figsize=(13, 5),
        gridspec_kw={"width_ratios": [3, 2]},
    )

    left_labels = list(counts.keys())
    left_values = [counts[label] for label in left_labels]
    left_bars = ax_left.bar(left_labels, left_values, color="#2f6c8f")
    ax_left.set_xlabel("Phi correlation range")
    ax_left.set_ylabel("Version-pair count")
    ax_left.set_title("Full Range")
    ax_left.set_axisbelow(True)
    ax_left.grid(axis="y", linestyle="--", alpha=0.35)
    ax_left.tick_params(axis="x", rotation=35)
    ax_left.text(
        0.01, 0.99, "(a)",
        transform=ax_left.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )
    for bar, value in zip(left_bars, left_values):
        ax_left.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    right_labels = list(zoom_counts.keys())
    right_values = [zoom_counts[label] for label in right_labels]
    right_bars = ax_right.bar(right_labels, right_values, color="#c44e52")
    ax_right.set_xlabel("Phi correlation range near 1")
    ax_right.set_ylabel("Version-pair count")
    ax_right.set_title("High-Correlation Zoom")
    ax_right.set_axisbelow(True)
    ax_right.grid(axis="y", linestyle="--", alpha=0.35)
    ax_right.tick_params(axis="x", rotation=20)
    ax_right.text(
        0.01, 0.99, "(b)",
        transform=ax_right.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )
    for bar, value in zip(right_bars, right_values):
        ax_right.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.suptitle("Pairwise Phi Correlation Distribution", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_split_view_stacked(
    counts_by_group: dict[str, Counter[str]],
    bucket_order: list[str],
    zoom_counts_by_group: dict[str, Counter[str]],
    zoom_bucket_order: list[str],
    output_path: Path,
) -> None:
    fig, (ax_left, ax_right) = plt.subplots(
        1,
        2,
        figsize=(13, 5),
        gridspec_kw={"width_ratios": [3, 2]},
    )
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
    groups = list(counts_by_group.keys())

    left_bottom = [0] * len(bucket_order)
    for group in groups:
        vals = [counts_by_group[group][bucket] for bucket in bucket_order]
        ax_left.bar(
            bucket_order,
            vals,
            bottom=left_bottom,
            color=colors[group],
            label=display_labels[group],
        )
        left_bottom = [a + b for a, b in zip(left_bottom, vals)]
    ax_left.set_xlabel("Phi correlation range")
    ax_left.set_ylabel("Version-pair count")
    ax_left.set_title("Full Range")
    ax_left.set_axisbelow(True)
    ax_left.grid(axis="y", linestyle="--", alpha=0.35)
    ax_left.tick_params(axis="x", rotation=35)
    ax_left.legend(title="Language pair")
    ax_left.text(
        0.01, 0.99, "(a)",
        transform=ax_left.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )
    for x, total in zip(range(len(bucket_order)), left_bottom):
        ax_left.text(x, total, str(total), ha="center", va="bottom", fontsize=8)

    right_bottom = [0] * len(zoom_bucket_order)
    for group in groups:
        vals = [zoom_counts_by_group[group][bucket] for bucket in zoom_bucket_order]
        ax_right.bar(
            zoom_bucket_order,
            vals,
            bottom=right_bottom,
            color=colors[group],
            label=display_labels[group],
        )
        right_bottom = [a + b for a, b in zip(right_bottom, vals)]
    ax_right.set_xlabel("Phi correlation range near 1")
    ax_right.set_ylabel("Version-pair count")
    ax_right.set_title("High-Correlation Zoom")
    ax_right.set_axisbelow(True)
    ax_right.grid(axis="y", linestyle="--", alpha=0.35)
    ax_right.tick_params(axis="x", rotation=20)
    ax_right.text(
        0.01, 0.99, "(b)",
        transform=ax_right.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        fontweight="bold",
    )
    for x, total in zip(range(len(zoom_bucket_order)), right_bottom):
        ax_right.text(x, total, str(total), ha="center", va="bottom", fontsize=8)

    fig.suptitle("Cross-Language Pairwise Phi Distribution", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path. Defaults to <input-dir>/phi_bucket_counts.pdf",
    )
    parser.add_argument(
        "--split-output",
        type=Path,
        default=None,
        help="Optional output path for a split-view chart with a zoom of high-correlation phi ranges.",
    )
    parser.add_argument(
        "--stack-by-language-pair",
        action="store_true",
        help="Stack phi ranges by cross-language pair type using language_i/language_j columns.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = (
        args.output.resolve()
        if args.output is not None
        else input_path.with_name("phi_bucket_counts.pdf")
    )
    split_output_path = (
        args.split_output.resolve()
        if args.split_output is not None
        else input_path.with_name("phi_bucket_counts_split_view.pdf")
    )

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
    if args.stack_by_language_pair:
        counts_by_group, bucket_order = count_buckets_stacked_by_language_pair(rows)
        zoom_counts_by_group, zoom_bucket_order = count_zoom_buckets_stacked_by_language_pair(rows)
        total_counts = Counter(
            {
                bucket: sum(counts_by_group[group][bucket] for group in counts_by_group)
                for bucket in bucket_order
            }
        )
        total_zoom_counts = Counter(
            {
                bucket: sum(zoom_counts_by_group[group][bucket] for group in zoom_counts_by_group)
                for bucket in zoom_bucket_order
            }
        )
        plot_bucket_counts(total_counts, output_path)
        plot_split_view_stacked(
            counts_by_group,
            bucket_order,
            zoom_counts_by_group,
            zoom_bucket_order,
            split_output_path,
        )
        counts = total_counts
        zoom_counts = total_zoom_counts
    else:
        counts = count_buckets(values)
        zoom_counts = count_zoom_buckets(values)
        plot_bucket_counts(counts, output_path)
        plot_split_view(counts, zoom_counts, split_output_path)

    print(f"Wrote {output_path}")
    print(f"Wrote {split_output_path}")
    print(f"Pairs with phi: {len(values)}")
    for label in counts:
        print(f"{label}: {counts[label]}")
    for label in zoom_counts:
        print(f"{label}: {zoom_counts[label]}")


if __name__ == "__main__":
    main()
