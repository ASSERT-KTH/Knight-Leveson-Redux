"""
Oracle-aware analysis from ``cmv_outputs.npz``.

This is the ``run_campaign_lic`` analog of ``analysis.analyze_results``.  It
reconstructs the oracle CMV stream from the generator seed and compares each
stored CMV vector against that oracle.  A version is counted as failing on a
test iff:

1. it did not produce a valid output tuple on that test, or
2. its stored 15-bit CMV differs from the oracle CMV.

Because ``cmv_outputs.npz`` stores only CMV bits plus a validity mask, this
analysis is oracle-aware at the CMV level.  It cannot detect cases where a
candidate returned the correct CMV but incorrect PUM/FUV/LAUNCH.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.analyze_results import (  # noqa: E402
    analyze_from_stream_aggregates,
    cross_language_matched_from_aggregates,
    format_version_label,
    plot_cross_language_phi,
    plot_failure_heatmaps,
    plot_failure_rates,
    plot_failures_by_language_stacked,
)
from benchmarks.launch_interceptor.generator import iter_campaign_cases  # noqa: E402

_BIT_MASK_15 = np.uint16((1 << 15) - 1)


def _pack_cmv_bits(cmv: list[bool]) -> np.uint16:
    bits = 0
    for b, val in enumerate(cmv):
        if val:
            bits |= 1 << b
    return np.uint16(bits)


def build_oracle_cmv_bits(seed: int, n: int) -> np.ndarray:
    """Regenerate the oracle CMV bit-pack stream for the CMV campaign."""
    out = np.empty(n, dtype=np.uint16)
    for test_id, case in enumerate(iter_campaign_cases(seed=seed, n=n)):
        out[test_id] = _pack_cmv_bits(case["cmv"])
    return out


def compute_aggregates(
    *,
    cmv_packed: np.ndarray,
    valid: np.ndarray,
    oracle_bits: np.ndarray,
    languages: list[str],
) -> tuple[
    np.ndarray,
    np.ndarray,
    int,
    dict[str, int],
    dict[str, np.ndarray],
    dict[str, np.ndarray],
    dict[str, list[int]],
    list[str],
    list[tuple[int, np.ndarray]],
    np.ndarray,
]:
    """
    Return aggregate failure statistics analogous to ``analyze_results``, plus
    per-version LIC mismatch counts.
    """
    valid_bool = valid.astype(bool, copy=False)
    xor = np.bitwise_xor(cmv_packed, oracle_bits[np.newaxis, :]) & _BIT_MASK_15
    fail_matrix = (~valid_bool) | (xor != 0)

    v_fail = fail_matrix.sum(axis=1, dtype=np.int64)
    fail_int = fail_matrix.astype(np.int64, copy=False)
    pair_counts = fail_int @ fail_int.T
    per_test_failures = fail_int.sum(axis=0, dtype=np.int64)
    K_full = int(np.count_nonzero(per_test_failures >= 2))

    lic_fail_counts = np.zeros((cmv_packed.shape[0], 15), dtype=np.int64)
    for b in range(15):
        lic_fail_counts[:, b] = (
            (((xor >> b) & np.uint16(1)) != 0) & valid_bool
        ).sum(axis=1, dtype=np.int64)

    langs = sorted(set(languages))
    lang_indices: dict[str, list[int]] = {
        lang: [i for i, v in enumerate(languages) if v == lang] for lang in langs
    }
    K_lang: dict[str, int] = {}
    pair_lang: dict[str, np.ndarray] = {}
    vfail_lang: dict[str, np.ndarray] = {}
    stacked_matrix = np.zeros((len(langs), fail_matrix.shape[1]), dtype=np.int64)
    for li, lang in enumerate(langs):
        idx = np.array(lang_indices[lang], dtype=np.int64)
        sub = fail_int[idx]
        stacked_matrix[li] = sub.sum(axis=0, dtype=np.int64)
        K_lang[lang] = int(np.count_nonzero(stacked_matrix[li] >= 2))
        pair_lang[lang] = sub @ sub.T
        vfail_lang[lang] = sub.sum(axis=1, dtype=np.int64)

    failing_rows: list[tuple[int, np.ndarray]] = []
    total_failures = stacked_matrix.sum(axis=0)
    for test_id in np.flatnonzero(total_failures >= 1):
        failing_rows.append((int(test_id), stacked_matrix[:, test_id].copy()))

    return (
        pair_counts,
        v_fail,
        K_full,
        K_lang,
        pair_lang,
        vfail_lang,
        lang_indices,
        langs,
        failing_rows,
        lic_fail_counts,
    )


def build_version_summary(
    *,
    versions: list[str],
    agents: list[str],
    languages: list[str],
    valid: np.ndarray,
    v_fail: np.ndarray,
    lic_fail_counts: np.ndarray,
    T: int,
) -> pd.DataFrame:
    rows: list[dict] = []
    for i, version_id in enumerate(versions):
        row = {
            "version_id": version_id,
            "label": format_version_label(version_id),
            "agent": agents[i],
            "language": languages[i],
            "total": T,
            "failed_count": int(v_fail[i]),
            "passed_count": int(T - v_fail[i]),
            "failure_rate": float(v_fail[i] / T),
            "valid_count": int(valid[i].sum()),
            "invalid_count": int(T - valid[i].sum()),
            "invalid_rate": float(1.0 - valid[i].mean()),
        }
        for lic in range(15):
            row[f"lic_{lic + 1}_mismatch_count"] = int(lic_fail_counts[i, lic])
        rows.append(row)
    df = pd.DataFrame(rows)
    return df.sort_values(
        by=["failure_rate", "invalid_rate", "language", "label"],
        ascending=[False, False, True, True],
    ).reset_index(drop=True)


def generate_report(
    output_path: Path,
    *,
    stats_dict: dict,
    version_summary: pd.DataFrame,
    pairwise_df: pd.DataFrame,
    cross_language_df: pd.DataFrame,
) -> None:
    kl = stats_dict["kl"]
    z = float(kl["z"]) if not math.isnan(float(kl["z"])) else float("nan")
    reject = bool(kl.get("reject_h0_99pct", False))
    lines = [
        "# Oracle-Aware CMV Analysis",
        "",
        "This report is derived from `cmv_outputs.npz`, not `campaign.csv`.",
        "A version fails a test if it produced an invalid output tuple or if its CMV differs from the oracle CMV.",
        "",
        "## Summary",
        "",
        f"- Tests: {int(kl['T']):,}",
        f"- Versions: {int(kl['n_versions'])}",
        f"- Observed K (2+ simultaneous failures): {int(kl['K_observed']):,}",
        f"- Expected K under independence: {float(kl['expected_K']):.2f}",
        f"- z-statistic: {z:.4f}" if not math.isnan(z) else "- z-statistic: n/a",
        "",
        "## Interpretation",
        "",
    ]
    if kl.get("n_versions", 0) < 2:
        lines.append("> Not enough versions to compute the pooled K&L statistic.")
    elif math.isnan(z):
        lines.append("> z-statistic could not be computed.")
    elif reject:
        lines.append(
            f"> **H0 rejected** at 99% confidence (z={z:.2f}). "
            "Observed coincident CMV failures exceed the independence prediction."
        )
    else:
        lines.append(
            f"> **H0 not rejected** at 99% confidence (z={z:.2f}). "
            "Observed coincident CMV failures are consistent with independence."
        )

    lines += [
        "",
        "## Highest Failure Rates",
        "",
        "| Version | Language | Failure rate | Invalid rate |",
        "|---------|----------|--------------|--------------|",
    ]
    for _, row in version_summary.head(20).iterrows():
        lines.append(
            f"| `{row['label']}` | {row['language']} | {float(row['failure_rate']):.6f} | "
            f"{float(row['invalid_rate']):.6f} |"
        )

    lines += [
        "",
        "## Highest Pairwise Co-Failures",
        "",
        "| Version i | Version j | Observed | Expected | Phi |",
        "|-----------|-----------|---------:|---------:|----:|",
    ]
    for _, row in pairwise_df.head(20).iterrows():
        lines.append(
            f"| `{format_version_label(row['version_i'])}` | "
            f"`{format_version_label(row['version_j'])}` | "
            f"{int(row['observed_cofailures']):,} | {float(row['expected_cofailures']):.2f} | "
            f"{float(row['phi_correlation']):.4f} |"
        )

    if not cross_language_df.empty:
        lines += [
            "",
            "## Cross-Language Matched Pairs",
            "",
            "| Pair | Observed | Expected | Phi |",
            "|------|---------:|---------:|----:|",
        ]
        for _, row in cross_language_df.head(20).iterrows():
            pair = (
                f"`{row['version_i']}` ({row['language_i']}) vs "
                f"`{row['version_j']}` ({row['language_j']})"
            )
            lines.append(
                f"| {pair} | {int(row['observed_cofailures']):,} | "
                f"{float(row['expected_cofailures']):.2f} | {float(row['phi_correlation']):.4f} |"
            )

    lines += [
        "",
        "## Caveat",
        "",
        "- This analysis is exact for CMV mismatches and invalid outputs.",
        "- It does not detect cases where a candidate returned the correct CMV but incorrect PUM/FUV/LAUNCH, because `cmv_outputs.npz` does not store those fields.",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {output_path}")


def run(cmv_path: Path, output_dir: Path, report_path: Path, *, cross_language: bool = True) -> None:
    if not cmv_path.is_file():
        raise SystemExit(f"cmv_outputs.npz not found: {cmv_path}")

    data = np.load(cmv_path, allow_pickle=True)
    versions = data["versions"].tolist()
    languages = data["languages"].tolist()
    agents = data["agents"].tolist()
    cmv_packed: np.ndarray = data["cmv_packed"]
    valid: np.ndarray = data["valid"].astype(np.uint8)
    seed = int(data["seed"])
    T = int(data["n"])

    print(f"Regenerating oracle CMV stream for {T} tests (seed={seed})...")
    oracle_bits = build_oracle_cmv_bits(seed, T)

    print(f"Computing oracle-aware CMV failure aggregates for {len(versions)} versions...")
    (
        pair_full,
        v_fail_full,
        K_full,
        K_lang,
        pair_lang,
        vfail_lang,
        lang_indices,
        langs,
        failing_tests_by_language,
        lic_fail_counts,
    ) = compute_aggregates(
        cmv_packed=cmv_packed,
        valid=valid,
        oracle_bits=oracle_bits,
        languages=languages,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    agent_by_vid = {version_id: agents[i] for i, version_id in enumerate(versions)}
    lang_by_vid = {version_id: languages[i] for i, version_id in enumerate(versions)}

    stats_dict, version_stats, pairwise_df = analyze_from_stream_aggregates(
        T,
        K_full,
        pair_full,
        v_fail_full,
        versions,
        agent_by_vid,
    )
    version_summary = build_version_summary(
        versions=versions,
        agents=agents,
        languages=languages,
        valid=valid,
        v_fail=v_fail_full,
        lic_fail_counts=lic_fail_counts,
        T=T,
    )

    (output_dir / "stats_cmv_oracle.json").write_text(
        json.dumps(stats_dict, indent=2, default=str),
        encoding="utf-8",
    )
    version_summary.to_csv(output_dir / "summary_table_cmv_oracle.csv", index=False)
    pairwise_df.to_csv(output_dir / "pairwise_table_cmv_oracle.csv", index=False)
    np.savez(
        output_dir / "failure_sets_cmv_oracle.npz",
        versions=np.asarray(versions, dtype=object),
        v_fail=v_fail_full,
        pair_counts=pair_full,
        lic_fail_counts=lic_fail_counts,
    )

    plot_failure_heatmaps(pairwise_df, output_dir / "failure_heatmap_cmv_oracle")
    plot_failure_rates(version_stats, output_dir / "failure_rates_cmv_oracle.pdf")
    plot_failures_by_language_stacked(
        langs,
        failing_tests_by_language,
        output_dir / "failures_by_language_stacked_cmv_oracle.pdf",
    )

    for lang in langs:
        idx = lang_indices[lang]
        versions_lang = [versions[i] for i in idx]
        agents_lang = {version_id: agent_by_vid[version_id] for version_id in versions_lang}
        stats_lang, version_stats_lang, pairwise_lang = analyze_from_stream_aggregates(
            T,
            K_lang[lang],
            pair_lang[lang],
            vfail_lang[lang],
            versions_lang,
            agents_lang,
        )
        sub_summary = version_summary[version_summary["language"] == lang].copy()
        (output_dir / f"stats_cmv_oracle_{lang}.json").write_text(
            json.dumps(stats_lang, indent=2, default=str),
            encoding="utf-8",
        )
        sub_summary.to_csv(output_dir / f"summary_table_cmv_oracle_{lang}.csv", index=False)
        if not pairwise_lang.empty:
            pairwise_lang.to_csv(output_dir / f"pairwise_table_cmv_oracle_{lang}.csv", index=False)
            plot_failure_heatmaps(pairwise_lang, output_dir / f"failure_heatmap_cmv_oracle_{lang}")
        plot_failure_rates(version_stats_lang, output_dir / f"failure_rates_cmv_oracle_{lang}.pdf")

    cross_language_df = pd.DataFrame()
    if cross_language and len(langs) >= 2:
        cross_language_df = cross_language_matched_from_aggregates(
            pair_full,
            v_fail_full,
            T,
            versions,
            lang_by_vid,
            agent_by_vid,
        )
        if not cross_language_df.empty:
            cross_language_df.to_csv(
                output_dir / "cross_language_pairwise_cmv_oracle.csv",
                index=False,
            )
            plot_cross_language_phi(
                cross_language_df,
                output_dir / "cross_language_phi_cmv_oracle.pdf",
            )

    generate_report(
        report_path,
        stats_dict=stats_dict,
        version_summary=version_summary,
        pairwise_df=pairwise_df,
        cross_language_df=cross_language_df,
    )
    print(f"\nOracle-aware CMV analysis complete. Output in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cmv", type=Path, required=True, help="cmv_outputs.npz from run_campaign_lic")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument("--report", type=Path, default=None, help="Markdown report path")
    parser.add_argument(
        "--no-cross-language",
        action="store_true",
        help="Skip matched cross-language pairwise analysis",
    )
    args = parser.parse_args()
    report = args.report or (args.output / "report_cmv_oracle.md")
    run(
        args.cmv.resolve(),
        args.output.resolve(),
        report.resolve(),
        cross_language=not args.no_cross_language,
    )


if __name__ == "__main__":
    main()
