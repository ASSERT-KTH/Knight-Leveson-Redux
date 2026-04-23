"""
Pipeline stage 4: Statistical analysis and report generation.

Implements the Knight & Leveson (1986) statistical methodology exactly:
  - Versions marked in ``versions/index.json`` as having no usable build/runner
    are dropped from all aggregates, plots, CSV exports, and the Markdown report.
  - Per-version failure rates
  - K&L z-statistic (observed vs expected simultaneous failures)
  - Pairwise coincident-failure analysis with Bonferroni correction
  - Pearson phi correlation
  - Summary table, heatmap, JSON stats
  - Stacked bar chart of failing tests × failures per language
  - Markdown report

Usage:
    python -m analysis.analyze_results \\
        --campaign results/pilot/campaign.csv \\
        --output results/pilot/ \\
        --report report.md
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


# ---------------------------------------------------------------------------
# Version identity (cross-language matching)
# ---------------------------------------------------------------------------

def match_base_key(version_id: str) -> str:
    """
    Strip ``__l_<language>__`` so versions generated for the same agent/model/run
    across languages share one key for matched-pair analysis.
    """
    return re.sub(r"__l_[a-z0-9]+__", "__", version_id, flags=re.IGNORECASE)


# ---------------------------------------------------------------------------
# K&L statistical methodology
# ---------------------------------------------------------------------------

def kl_z_statistic(failure_rates: list[float], T: int, K: int) -> dict:
    """
    Compute the Knight & Leveson (1986) z-statistic for independence.

    Parameters
    ----------
    failure_rates : list of per-version failure rates p_i
    T : total number of test cases
    K : observed number of test cases with 2+ simultaneous failures

    Returns dict with P_0, P_1, P_m, expected_K, z, p_value, reject_h0
    """
    n = len(failure_rates)
    if n < 2:
        # Full key set so callers (CLI print, stats_*.json, reports) never KeyError
        return {
            "error": "Need at least 2 versions for K&L pooled statistic",
            "n_versions": n,
            "T": T,
            "K_observed": K,
            "P_0": float("nan"),
            "P_1": float("nan"),
            "P_m": float("nan"),
            "expected_K": float("nan"),
            "std_K": float("nan"),
            "z": float("nan"),
            "p_value": float("nan"),
            "reject_h0_99pct": False,
            "reject_h0_95pct": False,
        }

    # P_0 = probability no version fails
    P_0 = math.prod(1 - p for p in failure_rates)

    # P_1 = probability exactly one version fails
    P_1 = sum(
        failure_rates[i] * math.prod(
            (1 - failure_rates[j]) for j in range(n) if j != i
        )
        for i in range(n)
    )

    # P_m = probability 2 or more fail simultaneously
    P_m = max(0.0, 1 - P_0 - P_1)

    mu = T * P_m
    sigma2 = T * P_m * (1 - P_m)
    sigma = math.sqrt(sigma2) if sigma2 > 0 else 0.0

    if sigma == 0:
        z = float("nan")
        p_value = float("nan")
    else:
        z = (K - mu) / sigma
        # Two-tailed p-value from normal approximation
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {
        "n_versions": n,
        "T": T,
        "K_observed": K,
        "P_0": P_0,
        "P_1": P_1,
        "P_m": P_m,
        "expected_K": mu,
        "std_K": sigma,
        "z": z,
        "p_value": p_value,
        "reject_h0_99pct": bool(abs(z) > 2.576) if not math.isnan(z) else False,
        "reject_h0_95pct": bool(abs(z) > 1.96) if not math.isnan(z) else False,
    }


def pairwise_analysis(
    failure_matrix: pd.DataFrame,
    T: int,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """
    Pairwise coincident-failure analysis.

    failure_matrix : DataFrame of shape (T, N) with bool values (True=failed)
    Returns a DataFrame with one row per pair.
    """
    versions = failure_matrix.columns.tolist()
    n = len(versions)
    pairs = []
    n_pairs = n * (n - 1) // 2
    bonferroni_alpha = alpha / n_pairs if n_pairs > 0 else alpha

    for i in range(n):
        for j in range(i + 1, n):
            vi, vj = versions[i], versions[j]
            pi = failure_matrix[vi].mean()
            pj = failure_matrix[vj].mean()
            expected = pi * pj * T
            observed = (failure_matrix[vi] & failure_matrix[vj]).sum()
            phi = _phi_correlation(failure_matrix[vi], failure_matrix[vj])

            # One-sided binomial test: P(X >= observed | T, pi*pj)
            p_independent = pi * pj
            if p_independent > 0 and p_independent < 1:
                binom_p = stats.binom.sf(observed - 1, T, p_independent)
            else:
                binom_p = float("nan")

            pairs.append({
                "version_i": vi,
                "version_j": vj,
                "p_i": pi,
                "p_j": pj,
                "expected_cofailures": expected,
                "observed_cofailures": int(observed),
                "ratio_obs_exp": (observed / expected) if expected > 0 else float("nan"),
                "phi_correlation": phi,
                "binomial_p": binom_p,
                "significant_bonferroni": (
                    bool(binom_p < bonferroni_alpha) if not math.isnan(binom_p) else False
                ),
                "bonferroni_alpha": bonferroni_alpha,
            })

    return pd.DataFrame(pairs)


def _phi_correlation(a: pd.Series, b: pd.Series) -> float:
    """Pearson phi (Matthews correlation) between two boolean series."""
    n = len(a)
    if n == 0:
        return float("nan")
    tp = (a & b).sum()
    tn = (~a & ~b).sum()
    fp = (~a & b).sum()
    fn = (a & ~b).sum()
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denom == 0:
        return float("nan")
    return (tp * tn - fp * fn) / denom


def _phi_from_contingency(n11: float, n10: float, n01: float, n00: float) -> float:
    """Matthews correlation from 2×2 counts (same labeling as ``_phi_correlation``)."""
    tp, fp, fn, tn = n11, n01, n10, n00
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    if denom == 0:
        return float("nan")
    return (tp * tn - fp * fn) / denom


def _parse_passed_cell(value: object) -> bool:
    s = str(value).strip().lower()
    return s in ("true", "1", "t", "yes")


def read_campaign_version_order(campaign_csv: Path) -> list[str]:
    """First campaign test block: ordered ``version_id`` list (one row per version)."""
    with campaign_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        first_tid: int | None = None
        out: list[str] = []
        for row in reader:
            tid = int(row["test_id"])
            if first_tid is None:
                first_tid = tid
            elif tid != first_tid:
                break
            out.append(row["version_id"])
        if not out:
            raise ValueError(f"empty or invalid campaign CSV: {campaign_csv}")
        return out


def load_api_unavailable_version_ids(index_json: Path) -> set[str]:
    """
    ``version_id`` values whose ``build_status`` is ``api_unavailable`` in
    ``versions/index.json`` next to a campaign (infrastructure / no runner).

    These are omitted from statistical analysis and generated reports entirely.
    """
    if not index_json.is_file():
        return set()
    raw = json.loads(index_json.read_text(encoding="utf-8"))
    rows = raw if isinstance(raw, list) else raw.get("versions", raw.get("admitted", []))
    return {
        str(r["version_id"])
        for r in rows
        if isinstance(r, dict) and r.get("build_status") == "api_unavailable"
    }


def analysis_version_ids(campaign_csv: Path, raw_order: list[str]) -> list[str]:
    """Campaign ``version_id`` order with infrastructure-only rows removed."""
    drop = load_api_unavailable_version_ids(campaign_csv.parent / "versions" / "index.json")
    out = [v for v in raw_order if v not in drop]
    if not out:
        raise ValueError(
            "After excluding versions with no usable build, no versions remain to analyze."
        )
    return out


def load_version_language_agent(
    campaign_csv: Path,
    versions: list[str],
) -> tuple[dict[str, str], dict[str, str]]:
    """
    Prefer ``versions_meta.json`` next to the campaign; else infer from CSV rows.
    """
    want = set(versions)
    lang: dict[str, str] = {}
    agent: dict[str, str] = {}
    meta_path = campaign_csv.parent / "versions_meta.json"
    if meta_path.is_file():
        raw = json.loads(meta_path.read_text(encoding="utf-8"))
        rows = raw if isinstance(raw, list) else raw.get("versions", raw.get("admitted", []))
        for x in rows:
            vid = x.get("version_id")
            if vid in want:
                lang[vid] = str(x.get("language", "python") or "python")
                agent[vid] = str(x.get("agent", "?") or "?")
    if len(lang) < len(want):
        with campaign_csv.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                vid = row["version_id"]
                if vid not in want:
                    continue
                if vid not in lang:
                    lang[vid] = (row.get("language") or "python").strip() or "python"
                    agent[vid] = (row.get("agent") or "?").strip() or "?"
                if len(lang) >= len(want):
                    break
    for v in versions:
        lang.setdefault(v, "python")
        agent.setdefault(v, "?")
    return lang, agent


def pairwise_dataframe_from_aggregates(
    pair_counts: np.ndarray,
    v_fail: np.ndarray,
    T: int,
    versions: list[str],
    *,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """Same rows as ``pairwise_analysis`` without building a T×N DataFrame."""
    n = len(versions)
    n_pairs = n * (n - 1) // 2
    bonferroni_alpha = alpha / n_pairs if n_pairs > 0 else alpha
    rows: list[dict] = []
    for i in range(n):
        for j in range(i + 1, n):
            vi, vj = versions[i], versions[j]
            observed = int(pair_counts[i, j])
            pi = float(v_fail[i]) / T
            pj = float(v_fail[j]) / T
            expected = pi * pj * T
            n11 = float(observed)
            n10 = float(v_fail[i]) - n11
            n01 = float(v_fail[j]) - n11
            n00 = float(T) - n11 - n10 - n01
            phi = _phi_from_contingency(n11, n10, n01, n00)
            p_independent = pi * pj
            if p_independent > 0 and p_independent < 1:
                binom_p = stats.binom.sf(observed - 1, T, p_independent)
            else:
                binom_p = float("nan")
            rows.append({
                "version_i": vi,
                "version_j": vj,
                "p_i": pi,
                "p_j": pj,
                "expected_cofailures": expected,
                "observed_cofailures": observed,
                "ratio_obs_exp": (observed / expected) if expected > 0 else float("nan"),
                "phi_correlation": phi,
                "binomial_p": binom_p,
                "significant_bonferroni": (
                    bool(binom_p < bonferroni_alpha) if not math.isnan(binom_p) else False
                ),
                "bonferroni_alpha": bonferroni_alpha,
            })
    return pd.DataFrame(rows)


def stream_campaign_aggregates(
    campaign_csv: Path,
    versions: list[str],
    lang_by_vid: dict[str, str],
) -> tuple[
    int,
    int,
    np.ndarray,
    np.ndarray,
    dict[str, int],
    dict[str, np.ndarray],
    dict[str, np.ndarray],
    dict[str, list[str]],
    list[str],
    list[tuple[int, np.ndarray]],
]:
    """
    Single pass over campaign CSV: O(1) RAM w.r.t. number of tests (only N×N counts).

    Also records each test with ≥1 failure as ``(test_id, counts)`` where ``counts[k]`` is the
    number of failed versions in ``langs[k]`` (for the stacked bar chart).

    Returns
    -------
    T, K_full, pair_full, v_fail_full,
    K_lang, pair_lang, vfail_lang, versions_per_lang,
    langs, failing_tests_by_language
    """
    N = len(versions)
    vid_to_i = {v: k for k, v in enumerate(versions)}
    langs = sorted({lang_by_vid.get(v, "python") for v in versions})
    lang_to_indices: dict[str, np.ndarray] = {}
    versions_per_lang: dict[str, list[str]] = {}
    for L in langs:
        ix = [i for i, v in enumerate(versions) if lang_by_vid.get(v, "python") == L]
        lang_to_indices[L] = np.array(ix, dtype=np.int64)
        versions_per_lang[L] = [versions[i] for i in ix]

    pair_full = np.zeros((N, N), dtype=np.int64)
    v_fail = np.zeros(N, dtype=np.int64)
    K_full = 0
    T_done = 0

    pair_lang = {L: np.zeros((len(lang_to_indices[L]), len(lang_to_indices[L])), dtype=np.int64) for L in langs}
    vfail_lang = {L: np.zeros(len(lang_to_indices[L]), dtype=np.int64) for L in langs}
    K_lang = {L: 0 for L in langs}

    fail_bits = np.zeros(N, dtype=np.uint8)
    buf_tid: int | None = None
    failing_tests_by_language: list[tuple[int, np.ndarray]] = []

    def flush_current_test() -> None:
        nonlocal K_full, T_done, pair_full, v_fail, pair_lang, vfail_lang, K_lang
        fl = fail_bits.astype(np.float64)
        if fl.sum() >= 2:
            K_full += 1
        pair_full += np.outer(fl, fl).astype(np.int64)
        v_fail += fl.astype(np.int64)
        T_done += 1
        for L in langs:
            ix = lang_to_indices[L]
            if ix.size == 0:
                continue
            sub = fl[ix]
            if sub.sum() >= 2:
                K_lang[L] += 1
            pair_lang[L] += np.outer(sub, sub).astype(np.int64)
            vfail_lang[L] += sub.astype(np.int64)
        if buf_tid is not None and int(fail_bits.sum()) >= 1:
            counts = np.zeros(len(langs), dtype=np.int64)
            for li, L in enumerate(langs):
                ix = lang_to_indices[L]
                if ix.size:
                    counts[li] = int(fail_bits[ix].sum())
            failing_tests_by_language.append((buf_tid, counts))

    with campaign_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vid = row["version_id"]
            if vid not in vid_to_i:
                # Row for a version dropped from analysis (e.g. no runner in index); skip.
                continue
            idx = vid_to_i[vid]
            tid = int(row["test_id"])
            failed = not _parse_passed_cell(row["passed"])

            if buf_tid is None:
                buf_tid = tid
            elif tid != buf_tid:
                flush_current_test()
                fail_bits.fill(0)
                buf_tid = tid

            fail_bits[idx] = 1 if failed else 0

        if buf_tid is not None:
            flush_current_test()

    failing_tests_by_language.sort(key=lambda x: x[0])
    return (
        T_done,
        K_full,
        pair_full,
        v_fail,
        K_lang,
        pair_lang,
        vfail_lang,
        versions_per_lang,
        langs,
        failing_tests_by_language,
    )


def plot_failures_by_language_stacked(
    langs: list[str],
    rows: list[tuple[int, np.ndarray]],
    output_path: Path,
    *,
    min_total_failures: int = 5,
) -> None:
    """
    Stacked bar chart: one bar per campaign test whose total failed-version count exceeds
    ``min_total_failures``; stacks = failure counts per language.
    """
    rows = [(tid, c) for tid, c in rows if int(c.sum()) > min_total_failures]
    if not rows:
        print(
            f"No tests with more than {min_total_failures} failures — "
            f"skipping stacked bar plot ({output_path})",
        )
        return

    lang_colors = {
        "python": "#4C72B0",
        "pascal": "#DD8452",
        "rust": "#55A868",
    }
    cmap = plt.get_cmap("tab10")

    n = len(rows)
    indices = np.arange(n, dtype=np.float64)
    test_ids = [t for t, _ in rows]
    bottom = np.zeros(n, dtype=np.float64)

    fig_w = float(min(48.0, max(10.0, n * 0.14)))
    fig, ax = plt.subplots(figsize=(fig_w, 6.0))

    for li, L in enumerate(langs):
        heights = np.array([float(c[li]) for _, c in rows], dtype=np.float64)
        if heights.sum() == 0:
            continue
        color = lang_colors.get(L.lower(), cmap(li % 10))
        ax.bar(
            indices,
            heights,
            bottom=bottom,
            label=L,
            color=color,
            edgecolor="white",
            linewidth=0.35,
        )
        bottom += heights

    ax.set_ylabel("Number of failed versions")
    ax.set_title(
        f"Failures per language for campaign tests with >{min_total_failures} failed versions "
        f"(n={n} tests, bars ordered by test_id)",
        fontsize=12,
    )
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(0, max(bottom.max() * 1.08, 1.0))
    ax.margins(x=0.01)

    if n <= 60:
        ax.set_xticks(indices)
        ax.set_xticklabels([str(t) for t in test_ids], rotation=90, ha="center", fontsize=max(5, min(9, 240 // max(n, 1))))
    elif n <= 200:
        step = max(1, n // 40)
        tick_pos = indices[::step]
        tick_lbl = [str(test_ids[i]) for i in range(0, n, step)]
        ax.set_xticks(tick_pos)
        ax.set_xticklabels(tick_lbl, rotation=90, ha="center", fontsize=7)
    else:
        ax.set_xticks([])
        ax.set_xlabel(
            f"Campaign tests with >{min_total_failures} failures "
            "(ordered by test_id; bar index 0…n−1)",
        )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Stacked failures-by-language plot saved: {output_path}")


def analyze_from_stream_aggregates(
    T: int,
    K: int,
    pair_counts: np.ndarray,
    v_fail: np.ndarray,
    versions: list[str],
    agent_by_vid: dict[str, str],
) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """Build the same outputs as ``analyze_campaign_core`` from streamed counts."""
    failure_rates = [float(v_fail[i]) / T for i in range(len(versions))]
    kl = kl_z_statistic(failure_rates, T, K)
    version_stats = pd.DataFrame({
        "version_id": versions,
        "agent": [agent_by_vid.get(v, "?") for v in versions],
        "total": T,
        "passed_count": T - v_fail,
    })
    version_stats["failure_rate"] = 1 - version_stats["passed_count"] / version_stats["total"]
    version_stats = version_stats.set_index("version_id")
    pairwise_df = pairwise_dataframe_from_aggregates(pair_counts, v_fail, T, versions)
    stats_dict = {
        "kl": kl,
        "version_stats": version_stats.reset_index().to_dict(orient="records"),
    }
    return stats_dict, version_stats, pairwise_df


def cross_language_matched_from_aggregates(
    pair_counts: np.ndarray,
    v_fail: np.ndarray,
    T: int,
    versions: list[str],
    lang_by_vid: dict[str, str],
    agent_by_vid: dict[str, str],
) -> pd.DataFrame:
    """Same logic as ``cross_language_matched_analysis`` without a full DataFrame pivot."""
    records: list[dict] = []
    for vid in versions:
        records.append({
            "version_id": vid,
            "language": lang_by_vid.get(vid, "python"),
            "agent": agent_by_vid.get(vid, "?"),
            "base_key": match_base_key(vid),
        })
    by_base: dict[str, list[int]] = defaultdict(list)
    for i, rec in enumerate(records):
        by_base[rec["base_key"]].append(i)

    rows: list[dict] = []
    for _bk, indices in by_base.items():
        if len(indices) < 2:
            continue
        for ii in range(len(indices)):
            for jj in range(ii + 1, len(indices)):
                i, j = indices[ii], indices[jj]
                if records[i]["language"] == records[j]["language"]:
                    continue
                vi, vj = versions[i], versions[j]
                observed = int(pair_counts[i, j])
                pi = float(v_fail[i]) / T
                pj = float(v_fail[j]) / T
                expected = pi * pj * T
                n11 = float(observed)
                n10 = float(v_fail[i]) - n11
                n01 = float(v_fail[j]) - n11
                n00 = float(T) - n11 - n10 - n01
                phi = _phi_from_contingency(n11, n10, n01, n00)
                p_independent = pi * pj
                if p_independent > 0 and p_independent < 1:
                    binom_p = stats.binom.sf(observed - 1, T, p_independent)
                else:
                    binom_p = float("nan")
                rows.append({
                    "base_key": records[i]["base_key"],
                    "version_i": vi,
                    "version_j": vj,
                    "language_i": records[i]["language"],
                    "language_j": records[j]["language"],
                    "agent": records[i]["agent"],
                    "p_i": pi,
                    "p_j": pj,
                    "expected_cofailures": expected,
                    "observed_cofailures": observed,
                    "ratio_obs_exp": (observed / expected) if expected > 0 else float("nan"),
                    "phi_correlation": phi,
                    "binomial_p": binom_p,
                })

    return pd.DataFrame(rows)


def cross_language_matched_analysis(df: pd.DataFrame, T: int) -> pd.DataFrame:
    """
    For each pair of versions that share ``match_base_key(version_id)`` but differ in
    ``language``, compute coincident-failure statistics (cross-language fault dependence).
    """
    df = df.copy()
    if "language" not in df.columns:
        df["language"] = "python"
    df["failed"] = ~df["passed"].astype(bool)

    meta = df[["version_id", "language", "agent"]].drop_duplicates()
    meta["base_key"] = meta["version_id"].map(match_base_key)

    rows: list[dict] = []
    for _, grp in meta.groupby("base_key"):
        if len(grp) < 2:
            continue
        vids = grp["version_id"].tolist()
        langs = grp["language"].tolist()
        agents = grp["agent"].tolist()
        for i in range(len(vids)):
            for j in range(i + 1, len(vids)):
                if langs[i] == langs[j]:
                    continue
                vi, vj = vids[i], vids[j]
                sub = df[df["version_id"].isin([vi, vj])].pivot_table(
                    index="test_id",
                    columns="version_id",
                    values="failed",
                    aggfunc="first",
                )
                if vi not in sub.columns or vj not in sub.columns:
                    continue
                a, b = sub[vi].astype(bool), sub[vj].astype(bool)
                pi, pj = float(a.mean()), float(b.mean())
                expected = pi * pj * T
                observed = int((a & b).sum())
                phi = _phi_correlation(a, b)
                p_independent = pi * pj
                if p_independent > 0 and p_independent < 1:
                    binom_p = stats.binom.sf(observed - 1, T, p_independent)
                else:
                    binom_p = float("nan")
                rows.append({
                    "base_key": grp["base_key"].iloc[0],
                    "version_i": vi,
                    "version_j": vj,
                    "language_i": langs[i],
                    "language_j": langs[j],
                    "agent": agents[i],
                    "p_i": pi,
                    "p_j": pj,
                    "expected_cofailures": expected,
                    "observed_cofailures": observed,
                    "ratio_obs_exp": (observed / expected) if expected > 0 else float("nan"),
                    "phi_correlation": phi,
                    "binomial_p": binom_p,
                })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def format_version_label(version_id: str) -> str:
    """
    Convert verbose version ids into a compact `agent-model` label for plots.
    """
    if "__m_" in version_id:
        agent, rest = version_id.split("__m_", 1)
        model = rest.split("__run", 1)[0]
        agent = agent.replace("_", "-")
        if agent == "claude-code":
            for prefix in (
                "anthropic_",
                "google_",
                "moonshot_",
                "openai_",
                "anthropic-",
                "google-",
                "moonshot-",
                "openai-",
            ):
                if model.startswith(prefix):
                    model = model[len(prefix):]
                    break
        model = re.sub(r"_+", "-", model).strip("-")
        return f"{agent}-{model}" if model else agent

    if "_run" in version_id:
        return version_id.rsplit("_run", 1)[0].replace("_", "-")

    return version_id.replace("_", "-")


def _heatmap_pdf_path(output_stem: Path, kind: str) -> Path:
    """``output_stem`` is a path without extension, e.g. ``.../failure_heatmap`` or ``.../failure_heatmap_rust``."""
    return output_stem.parent / f"{output_stem.name}_{kind}.pdf"


def _plot_single_pairwise_heatmap(
    mat: np.ndarray,
    labels: list[str],
    title: str,
    fmt: str,
    output_path: Path,
) -> None:
    """One square heatmap PDF; size scales with ``n`` so tick labels and cell values stay readable."""
    n = len(labels)
    if n == 0:
        return
    # Large square figure; cap max dimension so many-version runs stay usable (PDF size / render time).
    size_inches = float(min(26.0, max(18.0, n * 0.62)))
    fig, ax = plt.subplots(figsize=(size_inches, size_inches))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        im = ax.imshow(mat, cmap="YlOrRd", aspect="equal")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    tick_fs = max(8, min(13, 260 / max(n, 1)))
    ax.set_xticklabels(labels, fontsize=tick_fs, rotation=45, ha="right")
    ax.set_yticklabels(labels, fontsize=tick_fs)
    ax.set_title(title, fontsize=15, pad=16)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    # Cell annotations: shrink font with n; omit if too dense to stay legible
    ann_fs = max(6, min(11, 240 / max(n, 6)))
    show_cells = n <= 36
    if show_cells:
        for row_i in range(n):
            for col_j in range(n):
                val = mat[row_i, col_j]
                if not np.isnan(val):
                    ax.text(
                        col_j, row_i, f"{val:{fmt}}",
                        ha="center", va="center", fontsize=ann_fs, color="black",
                    )
    fig.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Heatmap saved: {output_path}")


def plot_failure_heatmaps(pairwise_df: pd.DataFrame, output_stem: Path) -> None:
    """
    Write three separate PDFs next to ``output_stem``:

    - ``{stem}_observed.pdf`` — observed co-failures
    - ``{stem}_expected.pdf`` — expected under independence
    - ``{stem}_phi.pdf`` — phi correlation
    """
    versions = sorted(set(
        list(pairwise_df["version_i"].unique()) +
        list(pairwise_df["version_j"].unique())
    ))
    n = len(versions)
    idx = {v: i for i, v in enumerate(versions)}

    obs_mat = np.full((n, n), np.nan)
    exp_mat = np.full((n, n), np.nan)
    phi_mat = np.full((n, n), np.nan)

    for _, row in pairwise_df.iterrows():
        i = idx[row["version_i"]]
        j = idx[row["version_j"]]
        obs_mat[i, j] = row["observed_cofailures"]
        obs_mat[j, i] = row["observed_cofailures"]
        exp_mat[i, j] = row["expected_cofailures"]
        exp_mat[j, i] = row["expected_cofailures"]
        phi_mat[i, j] = row["phi_correlation"]
        phi_mat[j, i] = row["phi_correlation"]

    labels = [format_version_label(v) for v in versions]
    prefix = "Pairwise failure analysis — "
    _plot_single_pairwise_heatmap(
        obs_mat, labels, prefix + "Observed co-failures", ".0f",
        _heatmap_pdf_path(output_stem, "observed"),
    )
    _plot_single_pairwise_heatmap(
        exp_mat, labels, prefix + "Expected co-failures (under independence)", ".1f",
        _heatmap_pdf_path(output_stem, "expected"),
    )
    _plot_single_pairwise_heatmap(
        phi_mat, labels, prefix + "Phi correlation", ".3f",
        _heatmap_pdf_path(output_stem, "phi"),
    )


def plot_failure_rates(version_stats: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(max(6, len(version_stats) * 0.8), 5))
    colors = {"mock": "#4C72B0", "cursor": "#DD8452", "claude_code": "#55A868", "codex": "#C44E52"}
    agents = version_stats.index.tolist()
    failure_rates = version_stats["failure_rate"].tolist()
    bar_colors = [
        colors.get(version_stats.loc[vid, "agent"], "#8172B2") for vid in agents
    ]

    bars = ax.bar(range(len(agents)), failure_rates, color=bar_colors, edgecolor="white", linewidth=0.5)
    ax.set_xticks(range(len(agents)))
    ax.set_xticklabels(
        [format_version_label(v) for v in agents],
        fontsize=8,
        rotation=45,
        ha="right",
    )
    ax.set_ylabel("Failure Rate")
    ax.set_title("Per-Version Failure Rates", fontsize=12)
    ax.set_ylim(0, max(failure_rates) * 1.2 + 0.01)
    for bar, rate in zip(bars, failure_rates):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{rate:.3f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Failure rates plot saved: {output_path}")


def plot_cross_language_phi(cx_df: pd.DataFrame, output_path: Path) -> None:
    """Bar chart of mean phi correlation per unordered language pair."""
    if cx_df.empty or "phi_correlation" not in cx_df.columns:
        return
    cx_df = cx_df.copy()
    pairs: list[str] = []
    for _, row in cx_df.iterrows():
        a, b = sorted([str(row["language_i"]), str(row["language_j"])])
        pairs.append(f"{a}–{b}")
    cx_df["lang_pair"] = pairs
    g = cx_df.groupby("lang_pair", sort=True)["phi_correlation"].mean()
    if len(g) == 0:
        return
    fig, ax = plt.subplots(figsize=(max(6, len(g) * 1.2), 5))
    g.plot(kind="bar", ax=ax, color="#6baed6", edgecolor="white")
    ax.set_ylabel("Mean phi (matched cross-language pairs)")
    ax.set_title("Cross-language fault dependence (matched agent/model/run)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Cross-language plot saved: {output_path}")


# ---------------------------------------------------------------------------
# Core analysis (reusable per language or full campaign)
# ---------------------------------------------------------------------------

def analyze_campaign_core(df: pd.DataFrame) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """Return (stats_dict with kl + version_stats, version_stats indexed, pairwise_df)."""
    T = df["test_id"].nunique()
    versions = df["version_id"].unique().tolist()
    failure_matrix = df.pivot_table(
        index="test_id", columns="version_id", values="passed", aggfunc="first"
    )
    failure_matrix = ~failure_matrix.astype(bool)
    version_stats = df.groupby(["version_id", "agent"])["passed"].agg(
        total="count", passed_count="sum"
    ).reset_index()
    version_stats["failure_rate"] = 1 - version_stats["passed_count"] / version_stats["total"]
    version_stats = version_stats.set_index("version_id")
    simultaneous_fail = failure_matrix.sum(axis=1)
    K = (simultaneous_fail >= 2).sum()
    failure_rates = [version_stats.loc[v, "failure_rate"] for v in versions]
    kl = kl_z_statistic(failure_rates, T, K)
    pairwise_df = pairwise_analysis(failure_matrix.astype(float) > 0.5, T)
    stats_dict = {
        "kl": kl,
        "version_stats": version_stats.reset_index().to_dict(orient="records"),
    }
    return stats_dict, version_stats, pairwise_df


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    stats_dict: dict,
    version_stats: pd.DataFrame,
    pairwise_df: pd.DataFrame,
    output_path: str,
    *,
    title_suffix: str = "",
    extra_sections: list[str] | None = None,
) -> None:
    kl = stats_dict["kl"]
    T = kl["T"]
    K = kl["K_observed"]
    z = kl["z"]
    p_val = kl["p_value"]
    reject = kl["reject_h0_99pct"]

    suf = f" ({title_suffix})" if title_suffix else ""
    lines = [
        f"# NVP AI Agent Fault-Independence Experiment — Results{suf}",
        "",
        "## Pilot Summary",
        "",
        f"- **Benchmark**: Launch Interceptor Program (Knight & Leveson 1986)",
        f"- **Admitted versions**: {kl['n_versions']}",
        f"- **Campaign test cases**: {T}",
        f"- **Observed simultaneous failures (K)**: {K}",
        f"- **Expected under independence (μ)**: {kl['expected_K']:.2f}",
        f"- **K&L z-statistic**: {z:.4f}" if not math.isnan(z) else "- **K&L z-statistic**: N/A",
        f"- **p-value**: {p_val:.4e}" if not math.isnan(p_val) else "- **p-value**: N/A",
        f"- **Reject H0 at 99% (|z|>2.576)**: {'YES' if reject else 'NO'}",
        "",
    ]

    if kl.get("error"):
        lines += [f"> **Warning**: {kl['error']}", ""]

    lines += [
        "## Per-Version Failure Rates",
        "",
        "| Version | Agent | Total Tests | Failures | Failure Rate |",
        "|---------|-------|-------------|----------|--------------|",
    ]
    for vid, row in version_stats.iterrows():
        lines.append(
            f"| {vid} | {row.get('agent', '?')} | {int(row['total'])} | "
            f"{int(row['total'] - row['passed_count'])} | {row['failure_rate']:.4f} |"
        )

    lines += [
        "",
        "## Pairwise Co-failure Analysis",
        "",
        "| Version i | Version j | Observed | Expected | Ratio | Phi | Binomial p | Sig? |",
        "|-----------|-----------|----------|----------|-------|-----|------------|------|",
    ]
    for _, row in pairwise_df.iterrows():
        ratio = f"{row['ratio_obs_exp']:.2f}" if not math.isnan(row["ratio_obs_exp"]) else "N/A"
        phi = f"{row['phi_correlation']:.4f}" if not math.isnan(row["phi_correlation"]) else "N/A"
        bp = f"{row['binomial_p']:.3e}" if not math.isnan(row["binomial_p"]) else "N/A"
        sig = "**YES**" if row["significant_bonferroni"] else "no"
        lines.append(
            f"| {row['version_i']} | {row['version_j']} | "
            f"{int(row['observed_cofailures'])} | {row['expected_cofailures']:.2f} | "
            f"{ratio} | {phi} | {bp} | {sig} |"
        )

    lines += [
        "",
        f"> Bonferroni-corrected α = {pairwise_df['bonferroni_alpha'].iloc[0]:.4f}" if len(pairwise_df) > 0 else "",
        "",
        "## Statistical Methodology",
        "",
        "Following Knight & Leveson (1986) exactly:",
        "",
        "```",
        "P_0 = ∏(1 - p_i)",
        "P_1 = Σ p_i · ∏_{j≠i}(1 - p_j)",
        "P_m = 1 - P_0 - P_1",
        f"μ = T · P_m = {T} · {kl['P_m']:.6f} = {kl['expected_K']:.2f}",
        f"z = (K - μ) / σ = ({K} - {kl['expected_K']:.2f}) / {kl['std_K']:.4f} = {z:.4f}" if not math.isnan(z) else "z = N/A",
        "```",
        "",
        "## Interpretation",
        "",
    ]

    if kl.get("n_versions", 0) < 2:
        lines.append("> Not enough admitted versions to compute the z-statistic.")
    elif math.isnan(z):
        lines.append("> z-statistic could not be computed (insufficient variance).")
    elif reject:
        lines.append(
            f"> **H0 rejected** at 99% confidence (z={z:.2f}). "
            "The observed coincident failures significantly exceed what independence would predict. "
            "This is consistent with the original Knight & Leveson finding for human programmers."
        )
    else:
        lines.append(
            f"> **H0 not rejected** at 99% confidence (z={z:.2f}, |z| < 2.576). "
            "The observed coincident failures are consistent with independent failures."
        )

    if extra_sections:
        lines.append("")
        lines.extend(extra_sections)

    lines += [
        "",
        "## Caveats",
        "",
        "- If this run used mock agents only, these results **validate the framework infrastructure**, "
          "not empirical claims about real AI coding agent behavior.",
        "- Real-agent runs require API keys (ANTHROPIC_API_KEY, CURSOR_API_KEY, CODEX_API_KEY).",
        "- Campaign size (1,000) is much smaller than K&L (1,000,000); statistical power is limited.",
        "- See `docs/experiment_design.md` for full discussion of confounders and threats to validity.",
        "",
        "## Files",
        "",
        "| File | Description |",
        "|------|-------------|",
        "| `results/pilot/campaign.csv` | Raw pass/fail matrix (test × version) |",
        "| `results/pilot/stats.json` | Full statistics in machine-readable format |",
        "| `results/pilot/summary_table.csv` | Per-version summary |",
        "| `results/pilot/failure_heatmap_{observed,expected,phi}.pdf` | Pairwise matrices (3 PDFs) |",
        "| `results/pilot/failure_rates.pdf` | Per-version failure rate bar chart |",
        "| `results/pilot/failures_by_language_stacked.pdf` | Stacked bars: tests with >20 failures × counts per language |",
        "",
        "## Reference",
        "",
        "Knight, J. C. & Leveson, N. G. (1986). An experimental evaluation of the assumption of "
        "independence in multiversion programming. *IEEE Transactions on Software Engineering*, 12(1), 96–109.",
    ]

    Path(output_path).write_text("\n".join(lines))
    print(f"Report written: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(
    campaign_csv: str,
    output_dir: str,
    report_path: str,
    *,
    cross_language: bool = True,
) -> None:
    campaign_path = Path(campaign_csv)
    versions = analysis_version_ids(
        campaign_path,
        read_campaign_version_order(campaign_path),
    )
    lang_by_vid, agent_by_vid = load_version_language_agent(campaign_path, versions)

    (
        T,
        K_full,
        pair_full,
        v_fail_full,
        K_lang,
        pair_lang,
        vfail_lang,
        versions_per_lang,
        langs,
        failing_tests_by_language,
    ) = stream_campaign_aggregates(campaign_path, versions, lang_by_vid)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print(f"Campaign: {T} tests × {len(versions)} versions; languages={langs}")

    # Pooled (all versions) — backward-compatible stats.json (streaming; O(N²) RAM, not O(T·N))
    stats_dict, version_stats, pairwise_df = analyze_from_stream_aggregates(
        T, K_full, pair_full, v_fail_full, versions, agent_by_vid,
    )
    K = stats_dict["kl"]["K_observed"]
    print(f"K (simultaneous failures, all versions): {K}")
    print(
        f"K&L z = {stats_dict['kl']['z']:.4f}  P_m = {stats_dict['kl']['P_m']:.6f} "
        f"expected_K = {stats_dict['kl']['expected_K']:.2f}"
    )

    (out / "stats.json").write_text(json.dumps(stats_dict, indent=2, default=str))
    version_stats.reset_index().to_csv(out / "summary_table.csv", index=False)
    if len(pairwise_df) > 0:
        pairwise_df.to_csv(out / "pairwise_table.csv", index=False)
        plot_failure_heatmaps(pairwise_df, out / "failure_heatmap")
    plot_failure_rates(version_stats, out / "failure_rates.pdf")

    plot_failures_by_language_stacked(
        langs, failing_tests_by_language, out / "failures_by_language_stacked.pdf",
    )

    extra: list[str] = []
    for lang in langs:
        v_sub = versions_per_lang.get(lang, [])
        if len(v_sub) < 1:
            continue
        pc = pair_lang[lang]
        vf = vfail_lang[lang]
        ag_sub = {v: agent_by_vid.get(v, "?") for v in v_sub}
        st_l, vs_l, pw_l = analyze_from_stream_aggregates(
            T, K_lang[lang], pc, vf, v_sub, ag_sub,
        )
        (out / f"stats_{lang}.json").write_text(json.dumps(st_l, indent=2, default=str))
        vs_l.reset_index().to_csv(out / f"summary_table_{lang}.csv", index=False)
        if len(pw_l) > 0:
            pw_l.to_csv(out / f"pairwise_table_{lang}.csv", index=False)
            plot_failure_heatmaps(pw_l, out / f"failure_heatmap_{lang}")
        plot_failure_rates(vs_l, out / f"failure_rates_{lang}.pdf")
        print(
            f"  [{lang}] z={st_l['kl']['z']:.4f}  K={st_l['kl']['K_observed']}  "
            f"versions={st_l['kl'].get('n_versions', 0)}"
        )

    cx_df = pd.DataFrame()
    if cross_language and len(langs) >= 2:
        cx_df = cross_language_matched_from_aggregates(
            pair_full, v_fail_full, T, versions, lang_by_vid, agent_by_vid,
        )
        if len(cx_df) > 0:
            cx_df.to_csv(out / "cross_language_pairwise.csv", index=False)
            gmean = cx_df.groupby(
                [cx_df["language_i"].astype(str), cx_df["language_j"].astype(str)],
                as_index=False,
            )["phi_correlation"].mean()
            pairs_by_lang = {
                f"{row['language_i']}|{row['language_j']}": float(row["phi_correlation"])
                for _, row in gmean.iterrows()
            }
            summary = {
                "n_matched_pairs": len(cx_df),
                "mean_phi": float(cx_df["phi_correlation"].mean()),
                "pairs_by_lang": pairs_by_lang,
            }
            (out / "cross_language_stats.json").write_text(json.dumps(summary, indent=2, default=str))
            plot_cross_language_phi(cx_df, out / "cross_language_phi.pdf")
            extra = [
                "## Cross-Language Fault Dependence (matched pairs)",
                "",
                "Pairs are versions with the same agent/model/run but different `language` "
                "(see `match_base_key` in `analysis/analyze_results.py`).",
                "",
                f"- **Matched pairs analyzed**: {len(cx_df)}",
                f"- **Mean phi**: {cx_df['phi_correlation'].mean():.4f}",
                "",
                "| version_i (lang) | version_j (lang) | Observed co-fails | Expected | Phi |",
                "|-------------------|------------------|---------------------|----------|-----|",
            ]
            for _, row in cx_df.head(40).iterrows():
                extra.append(
                    f"| {row['version_i']} ({row['language_i']}) | {row['version_j']} ({row['language_j']}) | "
                    f"{int(row['observed_cofailures'])} | {row['expected_cofailures']:.2f} | "
                    f"{row['phi_correlation']:.4f} |"
                )
            if len(cx_df) > 40:
                extra.append(f"| … | … | ({len(cx_df) - 40} more rows in cross_language_pairwise.csv) | | |")
            extra.append("")

    generate_report(
        stats_dict,
        version_stats,
        pairwise_df,
        report_path,
        extra_sections=extra if extra else None,
    )
    print(f"\nAnalysis complete. Output in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze campaign results")
    parser.add_argument("--campaign", required=True, help="campaign.csv from run_campaign")
    parser.add_argument("--output", required=True, help="Output directory for plots and stats")
    parser.add_argument("--report", default="report.md", help="Path for Markdown report")
    parser.add_argument(
        "--no-cross-language",
        action="store_true",
        help="Skip matched cross-language pairwise analysis",
    )
    args = parser.parse_args()
    run(args.campaign, args.output, args.report, cross_language=not args.no_cross_language)


if __name__ == "__main__":
    main()
