"""
Plot acceptance-stage admission counts as two stacked bar charts.

The left panel groups by language and the right panel groups by agent. In both
panels, green denotes admitted versions and red denotes excluded versions.

The accepted.json file is stored under results/main/, while the downstream
campaign artifacts for the same admitted pool live under results/main-spec-3/.
If --verify-meta is provided, this script checks that the admitted version IDs
in accepted.json match the version IDs in versions_meta.json before plotting.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


PASS_COLOR = "#54a24b"
FAIL_COLOR = "#e45756"

LANGUAGE_ORDER = ["python", "rust", "pascal"]
AGENT_ORDER = ["codex", "claude_code", "cursor", "opencode", "gemini"]
AGENT_LABELS = {
    "codex": "Codex",
    "claude_code": "Claude Code",
    "cursor": "Cursor",
    "opencode": "OpenCode",
    "gemini": "Gemini",
}
LANGUAGE_LABELS = {
    "python": "Python",
    "rust": "Rust",
    "pascal": "Pascal",
}


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def verify_same_admitted_pool(accepted_path: Path, meta_path: Path) -> None:
    accepted = load_json(accepted_path)
    meta = load_json(meta_path)
    accepted_ids = sorted(entry["version_id"] for entry in accepted["admitted"])
    meta_ids = sorted(entry["version_id"] for entry in meta)
    if accepted_ids != meta_ids:
        raise SystemExit(
            "accepted.json and versions_meta.json do not describe the same admitted pool"
        )


def counts_by_group(rows: list[dict], key: str, order: list[str]) -> tuple[list[int], list[int]]:
    admitted = defaultdict(int)
    excluded = defaultdict(int)
    for row in rows:
        group = row[key]
        if row.get("passed"):
            admitted[group] += 1
        else:
            excluded[group] += 1
    return [admitted[g] for g in order], [excluded[g] for g in order]


def add_value_labels(ax, x, admitted, excluded) -> None:
    for xi, p, f in zip(x, admitted, excluded):
        total = p + f
        ax.text(xi, total + 0.4, str(total), ha="center", va="bottom", fontsize=9)


def plot_panel(ax, labels: list[str], admitted: list[int], excluded: list[int], title: str) -> None:
    x = list(range(len(labels)))
    ax.bar(x, admitted, color=PASS_COLOR, label="Passed")
    ax.bar(x, excluded, bottom=admitted, color=FAIL_COLOR, label="Failed")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, max(a + b for a, b in zip(admitted, excluded)) + 3)
    ax.set_title(title)
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    add_value_labels(ax, x, admitted, excluded)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accepted", type=Path, required=True, help="Path to accepted.json")
    parser.add_argument(
        "--verify-meta",
        type=Path,
        default=None,
        help="Optional versions_meta.json path used to verify the admitted pool",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output PDF path")
    args = parser.parse_args()

    if args.verify_meta is not None:
        verify_same_admitted_pool(args.accepted, args.verify_meta)

    accepted = load_json(args.accepted)
    rows = accepted["admitted"] + accepted["excluded"]

    lang_passed, lang_failed = counts_by_group(rows, "language", LANGUAGE_ORDER)
    agent_passed, agent_failed = counts_by_group(rows, "agent", AGENT_ORDER)

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8), constrained_layout=True)

    plot_panel(
        axes[0],
        [LANGUAGE_LABELS[x] for x in LANGUAGE_ORDER],
        lang_passed,
        lang_failed,
        "By Language",
    )
    axes[0].set_ylabel("Versions")

    plot_panel(
        axes[1],
        [AGENT_LABELS[x] for x in AGENT_ORDER],
        agent_passed,
        agent_failed,
        "By Agent",
    )

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
