"""
Generate pairwise failure heatmaps after filtering versions.

The default filter keeps versions with at least one observed campaign failure,
including versions whose failures do not overlap with any other version.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from analysis.analyze_results import plot_failure_heatmaps


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairwise", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument("--failure-sets", type=Path, required=True, help="Path to failure_sets.npz")
    parser.add_argument("--output-stem", type=Path, required=True, help="Output stem without suffix")
    parser.add_argument(
        "--filter",
        choices=("cofailure-edge", "nonzero-faults"),
        default="nonzero-faults",
        help="Version filter to apply before plotting.",
    )
    return parser.parse_args()


def versions_with_nonzero_faults(failure_sets_path: Path) -> set[str]:
    data = np.load(failure_sets_path, allow_pickle=True)
    versions = [str(v) for v in data["versions"]]
    return {
        version
        for idx, version in enumerate(versions)
        if len(data[f"f_{idx}"]) > 0
    }


def versions_with_cofailure_edges(pairwise_df: pd.DataFrame) -> set[str]:
    keep: set[str] = set()
    for _, row in pairwise_df.iterrows():
        observed = int(float(row.get("observed_cofailures", 0) or 0))
        if observed > 0:
            keep.add(str(row["version_i"]))
            keep.add(str(row["version_j"]))
    return keep


def main() -> None:
    args = parse_args()
    pairwise_df = pd.read_csv(args.pairwise.resolve())
    if args.filter == "cofailure-edge":
        keep = versions_with_cofailure_edges(pairwise_df)
    else:
        keep = versions_with_nonzero_faults(args.failure_sets.resolve())

    filtered = pairwise_df[
        pairwise_df["version_i"].isin(keep) & pairwise_df["version_j"].isin(keep)
    ].copy()
    if filtered.empty:
        raise SystemExit(f"Filter {args.filter!r} removed all pairwise rows.")

    output_stem = args.output_stem.resolve()
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    plot_failure_heatmaps(filtered, output_stem)
    print(f"Filter: {args.filter}")
    print(f"Versions kept: {len(keep)}")
    print(f"Pairs kept: {len(filtered)}")


if __name__ == "__main__":
    main()
