"""
Enumerate all C(V,5) five-version units and compute oracle-aware unit failure
count K for each (majority-vote NVP with N=5).

For each 5-version unit, K is the number of tests where at least 3 members
fail, i.e. the majority vote is wrong.

Outputs (in --output dir):
  all_fives_K.npz                 full pool: compressed K array
  all_fives_K_trimmed.npz         trimmed pool (after exclusions)
  all_fives_K_stats.md            full + trimmed markdown summary
  all_fives_K_cdf.pdf             full pool: bucketed single-vs-unit distribution

Trimmed pool excludes versions with zero oracle failures and versions with
failure count >= --mega-threshold (default 10_000), mirroring all_triples_K.
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
import time
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.analyze_results import (  # noqa: E402
    analysis_version_ids,
    format_version_label,
    read_campaign_version_order,
)
from analysis.build_n_version_units import load_failure_sets  # noqa: E402

DEFAULT_MEGA_FAIL_THRESHOLD = 10_000
UNIT_SIZE = 5


def load_arrays(campaign_dir: Path) -> tuple[list[str], list[np.ndarray], int]:
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


def _build_choose(max_n: int, max_k: int = UNIT_SIZE) -> list[np.ndarray]:
    choose: list[np.ndarray] = [np.zeros(max_n + 1, dtype=np.int64) for _ in range(max_k + 1)]
    for k in range(1, max_k + 1):
        for n in range(max_n + 1):
            choose[k][n] = math.comb(n, k) if n >= k else 0
    return choose


def _rank3(a: int, b: int, c: int, ch: list[np.ndarray]) -> int:
    return int(ch[1][a] + ch[2][b] + ch[3][c])


def _rank4(a: int, b: int, c: int, d: int, ch: list[np.ndarray]) -> int:
    return int(ch[1][a] + ch[2][b] + ch[3][c] + ch[4][d])


def _rank5(a: int, b: int, c: int, d: int, e: int, ch: list[np.ndarray]) -> int:
    return int(ch[1][a] + ch[2][b] + ch[3][c] + ch[4][d] + ch[5][e])


def build_intersection_counts(fail_arrays: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[np.ndarray]]:
    V = len(fail_arrays)
    ch = _build_choose(V, UNIT_SIZE)
    counts3 = np.zeros(math.comb(V, 3), dtype=np.int32)
    counts4 = np.zeros(math.comb(V, 4), dtype=np.int32)
    counts5 = np.zeros(math.comb(V, 5), dtype=np.int32)

    per_test: dict[int, list[int]] = defaultdict(list)
    for vi, arr in enumerate(fail_arrays):
        for tid in arr.tolist():
            per_test[int(tid)].append(vi)

    for failers in per_test.values():
        failers.sort()
        f = len(failers)
        if f >= 3:
            for a, b, c in itertools.combinations(failers, 3):
                counts3[_rank3(a, b, c, ch)] += 1
        if f >= 4:
            for a, b, c, d in itertools.combinations(failers, 4):
                counts4[_rank4(a, b, c, d, ch)] += 1
        if f >= 5:
            for a, b, c, d, e in itertools.combinations(failers, 5):
                counts5[_rank5(a, b, c, d, e, ch)] += 1
    return counts3, counts4, counts5, ch


def compute_all_K(
    fail_arrays: list[np.ndarray],
    fail_counts: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    V = len(fail_arrays)
    N = math.comb(V, UNIT_SIZE)
    counts3, counts4, counts5, ch = build_intersection_counts(fail_arrays)

    K_all = np.empty(N, dtype=np.int32)
    K_min = np.empty(N, dtype=np.int32)
    K_max = np.empty(N, dtype=np.int32)

    t0 = time.time()
    report_every = max(1, N // 20)
    idx = 0
    for a in range(V - 4):
        ka = int(fail_counts[a])
        for b in range(a + 1, V - 3):
            kb = int(fail_counts[b])
            for c in range(b + 1, V - 2):
                kc = int(fail_counts[c])
                abc = counts3[_rank3(a, b, c, ch)]
                for d in range(c + 1, V - 1):
                    kd = int(fail_counts[d])
                    abd = counts3[_rank3(a, b, d, ch)]
                    acd = counts3[_rank3(a, c, d, ch)]
                    bcd = counts3[_rank3(b, c, d, ch)]
                    abcd = counts4[_rank4(a, b, c, d, ch)]
                    for e in range(d + 1, V):
                        ke = int(fail_counts[e])
                        k = (
                            abc
                            + counts3[_rank3(a, b, e, ch)]
                            + counts3[_rank3(a, c, e, ch)]
                            + counts3[_rank3(a, d, e, ch)]
                            + counts3[_rank3(b, c, e, ch)]
                            + counts3[_rank3(b, d, e, ch)]
                            + counts3[_rank3(c, d, e, ch)]
                            + abd + acd + bcd
                            - 3 * (
                                abcd
                                + counts4[_rank4(a, b, c, e, ch)]
                                + counts4[_rank4(a, b, d, e, ch)]
                                + counts4[_rank4(a, c, d, e, ch)]
                                + counts4[_rank4(b, c, d, e, ch)]
                            )
                            + 6 * counts5[_rank5(a, b, c, d, e, ch)]
                        )
                        K_all[idx] = int(k)
                        mn = min(ka, kb, kc, kd, ke)
                        mx = max(ka, kb, kc, kd, ke)
                        K_min[idx] = mn
                        K_max[idx] = mx
                        idx += 1
                        if idx % report_every == 0:
                            pct = idx / N * 100.0
                            elapsed = time.time() - t0
                            eta = elapsed / idx * (N - idx)
                            print(f"  {idx:9d}/{N:,} ({pct:4.1f}%) elapsed {elapsed:.1f}s ETA {eta:.0f}s", flush=True)
    print(f"  Done in {time.time()-t0:.1f}s", flush=True)
    return K_all, K_min, K_max


def collect_index_to_members(V: int, target_indices: set[int]) -> dict[int, tuple[int, int, int, int, int]]:
    out: dict[int, tuple[int, int, int, int, int]] = {}
    if not target_indices:
        return out
    for idx, combo in enumerate(itertools.combinations(range(V), UNIT_SIZE)):
        if idx in target_indices:
            out[idx] = combo
            if len(out) == len(target_indices):
                break
    return out


def _row_stat(label: str, single_v: float | int, unit_v: float | int, *, single_pct_T: float | None = None, unit_pct_T: float | None = None) -> str:
    def fmt(v: float | int, pct: float | None) -> str:
        x = float(np.asarray(v))
        if pct is not None:
            if abs(x - round(x)) < 1e-9:
                return f"{int(round(x)):,} ({float(pct) * 100:.4f}% of T)"
            return f"{x:.2f} ({float(pct) * 100:.4f}% of T)"
        if abs(x - round(x)) < 1e-9:
            return f"{int(round(x)):,}"
        return f"{x:.2f}"
    return f"| {label} | {fmt(single_v, single_pct_T)} | {fmt(unit_v, unit_pct_T)} |"


def pool_report_markdown(
    K_all: np.ndarray,
    fail_counts: np.ndarray,
    versions: list[str],
    T: int,
    *,
    section_title: str,
    pool_preamble: list[str],
    K_min_member: np.ndarray,
    K_max_member: np.ndarray,
) -> tuple[list[str], int, int, int, list[int], np.ndarray]:
    V = len(fail_counts)
    N = len(K_all)
    singles = fail_counts.astype(np.float64)
    beats_best = int(np.sum(K_all < K_min_member))
    beats_worst = int(np.sum(K_all < K_max_member))
    zero_K = int(np.sum(K_all == 0))
    worse_than_best = int(np.sum(K_all > K_min_member))

    pcts = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100]
    vals_unit = np.percentile(K_all, pcts)
    vals_single = np.percentile(singles, pcts)
    zero_single = int(np.sum(singles == 0))

    lines: list[str] = [
        section_title,
        "",
        *pool_preamble,
        f"- Versions in pool: **{V}**",
        f"- Five-version units C({V}, 5): **{N:,}**",
        f"- T (test cases): {T:,}",
        "",
        "### Single-version failure counts vs five-version unit K",
        "",
        "Oracle-aware failure count: per version, number of tests where output disagrees "
        "with the oracle; per 5-version unit, *K* is the number of tests where at least "
        "three members fail (majority is wrong). Rows **P0**–**P100** are empirical "
        "percentiles over the *n* single-version counts and over the *n* unit *K* values.",
        "",
        "| Statistic | Single versions (n = {:d}) | All 5-version units (n = {:,}) |".format(V, N),
        "|---|---:|---:|",
        _row_stat("Min", singles.min(), K_all.min(), single_pct_T=singles.min() / T, unit_pct_T=K_all.min() / T),
        _row_stat("Max", singles.max(), K_all.max(), single_pct_T=singles.max() / T, unit_pct_T=K_all.max() / T),
        "| Mean | {:.2f} ({:.4f}% of T) | {:.2f} ({:.4f}% of T) |".format(
            float(singles.mean()), float(singles.mean()) / T * 100,
            float(K_all.mean()), float(K_all.mean()) / T * 100,
        ),
        _row_stat("Std dev", singles.std(), K_all.std()),
        _row_stat("With K = 0 (count)", zero_single, zero_K),
        "| With K = 0 (% of row population) | {:.2f}% | {:.2f}% |".format(100.0 * zero_single / V, 100.0 * zero_K / N),
        "| Unique K values | {:,} | {:,} |".format(int(len(np.unique(singles))), int(len(np.unique(K_all)))),
    ]
    for p, vs, vu in zip(pcts, vals_single, vals_unit):
        lines.append(_row_stat(f"P{p}", vs, vu, single_pct_T=float(vs) / T, unit_pct_T=float(vu) / T))

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
        "### Comparison to individual members (within each 5-version unit)",
        "",
        f"- Units with K = 0:  **{zero_K:,}**  ({zero_K/N*100:.2f}% of all units)",
        f"- K < min(member K)  — unit beats its best member:   **{beats_best:,}**  ({beats_best/N*100:.1f}%)",
        f"- K > min(member K)  — unit worse than best member:  **{worse_than_best:,}**  ({worse_than_best/N*100:.1f}%)",
        f"- K < max(member K)  — unit beats its worst member:  **{beats_worst:,}**  ({beats_worst/N*100:.1f}%)",
        "",
        "### Best 20 five-version units (lowest K)",
        "",
        "| Rank | K | K/T (%) | Members |",
        "|---:|---:|---:|---|",
    ]
    order = np.argsort(K_all)
    target = set(order[:20].tolist() + order[-20:].tolist())
    idx_to_members = collect_index_to_members(V, target)
    for rank, idx in enumerate(order[:20]):
        members = idx_to_members[int(idx)]
        labels = [format_version_label(versions[i]) for i in members]
        k = int(K_all[idx])
        lines.append(f"| {rank+1} | {k:,} | {k/T*100:.4f}% | `{' · '.join(labels)}` |")

    lines += [
        "",
        "### Worst 20 five-version units (highest K)",
        "",
        "| Rank | K | K/T (%) | Members |",
        "|---:|---:|---:|---|",
    ]
    for rank, idx in enumerate(order[-20:][::-1]):
        members = idx_to_members[int(idx)]
        labels = [format_version_label(versions[i]) for i in members]
        k = int(K_all[idx])
        lines.append(f"| {rank+1} | {k:,} | {k/T*100:.4f}% | `{' · '.join(labels)}` |")

    uvals, ucounts = np.unique(K_all, return_counts=True)
    lines += [
        "",
        "### K value breakdown (all unique values)",
        "",
        "| K | # units | % of total | K / T (%) |",
        "|---:|---:|---:|---:|",
    ]
    for v, c in zip(uvals, ucounts):
        lines.append(f"| {int(v):,} | {c:,} | {c/N*100:.2f}% | {v/T*100:.4f}% |")

    return lines, beats_best, zero_K, worse_than_best, pcts, vals_unit


def write_bucket_plot(fail_counts: np.ndarray, K_all: np.ndarray, *, T: int, plot_path: Path, unit_label: str) -> None:
    bucket_specs = [
        ("0", lambda x: x == 0),
        ("(0,10]", lambda x: (x > 0) & (x <= 10)),
        ("(10,100]", lambda x: (x > 10) & (x <= 100)),
        ("(100,1000]", lambda x: (x > 100) & (x <= 1000)),
        (">1000", lambda x: x > 1000),
    ]
    singles = fail_counts.astype(np.int64)
    units = K_all.astype(np.int64)
    n_s = singles.size
    n_u = units.size
    singles_pct, units_pct, labels = [], [], []
    for label, pred in bucket_specs:
        labels.append(label)
        singles_pct.append(100.0 * float(np.count_nonzero(pred(singles))) / max(n_s, 1))
        units_pct.append(100.0 * float(np.count_nonzero(pred(units))) / max(n_u, 1))
    x = np.arange(len(labels), dtype=np.float64)
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    bars_s = ax.bar(x - width / 2, singles_pct, width=width, color="#1f77b4", label=f"Single version (n = {n_s})")
    bars_u = ax.bar(x + width / 2, units_pct, width=width, color="#ff7f0e", alpha=0.92, label=f"{unit_label} (n = {n_u:,})")
    ax.set_xticks(x, labels)
    ax.tick_params(axis="x", labelrotation=15, labelsize=10)
    ax.set_xlabel(f"Oracle failures K (of {T:,} tests)", fontsize=11)
    ax.set_ylabel("Percentage of versions", fontsize=11)
    ax.set_title(f"Bucketed failure-count distribution: single-version vs {unit_label.lower()}", fontsize=11)
    ymax = max(max(singles_pct, default=0.0), max(units_pct, default=0.0))
    ax.set_ylim(0.0, min(100.0, ymax + 12.0))
    ax.grid(True, axis="y", linestyle=":", alpha=0.5)
    ax.legend(loc="upper right", fontsize=10)
    for bars in (bars_s, bars_u):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 1.0, f"{height:.1f}%", ha="center", va="bottom", fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(plot_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Wrote {plot_path}")


def _trim_pool_preamble(versions: list[str], fail_counts: np.ndarray, *, mega_threshold: int) -> tuple[list[str], list[str], np.ndarray]:
    zero_idx = np.flatnonzero(fail_counts == 0)
    mega_idx = np.flatnonzero(fail_counts >= mega_threshold)
    keep = np.ones(len(versions), dtype=bool)
    keep[zero_idx] = False
    keep[mega_idx] = False
    idx = np.flatnonzero(keep)
    prem: list[str] = [
        f"**Exclusion rule:** drop versions with **zero** oracle failures and versions with **K ≥ {mega_threshold:,}**.",
        "",
    ]
    def _table(title: str, indices: np.ndarray) -> None:
        prem.append(f"#### {title}")
        prem.append("")
        prem.append("| Version | K |")
        prem.append("|---|---:|")
        for i in indices:
            prem.append(f"| `{format_version_label(versions[int(i)])}` | {int(fail_counts[int(i)]):,} |")
        prem.append("")
    _table("Excluded: zero oracle failures", zero_idx)
    _table(f"Excluded: K ≥ {mega_threshold:,}", mega_idx)
    prem.append(f"**Remaining versions:** **{len(idx)}**")
    prem.append("")
    v2 = [versions[int(i)] for i in idx]
    fc2 = fail_counts[idx].copy()
    return prem, v2, fc2


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--campaign", type=Path, default=Path("results/main-spec-3"))
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--cache", type=Path, default=None)
    p.add_argument("--mega-threshold", type=int, default=DEFAULT_MEGA_FAIL_THRESHOLD)
    args = p.parse_args()

    campaign_dir = args.campaign.resolve()
    output_dir = (args.output or campaign_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading failure sets …")
    versions, fail_arrays, T = load_arrays(campaign_dir)
    fail_counts = np.array([len(a) for a in fail_arrays], dtype=np.int64)
    V = len(versions)
    N = math.comb(V, UNIT_SIZE)
    print(f"  {V} versions, T={T:,}, C({V},5)={N:,} units")
    print()

    cache_path = args.cache or (output_dir / "all_fives_K.npz")
    if cache_path.exists():
        print(f"Loading cached K values from {cache_path} …")
        cached = np.load(cache_path)
        K_all = cached["K_all"]
        K_min = cached["K_min"]
        K_max = cached["K_max"]
        print(f"  Loaded {len(K_all):,} K values")
    else:
        print(f"Computing K for all {N:,} five-version units …")
        K_all, K_min, K_max = compute_all_K(fail_arrays, fail_counts)
        np.savez_compressed(cache_path, K_all=K_all, K_min=K_min, K_max=K_max, versions=np.array(versions, dtype=object), T=T)
        print(f"Saved cache to {cache_path}")

    lines_full, bb_f, zk_f, wtb_f, pcts_f, vals_f = pool_report_markdown(
        K_all, fail_counts, versions, T,
        section_title="## Full pool (all campaign versions)",
        pool_preamble=[],
        K_min_member=K_min,
        K_max_member=K_max,
    )
    print()
    print("=== Full pool ===")
    print(f"  Single: min={int(fail_counts.min())}, med={int(np.median(fail_counts))}, mean={fail_counts.mean():.1f}, max={int(fail_counts.max())}, K=0: {int(np.sum(fail_counts==0))}/{V}")
    print(f"  5-unit: min={int(K_all.min())}, med={int(np.median(K_all))}, mean={K_all.mean():.1f}, max={int(K_all.max())}, K=0: {int(zk_f)}/{N}")
    write_bucket_plot(fail_counts, K_all, T=T, plot_path=output_dir / "all_fives_K_cdf.pdf", unit_label="5-version unit")

    prem_trim, v_trim, fc_trim = _trim_pool_preamble(versions, fail_counts, mega_threshold=int(args.mega_threshold))
    if len(v_trim) >= UNIT_SIZE:
        v_to_i = {v: i for i, v in enumerate(versions)}
        fa_trim = [fail_arrays[v_to_i[v]] for v in v_trim]
        cache_trim = output_dir / "all_fives_K_trimmed.npz"
        if cache_trim.exists():
            ct = np.load(cache_trim)
            K_trim = ct["K_all"]
            K_min_trim = ct["K_min"]
            K_max_trim = ct["K_max"]
        else:
            print(f"Computing trimmed pool C({len(v_trim)},5)={math.comb(len(v_trim), UNIT_SIZE):,} units …")
            K_trim, K_min_trim, K_max_trim = compute_all_K(fa_trim, fc_trim)
            np.savez_compressed(cache_trim, K_all=K_trim, K_min=K_min_trim, K_max=K_max_trim, versions=np.array(v_trim, dtype=object), T=T)
            print(f"Saved {cache_trim}")
        lines_trim, _, _, _, _, _ = pool_report_markdown(
            K_trim, fc_trim, v_trim, T,
            section_title="## Trimmed pool (no 0-fail, no mega-fail versions)",
            pool_preamble=prem_trim,
            K_min_member=K_min_trim,
            K_max_member=K_max_trim,
        )
    else:
        lines_trim = ["## Trimmed pool (no 0-fail, no mega-fail versions)", "", f"*Too few versions left after exclusions ({len(v_trim)}); need at least {UNIT_SIZE}.*"]

    md = ["# All-fives K statistics", ""] + lines_full + ["", "---", ""] + lines_trim
    md_path = output_dir / "all_fives_K_stats.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
