"""
Plot ECDF-style views of pairwise phi correlations.

Outputs:
  - An ECDF of all nonblank `phi_correlation` values.
  - A two-panel figure that separates the exact `phi = 1` mass from the
    sub-1 distribution.

Usage:
    python -m analysis.plot_phi_ecdf \
        --input results/main-spec-3/pairwise_table.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def iter_phi_values(input_path: Path) -> list[float]:
    values: list[float] = []
    with input_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "phi_correlation" not in (reader.fieldnames or []):
            raise SystemExit("CSV is missing required column: phi_correlation")
        for row in reader:
            raw = (row.get("phi_correlation") or "").strip()
            if not raw:
                continue
            values.append(float(raw))
    return sorted(values)


def plot_ecdf(values: list[float], output_path: Path) -> None:
    n = len(values)
    y = [(i + 1) / n for i in range(n)]

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.step(values, y, where="post", color="#2f6c8f", linewidth=1.8)
    ax.set_xlabel("Phi correlation")
    ax.set_ylabel("ECDF")
    ax.set_title("ECDF of Pairwise Phi Correlations")
    ax.set_axisbelow(True)
    ax.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_two_panel(values: list[float], output_path: Path) -> None:
    sub_one = [v for v in values if v < 1.0]
    n_total = len(values)
    n_eq_one = n_total - len(sub_one)

    fig, (ax_left, ax_right) = plt.subplots(
        1,
        2,
        figsize=(11, 4.8),
        gridspec_kw={"width_ratios": [4, 1]},
    )

    ax_left.hist(sub_one, bins=40, color="#2f6c8f", edgecolor="white")
    ax_left.set_xlabel("Phi correlation (< 1)")
    ax_left.set_ylabel("Version-pair count")
    ax_left.set_title("Sub-1 Phi Distribution")
    ax_left.set_axisbelow(True)
    ax_left.grid(axis="y", linestyle="--", alpha=0.3)

    ax_right.bar(["=1"], [n_eq_one], color="#c44e52")
    ax_right.set_ylabel("Version-pair count")
    ax_right.set_title("Exact-Match Mass")
    ax_right.set_axisbelow(True)
    ax_right.grid(axis="y", linestyle="--", alpha=0.3)
    ax_right.text(0, n_eq_one, str(n_eq_one), ha="center", va="bottom")

    fig.suptitle("Pairwise Phi Correlations: Split View", y=1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument(
        "--ecdf-output",
        type=Path,
        default=None,
        help="Output path for the ECDF plot. Defaults to <input-dir>/phi_ecdf.pdf",
    )
    parser.add_argument(
        "--split-output",
        type=Path,
        default=None,
        help="Output path for the split-view plot. Defaults to <input-dir>/phi_split_view.pdf",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    ecdf_output = (
        args.ecdf_output.resolve()
        if args.ecdf_output is not None
        else input_path.with_name("phi_ecdf.pdf")
    )
    split_output = (
        args.split_output.resolve()
        if args.split_output is not None
        else input_path.with_name("phi_split_view.pdf")
    )

    values = iter_phi_values(input_path)
    if not values:
        raise SystemExit("No phi_correlation values found.")

    ecdf_output.parent.mkdir(parents=True, exist_ok=True)
    split_output.parent.mkdir(parents=True, exist_ok=True)
    plot_ecdf(values, ecdf_output)
    plot_two_panel(values, split_output)

    print(f"Wrote {ecdf_output}")
    print(f"Wrote {split_output}")
    print(f"Pairs with phi: {len(values)}")
    print(f"Pairs with phi = 1: {sum(1 for v in values if v == 1.0)}")


if __name__ == "__main__":
    main()
