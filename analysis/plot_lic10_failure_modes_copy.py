"""
LIC-10 oracle-aware failure-mode UpSet plot.

Rows  = specific test cases that cause at least one LIC-10 failure
Cols  = exact failure-mode fingerprints across those tests
Bars  = versions per fingerprint / versions per failing test case

Usage:
    python -m analysis.plot_lic10_failure_modes \\
        --fault-events results/main-spec-3/fault_events.jsonl \\
        --output       results/main-spec-3/lic10_failure_modes.pdf
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from upsetplot import UpSet


_COLORS = {
    "main": "#d62728",
    "minor": "#1f77b4",
    "correct": "#2ca02c",
    "shared": "#ff7f0e",
}

_LANGUAGE_COLORS = {
    "pascal": "#b07aa1",
    "python": "#f28e2b",
    "rust": "#9c755f",
}


def load_lic_failures(fault_events_path: Path, lic_number: int) -> dict[str, frozenset[int]]:
    """Return {version_id: frozenset of test_ids that cause the selected LIC failure}."""
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


def short_label(version_id: str) -> str:
    parts = version_id.split("__")
    model = ""
    lang = ""
    for part in parts:
        if part.startswith("m_"):
            model = part[2:]
        elif part.startswith("l_"):
            lang = part[2:]
    return f"{model}-{lang}" if lang else model


def language_of(version_id: str) -> str:
    for part in version_id.split("__"):
        if part.startswith("l_"):
            return part[2:]
    return "unknown"


def build_groups(
    failures: dict[str, frozenset[int]],
    all_versions: list[str],
) -> list[dict]:
    """Group versions by identical selected-LIC failing test set."""
    by_set: dict[frozenset[int], list[str]] = collections.defaultdict(list)
    for version_id in all_versions:
        by_set[failures.get(version_id, frozenset())].append(version_id)

    groups = []
    for failure_set, members in sorted(
        by_set.items(),
        key=lambda item: (
            0 if not item[0] else 1,
            -len(item[1]),
            len(item[0]),
            tuple(sorted(item[0])),
        ),
    ):
        groups.append({"failure_set": failure_set, "members": members})
    return groups


def sorted_test_cases(groups: list[dict]) -> list[int]:
    """Sort test cases by total affected versions, then by test id."""
    all_tests: set[int] = set()
    for group in groups:
        all_tests |= group["failure_set"]

    def versions_on(test_id: int) -> int:
        return sum(len(group["members"]) for group in groups if test_id in group["failure_set"])

    return sorted(all_tests, key=lambda test_id: (-versions_on(test_id), test_id))


class FixedUpSet(UpSet):
    """UpSet with a pandas-copy-on-write-safe matrix renderer."""

    def plot_matrix(self, ax):
        ax = self._reorient(ax)
        data = self.intersections
        n_cats = data.index.nlevels
        inclusion = data.index.to_frame().values

        styles = [
            [
                self.subset_styles[i]
                if inclusion[i, j]
                else {"facecolor": self._other_dots_color, "linewidth": 0}
                for j in range(n_cats)
            ]
            for i in range(len(data))
        ]
        styles = sum(styles, [])
        style_columns = {
            "facecolor": "facecolors",
            "edgecolor": "edgecolors",
            "linewidth": "linewidths",
            "linestyle": "linestyles",
            "hatch": "hatch",
        }
        styles = pd.DataFrame(styles).reindex(columns=style_columns).astype(
            {
                "facecolor": "O",
                "edgecolor": "O",
                "linewidth": float,
                "linestyle": "O",
                "hatch": "O",
            }
        )
        styles["linewidth"] = styles["linewidth"].fillna(1)
        styles["facecolor"] = styles["facecolor"].fillna(self._facecolor)
        styles["edgecolor"] = styles["edgecolor"].fillna(styles["facecolor"])
        styles["linestyle"] = styles["linestyle"].fillna("solid")
        del styles["hatch"]

        x = np.repeat(np.arange(len(data)), n_cats)
        y = np.tile(np.arange(n_cats), len(data))
        marker_size = (self._element_size * 0.30) ** 2 if self._element_size is not None else 160
        ax.scatter(
            *self._swapaxes(x, y),
            s=marker_size,
            zorder=10,
            **styles.rename(columns=style_columns),
        )

        if self._with_lines:
            idx = np.flatnonzero(inclusion)
            line_data = (
                pd.Series(y[idx], index=x[idx])
                .groupby(level=0)
                .aggregate(["min", "max"])
            )
            colors = pd.Series(
                [
                    style.get("edgecolor", style.get("facecolor", self._facecolor))
                    for style in self.subset_styles
                ],
                name="color",
            )
            line_data = line_data.join(colors)
            ax.vlines(
                line_data.index.values,
                line_data["min"],
                line_data["max"],
                lw=1.8,
                colors=line_data["color"],
                zorder=5,
            )
            for row_idx in range(n_cats):
                ax.hlines(
                    row_idx,
                    -0.5,
                    len(data) - 0.5,
                    lw=0.5,
                    colors="#c7c7c7",
                    zorder=4,
                )

        tick_axis = ax.yaxis
        tick_axis.set_ticks(np.arange(n_cats))
        tick_axis.set_ticklabels(data.index.names, rotation=0 if self._horizontal else -90)
        ax.xaxis.set_visible(False)
        ax.tick_params(axis="both", which="both", length=0)
        if not self._horizontal:
            ax.yaxis.set_ticks_position("top")
        ax.set_frame_on(False)
        ax.set_xlim(-0.5, x[-1] + 0.5, auto=False)
        ax.grid(False)


def build_upset_series(groups: list[dict], test_list: list[int]) -> tuple[pd.Series, list[str], list[str]]:
    """Return the input series plus human-readable column labels and subset colors."""
    tuples = []
    counts = []
    subset_labels = []
    subset_colors = []
    failure_mode_num = 1

    for group in groups:
        tuples.append(tuple(test_id in group["failure_set"] for test_id in test_list))
        counts.append(len(group["members"]))
        if group["failure_set"]:
            subset_labels.append(f"Failure mode {failure_mode_num}")
            failure_mode_num += 1
            subset_colors.append(_COLORS["main"] if len(group["members"]) >= 20 else _COLORS["minor"])
        else:
            subset_labels.append("Correct")
            subset_colors.append(_COLORS["correct"])

    index = pd.MultiIndex.from_tuples(tuples, names=[str(test_id) for test_id in test_list])
    return pd.Series(counts, index=index), subset_labels, subset_colors


def build_language_totals(
    groups: list[dict],
    test_list: list[int],
) -> tuple[list[str], dict[str, list[int]]]:
    languages = sorted({language_of(version_id) for group in groups for version_id in group["members"]})
    counts_by_language = {language: [0] * len(test_list) for language in languages}
    for row_idx, test_id in enumerate(test_list):
        for group in groups:
            if test_id not in group["failure_set"]:
                continue
            for version_id in group["members"]:
                counts_by_language[language_of(version_id)][row_idx] += 1
    return languages, counts_by_language


def style_axes(axes: dict[str, plt.Axes], subset_labels: list[str]) -> None:
    axes["totals"].set_xlabel("Versions per\ntest case failed", fontsize=6)
    axes["totals"].xaxis.label.set_size(6)
    axes["totals"].tick_params(axis="x", labelsize=6)
    axes["totals"].tick_params(axis="y", left=False, labelleft=False)
    axes["totals"].set_axisbelow(True)
    axes["totals"].grid(axis="x", color="#d0d0d0", linewidth=0.6)

    axes["intersections"].set_ylabel("Versions per\nfailure mode", fontsize=6, labelpad=10)
    axes["intersections"].tick_params(axis="y", labelsize=6)
    axes["intersections"].tick_params(axis="x", labelbottom=False, bottom=False)

    axes["matrix"].tick_params(axis="y", labelsize=6)
    axes["matrix"].xaxis.set_visible(True)
    axes["matrix"].set_xticks(np.arange(len(subset_labels)))
    axes["matrix"].set_xticklabels(subset_labels, rotation=45, ha="right", fontsize=6)
    axes["matrix"].tick_params(axis="x", length=0, pad=2, labelsize=6)

    for key in ("intersections", "totals"):
        axes[key].spines["top"].set_visible(False)
        axes[key].spines["right"].set_visible(False)


def annotate_intersection_counts(ax: plt.Axes, fontsize: int = 5) -> None:
    heights = [patch.get_height() for patch in ax.patches]
    if not heights:
        return
    ymax = max(heights)
    pad = max(0.15, ymax * 0.015)
    for patch, height in zip(ax.patches, heights):
        x = patch.get_x() + patch.get_width() / 2
        ax.text(x, height + pad, f"{int(height)}", ha="center", va="bottom", fontsize=fontsize)


def annotate_total_counts(ax: plt.Axes, totals: list[int], fontsize: int = 5) -> None:
    if not totals:
        return
    xmax = max(totals)
    for y, total in enumerate(totals):
        label = f"{int(total)}"
        base_pad = max(0.4, xmax * 0.05)
        pad = base_pad * max(1, len(label))
        ax.text(total + pad, y, label, ha="left", va="center", fontsize=fontsize)


def shift_axes_left(axes: dict[str, plt.Axes], fraction: float) -> None:
    for ax in axes.values():
        pos = ax.get_position()
        new_x0 = max(0.0, pos.x0 * (1.0 - fraction))
        ax.set_position([new_x0, pos.y0, pos.width, pos.height])


def shift_axis_left(ax: plt.Axes, delta: float) -> None:
    pos = ax.get_position()
    ax.set_position([max(0.0, pos.x0 - delta), pos.y0, pos.width, pos.height])


def draw_language_stacked_totals(
    ax: plt.Axes,
    test_list: list[int],
    languages: list[str],
    counts_by_language: dict[str, list[int]],
) -> list[int]:
    for patch in list(ax.patches):
        patch.remove()
    y_pos = np.arange(len(test_list))
    cumulative = np.zeros(len(test_list), dtype=int)
    for language in languages:
        values = np.array(counts_by_language[language], dtype=int)
        ax.barh(
            y_pos,
            values,
            left=cumulative,
            color=_LANGUAGE_COLORS.get(language, "#999999"),
            edgecolor="white",
            linewidth=0.6,
            height=0.7,
            zorder=3,
        )
        cumulative += values
    return cumulative.tolist()


def plot_lic(groups: list[dict], output_path: Path, lic_number: int) -> None:
    test_list = sorted_test_cases(groups)
    if not test_list:
        raise ValueError(f"No LIC-{lic_number} failures found; there are no test-case rows to plot.")

    series, subset_labels, subset_colors = build_upset_series(groups, test_list)
    languages, counts_by_language = build_language_totals(groups, test_list)

    fig_w = max(16.0, 9.0 + 1.8 * len(groups))
    fig_h = min(max(10.5, 6.8 + 0.95 * len(test_list)), 120.0)
    fig = plt.figure(figsize=(fig_w, fig_h))

    upset = FixedUpSet(
        series,
        orientation="horizontal",
        sort_by="input",
        sort_categories_by="input",
        subset_size="sum",
        facecolor="#222222",
        other_dots_color="#d3d3d3",
        shading_color="white",
        with_lines=True,
        element_size=28,
        intersection_plot_elements=6,
        totals_plot_elements=3,
        show_counts="",
        include_empty_subsets=False,
    )

    for idx, color in enumerate(subset_colors):
        upset.subset_styles[idx] = {
            "facecolor": color,
            "edgecolor": color,
            "linewidth": 0.8,
        }

    axes = upset.plot(fig=fig)
    fig.subplots_adjust(top=0.82, bottom=0.26, left=0.16, right=0.99)
    if "totals" in axes and "matrix" in axes:
        totals_pos = axes["totals"].get_position()
        matrix_pos = axes["matrix"].get_position()
        gap = 0.1
        new_totals_x0 = matrix_pos.x0 - gap - totals_pos.width
        axes["totals"].set_position([new_totals_x0, totals_pos.y0, totals_pos.width, totals_pos.height])
    if "shading" in axes and "matrix" in axes:
        shading_pos = axes["shading"].get_position()
        matrix_pos = axes["matrix"].get_position()
        axes["shading"].set_position([matrix_pos.x0, shading_pos.y0, shading_pos.x1 - matrix_pos.x0, shading_pos.height])
    shift_axes_left(axes, fraction=0.2)
    if "totals" in axes:
        shift_axis_left(axes["totals"], delta=0.04)
        total_counts = draw_language_stacked_totals(axes["totals"], test_list, languages, counts_by_language)
    else:
        total_counts = []
    style_axes(axes, subset_labels)
    annotate_intersection_counts(axes["intersections"], fontsize=5)
    annotate_total_counts(axes["totals"], total_counts, fontsize=5)

    fig.suptitle(
        f"LIC-{lic_number} Failure Modes",
        fontsize=8,
        fontweight="bold",
        y=0.89,
    )
    fig.savefig(output_path, dpi=150, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"Wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fault-events",
        type=Path,
        default=Path("results/main-spec-3/fault_events.jsonl"),
    )
    parser.add_argument(
        "--campaign",
        type=Path,
        default=Path("results/main-spec-3"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/main-spec-3/lic10_failure_modes.pdf"),
    )
    parser.add_argument(
        "--lic",
        type=int,
        default=10,
        help="1-based LIC number to visualize (default: 10).",
    )
    args = parser.parse_args()

    if args.lic < 1 or args.lic > 15:
        raise SystemExit("--lic must be between 1 and 15.")

    failures = load_lic_failures(args.fault_events, args.lic)

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from analysis.analyze_results import analysis_version_ids, read_campaign_version_order

    campaign_dir = args.campaign if args.campaign.is_dir() else args.campaign.parent
    all_versions = analysis_version_ids(
        campaign_dir,
        read_campaign_version_order(campaign_dir / "campaign.csv"),
    )
    groups = build_groups(failures, all_versions)

    print(f"Distinct failure-mode groups (incl. correct): {len(groups)}")
    for group in groups:
        failure_set = group["failure_set"]
        fs_str = "{" + ", ".join(str(test_id) for test_id in sorted(failure_set)) + "}" if failure_set else "∅"
        member_names = [short_label(version_id) for version_id in group["members"][:3]]
        ellipsis = f", … +{len(group['members']) - 3}" if len(group["members"]) > 3 else ""
        print(
            f"  {len(group['members']):3d} versions  failing={fs_str:50s}  "
            f"e.g. {', '.join(member_names)}{ellipsis}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    plot_lic(groups, args.output, args.lic)


if __name__ == "__main__":
    main()
