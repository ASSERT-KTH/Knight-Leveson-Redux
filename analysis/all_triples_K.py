"""
Enumerate all C(59,3) = 32,509 triples and compute oracle-aware unit failure
count K for each (majority-vote NVP with N=3).

For each triple (A, B, C):
    K = |{tests where ≥2 members fail}|
      = |A∩B| + |A∩C| + |B∩C| − 2·|A∩B∩C|   (inclusion-exclusion)

Statistics reported:
  · K distribution: min/max/median/mean/percentiles
  · How many triples achieve K = 0
  · K vs min/max individual member failure count
  · "beats best member": triples where K < min(K_A, K_B, K_C)
  · Best and worst 20 triples by K
  · **Full pool** (all versions) and **trimmed pool** (excluding 0-fail and
    very high-fail outliers; see ``--mega-threshold``)

Outputs (in --output dir):
  all_triples_K.npz                 full pool: compressed K array
  all_triples_K_trimmed.npz         trimmed pool (after exclusions)
  all_triples_K_stats.md            full + trimmed markdown summary
  all_triples_K_dist.pdf            full pool: histogram + scatter
  all_triples_K_cdf.pdf             full pool: ECDF single-version K vs triple K
  all_triples_K_dist_trimmed.pdf    trimmed pool plots

Trimmed pool (second analysis) excludes versions with zero oracle failures and
versions with failure count ≥ ``--mega-threshold`` (default 10_000).

Usage:
    python -m analysis.all_triples_K \\
        --campaign results/main-spec-3 \\
        --output   results/main-spec-3
"""
from __future__ import annotations

import argparse
import itertools
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.build_n_version_units import load_failure_sets  # noqa: E402
from analysis.analyze_results import (                          # noqa: E402
    analysis_version_ids,
    format_version_label,
    read_campaign_version_order,
)


DEFAULT_MEGA_FAIL_THRESHOLD = 10_000


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def load_arrays(campaign_dir: Path) -> tuple[list[str], list[np.ndarray], int]:
    """Return (versions, fail_arrays, T)."""
    versions = analysis_version_ids(
        campaign_dir,
        read_campaign_version_order(campaign_dir / "campaign.csv"),
    )
    T, fail_sets = load_failure_sets(
        campaign_dir / "campaign.csv",
        versions,
        cache_path=campaign_dir / "failure_sets.npz",
    )
    fail_arrays = [fail_sets[v] for v in versions]
    return versions, fail_arrays, T


def compute_all_K(fail_arrays: list[np.ndarray]) -> np.ndarray:
    """
    Enumerate all C(V,3) triples and return a 1-D int32 array of K values,
    indexed by triple index in lexicographic order.
    """
    V = len(fail_arrays)
    N = V * (V - 1) * (V - 2) // 6   # C(V, 3)
    K_all = np.empty(N, dtype=np.int32)

    t0 = time.time()
    report_every = max(1, N // 20)

    for idx, (a, b, c) in enumerate(itertools.combinations(range(V), 3)):
        ab  = np.intersect1d(fail_arrays[a], fail_arrays[b], assume_unique=True)
        ac  = np.intersect1d(fail_arrays[a], fail_arrays[c], assume_unique=True)
        bc  = np.intersect1d(fail_arrays[b], fail_arrays[c], assume_unique=True)
        abc = np.intersect1d(ab, fail_arrays[c],             assume_unique=True)
        K_all[idx] = len(ab) + len(ac) + len(bc) - 2 * len(abc)

        if (idx + 1) % report_every == 0:
            pct = (idx + 1) / N * 100
            elapsed = time.time() - t0
            eta = elapsed / (idx + 1) * (N - idx - 1)
            print(f"  {idx+1:6d}/{N}  ({pct:4.1f}%)  elapsed {elapsed:.1f}s  ETA {eta:.0f}s",
                  flush=True)

    print(f"  Done in {time.time()-t0:.1f}s", flush=True)
    return K_all


def triple_index_to_ids(idx: int, V: int) -> tuple[int, int, int]:
    """Convert a linear triple index back to (a, b, c) with a<b<c."""
    for pos, (a, b, c) in enumerate(itertools.combinations(range(V), 3)):
        if pos == idx:
            return a, b, c
    raise ValueError(f"Index {idx} out of range for V={V}")


# ---------------------------------------------------------------------------
# Stats + report
# ---------------------------------------------------------------------------

def _row_stat(
    label: str,
    single_v: float | int,
    triple_v: float | int,
    *,
    single_pct_T: float | None = None,
    triple_pct_T: float | None = None,
) -> str:
    """One markdown table row: statistic vs single-version value vs triple value."""

    def s_cell(v: float | int, pct: float | None) -> str:
        if pct is not None:
            xv = float(np.asarray(v))
            return f"{int(round(xv)):,} ({float(pct) * 100:.4f}% of T)"
        x = float(np.asarray(v))
        if abs(x - round(x)) < 1e-9:
            return f"{int(round(x)):,}"
        return f"{x:.2f}"

    return (
        f"| {label} | {s_cell(single_v, single_pct_T)} | "
        f"{s_cell(triple_v, triple_pct_T)} |"
    )


def pool_report_markdown(
    K_all: np.ndarray,
    fail_counts: np.ndarray,
    versions: list[str],
    T: int,
    *,
    section_title: str,
    pool_preamble: list[str],
) -> tuple[list[str], np.ndarray, int, int, int, list[int], np.ndarray]:
    """
    Return (markdown lines, K_min_member, beats_best, zero_K, worse_than_best,
            pcts, vals_triple).
    """
    V = len(fail_counts)
    N = len(K_all)
    singles = fail_counts.astype(np.float64)

    K_min_member = np.empty(N, dtype=np.int32)
    K_max_member = np.empty(N, dtype=np.int32)
    for idx, (a, b, c) in enumerate(itertools.combinations(range(V), 3)):
        K_min_member[idx] = min(fail_counts[a], fail_counts[b], fail_counts[c])
        K_max_member[idx] = max(fail_counts[a], fail_counts[b], fail_counts[c])

    beats_best = int(np.sum(K_all < K_min_member))
    beats_worst = int(np.sum(K_all < K_max_member))
    zero_K = int(np.sum(K_all == 0))
    worse_than_best = int(np.sum(K_all > K_min_member))

    pcts = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]
    vals_triple = np.percentile(K_all, pcts)
    vals_single = np.percentile(singles, pcts)

    zero_single = int(np.sum(singles == 0))
    zero_triple = zero_K

    lines: list[str] = [
        section_title,
        "",
        *pool_preamble,
        f"- Versions in pool: **{V}**",
        f"- Triples C({V}, 3): **{N:,}**",
        f"- T (test cases): {T:,}",
        "",
        "### Single-version failure counts vs triple unit K",
        "",
        "Oracle-aware failure count: per version, number of tests where output disagrees "
        "with the oracle; per triple (N=3), *K* is the number of tests where at least "
        "two members fail (majority is wrong). "
        "Rows **P0**–**P100** are empirical percentiles over the *n* single-version counts "
        "and over the *n* triple *K* values, respectively (same labels as numpy `percentile`).",
        "",
        "| Statistic | Single versions (n = {:d}) | All triples (n = {:,}) |".format(V, N),
        "|---|---:|---:|",
        _row_stat("Min", singles.min(), K_all.min(), single_pct_T=singles.min() / T, triple_pct_T=K_all.min() / T),
        _row_stat("Max", singles.max(), K_all.max(), single_pct_T=singles.max() / T, triple_pct_T=K_all.max() / T),
        "| Mean | {:.2f} ({:.4f}% of T) | {:.2f} ({:.4f}% of T) |".format(
            float(singles.mean()),
            float(singles.mean()) / T * 100,
            float(K_all.mean()),
            float(K_all.mean()) / T * 100,
        ),
        _row_stat("Std dev", singles.std(), K_all.std()),
        _row_stat("With K = 0 (count)", zero_single, zero_triple),
        "| With K = 0 (% of row population) | {:.2f}% | {:.2f}% |".format(
            100.0 * zero_single / V,
            100.0 * zero_triple / N,
        ),
        "| Unique K values | {:,} | {:,} |".format(
            int(len(np.unique(singles))),
            int(len(np.unique(K_all))),
        ),
    ]
    for p, vs, vt in zip(pcts, vals_single, vals_triple):
        lines.append(
            _row_stat(f"P{p}", vs, vt, single_pct_T=float(vs) / T, triple_pct_T=float(vt) / T)
        )

    svals, scounts = np.unique(fail_counts, return_counts=True)
    lines += [
        "",
        "#### Single-version failure counts (unique values)",
        "",
        "| K | # versions | % of versions | K / T (%) |",
        "|---:|---:|---:|---:|",
    ]
    for v, c in zip(svals, scounts):
        lines.append(f"| {int(v):,} | {c:,} | {c/V*100:.2f}% | {v/T*100:.4f}% |")

    lines += [
        "",
        "### Comparison to individual members (within each triple)",
        "",
        f"- Triples with K = 0:  **{zero_K:,}**  ({zero_K/N*100:.2f}% of all triples)",
        f"- K < min(member K)  — unit beats its best member:   **{beats_best:,}**  ({beats_best/N*100:.1f}%)",
        f"- K > min(member K)  — unit worse than best member:  **{worse_than_best:,}**  ({worse_than_best/N*100:.1f}%)",
        f"- K < max(member K)  — unit beats its worst member:  **{beats_worst:,}**  ({beats_worst/N*100:.1f}%)",
        "",
        "### Individual version K (pool)",
        "",
        "| Version | K | K/T (%) |",
        "|---|---:|---:|",
    ]
    for vi, v in enumerate(versions):
        k = int(fail_counts[vi])
        lines.append(f"| `{format_version_label(v)}` | {k:,} | {k/T*100:.4f}% |")

    lines += [
        "",
        "### Best 20 triples (lowest K)",
        "",
        "| Rank | K | K/T (%) | Members |",
        "|---:|---:|---:|---|",
    ]
    order = np.argsort(K_all)
    for rank, idx in enumerate(order[:20]):
        a, b, c = triple_index_to_ids(int(idx), V)
        k = int(K_all[idx])
        lA = format_version_label(versions[a])
        lB = format_version_label(versions[b])
        lC = format_version_label(versions[c])
        lines.append(f"| {rank+1} | {k:,} | {k/T*100:.4f}% | `{lA}` · `{lB}` · `{lC}` |")

    lines += [
        "",
        "### Worst 20 triples (highest K)",
        "",
        "| Rank | K | K/T (%) | Members |",
        "|---:|---:|---:|---|",
    ]
    for rank, idx in enumerate(order[-20:][::-1]):
        a, b, c = triple_index_to_ids(int(idx), V)
        k = int(K_all[idx])
        lA = format_version_label(versions[a])
        lB = format_version_label(versions[b])
        lC = format_version_label(versions[c])
        lines.append(f"| {rank+1} | {k:,} | {k/T*100:.4f}% | `{lA}` · `{lB}` · `{lC}` |")

    uvals, ucounts = np.unique(K_all, return_counts=True)
    lines += [
        "",
        "### K value breakdown (all unique values)",
        "",
        "| K | # triples | % of total | K / T (%) |",
        "|---:|---:|---:|---:|",
    ]
    for v, c in zip(uvals, ucounts):
        lines.append(f"| {int(v):,} | {c:,} | {c/N*100:.2f}% | {v/T*100:.4f}% |")

    return lines, K_min_member, beats_best, zero_K, worse_than_best, pcts, vals_triple


def print_pool_summary(
    label: str,
    K_all: np.ndarray,
    singles: np.ndarray,
    *,
    V: int,
    N: int,
    T: int,
    pcts: list[int],
    vals_triple: np.ndarray,
    zero_K: int,
    beats_best: int,
    worse_than_best: int,
) -> None:
    zero_single = int(np.sum(singles == 0))
    print()
    print(f"=== {label} ===")
    print(f"  Single: min={int(singles.min())}, med={int(np.median(singles))}, "
          f"mean={singles.mean():.1f}, max={int(singles.max())}, K=0: {zero_single}/{V}")
    print(f"  Triple: min={int(K_all.min())}, med={int(np.median(K_all))}, "
          f"mean={K_all.mean():.1f}, max={int(K_all.max())}, K=0: {int(zero_K)}/{N}")
    print()
    print(f"  Percentiles (triples), C({V},3)={N:,}:")
    for p, v in zip(pcts, vals_triple):
        print(f"  {p:3d}th pct: {int(v):7,}  ({v/T*100:.4f}%)")
    print(f"  Mean:       {K_all.mean():7.1f}")
    print()
    print(f"  K = 0 triples:      {zero_K:6,}  ({zero_K/N*100:.2f}%)")
    print(f"  beats best member:  {beats_best:6,}  ({beats_best/N*100:.1f}%)")
    print(f"  worse than best:    {worse_than_best:6,}  ({worse_than_best/N*100:.1f}%)")


def write_pool_plots(
    K_all: np.ndarray,
    K_min_member: np.ndarray,
    *,
    V: int,
    N: int,
    beats_best: int,
    plot_path: Path,
    title_suffix: str = "",
) -> None:
    uvals, ucounts = np.unique(K_all, return_counts=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))

    ax = axes[0]
    colors = ["#1f77b4" if v <= 10 else "#ff7f0e" if v <= 450 else "#d62728"
              for v in uvals]
    ax.bar(range(len(uvals)), ucounts, color=colors, edgecolor="none", alpha=0.85)
    ax.set_xticks(range(len(uvals)))
    ax.set_xticklabels([f"{int(v):,}" for v in uvals], rotation=55, ha="right", fontsize=8)
    ax.set_yscale("log")
    ax.set_xlabel("Unit failure count K", fontsize=10)
    ax.set_ylabel("# triples (log scale)", fontsize=10)
    ts = f" ({title_suffix})" if title_suffix else ""
    ax.set_title(f"K distribution — C({V},3)={N:,} triples{ts}\n({len(uvals)} unique K)", fontsize=10)
    legend_els = [Patch(color="#1f77b4", label="K ≤ 10  (near-perfect)"),
                  Patch(color="#ff7f0e", label="K 11–450  (LIC-10 mode)"),
                  Patch(color="#d62728", label="K > 450  (catastrophic)")]
    ax.legend(handles=legend_els, fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    rng = np.random.default_rng(42)
    n_plot = min(N, 6000)
    idx_sample = rng.choice(N, size=n_plot, replace=False)
    kp = K_all[idx_sample].astype(float)
    kminp = K_min_member[idx_sample].astype(float)
    jitter = rng.uniform(-0.015, 0.015, size=n_plot)
    kp_j = kp * (1 + jitter)
    kminp_j = kminp * (1 + jitter)
    beats_mask = K_all[idx_sample] < K_min_member[idx_sample]
    ax.scatter(kminp_j[~beats_mask], kp_j[~beats_mask],
               s=4, alpha=0.25, color="#aaaaaa", rasterized=True, label="K ≥ best member")
    ax.scatter(kminp_j[beats_mask], kp_j[beats_mask],
               s=6, alpha=0.6, color="#d62728", rasterized=True,
               label=f"K < best member ({beats_best:,})")
    lim = max(float(K_all.max()), float(K_min_member.max())) * 1.05
    ax.plot([0, lim], [0, lim], "k--", linewidth=0.8, alpha=0.5)
    ax.set_xscale("symlog", linthresh=3)
    ax.set_yscale("symlog", linthresh=3)
    ax.set_xlabel("min(K_A, K_B, K_C) — best individual member", fontsize=10)
    ax.set_ylabel("K — unit (majority vote)", fontsize=10)
    ax.set_title("Unit K vs best member K", fontsize=10)
    ax.legend(fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(plot_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Wrote {plot_path}")


def write_full_pool_cdf_plot(
    fail_counts: np.ndarray,
    K_all: np.ndarray,
    *,
    T: int,
    plot_path: Path,
) -> None:
    """
    Empirical CDF of per-version oracle failure counts vs. empirical CDF of
    majority-vote unit failure counts K over all triples (full pool only).
    """
    singles = np.sort(fail_counts.astype(np.float64))
    triples = np.sort(K_all.astype(np.float64))
    n_s = singles.size
    n_t = triples.size
    y_s = np.arange(1, n_s + 1, dtype=np.float64) / n_s
    y_t = np.arange(1, n_t + 1, dtype=np.float64) / n_t

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.step(
        singles,
        y_s,
        where="post",
        color="#1f77b4",
        linewidth=1.8,
        label=f"Single version (n = {n_s})",
    )
    ax.step(
        triples,
        y_t,
        where="post",
        color="#ff7f0e",
        linewidth=1.8,
        alpha=0.92,
        label=f"3-version unit, all triples (n = {n_t:,})",
    )
    ax.set_xlabel(f"Oracle failures K (of {T:,} tests)", fontsize=11)
    ax.set_ylabel("Cumulative fraction", fontsize=11)
    ax.set_title(
        "Empirical CDF: single-version vs 3-version unit (full pool)",
        fontsize=11,
    )
    ax.set_xscale("symlog", linthresh=10, base=10)
    ax.set_ylim(0.0, 1.01)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="lower right", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plot_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Wrote {plot_path}")


def _trim_pool_preamble(
    versions: list[str],
    fail_counts: np.ndarray,
    *,
    mega_threshold: int,
) -> tuple[list[str], list[str], np.ndarray]:
    """
    Exclude versions with K=0 or K >= mega_threshold.
    Return (preamble_md_lines, versions_kept, fail_counts_kept).
    """
    zero_idx = np.flatnonzero(fail_counts == 0)
    mega_idx = np.flatnonzero(fail_counts >= mega_threshold)
    keep = np.ones(len(versions), dtype=bool)
    keep[zero_idx] = False
    keep[mega_idx] = False
    idx = np.flatnonzero(keep)

    prem: list[str] = [
        f"**Exclusion rule:** drop versions with **zero** oracle failures and "
        f"versions with **K ≥ {mega_threshold:,}**.",
        "",
    ]

    def _table(title: str, indices: np.ndarray) -> None:
        prem.append(f"#### {title}")
        prem.append("")
        prem.append("| Version | K |")
        prem.append("|---|---:|")
        for i in indices:
            prem.append(
                f"| `{format_version_label(versions[int(i)])}` | "
                f"{int(fail_counts[int(i)]):,} |"
            )
        prem.append("")

    _table("Excluded: zero oracle failures", zero_idx)
    _table(f"Excluded: K ≥ {mega_threshold:,}", mega_idx)

    prem.append(f"**Remaining versions:** **{len(idx)}**")
    prem.append("")

    v2 = [versions[int(i)] for i in idx]
    fc2 = fail_counts[idx].copy()
    return prem, v2, fc2


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--campaign", type=Path, default=Path("results/main-spec-3"))
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--cache", type=Path, default=None)
    p.add_argument(
        "--mega-threshold",
        type=int,
        default=DEFAULT_MEGA_FAIL_THRESHOLD,
        help="Exclude single versions with failure count >= this (default: %(default)s).",
    )
    args = p.parse_args()

    campaign_dir = args.campaign.resolve()
    output_dir = (args.output or campaign_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    mega_thr = int(args.mega_threshold)

    print("Loading failure sets …")
    versions, fail_arrays, T = load_arrays(campaign_dir)
    V = len(versions)
    fail_counts = np.array([len(fa) for fa in fail_arrays], dtype=np.int64)
    N = V * (V - 1) * (V - 2) // 6
    print(f"  {V} versions, T={T:,}, C({V},3)={N:,} triples")
    print()

    cache_path = args.cache or (output_dir / "all_triples_K.npz")
    if cache_path.exists():
        print(f"Loading cached K values from {cache_path} …")
        cached = np.load(cache_path)
        K_all = cached["K_all"]
        print(f"  Loaded {len(K_all):,} K values")
    else:
        print(f"Computing K for all {N:,} triples …")
        K_all = compute_all_K(fail_arrays)
        np.savez_compressed(cache_path, K_all=K_all, versions=versions, T=T)
        print(f"Saved cache to {cache_path}")

    print()
    print("Building reports …")
    lines_full, Kmin_f, bb_f, zk_f, wtb_f, pcts, vt_f = pool_report_markdown(
        K_all,
        fail_counts,
        versions,
        T,
        section_title="## Full pool (all campaign versions)",
        pool_preamble=[],
    )
    print_pool_summary(
        "Full pool",
        K_all,
        fail_counts.astype(float),
        V=V,
        N=N,
        T=T,
        pcts=pcts,
        vals_triple=vt_f,
        zero_K=zk_f,
        beats_best=bb_f,
        worse_than_best=wtb_f,
    )
    write_pool_plots(
        K_all,
        Kmin_f,
        V=V,
        N=N,
        beats_best=bb_f,
        plot_path=output_dir / "all_triples_K_dist.pdf",
        title_suffix="full pool",
    )
    write_full_pool_cdf_plot(
        fail_counts,
        K_all,
        T=T,
        plot_path=output_dir / "all_triples_K_cdf.pdf",
    )

    prem_trim, v_trim, fc_trim_only = _trim_pool_preamble(
        versions, fail_counts, mega_threshold=mega_thr,
    )
    v_to_i = {v: i for i, v in enumerate(versions)}
    fa_trim = [fail_arrays[v_to_i[v]] for v in v_trim]
    Vt = len(v_trim)
    if Vt < 3:
        md_body = (
            ["# All-triples K statistics", ""]
            + lines_full
            + ["", "---", "", "## Trimmed pool", "", f"*Too few versions left after exclusions ({Vt}); need at least 3.*"]
        )
        (output_dir / "all_triples_K_stats.md").write_text("\n".join(md_body), encoding="utf-8")
        print(f"Wrote {output_dir / 'all_triples_K_stats.md'} (trimmed section skipped)")
        return

    Nt = Vt * (Vt - 1) * (Vt - 2) // 6
    cache_trim = output_dir / "all_triples_K_trimmed.npz"
    if cache_trim.exists():
        print(f"Loading trimmed cache {cache_trim} …")
        ct = np.load(cache_trim, allow_pickle=True)
        K_trim = ct["K_all"]
        saved_v = list(ct["versions"]) if "versions" in ct.files else None
        if saved_v != v_trim:
            print("  Cache version list mismatch; recomputing …")
            K_trim = compute_all_K(fa_trim)
            np.savez_compressed(
                cache_trim,
                K_all=K_trim,
                versions=v_trim,
                T=T,
                mega_threshold=mega_thr,
            )
    else:
        print(f"Computing trimmed pool C({Vt},3)={Nt:,} triples …")
        K_trim = compute_all_K(fa_trim)
        np.savez_compressed(
            cache_trim,
            K_all=K_trim,
            versions=v_trim,
            T=T,
            mega_threshold=mega_thr,
        )
        print(f"Saved {cache_trim}")

    lines_trim, Kmin_t, bb_t, zk_t, wtb_t, pcts_t, vt_t = pool_report_markdown(
        K_trim,
        fc_trim_only,
        v_trim,
        T,
        section_title="## Trimmed pool (no 0-fail, no mega-fail versions)",
        pool_preamble=prem_trim,
    )
    print_pool_summary(
        "Trimmed pool",
        K_trim,
        fc_trim_only.astype(float),
        V=Vt,
        N=Nt,
        T=T,
        pcts=pcts_t,
        vals_triple=vt_t,
        zero_K=zk_t,
        beats_best=bb_t,
        worse_than_best=wtb_t,
    )
    write_pool_plots(
        K_trim,
        Kmin_t,
        V=Vt,
        N=Nt,
        beats_best=bb_t,
        plot_path=output_dir / "all_triples_K_dist_trimmed.pdf",
        title_suffix="trimmed",
    )

    md_all = (
        ["# All-triples K statistics", ""]
        + lines_full
        + ["", "---", ""]
        + lines_trim
    )
    md_path = output_dir / "all_triples_K_stats.md"
    md_path.write_text("\n".join(md_all), encoding="utf-8")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
