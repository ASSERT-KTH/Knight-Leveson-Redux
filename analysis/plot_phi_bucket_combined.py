"""
Generate the combined RQ3 phi-bucket figure used in the paper.

The chart places two stacked bars in each phi bucket:
1. cross-language pairs, stacked by language pair
2. all pairs, stacked by same-agent vs cross-agent relation
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from analysis.plot_phi_buckets import (
    BUCKET_ORDER,
    count_buckets_stacked,
    iter_phi_rows,
)


LANGUAGE_GROUPS = ["(pascal,python)", "(pascal,rust)", "(python,rust)"]
AGENT_GROUPS = ["same-agent", "cross-agent"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument("--output", type=Path, required=True, help="Output PDF path")
    return parser.parse_args()


def _stacked_totals(counts_by_group: dict[str, dict[str, int]], groups: list[str]) -> list[int]:
    return [sum(counts_by_group[group][bucket] for group in groups) for bucket in BUCKET_ORDER]


def main() -> None:
    args = parse_args()
    rows = iter_phi_rows(args.input.resolve())

    lang_counts, _, lang_colors, lang_labels, _ = count_buckets_stacked(rows, "language-pair")
    agent_counts, _, agent_colors, agent_labels, _ = count_buckets_stacked(rows, "agent-relation")

    plt.rcParams.update(
        {
            "font.size": 13,
            "axes.titlesize": 15,
            "axes.labelsize": 15,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 11.5,
            "legend.title_fontsize": 12,
        }
    )

    fig, ax = plt.subplots(figsize=(8.8, 4.9))

    x_positions = list(range(len(BUCKET_ORDER)))
    width = 0.34
    gap = 0.04
    lang_x = [x - (width + gap) / 2 for x in x_positions]
    agent_x = [x + (width + gap) / 2 for x in x_positions]

    lang_bottom = [0] * len(BUCKET_ORDER)
    for group in LANGUAGE_GROUPS:
        values = [lang_counts[group][bucket] for bucket in BUCKET_ORDER]
        ax.bar(
            lang_x,
            values,
            width=width,
            bottom=lang_bottom,
            color=lang_colors[group],
            edgecolor="white",
            linewidth=0.6,
        )
        lang_bottom = [a + b for a, b in zip(lang_bottom, values)]

    agent_bottom = [0] * len(BUCKET_ORDER)
    for group in AGENT_GROUPS:
        values = [agent_counts[group][bucket] for bucket in BUCKET_ORDER]
        ax.bar(
            agent_x,
            values,
            width=width,
            bottom=agent_bottom,
            color=agent_colors[group],
            edgecolor="white",
            linewidth=0.6,
        )
        agent_bottom = [a + b for a, b in zip(agent_bottom, values)]

    ax.set_xlabel("Phi correlation range")
    ax.set_ylabel("Version-pair count")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(BUCKET_ORDER, rotation=32, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.margins(x=0.02)

    max_total = max(_stacked_totals(lang_counts, LANGUAGE_GROUPS) + _stacked_totals(agent_counts, AGENT_GROUPS))
    ax.set_ylim(0, max_total * 1.22)

    lang_legend = ax.legend(
        handles=[Patch(facecolor=lang_colors[group], label=lang_labels[group]) for group in LANGUAGE_GROUPS],
        title="Language pair",
        loc="upper left",
        bbox_to_anchor=(0.015, 0.995),
        frameon=True,
        fancybox=False,
        edgecolor="black",
        borderpad=0.45,
        labelspacing=0.35,
        handlelength=1.4,
    )
    ax.add_artist(lang_legend)

    ax.legend(
        handles=[Patch(facecolor=agent_colors[group], label=agent_labels[group]) for group in AGENT_GROUPS],
        title="Agent relation",
        loc="upper left",
        bbox_to_anchor=(0.275, 0.995),
        frameon=True,
        fancybox=False,
        edgecolor="black",
        borderpad=0.45,
        labelspacing=0.35,
        handlelength=1.4,
    )

    fig.tight_layout()
    args.output.resolve().parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output.resolve(), bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {args.output.resolve()}")


if __name__ == "__main__":
    main()
