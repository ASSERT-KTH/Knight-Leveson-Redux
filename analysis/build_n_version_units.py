"""
RQ4 — Can reliable N-version units be built from apparently failure-independent
versions?

For each admitted version we have a binary failure vector over the shared
1{,}000{,}000-case test campaign and a Pearson phi correlation with every other
admitted version (results of RQ2).  This script:

1.  Builds a candidate pool of versions ranked by ascending mean pairwise phi
    (i.e. those that look most failure-independent on the campaign).
2.  Constructs ``--num-units`` N-version units (default ``N=3``, 20 units) by
    enumerating all triples within the candidate pool and selecting those whose
    *worst* internal pairwise phi is smallest.  Two extra unit families are
    constructed for comparison: the worst-case (highest internal phi) units and
    a uniformly random sample, both drawn from the full admitted population.
3.  Evaluates each unit on the campaign by simple majority voting at the
    pass/fail level: a unit fails on a test case when ⌈N/2⌉ or more of its
    versions fail simultaneously.  This matches the K&L K-statistic definition
    of "≥k simultaneous failures" applied at the unit level.
4.  Reports, per unit, the empirical failure rate, the independence-based
    prediction, the per-member empirical failure rates, and the within-unit
    pairwise phi summary.

Outputs (in ``--output`` directory, defaults to the campaign directory):

    n_version_units.csv           # one row per evaluated unit
    n_version_units_summary.json  # aggregate statistics by unit family / N
    n_version_units.pdf           # bar chart: per-unit empirical vs predicted
    n_version_units_pool.csv      # candidate pool ranking by mean phi

Usage:
    python -m analysis.build_n_version_units \
        --campaign results/main-spec-3/campaign.csv \
        --pairwise results/main-spec-3/pairwise_table.csv \
        --num-units 20 --n 3
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.analyze_results import (  # noqa: E402
    analysis_version_ids,
    format_version_label,
    load_version_language_agent,
    read_campaign_version_order,
)


# ---------------------------------------------------------------------------
# Failure-bitmap loader (sparse) with on-disk cache
# ---------------------------------------------------------------------------

def _parse_passed(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "t", "yes")


def load_failure_sets(
    campaign_csv: Path,
    versions: list[str],
    *,
    cache_path: Path | None = None,
) -> tuple[int, dict[str, np.ndarray]]:
    """
    Return ``(T, fail_sets)`` where ``fail_sets[vid]`` is a sorted ``np.int64``
    array of test ids on which version ``vid`` failed.

    On first run this streams the (large) ``campaign.csv``.  Subsequent runs
    load the precomputed ``.npz`` cache when available.  ``T`` is recovered as
    the maximum ``test_id`` plus one (``test_id`` is 0-indexed by the campaign
    runner).
    """
    if cache_path is not None and cache_path.is_file():
        data = np.load(cache_path, allow_pickle=True)  # cache is local-only
        cached_versions = data["versions"].tolist()
        if cached_versions == versions:
            T = int(data["T"])
            fail_sets = {v: data[f"f_{i}"] for i, v in enumerate(versions)}
            return T, fail_sets
        # Cache stale, fall through to recompute.

    fail_lists: dict[str, list[int]] = {v: [] for v in versions}
    want = set(versions)
    max_tid = -1

    print(f"Streaming {campaign_csv} (this is the slow part — ~1–2 min)...")
    with campaign_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for n_lines, row in enumerate(reader):
            vid = row["version_id"]
            if vid not in want:
                continue
            tid = int(row["test_id"])
            if tid > max_tid:
                max_tid = tid
            if not _parse_passed(row["passed"]):
                fail_lists[vid].append(tid)
            if (n_lines + 1) % 5_000_000 == 0:
                print(f"  ...read {n_lines + 1:>10,} rows, current test_id={tid}")

    T = max_tid + 1
    fail_sets = {v: np.asarray(fail_lists[v], dtype=np.int64) for v in versions}

    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        kwargs = {f"f_{i}": fail_sets[v] for i, v in enumerate(versions)}
        np.savez(
            cache_path,
            versions=np.asarray(versions, dtype=object),
            T=np.int64(T),
            **kwargs,
        )
        print(f"Cached failure sets at {cache_path}")
    return T, fail_sets


# ---------------------------------------------------------------------------
# Phi matrix and pool selection
# ---------------------------------------------------------------------------

def load_phi_matrix(
    pairwise_csv: Path, versions: list[str]
) -> np.ndarray:
    """Build an ``(N, N)`` symmetric phi matrix.  Diagonal is ``NaN``."""
    n = len(versions)
    idx = {v: i for i, v in enumerate(versions)}
    phi = np.full((n, n), np.nan, dtype=np.float64)
    with pairwise_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            vi, vj = row["version_i"], row["version_j"]
            if vi not in idx or vj not in idx:
                continue
            raw = (row.get("phi_correlation") or "").strip()
            if not raw:
                continue
            try:
                value = float(raw)
            except ValueError:
                continue
            i, j = idx[vi], idx[vj]
            phi[i, j] = value
            phi[j, i] = value
    return phi


def mean_phi_per_version(
    phi: np.ndarray,
    *,
    nan_policy: str = "exclude",
) -> np.ndarray:
    """
    Average over each row excluding ``NaN`` (``exclude``) or treating NaN as 0
    (``zero``).  Diagonal is ignored (it is NaN by construction).
    """
    out = np.full(phi.shape[0], np.nan, dtype=np.float64)
    if nan_policy not in {"exclude", "zero"}:
        raise ValueError("nan_policy must be 'exclude' or 'zero'")
    for i in range(phi.shape[0]):
        row = phi[i].copy()
        row[i] = np.nan
        if nan_policy == "zero":
            row = np.where(np.isnan(row), 0.0, row)
        if np.all(np.isnan(row)):
            continue
        out[i] = float(np.nanmean(row))
    return out


# ---------------------------------------------------------------------------
# Unit construction and evaluation
# ---------------------------------------------------------------------------

def unit_max_phi(triple: tuple[int, ...], phi: np.ndarray) -> float:
    """Return the worst (largest) finite pairwise phi within the unit.

    NaN entries (failure-free version pairs) are treated as 0: by definition
    such versions are perfectly uncorrelated with every other version, so they
    contribute the most-independent value to the unit's worst-pair score.
    """
    vals = []
    for a, b in itertools.combinations(triple, 2):
        v = phi[a, b]
        vals.append(0.0 if math.isnan(v) else v)
    return max(vals) if vals else float("nan")


def unit_sum_phi(triple: tuple[int, ...], phi: np.ndarray) -> float:
    """Sum of pairwise phi values within the unit (NaN → 0).

    For ``N=3`` this is the sum of the three pairwise correlations; selecting
    the lowest-sum triples penalises correlation across *all* member pairs
    rather than only the worst pair (which is what ``unit_max_phi`` rewards).
    """
    total = 0.0
    for a, b in itertools.combinations(triple, 2):
        v = phi[a, b]
        total += 0.0 if math.isnan(v) else v
    return total


# ---------------------------------------------------------------------------
# LIC-failure-based unit construction
# ---------------------------------------------------------------------------

def load_lic_failure_sets(
    fault_events_path: Path,
    versions: list[str],
    *,
    include_fuv: bool = False,
) -> dict[int, frozenset[int]]:
    """Return ``{version_index: frozenset(LIC indices)}`` for each version.

    ``LIC indices`` are 0-based to match ``cmv_mismatch_indices`` (the spec's
    1-based LIC numbers are ``index + 1``).  By default only the per-test
    ``cmv_mismatch_indices`` field is consulted: that is the most direct
    "this version computed the wrong boolean for LIC ``k`` on this test"
    signal.  ``include_fuv=True`` additionally folds in
    ``fuv_mismatch_indices`` (a downstream / cascaded signal).
    """
    if not fault_events_path.is_file():
        raise FileNotFoundError(fault_events_path)
    idx = {v: i for i, v in enumerate(versions)}
    accum: dict[int, set[int]] = {i: set() for i in range(len(versions))}
    with fault_events_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            vid = rec.get("version_id")
            if vid not in idx:
                continue
            diff = rec.get("diff", {}) or {}
            for k in diff.get("cmv_mismatch_indices") or []:
                accum[idx[vid]].add(int(k))
            if include_fuv:
                for k in diff.get("fuv_mismatch_indices") or []:
                    accum[idx[vid]].add(int(k))
    return {i: frozenset(s) for i, s in accum.items()}


def unit_lic_intersection_size(
    triple: tuple[int, ...],
    lic_sets: dict[int, frozenset[int]],
) -> int:
    """``|⋂_{v ∈ triple} lic_set(v)|`` — number of LICs misimplemented by
    *every* member of the unit (lower is better)."""
    sets = [lic_sets[i] for i in triple]
    if not sets:
        return 0
    inter = sets[0]
    for s in sets[1:]:
        inter = inter & s
        if not inter:
            return 0
    return len(inter)


def unit_lic_pairwise_sum(
    triple: tuple[int, ...],
    lic_sets: dict[int, frozenset[int]],
) -> int:
    """Σ_{(i,j)} |lic_set(i) ∩ lic_set(j)| — sum of LIC overlaps over all
    pairs in the unit.  Used as a tie-breaker when many triples share the
    same N-way intersection size."""
    total = 0
    for a, b in itertools.combinations(triple, 2):
        total += len(lic_sets[a] & lic_sets[b])
    return total


def select_units_anchored_lic(
    pool: list[int],
    *,
    n: int,
    num_units: int,
    mean_phi: np.ndarray,
    lic_sets: dict[int, frozenset[int]],
    phi: np.ndarray,
) -> list[tuple[int, ...]]:
    """Anchored construction with the **pairwise** LIC-intersection objective.

    Anchors are iterated in ascending mean-phi order (the same "apparently
    independent" ranking used by the other low-correlation families).  For
    each anchor, candidate triples are scored by:

      (1) primary: ``Σ_pairs |lic_set(i) ∩ lic_set(j)|``
          — total LIC overlap across all member pairs.  This is the
          appropriate criterion for ⌈N/2⌉ majority voting: a unit fails
          whenever *any two* members fail on the same input, so what
          matters is whether any two members share LIC mistakes — not
          whether all N share at least one mistake.
      (2) secondary: ``max_pairs |lic_set(i) ∩ lic_set(j)|`` (penalise the
          worst pair, breaks ties on primary).
      (3) tertiary: ``|⋂ lic_set(v)|`` (3-way intersection — kept as a
          tie-break only).
      (4) quaternary: within-unit ``max φ`` (final tie-break).

    Globally de-duplicated against earlier anchors.
    """
    if len(pool) < n:
        raise ValueError(
            f"Need at least n={n} versions in the pool to build a unit; got {len(pool)}"
        )
    pool_sorted = sorted(pool, key=lambda i: float(mean_phi[i]))
    anchors = pool_sorted[:num_units]
    seen: set[tuple[int, ...]] = set()
    units: list[tuple[int, ...]] = []
    for anchor in anchors:
        candidates = [v for v in pool if v != anchor]
        scored: list[tuple[tuple[int, int, int, float], tuple[int, ...]]] = []
        for combo in itertools.combinations(candidates, n - 1):
            triple = tuple(sorted((anchor,) + combo))
            primary = unit_lic_pairwise_sum(triple, lic_sets)
            secondary = max(
                (len(lic_sets[a] & lic_sets[b])
                 for a, b in itertools.combinations(triple, 2)),
                default=0,
            )
            tertiary = unit_lic_intersection_size(triple, lic_sets)
            quaternary = unit_max_phi(triple, phi)
            scored.append(((primary, secondary, tertiary, quaternary), triple))
        scored.sort(key=lambda item: item[0])
        for _score, triple in scored:
            if triple in seen:
                continue
            seen.add(triple)
            units.append(triple)
            break
    return units


def select_units(
    phi: np.ndarray,
    pool: list[int],
    *,
    n: int,
    num_units: int,
    objective: str = "min",
) -> list[tuple[int, ...]]:
    """Enumerate all unit-of-N combinations from ``pool``, sort by the
    within-unit max pairwise phi, return the top ``num_units`` for the
    requested objective (``min`` for low-correlation, ``max`` for the worst-
    case sanity baseline).

    Note: this strategy concentrates on the global extremum and tends to
    produce nearly identical units that all share the same low-phi pair as
    an anchor.  For a more diverse construction prefer ``select_units_anchored``.
    """
    if len(pool) < n:
        raise ValueError(
            f"Need at least n={n} versions in the pool to build a unit; got {len(pool)}"
        )
    triples = list(itertools.combinations(pool, n))
    triples.sort(key=lambda t: unit_max_phi(t, phi), reverse=(objective == "max"))
    if num_units > len(triples):
        return triples
    return triples[:num_units]


def select_units_anchored(
    phi: np.ndarray,
    pool: list[int],
    *,
    n: int,
    num_units: int,
    mean_phi: np.ndarray,
    score_fn=unit_max_phi,
    minimise: bool = True,
) -> list[tuple[int, ...]]:
    """One unit per anchor version, with global de-duplication.

    Iterate over pool versions in ascending ``mean_phi`` order; each anchor
    contributes one unit consisting of itself and the ``n-1`` other pool
    members that ``score_fn`` ranks best, *subject to* the resulting triple
    not having been picked by an earlier anchor.

    Without this de-duplication step distinct anchors can converge on the
    same triple (e.g. anchor A picks ``{A, B, C}`` and anchor B independently
    picks ``{A, B, C}``), which would produce visually identical "units".

    Parameters
    ----------
    score_fn : callable(tuple[int,...], phi) -> float
        Default ``unit_max_phi`` (the lowest worst-pair).  Pass
        ``unit_sum_phi`` to instead minimise the sum of within-unit pairwise
        phi correlations.
    minimise : bool
        If ``True`` (default) the unit with the lowest score is preferred;
        set to ``False`` for the high-correlation sanity baseline.
    """
    if len(pool) < n:
        raise ValueError(
            f"Need at least n={n} versions in the pool to build a unit; got {len(pool)}"
        )
    pool_sorted = sorted(pool, key=lambda i: float(mean_phi[i]),
                         reverse=not minimise)
    anchors = pool_sorted[:num_units]
    seen: set[tuple[int, ...]] = set()
    units: list[tuple[int, ...]] = []
    sign = 1.0 if minimise else -1.0
    for anchor in anchors:
        candidates = [v for v in pool if v != anchor]
        scored: list[tuple[float, tuple[int, ...]]] = []
        for combo in itertools.combinations(candidates, n - 1):
            triple = tuple(sorted((anchor,) + combo))
            scored.append((sign * score_fn(triple, phi), triple))
        scored.sort(key=lambda item: item[0])
        for _score, triple in scored:
            if triple in seen:
                continue
            seen.add(triple)
            units.append(triple)
            break
    return units


def select_units_disjoint(
    phi: np.ndarray,
    pool: list[int],
    *,
    n: int,
    num_units: int,
) -> list[tuple[int, ...]]:
    """Greedy non-overlapping construction.

    At each step pick the lowest-max-phi triple from the remaining pool, then
    remove its members from consideration.  Stops when fewer than ``n``
    versions remain or after ``num_units`` selections.  The pool size bounds
    the number of disjoint units (``len(pool) // n``).
    """
    remaining = set(pool)
    units: list[tuple[int, ...]] = []
    while len(remaining) >= n and len(units) < num_units:
        best: tuple[int, ...] | None = None
        best_score = float("inf")
        for combo in itertools.combinations(sorted(remaining), n):
            score = unit_max_phi(combo, phi)
            if score < best_score:
                best_score = score
                best = combo
        if best is None:
            break
        units.append(best)
        for v in best:
            remaining.discard(v)
    return units


def random_units(
    rng: np.random.Generator,
    pool: list[int],
    *,
    n: int,
    num_units: int,
) -> list[tuple[int, ...]]:
    seen: set[tuple[int, ...]] = set()
    out: list[tuple[int, ...]] = []
    pool_arr = np.asarray(pool)
    while len(out) < num_units:
        sel = tuple(sorted(rng.choice(pool_arr, size=n, replace=False).tolist()))
        if sel in seen:
            continue
        seen.add(sel)
        out.append(sel)
    return out


def kway_intersection_size(arrays: list[np.ndarray]) -> int:
    """Size of the intersection of K sorted ``np.int64`` arrays."""
    if not arrays:
        return 0
    sizes = [a.size for a in arrays]
    if min(sizes) == 0:
        return 0
    arrays = sorted(arrays, key=lambda a: a.size)
    base = arrays[0]
    for other in arrays[1:]:
        if base.size == 0:
            return 0
        # np.intersect1d with assume_unique is O(n+m) on sorted arrays
        base = np.intersect1d(base, other, assume_unique=True)
    return int(base.size)


def unit_observed_failure_count(
    triple: tuple[int, ...],
    fail_sets: list[np.ndarray],
    *,
    majority: int,
) -> int:
    """Count campaign cases where at least ``majority`` versions in ``triple``
    fail simultaneously.

    Uses inclusion–exclusion over pair / triple intersections; works for any N
    but is most useful for small N (3, 5).
    """
    sets = [fail_sets[i] for i in triple]
    n = len(sets)
    # Enumerate all subsets of size >= majority and apply inclusion–exclusion
    # to count |union over choices of >= majority indices simultaneously
    # failing|.  Equivalent expression for small N:
    #     count(>=k) = Σ_{j=k..N} (-1)^(j-k) · C(j-1, k-1) · S_j
    # where S_j = Σ over j-subsets of |intersection|.
    s_terms: list[int] = [0] * (n + 1)
    for size in range(majority, n + 1):
        total = 0
        for combo in itertools.combinations(range(n), size):
            total += kway_intersection_size([sets[c] for c in combo])
        s_terms[size] = total

    count = 0
    for j in range(majority, n + 1):
        coeff = ((-1) ** (j - majority)) * math.comb(j - 1, majority - 1)
        count += coeff * s_terms[j]
    return int(count)


def independence_unit_failure_prob(
    member_rates: list[float], *, majority: int
) -> float:
    """Probability that ≥ ``majority`` independent Bernoulli failures occur."""
    n = len(member_rates)
    p = 0.0
    for combo in itertools.product([0, 1], repeat=n):
        if sum(combo) < majority:
            continue
        prob = 1.0
        for bit, rate in zip(combo, member_rates):
            prob *= rate if bit == 1 else (1.0 - rate)
        p += prob
    return p


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _format_phi_label(value: float) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    if value == 0:
        return "0"
    abs_v = abs(value)
    if abs_v >= 0.01:
        return f"{value:.3f}"
    # Compact scientific for very small magnitudes (e.g. -3e-5)
    return f"{value:.0e}"


def plot_unit_failures(
    rows: pd.DataFrame, output_path: Path, *, T: int, family_label: str
) -> None:
    if rows.empty:
        return
    rows = rows.copy()
    rows = rows.sort_values("observed_unit_fail_count", ascending=True).reset_index(drop=True)
    n = len(rows)
    # Three grouped bars: width must satisfy 3·width + gap ≤ 1.0 (the
    # spacing between adjacent x-tick groups) or bars from neighbouring
    # groups visually overlap.  width = 0.28 leaves a 0.16 gap between groups.
    width = 0.28
    fig, ax = plt.subplots(figsize=(max(8, 0.55 * n + 4), 5))
    x = np.arange(n)

    obs = rows["observed_unit_fail_count"].to_numpy(dtype=float)
    pred = rows["expected_unit_fail_count"].to_numpy(dtype=float)
    member_min = rows["member_min_fail_count"].to_numpy(dtype=float)

    ax.bar(x - width, pred, width, label="Independence prediction (μ)",
           color="#9ecae1", edgecolor="white")
    ax.bar(x, obs, width, label="Observed unit failures (K)",
           color="#c44e52", edgecolor="white")
    ax.bar(x + width, member_min, width, label="Best single member",
           color="#55a868", edgecolor="white")

    tick_labels = [
        f"U{i+1}\n(φ={_format_phi_label(rows['max_pairwise_phi'].iloc[i])})"
        for i in range(n)
    ]
    ax.set_xticks(x)
    ax.set_xticklabels(tick_labels, rotation=30, ha="right", fontsize=8)
    ax.set_xlabel(
        f"{family_label} units sorted by observed K — "
        "second line is the unit's max within-unit φ"
    )
    ax.set_ylabel(f"Failures over {T:,} campaign cases")
    ax.set_yscale("symlog", linthresh=1.0)
    ax.set_title(f"Per-unit observed vs independence-predicted failures — {family_label}")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.margins(x=0.01)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path}")


def plot_family_summary(
    summary: pd.DataFrame, output_path: Path, *, T: int
) -> None:
    if summary.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 4.5))
    families = summary["family"].tolist()
    x = np.arange(len(families))
    width = 0.28

    obs = summary["mean_observed"].to_numpy(dtype=float)
    pred = summary["mean_expected"].to_numpy(dtype=float)
    best = summary["mean_member_min"].to_numpy(dtype=float)

    ax.bar(x - width, pred, width, label="Independence prediction (μ)",
           color="#9ecae1", edgecolor="white")
    ax.bar(x, obs, width, label="Observed unit failures (K)",
           color="#c44e52", edgecolor="white")
    ax.bar(x + width, best, width, label="Best single member",
           color="#55a868", edgecolor="white")

    ax.set_xticks(x)
    ax.set_xticklabels(families, rotation=15, ha="right")
    ax.set_ylabel(f"Mean failures over {T:,} campaign cases")
    ax.set_yscale("symlog", linthresh=1.0)
    ax.set_title("Mean per-unit observed vs predicted failures, by unit family")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path}")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def evaluate_units(
    units: Iterable[tuple[int, ...]],
    *,
    family: str,
    versions: list[str],
    fail_sets_arrays: list[np.ndarray],
    fail_counts: np.ndarray,
    phi: np.ndarray,
    T: int,
    lic_sets: dict[int, frozenset[int]] | None = None,
) -> list[dict]:
    rows: list[dict] = []
    for u_idx, triple in enumerate(units):
        majority = (len(triple) // 2) + 1
        observed = unit_observed_failure_count(
            triple, fail_sets_arrays, majority=majority
        )
        member_rates = [float(fail_counts[i]) / T for i in triple]
        member_count = [int(fail_counts[i]) for i in triple]
        p_unit = independence_unit_failure_prob(member_rates, majority=majority)
        expected = T * p_unit
        # Within-unit phi summary
        phis = [
            phi[a, b]
            for a, b in itertools.combinations(triple, 2)
        ]
        phis_finite = [v for v in phis if not math.isnan(v)]
        rows.append({
            "family": family,
            "unit_index": u_idx,
            "n": len(triple),
            "majority": majority,
            "members": "|".join(versions[i] for i in triple),
            "member_labels": "|".join(format_version_label(versions[i]) for i in triple),
            "member_fail_counts": "|".join(str(c) for c in member_count),
            "member_min_fail_count": int(min(member_count)),
            "member_max_fail_count": int(max(member_count)),
            "max_pairwise_phi": (max(phis_finite) if phis_finite else float("nan")),
            "mean_pairwise_phi": (
                float(np.mean(phis_finite)) if phis_finite else float("nan")
            ),
            "sum_pairwise_phi": (
                float(np.sum(phis_finite)) if phis_finite else float("nan")
            ),
            **(
                {
                    "lic_intersection_size": unit_lic_intersection_size(
                        triple, lic_sets
                    ),
                    "lic_intersection": ",".join(
                        # 1-based LIC numbers (spec convention)
                        str(k + 1)
                        for k in sorted(
                            set.intersection(
                                *[set(lic_sets[i]) for i in triple]
                            )
                            if all(lic_sets[i] for i in triple)
                            else set()
                        )
                    ),
                    "lic_pairwise_sum": unit_lic_pairwise_sum(triple, lic_sets),
                    "lic_pairwise_max": max(
                        (len(lic_sets[a] & lic_sets[b])
                         for a, b in itertools.combinations(triple, 2)),
                        default=0,
                    ),
                    "member_lic_sets": "|".join(
                        ",".join(str(k + 1) for k in sorted(lic_sets[i]))
                        for i in triple
                    ),
                }
                if lic_sets is not None
                else {}
            ),
            "observed_unit_fail_count": observed,
            "observed_unit_fail_rate": observed / T,
            "expected_unit_fail_prob": p_unit,
            "expected_unit_fail_count": expected,
            "ratio_obs_exp": (
                observed / expected if expected > 0 else float("nan")
            ),
        })
    return rows


def _split_pipe(value: str) -> list[str]:
    return [part for part in str(value).split("|") if part != ""]


def write_units_markdown(
    units_df: pd.DataFrame,
    output_path: Path,
    *,
    T: int,
    family_order: list[str] | None = None,
) -> None:
    """Write a Markdown report listing the members of every unit per family,
    each with its individual fault count and the unit-level statistics.
    """
    if units_df.empty:
        return
    if family_order is None:
        family_order = list(units_df["family"].unique())

    lines: list[str] = [
        "# RQ4 — N-version units: composition and fault counts",
        "",
        f"All counts are over a shared campaign of T = {T:,} test cases.",
        "Each unit's failure model is majority voting at the version pass/fail level: "
        "the unit fails on a campaign case when ⌈N/2⌉ or more of its versions fail "
        "simultaneously.  *member f* is the per-version individual failure count over "
        "the same campaign.  *max φ* is the largest pairwise φ correlation between any "
        "two members of the unit (NaN when one of the members is failure-free).",
        "",
    ]

    for family in family_order:
        sub = units_df[units_df["family"] == family].reset_index(drop=True)
        if sub.empty:
            continue
        n_versions = int(sub["n"].iloc[0])
        max_members_seen = max(
            len(_split_pipe(row["member_labels"])) for _, row in sub.iterrows()
        )
        member_cols = max_members_seen
        lines.append(f"## Family `{family}` (N = {n_versions}, {len(sub)} units)")
        lines.append("")
        if family == "low_phi_pool":
            lines.append(
                "Anchored construction: 20 lowest-mean-φ versions act as anchors; each "
                "is paired with the two pool members minimising the within-unit max φ."
            )
        elif family == "low_phi_pool_sum":
            lines.append(
                "Anchored construction with the **sum** of within-unit pairwise φ as the "
                "selection objective: each anchor is paired with the two pool members "
                "minimising Σ φ over the three pairs (rather than the max φ of any single "
                "pair).  Globally de-duplicated against earlier anchors."
            )
        elif family == "low_phi_pool_sum_n5":
            lines.append(
                "Same as `low_phi_pool_sum` but with N = 5 and Σ φ taken over all "
                "C(5,2) = 10 pairs."
            )
        elif family in ("low_lic_intersection_pool", "low_lic_intersection_pool_n5"):
            lines.append(
                "Anchored construction with the **pairwise LIC-failure overlap** as "
                "the primary selection objective: each anchor is paired with the pool "
                "members minimising `Σ_pairs |LIC-set(i) ∩ LIC-set(j)|` — the total "
                "number of shared LIC mistakes across all member pairs.  This is the "
                "relevant criterion for ⌈N/2⌉ majority voting (the unit fails when "
                "*any two* members fail on the same input), unlike the 3-way "
                "intersection, which can vanish even when individual pairs share many "
                "LICs.  Tie-breaks: max pairwise |LIC ∩|, then 3-way |LIC ∩|, then "
                "within-unit max φ.  LIC numbers below are 1-based (spec convention).  "
                "Globally de-duplicated against earlier anchors."
            )
        elif family == "high_phi_baseline":
            lines.append(
                "Sanity baseline: anchors picked from the *highest*-mean-φ versions, "
                "completed with high-φ partners."
            )
        elif family == "random_baseline":
            lines.append(
                "Sanity baseline: 20 unit triples drawn uniformly at random from all "
                "admitted versions."
            )
        elif family == "low_phi_pool_n5":
            lines.append("Same anchored construction as `low_phi_pool` but with N = 5.")
        lines.append("")

        has_lic = "lic_intersection_size" in sub.columns
        header = ["Unit"]
        for k in range(member_cols):
            header.append(f"Member {k+1}")
            header.append(f"f{k+1}")
        header.extend(["max φ", "Σ φ"])
        if has_lic:
            # pairwise sum / max LIC overlap is the relevant selection
            # quantity; the 3-way intersection is a diagnostic only.
            header.extend(["Σ |LIC ∩|", "max |LIC ∩|", "3-way |LIC ∩|", "LIC ∩"])
        header.extend(["Observed K", "Predicted μ", "K/μ"])
        lines.append("| " + " | ".join(header) + " |")
        right_aligned = {
            "Unit", "max φ", "Σ φ", "Σ |LIC ∩|", "max |LIC ∩|",
            "3-way |LIC ∩|", "Observed K", "Predicted μ", "K/μ",
        }
        lines.append(
            "|" + "|".join(
                ["---:" if (h.startswith("f") or h in right_aligned) else "---"
                 for h in header]
            ) + "|"
        )

        sub = sub.sort_values("observed_unit_fail_count").reset_index(drop=True)
        for i, row in sub.iterrows():
            members = _split_pipe(row["member_labels"])
            counts = _split_pipe(row["member_fail_counts"])
            cells: list[str] = [f"U{i+1}"]
            for k in range(member_cols):
                if k < len(members):
                    cells.append(f"`{members[k]}`")
                    cells.append(counts[k] if k < len(counts) else "")
                else:
                    cells.append("")
                    cells.append("")
            cells.append(_format_phi_label(float(row["max_pairwise_phi"])))
            cells.append(_format_phi_label(float(row.get("sum_pairwise_phi", float("nan")))))
            if has_lic:
                pair_sum = row.get("lic_pairwise_sum")
                pair_max = row.get("lic_pairwise_max")
                three_way = row.get("lic_intersection_size")
                lic_set = row.get("lic_intersection") or ""
                cells.append("" if pd.isna(pair_sum) else str(int(pair_sum)))
                cells.append("" if pd.isna(pair_max) else str(int(pair_max)))
                cells.append("" if pd.isna(three_way) else str(int(three_way)))
                cells.append("—" if not str(lic_set).strip() else f"{{{lic_set}}}")
            cells.append(f"{int(row['observed_unit_fail_count'])}")
            mu = float(row["expected_unit_fail_count"])
            cells.append(f"{mu:.3g}")
            ratio = row["ratio_obs_exp"]
            cells.append(
                "n/a"
                if (isinstance(ratio, float) and math.isnan(ratio))
                else f"{ratio:.2f}"
            )
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"Wrote {output_path}")


def family_summary(rows: pd.DataFrame, *, T: int) -> dict:
    if rows.empty:
        return {}
    return {
        "n_units": int(len(rows)),
        "n": int(rows["n"].iloc[0]),
        "T": T,
        "mean_observed": float(rows["observed_unit_fail_count"].mean()),
        "median_observed": float(rows["observed_unit_fail_count"].median()),
        "max_observed": int(rows["observed_unit_fail_count"].max()),
        "min_observed": int(rows["observed_unit_fail_count"].min()),
        "mean_expected": float(rows["expected_unit_fail_count"].mean()),
        "mean_member_min": float(rows["member_min_fail_count"].mean()),
        "mean_member_max": float(rows["member_max_fail_count"].mean()),
        "n_units_better_than_best_member": int(
            (rows["observed_unit_fail_count"] < rows["member_min_fail_count"]).sum()
        ),
        "n_units_zero_failures": int(
            (rows["observed_unit_fail_count"] == 0).sum()
        ),
        "max_internal_phi_mean": float(rows["max_pairwise_phi"].mean()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument(
        "--pairwise",
        type=Path,
        default=None,
        help="pairwise_table.csv (defaults to <campaign-dir>/pairwise_table.csv)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output dir (defaults to campaign-dir)",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=None,
        help=".npz cache for the failure-sets bitmap "
             "(defaults to <campaign-dir>/failure_sets.npz)",
    )
    parser.add_argument("--num-units", type=int, default=20)
    parser.add_argument(
        "--n",
        type=int,
        default=3,
        help="Versions per unit (3 or 5 are typical NVP choices)",
    )
    parser.add_argument(
        "--pool-size",
        type=int,
        default=25,
        help="Top-K versions by lowest mean phi to use as the candidate pool",
    )
    parser.add_argument(
        "--include-failure-free",
        action="store_true",
        help="Include versions with 0 campaign failures in the candidate pool. "
             "By default they are excluded so the analysis focuses on "
             "non-trivially correlated versions.",
    )
    parser.add_argument(
        "--seed", type=int, default=20260507,
        help="Seed for the random-units baseline.",
    )
    parser.add_argument(
        "--also-n5",
        action="store_true",
        help="Also evaluate N=5 units (smaller pool / fewer combinations).",
    )
    parser.add_argument(
        "--fault-events",
        type=Path,
        default=None,
        help=(
            "Path to fault_events.jsonl, used by the LIC-intersection family. "
            "Defaults to <campaign-dir>/fault_events.jsonl.  If the file is "
            "absent the LIC family is silently skipped."
        ),
    )
    parser.add_argument(
        "--lic-include-fuv",
        action="store_true",
        help=(
            "Fold fuv_mismatch_indices into each version's LIC failure set "
            "in addition to cmv_mismatch_indices (default uses cmv only — "
            "the most direct 'wrong LIC boolean' signal)."
        ),
    )
    parser.add_argument(
        "--selection",
        choices=["anchored", "lowest_max_phi", "disjoint"],
        default="anchored",
        help=(
            "How to draw 'low-phi pool' units. ``anchored`` (default): one "
            "unit per pool anchor, completed greedily with the lowest-phi "
            "partners (gives the most diverse 20 units).  ``lowest_max_phi``: "
            "global top-K triples by within-unit max phi (concentrates on a "
            "few anchor pairs and tends to produce near-duplicate units).  "
            "``disjoint``: greedy non-overlapping triples (capped at "
            "``floor(pool_size / n)``)."
        ),
    )
    args = parser.parse_args()

    campaign_path: Path = args.campaign.resolve()
    output_dir = (args.output or campaign_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    pairwise_path = (args.pairwise or campaign_path.parent / "pairwise_table.csv").resolve()
    cache_path = (args.cache or campaign_path.parent / "failure_sets.npz").resolve()

    if not campaign_path.is_file():
        raise SystemExit(f"campaign.csv not found: {campaign_path}")
    if not pairwise_path.is_file():
        raise SystemExit(
            f"pairwise_table.csv not found: {pairwise_path} "
            "(run analysis.analyze_results first)"
        )

    versions = analysis_version_ids(
        campaign_path, read_campaign_version_order(campaign_path)
    )
    lang_by_vid, agent_by_vid = load_version_language_agent(campaign_path, versions)
    print(f"Admitted versions: {len(versions)}")

    # 1. Load failure sets and per-version failure counts
    T, fail_sets_dict = load_failure_sets(
        campaign_path, versions, cache_path=cache_path
    )
    fail_sets_arrays = [fail_sets_dict[v] for v in versions]
    fail_counts = np.asarray([a.size for a in fail_sets_arrays], dtype=np.int64)
    print(f"T = {T:,}; min/median/max per-version failures = "
          f"{fail_counts.min()} / {int(np.median(fail_counts))} / {fail_counts.max()}")

    # 2. Phi matrix and per-version mean phi
    phi = load_phi_matrix(pairwise_path, versions)
    mean_phi = mean_phi_per_version(phi, nan_policy="exclude")

    pool_rows = []
    for i, v in enumerate(versions):
        pool_rows.append({
            "rank_index": i,
            "version_id": v,
            "label": format_version_label(v),
            "agent": agent_by_vid.get(v, "?"),
            "language": lang_by_vid.get(v, "?"),
            "fail_count": int(fail_counts[i]),
            "fail_rate": float(fail_counts[i]) / T,
            "mean_phi_excl_nan": float(mean_phi[i]) if not math.isnan(mean_phi[i]) else float("nan"),
        })
    pool_df = pd.DataFrame(pool_rows)

    eligible_mask = np.ones(len(versions), dtype=bool)
    if not args.include_failure_free:
        eligible_mask &= fail_counts > 0
    eligible_mask &= ~np.isnan(mean_phi)  # need a defined ranking key
    eligible_indices = np.where(eligible_mask)[0]
    eligible_sorted = sorted(eligible_indices.tolist(), key=lambda i: float(mean_phi[i]))
    pool_indices = eligible_sorted[: args.pool_size]
    print(
        f"Pool size: {len(pool_indices)} (drawn from {eligible_mask.sum()} eligible "
        f"versions; failure-free {'included' if args.include_failure_free else 'excluded'})"
    )

    pool_df["in_pool_low_phi"] = False
    pool_df.loc[pool_indices, "in_pool_low_phi"] = True
    pool_df = pool_df.sort_values("mean_phi_excl_nan", na_position="last").reset_index(drop=True)
    pool_df.to_csv(output_dir / "n_version_units_pool.csv", index=False)

    # 3. Build the three families of units
    rng = np.random.default_rng(args.seed)

    def build_low_phi_units(unit_size: int) -> list[tuple[int, ...]]:
        if args.selection == "anchored":
            return select_units_anchored(
                phi, pool_indices, n=unit_size, num_units=args.num_units,
                mean_phi=mean_phi,
            )
        if args.selection == "disjoint":
            return select_units_disjoint(
                phi, pool_indices, n=unit_size, num_units=args.num_units,
            )
        return select_units(
            phi, pool_indices, n=unit_size, num_units=args.num_units, objective="min",
        )

    # High-phi baseline: anchor on the highest-mean-phi versions and pull
    # high-phi partners.  Symmetry with ``select_units_anchored`` keeps the
    # baseline equally diverse rather than collapsing onto one anchor pair.
    high_pool_indices = sorted(
        eligible_indices.tolist(),
        key=lambda i: float(mean_phi[i]),
        reverse=True,
    )[: args.pool_size]

    def select_units_anchored_max(unit_size: int) -> list[tuple[int, ...]]:
        # Mirror of select_units_anchored with the score sign flipped and the
        # same global de-duplication so anchors don't collapse onto a single
        # triple (the high-phi pool has many ties at φ ≈ 1.0).
        anchors = sorted(high_pool_indices, key=lambda i: -float(mean_phi[i]))[: args.num_units]
        seen: set[tuple[int, ...]] = set()
        units: list[tuple[int, ...]] = []
        for anchor in anchors:
            candidates = [v for v in high_pool_indices if v != anchor]
            scored: list[tuple[float, tuple[int, ...]]] = []
            for combo in itertools.combinations(candidates, unit_size - 1):
                triple = tuple(sorted((anchor,) + combo))
                scored.append((unit_max_phi(triple, phi), triple))
            scored.sort(key=lambda item: -item[0])
            for _score, triple in scored:
                if triple in seen:
                    continue
                seen.add(triple)
                units.append(triple)
                break
        return units

    # Optional LIC-failure-intersection family
    fault_events_path = (
        args.fault_events
        or campaign_path.parent / "fault_events.jsonl"
    ).resolve()
    lic_sets: dict[int, frozenset[int]] | None = None
    if fault_events_path.is_file():
        lic_sets = load_lic_failure_sets(
            fault_events_path, versions, include_fuv=args.lic_include_fuv,
        )
        non_empty = sum(1 for s in lic_sets.values() if s)
        print(
            f"Loaded LIC failure sets from {fault_events_path.name} "
            f"({non_empty}/{len(versions)} versions have ≥1 LIC mismatch; "
            f"include_fuv={args.lic_include_fuv})"
        )
    else:
        print(f"fault_events.jsonl not found at {fault_events_path}; "
              "skipping LIC-intersection family")

    families = {
        "low_phi_pool": build_low_phi_units(args.n),
        "low_phi_pool_sum": select_units_anchored(
            phi, pool_indices, n=args.n, num_units=args.num_units,
            mean_phi=mean_phi, score_fn=unit_sum_phi, minimise=True,
        ),
        "high_phi_baseline": select_units_anchored_max(args.n),
        "random_baseline": random_units(
            rng,
            list(range(len(versions))),
            n=args.n,
            num_units=args.num_units,
        ),
    }

    if lic_sets is not None:
        families["low_lic_intersection_pool"] = select_units_anchored_lic(
            pool_indices, n=args.n, num_units=args.num_units,
            mean_phi=mean_phi, lic_sets=lic_sets, phi=phi,
        )

    if args.also_n5 and len(pool_indices) >= 5:
        families["low_phi_pool_n5"] = build_low_phi_units(5)
        families["low_phi_pool_sum_n5"] = select_units_anchored(
            phi, pool_indices, n=5, num_units=args.num_units,
            mean_phi=mean_phi, score_fn=unit_sum_phi, minimise=True,
        )
        if lic_sets is not None:
            families["low_lic_intersection_pool_n5"] = select_units_anchored_lic(
                pool_indices, n=5, num_units=args.num_units,
                mean_phi=mean_phi, lic_sets=lic_sets, phi=phi,
            )

    # 4. Evaluate
    all_rows: list[dict] = []
    summary_rows: list[dict] = []
    for fam_name, units in families.items():
        rows = evaluate_units(
            units,
            family=fam_name,
            versions=versions,
            fail_sets_arrays=fail_sets_arrays,
            fail_counts=fail_counts,
            phi=phi,
            T=T,
            lic_sets=lic_sets,
        )
        all_rows.extend(rows)
        df = pd.DataFrame(rows)
        if df.empty:
            continue
        summary = family_summary(df, T=T)
        summary["family"] = fam_name
        summary_rows.append(summary)
        print(
            f"[{fam_name}] N={summary['n']} units={summary['n_units']} "
            f"mean obs={summary['mean_observed']:.2f} (pred={summary['mean_expected']:.4g}) "
            f"zero-failure units={summary['n_units_zero_failures']} "
            f"better-than-best-member={summary['n_units_better_than_best_member']}"
        )
        plot_unit_failures(
            df, output_dir / f"n_version_units_{fam_name}.pdf",
            T=T, family_label=fam_name,
        )

    # 5. Persist all-unit table and family summary
    units_df = pd.DataFrame(all_rows)
    units_df.to_csv(output_dir / "n_version_units.csv", index=False)
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(output_dir / "n_version_units_summary.csv", index=False)
    (output_dir / "n_version_units_summary.json").write_text(
        json.dumps(summary_rows, indent=2, default=str)
    )
    plot_family_summary(
        summary_df, output_dir / "n_version_units_summary.pdf", T=T,
    )
    write_units_markdown(
        units_df,
        output_dir / "n_version_units_table.md",
        T=T,
        family_order=list(families.keys()),
    )

    # 6. Headline log line answering RQ4
    main_summary = next(
        (s for s in summary_rows if s["family"] == "low_phi_pool"), None
    )
    if main_summary is not None:
        print()
        print("=" * 72)
        print("RQ4 headline (low-phi pool, N=3)")
        print("=" * 72)
        print(
            f"  units evaluated      : {main_summary['n_units']}\n"
            f"  zero-failure units   : {main_summary['n_units_zero_failures']}\n"
            f"  units better than    : {main_summary['n_units_better_than_best_member']}\n"
            f"    best single member \n"
            f"  mean observed K      : {main_summary['mean_observed']:.2f}\n"
            f"  mean predicted μ     : {main_summary['mean_expected']:.4g}\n"
            f"  mean K/μ             : "
            f"{(main_summary['mean_observed'] / main_summary['mean_expected']):.2f}"
            if main_summary['mean_expected'] > 0 else "  mean K/μ             : N/A"
        )
        print("=" * 72)


if __name__ == "__main__":
    main()
