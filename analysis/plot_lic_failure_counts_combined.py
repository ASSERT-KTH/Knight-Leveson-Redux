"""
Generate the combined LIC failure-count figure used for RQ4.

For each LIC bucket, the chart places two stacked bars:
1. failures stacked by target language
2. failures stacked by coding agent
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from analysis.plot_lic_failure_counts import (
    count_unique_triples_by_lic_and_group,
    count_unique_triples_from_summary_csv,
    infer_input_kind,
)


LANGUAGE_GROUPS = ["pascal", "python", "rust"]
AGENT_GROUPS = ["claude_code", "cursor", "gemini", "opencode"]

LANGUAGE_COLORS = {
    "python": "#4c78a8",
    "rust": "#f58518",
    "pascal": "#54a24b",
}

AGENT_COLORS = {
    "claude_code": "#e45756",
    "cursor": "#72b7b2",
    "gemini": "#f58518",
    "opencode": "#54a24b",
}

LANGUAGE_LABELS = {
    "pascal": "Pascal",
    "python": "Python",
    "rust": "Rust",
}

AGENT_LABELS = {
    "claude_code": "Claude Code",
    "cursor": "Cursor",
    "gemini": "Gemini",
    "opencode": "OpenCode",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to fault_events.jsonl or summary CSV")
    parser.add_argument("--output", type=Path, required=True, help="Output PDF path")
    parser.add_argument(
        "--font-scale",
        type=float,
        default=1.0,
        help="Multiply all plot font sizes by this factor.",
    )
    return parser.parse_args()


def _load_counts(input_path: Path) -> tuple[dict[str, dict[int, int]], dict[str, dict[int, int]]]:
    input_kind = infer_input_kind(input_path)
    if input_kind == "fault-events":
        lang_counts, _ = count_unique_triples_by_lic_and_group(input_path, stack_by="language")
        agent_counts, _ = count_unique_triples_by_lic_and_group(input_path, stack_by="agent")
    else:
        lang_counts, _ = count_unique_triples_from_summary_csv(input_path, stack_by="language")
        agent_counts, _ = count_unique_triples_from_summary_csv(input_path, stack_by="agent")
    return lang_counts, agent_counts


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    lang_counts, agent_counts = _load_counts(input_path)

    base_font = 11.0 * args.font_scale
    plt.rcParams.update(
        {
            "font.size": base_font,
            "axes.titlesize": base_font * 1.2,
            "axes.labelsize": base_font * 1.15,
            "xtick.labelsize": base_font,
            "ytick.labelsize": base_font,
            "legend.fontsize": base_font * 0.95,
            "legend.title_fontsize": base_font,
        }
    )

    fig, ax = plt.subplots(figsize=(9.0, 5.1))

    lics = list(range(1, 16))
    x_positions = list(range(len(lics)))
    width = 0.34
    gap = 0.04
    lang_x = [x - (width + gap) / 2 for x in x_positions]
    agent_x = [x + (width + gap) / 2 for x in x_positions]

    lang_bottom = [0] * len(lics)
    for group in LANGUAGE_GROUPS:
        values = [lang_counts.get(group, {}).get(lic, 0) for lic in lics]
        ax.bar(
            lang_x,
            values,
            width=width,
            bottom=lang_bottom,
            color=LANGUAGE_COLORS[group],
            edgecolor="white",
            linewidth=0.6,
        )
        lang_bottom = [a + b for a, b in zip(lang_bottom, values)]

    agent_bottom = [0] * len(lics)
    for group in AGENT_GROUPS:
        values = [agent_counts.get(group, {}).get(lic, 0) for lic in lics]
        ax.bar(
            agent_x,
            values,
            width=width,
            bottom=agent_bottom,
            color=AGENT_COLORS[group],
            edgecolor="white",
            linewidth=0.6,
        )
        agent_bottom = [a + b for a, b in zip(agent_bottom, values)]

    ax.set_xlabel("LIC")
    ax.set_ylabel("Distinct failing triples")
    ax.set_xticks(x_positions)
    ax.set_xticklabels([str(lic) for lic in lics])
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.margins(x=0.02)

    max_total = max(lang_bottom + agent_bottom)
    ax.set_ylim(0, max_total * 1.24)

    lang_legend = ax.legend(
        handles=[Patch(facecolor=LANGUAGE_COLORS[group], label=LANGUAGE_LABELS[group]) for group in LANGUAGE_GROUPS],
        title="Target language",
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
        handles=[Patch(facecolor=AGENT_COLORS[group], label=AGENT_LABELS[group]) for group in AGENT_GROUPS],
        title="Coding agent",
        loc="upper left",
        bbox_to_anchor=(0.235, 0.995),
        frameon=True,
        fancybox=False,
        edgecolor="black",
        borderpad=0.45,
        labelspacing=0.35,
        handlelength=1.4,
    )

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
