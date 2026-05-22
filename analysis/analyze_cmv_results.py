"""
Analyze oracle-free CMV-output campaigns from ``pipeline.run_campaign_lic``.

This complements ``analysis.analyze_results``.  That script is oracle-aware and
requires ``campaign.csv`` pass/fail data.  This script instead consumes
``cmv_outputs.npz`` and summarizes how implementations differ in their 15-bit CMV
outputs, plus how often they fail to produce a valid output at all.

Outputs (written to ``--output``):
    cmv_version_stats.csv
    cmv_pairwise_table.csv
    cmv_disagreement_matrix.npz
    cmv_disagreement_heatmap_{bit,any,valid}.pdf
    cmv_invalid_rates.pdf
    cmv_mean_disagreement.pdf
    cmv_cross_language_pairwise.csv          (when matched cross-language pairs exist)
    cmv_cross_language_bit.pdf               (when matched cross-language pairs exist)
    cmv_cross_language_any.pdf               (when matched cross-language pairs exist)
    stats_cmv.json
    report_cmv.md                           (or ``--report`` path)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.analyze_results import format_version_label, match_base_key  # noqa: E402
from analysis.build_n_version_units_lic_disagree import compute_cmv_disagreement  # noqa: E402


def _safe_nanmean(values: np.ndarray) -> float:
    if values.size == 0:
        return float("nan")
    with np.errstate(invalid="ignore"):
        out = np.nanmean(values)
    return float(out) if not np.isnan(out) else float("nan")


def build_version_stats(
    versions: list[str],
    languages: list[str],
    agents: list[str],
    valid: np.ndarray,
    bit_disagree: np.ndarray,
    any_disagree: np.ndarray,
    pair_valid_count: np.ndarray,
) -> pd.DataFrame:
    rows: list[dict] = []
    V, T = valid.shape
    for i in range(V):
        jointly_valid = pair_valid_count[i] > 0
        jointly_valid[i] = False
        bit_vals = bit_disagree[i, jointly_valid]
        any_vals = any_disagree[i, jointly_valid]
        rows.append({
            "version_id": versions[i],
            "label": format_version_label(versions[i]),
            "language": languages[i],
            "agent": agents[i],
            "valid_count": int(valid[i].sum()),
            "invalid_count": int(T - valid[i].sum()),
            "invalid_rate": float(1.0 - valid[i].mean()),
            "mean_bit_disagree_rate": _safe_nanmean(bit_vals),
            "mean_any_disagree_rate": _safe_nanmean(any_vals),
            "max_bit_disagree_rate": float(np.nanmax(bit_vals)) if bit_vals.size else float("nan"),
            "max_any_disagree_rate": float(np.nanmax(any_vals)) if any_vals.size else float("nan"),
        })
    df = pd.DataFrame(rows)
    return df.sort_values(
        by=["invalid_rate", "mean_bit_disagree_rate", "mean_any_disagree_rate"],
        ascending=[False, False, False],
    ).reset_index(drop=True)


def build_pairwise_table(
    versions: list[str],
    languages: list[str],
    agents: list[str],
    bit_disagree: np.ndarray,
    any_disagree: np.ndarray,
    pair_valid_count: np.ndarray,
    pair_hamming_total: np.ndarray,
) -> pd.DataFrame:
    rows: list[dict] = []
    V = len(versions)
    for i in range(V):
        for j in range(i + 1, V):
            rows.append({
                "version_i": versions[i],
                "version_j": versions[j],
                "label_i": format_version_label(versions[i]),
                "label_j": format_version_label(versions[j]),
                "language_i": languages[i],
                "language_j": languages[j],
                "agent_i": agents[i],
                "agent_j": agents[j],
                "pair_valid_count": int(pair_valid_count[i, j]),
                "bit_disagree_rate": float(bit_disagree[i, j]),
                "any_disagree_rate": float(any_disagree[i, j]),
                "pair_hamming_total": int(pair_hamming_total[i, j]),
            })
    df = pd.DataFrame(rows)
    return df.sort_values(
        by=["bit_disagree_rate", "any_disagree_rate", "pair_valid_count"],
        ascending=[False, False, False],
    ).reset_index(drop=True)


def build_cross_language_pairwise(pairwise_df: pd.DataFrame) -> pd.DataFrame:
    if pairwise_df.empty:
        return pd.DataFrame()
    out = pairwise_df.copy()
    out["base_i"] = out["version_i"].map(match_base_key)
    out["base_j"] = out["version_j"].map(match_base_key)
    out = out[
        (out["base_i"] == out["base_j"]) &
        (out["language_i"] != out["language_j"])
    ].copy()
    if out.empty:
        return out
    out["base_key"] = out["base_i"]
    return out.drop(columns=["base_i", "base_j"]).sort_values(
        by=["bit_disagree_rate", "any_disagree_rate"],
        ascending=[False, False],
    ).reset_index(drop=True)


def _plot_square_heatmap(
    mat: np.ndarray,
    labels: list[str],
    title: str,
    fmt: str,
    output_path: Path,
    *,
    cmap: str = "YlOrRd",
) -> None:
    n = len(labels)
    if n == 0:
        return
    size_inches = float(min(26.0, max(18.0, n * 0.62)))
    fig, ax = plt.subplots(figsize=(size_inches, size_inches))
    im = ax.imshow(mat, cmap=cmap, aspect="equal")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    tick_fs = max(8, min(13, 260 / max(n, 1)))
    ax.set_xticklabels(labels, fontsize=tick_fs, rotation=45, ha="right")
    ax.set_yticklabels(labels, fontsize=tick_fs)
    ax.set_title(title, fontsize=15, pad=16)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if n <= 36:
        ann_fs = max(6, min(11, 240 / max(n, 6)))
        for row_i in range(n):
            for col_j in range(n):
                val = mat[row_i, col_j]
                if not np.isnan(val):
                    ax.text(
                        col_j,
                        row_i,
                        f"{val:{fmt}}",
                        ha="center",
                        va="center",
                        fontsize=ann_fs,
                        color="black",
                    )
    fig.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Wrote {output_path}")


def plot_cmv_heatmaps(
    versions: list[str],
    bit_disagree: np.ndarray,
    any_disagree: np.ndarray,
    pair_valid_count: np.ndarray,
    output_dir: Path,
) -> None:
    labels = [format_version_label(v) for v in versions]
    _plot_square_heatmap(
        bit_disagree,
        labels,
        "Pairwise CMV disagreement rate per LIC bit",
        ".3f",
        output_dir / "cmv_disagreement_heatmap_bit.pdf",
    )
    _plot_square_heatmap(
        any_disagree,
        labels,
        "Pairwise CMV disagreement rate per test",
        ".3f",
        output_dir / "cmv_disagreement_heatmap_any.pdf",
    )
    _plot_square_heatmap(
        pair_valid_count.astype(float),
        labels,
        "Jointly valid test count per pair",
        ".0f",
        output_dir / "cmv_disagreement_heatmap_valid.pdf",
        cmap="Blues",
    )


def plot_invalid_rates(version_stats: pd.DataFrame, output_path: Path) -> None:
    labels = version_stats["label"].tolist()
    values = version_stats["invalid_rate"].tolist()
    colors = [("#DD8452" if v > 0 else "#4C72B0") for v in values]
    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 0.8), 5))
    bars = ax.bar(range(len(labels)), values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8, rotation=45, ha="right")
    ax.set_ylabel("Invalid output rate")
    ax.set_title("Per-version invalid output rate", fontsize=12)
    ax.set_ylim(0, max(values) * 1.2 + 0.001 if values else 1.0)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.001,
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Wrote {output_path}")


def plot_mean_disagreement(version_stats: pd.DataFrame, output_path: Path) -> None:
    df = version_stats.sort_values("mean_bit_disagree_rate", ascending=False).reset_index(drop=True)
    labels = df["label"].tolist()
    bit_vals = df["mean_bit_disagree_rate"].to_numpy(dtype=float)
    any_vals = df["mean_any_disagree_rate"].to_numpy(dtype=float)
    x = np.arange(len(labels), dtype=float)
    width = 0.42
    fig, ax = plt.subplots(figsize=(max(8, len(labels) * 0.9), 5.5))
    ax.bar(x - width / 2, bit_vals, width, label="Mean bit disagreement", color="#C44E52")
    ax.bar(x + width / 2, any_vals, width, label="Mean any-test disagreement", color="#55A868")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8, rotation=45, ha="right")
    ax.set_ylabel("Disagreement rate")
    ax.set_title("Mean pairwise CMV disagreement by version", fontsize=12)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Wrote {output_path}")


def plot_cross_language_metric(
    df: pd.DataFrame,
    metric: str,
    title: str,
    output_path: Path,
) -> None:
    if df.empty:
        return
    ordered = df.sort_values(metric, ascending=False).reset_index(drop=True)
    labels = [
        f"{row['label_i']} [{row['language_i']}] vs {row['label_j']} [{row['language_j']}]"
        for _, row in ordered.iterrows()
    ]
    values = ordered[metric].to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.65), 5.5))
    bars = ax.bar(range(len(labels)), values, color="#8172B2", edgecolor="white", linewidth=0.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=8, rotation=45, ha="right")
    ax.set_ylabel(metric.replace("_", " "))
    ax.set_title(title, fontsize=12)
    ax.set_ylim(0, max(values) * 1.15 + 0.001)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.001,
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Wrote {output_path}")


def build_stats_summary(
    version_stats: pd.DataFrame,
    pairwise_df: pd.DataFrame,
    cross_language_df: pd.DataFrame,
    *,
    n_tests: int,
    seed: int,
) -> dict:
    langs = sorted(set(version_stats["language"].tolist()))
    by_language: dict[str, dict[str, float | int]] = {}
    for lang in langs:
        sub = version_stats[version_stats["language"] == lang]
        by_language[lang] = {
            "n_versions": int(len(sub)),
            "mean_invalid_rate": float(sub["invalid_rate"].mean()),
            "mean_bit_disagree_rate": float(sub["mean_bit_disagree_rate"].mean()),
            "mean_any_disagree_rate": float(sub["mean_any_disagree_rate"].mean()),
        }

    top_pair = pairwise_df.iloc[0].to_dict() if not pairwise_df.empty else None
    top_cross = cross_language_df.iloc[0].to_dict() if not cross_language_df.empty else None
    return {
        "seed": int(seed),
        "n_tests": int(n_tests),
        "n_versions": int(len(version_stats)),
        "languages": langs,
        "mean_invalid_rate": float(version_stats["invalid_rate"].mean()),
        "max_invalid_rate": float(version_stats["invalid_rate"].max()),
        "mean_pairwise_bit_disagree_rate": float(pairwise_df["bit_disagree_rate"].mean()),
        "mean_pairwise_any_disagree_rate": float(pairwise_df["any_disagree_rate"].mean()),
        "top_pairwise_bit_disagree": top_pair,
        "top_cross_language_bit_disagree": top_cross,
        "by_language": by_language,
    }


def write_report(
    output_path: Path,
    stats_summary: dict,
    version_stats: pd.DataFrame,
    pairwise_df: pd.DataFrame,
    cross_language_df: pd.DataFrame,
) -> None:
    top_versions = version_stats.head(15)
    top_pairs = pairwise_df.head(20)
    lines = [
        "# CMV Output Analysis",
        "",
        "Oracle-free summary from `cmv_outputs.npz` produced by `pipeline.run_campaign_lic`.",
        "",
        "## Overview",
        "",
        f"- Tests: {int(stats_summary['n_tests']):,}",
        f"- Versions: {int(stats_summary['n_versions'])}",
        f"- Languages: {', '.join(stats_summary['languages'])}",
        f"- Mean invalid output rate: {float(stats_summary['mean_invalid_rate']):.6f}",
        f"- Mean pairwise bit disagreement rate: {float(stats_summary['mean_pairwise_bit_disagree_rate']):.6f}",
        f"- Mean pairwise any-test disagreement rate: {float(stats_summary['mean_pairwise_any_disagree_rate']):.6f}",
        "",
        "## Highest-Invalid Versions",
        "",
        "| Version | Language | Invalid rate | Mean bit disagree | Mean any disagree |",
        "|---------|----------|--------------|-------------------|-------------------|",
    ]
    for _, row in top_versions.iterrows():
        lines.append(
            f"| `{row['label']}` | {row['language']} | {float(row['invalid_rate']):.6f} | "
            f"{float(row['mean_bit_disagree_rate']):.6f} | {float(row['mean_any_disagree_rate']):.6f} |"
        )

    lines += [
        "",
        "## Highest-Disagreement Pairs",
        "",
        "| Version i | Version j | Joint valid tests | Bit disagree | Any disagree |",
        "|-----------|-----------|------------------:|-------------:|-------------:|",
    ]
    for _, row in top_pairs.iterrows():
        lines.append(
            f"| `{row['label_i']}` | `{row['label_j']}` | {int(row['pair_valid_count']):,} | "
            f"{float(row['bit_disagree_rate']):.6f} | {float(row['any_disagree_rate']):.6f} |"
        )

    if not cross_language_df.empty:
        lines += [
            "",
            "## Cross-Language Matched Pairs",
            "",
            "Matched on `agent/model/run`, differing only in language.",
            "",
            "| Pair | Bit disagree | Any disagree |",
            "|------|-------------:|-------------:|",
        ]
        for _, row in cross_language_df.head(20).iterrows():
            pair = (
                f"`{row['label_i']}` [{row['language_i']}] vs "
                f"`{row['label_j']}` [{row['language_j']}]"
            )
            lines.append(
                f"| {pair} | {float(row['bit_disagree_rate']):.6f} | "
                f"{float(row['any_disagree_rate']):.6f} |"
            )

    lines += [
        "",
        "## Files",
        "",
        "| File | Description |",
        "|------|-------------|",
        "| `cmv_version_stats.csv` | Per-version valid/invalid and disagreement summary |",
        "| `cmv_pairwise_table.csv` | Pairwise disagreement rates and jointly-valid counts |",
        "| `cmv_disagreement_matrix.npz` | Cached pairwise matrices |",
        "| `cmv_disagreement_heatmap_{bit,any,valid}.pdf` | Pairwise heatmaps |",
        "| `cmv_invalid_rates.pdf` | Invalid output rates by version |",
        "| `cmv_mean_disagreement.pdf` | Mean disagreement rates by version |",
        "",
    ]
    if not cross_language_df.empty:
        lines += [
            "| `cmv_cross_language_pairwise.csv` | Cross-language matched-pair disagreements |",
            "| `cmv_cross_language_{bit,any}.pdf` | Cross-language matched-pair plots |",
            "",
        ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")


def run(cmv_path: Path, output_dir: Path, report_path: Path) -> None:
    if not cmv_path.is_file():
        raise SystemExit(f"cmv_outputs.npz not found: {cmv_path}")

    data = np.load(cmv_path, allow_pickle=True)
    versions = data["versions"].tolist()
    languages = data["languages"].tolist()
    agents = data["agents"].tolist()
    cmv_packed = data["cmv_packed"]
    valid = data["valid"].astype(np.uint8)
    seed = int(data["seed"])
    n_tests = int(data["n"])

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"CMV campaign: {n_tests} tests x {len(versions)} versions")
    bit_disagree, any_disagree, pair_valid_count, pair_hamming_total = compute_cmv_disagreement(
        cmv_packed,
        valid,
    )

    version_stats = build_version_stats(
        versions,
        languages,
        agents,
        valid,
        bit_disagree,
        any_disagree,
        pair_valid_count,
    )
    pairwise_df = build_pairwise_table(
        versions,
        languages,
        agents,
        bit_disagree,
        any_disagree,
        pair_valid_count,
        pair_hamming_total,
    )
    cross_language_df = build_cross_language_pairwise(pairwise_df)

    version_stats.to_csv(output_dir / "cmv_version_stats.csv", index=False)
    pairwise_df.to_csv(output_dir / "cmv_pairwise_table.csv", index=False)
    np.savez(
        output_dir / "cmv_disagreement_matrix.npz",
        versions=np.asarray(versions, dtype=object),
        bit_disagree=bit_disagree,
        any_disagree=any_disagree,
        pair_valid_count=pair_valid_count,
        pair_hamming_total=pair_hamming_total,
    )

    plot_cmv_heatmaps(versions, bit_disagree, any_disagree, pair_valid_count, output_dir)
    plot_invalid_rates(version_stats, output_dir / "cmv_invalid_rates.pdf")
    plot_mean_disagreement(version_stats, output_dir / "cmv_mean_disagreement.pdf")

    if not cross_language_df.empty:
        cross_language_df.to_csv(output_dir / "cmv_cross_language_pairwise.csv", index=False)
        plot_cross_language_metric(
            cross_language_df,
            "bit_disagree_rate",
            "Cross-language matched-pair bit disagreement",
            output_dir / "cmv_cross_language_bit.pdf",
        )
        plot_cross_language_metric(
            cross_language_df,
            "any_disagree_rate",
            "Cross-language matched-pair any-test disagreement",
            output_dir / "cmv_cross_language_any.pdf",
        )

    stats_summary = build_stats_summary(
        version_stats,
        pairwise_df,
        cross_language_df,
        n_tests=n_tests,
        seed=seed,
    )
    (output_dir / "stats_cmv.json").write_text(
        json.dumps(stats_summary, indent=2, default=str),
        encoding="utf-8",
    )
    write_report(report_path, stats_summary, version_stats, pairwise_df, cross_language_df)
    print(f"\nCMV analysis complete. Output in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cmv", type=Path, required=True, help="cmv_outputs.npz from run_campaign_lic")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Markdown report path (default: <output>/report_cmv.md)",
    )
    args = parser.parse_args()
    report = args.report or (args.output / "report_cmv.md")
    run(args.cmv.resolve(), args.output.resolve(), report.resolve())


if __name__ == "__main__":
    main()
