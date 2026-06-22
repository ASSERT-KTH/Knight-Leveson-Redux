"""
Plot acceptance-stage admission counts as stacked bar charts.

The left panel shows the full configured total, the center panel groups by
agent, and the right panel groups by language. In all panels, green denotes
admitted versions and red denotes excluded versions.

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

import yaml

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


def configure_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 18,
            "axes.titlesize": 20,
            "axes.labelsize": 20,
            "xtick.labelsize": 18,
            "ytick.labelsize": 17,
            "legend.fontsize": 17,
            "legend.title_fontsize": 17,
        }
    )


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




def _normalize_model(agent: str, model: str) -> str:
    if agent == "opencode" and model.startswith("openrouter/"):
        return model[len("openrouter/"):]
    return model


def load_allowed_triples_from_config(config_path: Path) -> tuple[set[tuple[str, str, str]], dict[tuple[str, str, str], dict]]:
    with config_path.open(encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    languages = config.get("languages", [])
    allowed: set[tuple[str, str, str]] = set()
    row_template: dict[tuple[str, str, str], dict] = {}
    for agent in config.get("agents", []):
        agent_name = agent.get("name")
        agent_config = agent.get("config", {})
        models = agent_config.get("models") or []
        for model in models:
            for language in languages:
                key = (agent_name, model, language)
                allowed.add(key)
                row_template[key] = {
                    "agent": agent_name,
                    "model": model,
                    "language": language,
                    "passed": False,
                }
    return allowed, row_template


def expand_rows_to_allowed_triples(rows: list[dict], allowed: set[tuple[str, str, str]], row_template: dict[tuple[str, str, str], dict]) -> list[dict]:
    by_key: dict[tuple[str, str, str], dict] = {}
    for row in rows:
        key = (row.get("agent"), _normalize_model(row.get("agent", ""), row.get("model", "")), row.get("language"))
        if key not in allowed:
            continue
        current = by_key.get(key)
        if current is None or bool(row.get("passed")):
            normalized = dict(row)
            normalized["model"] = key[1]
            by_key[key] = normalized

    expanded = []
    for key, template in row_template.items():
        expanded.append(by_key.get(key, dict(template)))
    return expanded

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


def total_counts(rows: list[dict]) -> tuple[list[int], list[int]]:
    admitted = sum(1 for row in rows if row.get("passed"))
    excluded = len(rows) - admitted
    return [admitted], [excluded]


def add_value_labels(ax, x, admitted, excluded) -> None:
    for xi, p, f in zip(x, admitted, excluded):
        total = p + f
        if p > 0 and p != total:
            ax.text(
                xi,
                p + 0.15,
                str(p),
                ha="center",
                va="bottom",
                fontsize=17,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.4, "alpha": 0.85},
            )
        ax.text(xi, total + 0.4, str(total), ha="center", va="bottom", fontsize=17)


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
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Optional experiment YAML. When provided, count only (agent, model, language) triples declared in the config.",
    )
    args = parser.parse_args()

    if args.verify_meta is not None:
        verify_same_admitted_pool(args.accepted, args.verify_meta)

    accepted = load_json(args.accepted)
    rows = accepted["admitted"] + accepted["excluded"]
    if args.config is not None:
        allowed, row_template = load_allowed_triples_from_config(args.config)
        rows = expand_rows_to_allowed_triples(rows, allowed, row_template)

    lang_passed, lang_failed = counts_by_group(rows, "language", LANGUAGE_ORDER)
    agent_passed, agent_failed = counts_by_group(rows, "agent", AGENT_ORDER)

    configure_plot_style()
    total_passed, total_failed = total_counts(rows)
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(14.8, 6.15),
        constrained_layout=True,
        gridspec_kw={"width_ratios": [0.7, 1.7, 1.2]},
    )

    plot_panel(
        axes[0],
        ["All"],
        total_passed,
        total_failed,
        "Total",
    )
    axes[0].set_ylabel("Versions")

    plot_panel(
        axes[1],
        [AGENT_LABELS[x] for x in AGENT_ORDER],
        agent_passed,
        agent_failed,
        "By Agent",
    )

    plot_panel(
        axes[2],
        [LANGUAGE_LABELS[x] for x in LANGUAGE_ORDER],
        lang_passed,
        lang_failed,
        "By Language",
    )

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        frameon=False,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    for ax in axes:
        ax.tick_params(axis="x", pad=8)
        for label in ax.get_xticklabels():
            label.set_rotation(28)
            label.set_ha("right")

    fig.savefig(args.output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {args.output}")
    if args.config is not None:
        print(f"Counted configured triples only from {args.config}")
        print(f"Rows counted: {len(rows)}")


if __name__ == "__main__":
    main()
