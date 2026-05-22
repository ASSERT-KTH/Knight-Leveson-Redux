"""
RQ4 — No-oracle variant of N-version unit construction.

In the deployment scenario where no trusted oracle exists for the target
specification, individual versions cannot be labelled correct or incorrect
on a given test case, so the Pearson φ correlation between failure vectors
is not directly computable.

This script substitutes φ with a purely inter-version proxy: the
**pairwise output-disagreement rate**.  Two versions ``i`` and ``j``
disagree on test ``t`` whenever they produce different outputs on ``t``.
Crucially, this comparison is oracle-free: it asks only whether the
versions' outputs are identical, not whether either of them is correct.

In the experimental data the per-test outputs are recorded as diffs
against the oracle (in ``fault_events.jsonl``) plus a pass/fail bit (in
``campaign.csv``).  Two versions produce identical outputs on ``t`` iff
they both have *no* diff on ``t`` (both pass) **or** they both fail on
``t`` with the *same* diff payload.  No oracle label is needed to detect
this — only inter-version comparison of recorded outputs.  We exploit
this to compute pairwise disagreement counts as

    disagree(i, j) = fail_i + fail_j − cofail(i, j) − same_diff(i, j)

where ``same_diff(i, j)`` counts campaign cases on which ``i`` and ``j``
both fail with byte-equal diff payloads.

Selection.  We then mirror the anchored construction of
``analysis.build_n_version_units`` but invert the objective: anchors are
the 20 versions with the *highest* mean pairwise disagreement (the
"most diverse" versions); each anchor is paired with the 2 pool members
that **maximise** the within-unit *min* pairwise disagreement (i.e.
make the *worst* pair as different as possible).  Unit families:

    max_disagreement_pool          — primary, no-oracle anchored
    max_disagreement_pool_sum      — variant: maximise Σ pairwise disagreement
    min_disagreement_pool          — sanity baseline (least-diverse anchors)
    random_baseline                — uniform-random triples

Each unit is then evaluated against the oracle for reporting purposes
only — the *selection* never consults the oracle.

Outputs (in ``--output``, default = campaign dir):

    n_version_units_no_oracle.csv               # one row per unit
    n_version_units_no_oracle_summary.{csv,json}
    n_version_units_no_oracle_table.md
    n_version_units_no_oracle_<family>.pdf
    n_version_units_no_oracle_pool.csv          # version pool ranking
    output_disagreement_matrix.npz              # cached (N×N) counts

Usage:
    python -m analysis.build_n_version_units_no_oracle \\
        --campaign results/main-spec-3/campaign.csv \\
        --num-units 20 --n 3 --pool-size 25
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.analyze_results import (  # noqa: E402
    analysis_version_ids,
    format_version_label,
    load_version_language_agent,
    read_campaign_version_order,
)
from analysis.build_n_version_units import (  # noqa: E402
    _format_phi_label,
    evaluate_units,
    family_summary,
    load_failure_sets,
    plot_family_summary,
    plot_unit_failures,
    random_units,
    write_units_markdown,
)


# ---------------------------------------------------------------------------
# Output-disagreement matrix
# ---------------------------------------------------------------------------

def _diff_hash(diff: dict) -> str:
    """Stable hash of a diff payload.  Two version outputs on a given test
    are equal iff their diffs are equal, so this hash uniquely identifies
    the version's output equivalence class on that test."""
    norm = {
        "cmv": sorted(int(x) for x in (diff.get("cmv_mismatch_indices") or [])),
        "fuv": sorted(int(x) for x in (diff.get("fuv_mismatch_indices") or [])),
        "pum": sorted(
            tuple(int(x) for x in cell)
            for cell in (diff.get("pum_mismatch_cells") or [])
        ),
        "launch": bool(diff.get("launch_mismatch", False)),
        "malformed": bool(diff.get("malformed_actual", False)),
    }
    blob = json.dumps(norm, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.blake2b(blob, digest_size=16).hexdigest()


def compute_pair_cofailure_matrix(
    fail_sets: list[np.ndarray], N: int
) -> np.ndarray:
    """``cofail[i, j]`` = |fail_set_i ∩ fail_set_j|.  Computed by sorted
    array intersection so it is fast even with sparse failure vectors.
    """
    cofail = np.zeros((N, N), dtype=np.int64)
    for i in range(N):
        a = fail_sets[i]
        if a.size == 0:
            continue
        cofail[i, i] = a.size
        for j in range(i + 1, N):
            b = fail_sets[j]
            if b.size == 0:
                continue
            inter = np.intersect1d(a, b, assume_unique=True).size
            cofail[i, j] = inter
            cofail[j, i] = inter
    return cofail


def compute_same_diff_matrix(
    fault_events_path: Path, versions: list[str], N: int
) -> np.ndarray:
    """``same_diff[i, j]`` = #{t: i and j both fail on t with byte-equal diffs}.

    Streams ``fault_events.jsonl`` once and groups consecutive rows by
    ``test_id``.  Within each test the failing versions are bucketed by
    diff hash; for every bucket of size ≥ 2, all pairs in the bucket gain
    one ``same_diff`` count.

    Note: rows are not strictly required to be sorted by test_id — we
    accumulate via a dict of ``test_id → list[(version_idx, hash)]`` and
    flush once per test.  In practice the file is already test-id sorted.
    """
    idx = {v: i for i, v in enumerate(versions)}
    same = np.zeros((N, N), dtype=np.int64)
    by_test: dict[int, list[tuple[int, str]]] = defaultdict(list)

    with fault_events_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            vid = rec.get("version_id")
            if vid not in idx:
                continue
            tid = int(rec["test_id"])
            h = _diff_hash(rec.get("diff") or {})
            by_test[tid].append((idx[vid], h))

    for items in by_test.values():
        if len(items) < 2:
            continue
        groups: dict[str, list[int]] = defaultdict(list)
        for vi, h in items:
            groups[h].append(vi)
        for vs in groups.values():
            if len(vs) < 2:
                continue
            for ii in range(len(vs)):
                for jj in range(ii + 1, len(vs)):
                    a, b = vs[ii], vs[jj]
                    if a > b:
                        a, b = b, a
                    same[a, b] += 1
                    same[b, a] += 1
    return same


def compute_disagreement_matrix(
    *,
    fail_counts: np.ndarray,
    cofail: np.ndarray,
    same_diff: np.ndarray,
    T: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return ``(disagree_counts, disagree_rate)``.

    Each entry ``[i, j]`` = #{tests where i and j produce different outputs}
    derived oracle-free as ``fail_i + fail_j − cofail − same_diff``.
    The diagonal is set to 0 by convention.
    """
    N = fail_counts.size
    fi = fail_counts.reshape(-1, 1)
    fj = fail_counts.reshape(1, -1)
    disagree = fi + fj - cofail - same_diff
    np.fill_diagonal(disagree, 0)
    if (disagree < 0).any():
        raise RuntimeError(
            "Negative disagreement count — internal accounting error."
        )
    rate = disagree.astype(np.float64) / max(T, 1)
    return disagree, rate


# ---------------------------------------------------------------------------
# Anchored selection on disagreement
# ---------------------------------------------------------------------------

def unit_min_disagree_rate(triple: tuple[int, ...], rate: np.ndarray) -> float:
    """Worst-pair disagreement rate within the unit (min over pairs)."""
    vals = [rate[a, b] for a, b in itertools.combinations(triple, 2)]
    return min(vals) if vals else float("nan")


def unit_max_disagree_rate(triple: tuple[int, ...], rate: np.ndarray) -> float:
    vals = [rate[a, b] for a, b in itertools.combinations(triple, 2)]
    return max(vals) if vals else float("nan")


def unit_sum_disagree_rate(triple: tuple[int, ...], rate: np.ndarray) -> float:
    return float(sum(rate[a, b] for a, b in itertools.combinations(triple, 2)))


def select_units_anchored_disagree(
    pool: list[int],
    *,
    n: int,
    num_units: int,
    mean_disagree_rate: np.ndarray,
    rate: np.ndarray,
    objective: str = "min",
    minimise: bool = False,
) -> list[tuple[int, ...]]:
    """Anchored construction with a disagreement-rate objective.

    Anchors iterate over ``pool`` in descending mean-disagreement order
    (the "most diverse" versions first) when ``minimise=False``, or
    ascending order when ``minimise=True`` (sanity-baseline use).
    For each anchor, candidate triples are ranked by:

      objective="min": within-unit *minimum* pairwise disagreement
                      (we want the worst-pair to still be as diverse as
                      possible — analogous to "min max φ").
      objective="sum": within-unit *sum* of pairwise disagreement.

    Globally de-duplicated against earlier anchors.
    """
    if len(pool) < n:
        raise ValueError(
            f"Need at least n={n} versions in the pool to build a unit; got {len(pool)}"
        )
    if objective == "min":
        score = unit_min_disagree_rate
    elif objective == "sum":
        score = unit_sum_disagree_rate
    else:
        raise ValueError(f"unknown objective {objective!r}")

    pool_sorted = sorted(pool, key=lambda i: float(mean_disagree_rate[i]),
                         reverse=not minimise)
    anchors = pool_sorted[:num_units]
    sign = 1.0 if minimise else -1.0  # we want maximum by default
    seen: set[tuple[int, ...]] = set()
    units: list[tuple[int, ...]] = []
    for anchor in anchors:
        candidates = [v for v in pool if v != anchor]
        scored: list[tuple[float, tuple[int, ...]]] = []
        for combo in itertools.combinations(candidates, n - 1):
            triple = tuple(sorted((anchor,) + combo))
            scored.append((sign * score(triple, rate), triple))
        scored.sort(key=lambda item: item[0])
        for _s, triple in scored:
            if triple in seen:
                continue
            seen.add(triple)
            units.append(triple)
            break
    return units


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument(
        "--fault-events",
        type=Path,
        default=None,
        help="Path to fault_events.jsonl (default: <campaign-dir>/fault_events.jsonl)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output dir (default: campaign-dir)",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=None,
        help=".npz cache for failure-set bitmaps (shared with build_n_version_units)",
    )
    parser.add_argument(
        "--disagree-cache",
        type=Path,
        default=None,
        help=".npz cache for the (N×N) disagreement matrix",
    )
    parser.add_argument("--num-units", type=int, default=20)
    parser.add_argument(
        "--n", type=int, default=3,
        help="Versions per unit",
    )
    parser.add_argument(
        "--pool-size", type=int, default=25,
        help="Top-K versions by mean pairwise disagreement to use as the candidate pool",
    )
    parser.add_argument(
        "--also-n5",
        action="store_true",
        help="Also evaluate N=5 units.",
    )
    parser.add_argument(
        "--seed", type=int, default=20260507,
        help="Random-baseline seed",
    )
    args = parser.parse_args()

    campaign_path: Path = args.campaign.resolve()
    output_dir = (args.output or campaign_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    fault_events_path = (
        args.fault_events or campaign_path.parent / "fault_events.jsonl"
    ).resolve()
    cache_path = (
        args.cache or campaign_path.parent / "failure_sets.npz"
    ).resolve()
    disagree_cache = (
        args.disagree_cache
        or campaign_path.parent / "output_disagreement_matrix.npz"
    ).resolve()

    if not campaign_path.is_file():
        raise SystemExit(f"campaign.csv not found: {campaign_path}")
    if not fault_events_path.is_file():
        raise SystemExit(f"fault_events.jsonl not found: {fault_events_path}")

    versions = analysis_version_ids(
        campaign_path, read_campaign_version_order(campaign_path)
    )
    lang_by_vid, agent_by_vid = load_version_language_agent(campaign_path, versions)
    N = len(versions)
    print(f"Admitted versions: {N}")

    # 1. Per-version failure bitmaps (reuses cache from build_n_version_units)
    T, fail_sets_dict = load_failure_sets(
        campaign_path, versions, cache_path=cache_path
    )
    fail_sets = [fail_sets_dict[v] for v in versions]
    fail_counts = np.asarray([a.size for a in fail_sets], dtype=np.int64)

    # 2. Output-disagreement matrix (cached)
    if disagree_cache.is_file():
        data = np.load(disagree_cache, allow_pickle=True)
        cached_versions = data["versions"].tolist()
        if cached_versions == versions:
            disagree = data["disagree"]
            same_diff = data["same_diff"]
            cofail = data["cofail"]
            print(f"Loaded disagreement matrix from {disagree_cache.name}")
        else:
            disagree = same_diff = cofail = None
    else:
        disagree = same_diff = cofail = None

    if disagree is None:
        print("Computing pairwise output-disagreement matrix...")
        cofail = compute_pair_cofailure_matrix(fail_sets, N)
        same_diff = compute_same_diff_matrix(fault_events_path, versions, N)
        disagree, _ = compute_disagreement_matrix(
            fail_counts=fail_counts, cofail=cofail, same_diff=same_diff, T=T,
        )
        np.savez(
            disagree_cache,
            versions=np.asarray(versions, dtype=object),
            T=np.int64(T),
            fail_counts=fail_counts,
            cofail=cofail,
            same_diff=same_diff,
            disagree=disagree,
        )
        print(f"Cached disagreement matrix at {disagree_cache}")

    rate = disagree.astype(np.float64) / float(T)
    # Mean pairwise disagreement per version (excluding the diagonal, which
    # is 0 by construction and would otherwise bias the per-row mean down
    # by a factor of N/(N-1)).
    rate_no_diag = rate.copy()
    np.fill_diagonal(rate_no_diag, np.nan)
    mean_rate = np.nanmean(rate_no_diag, axis=1)

    # 3. Pool: top-K by *highest* mean disagreement.  We do not use any
    # oracle label for pool selection; we only consult inter-version output
    # comparisons.  Versions whose outputs never deviate from the rest
    # (e.g. failure-free versions, which agree with every other passing
    # version on every test) end up with the lowest mean disagreement and
    # are therefore *not* in the diversity pool.
    eligible_indices = np.arange(N)
    eligible_sorted = sorted(eligible_indices, key=lambda i: -float(mean_rate[i]))
    pool_indices = eligible_sorted[: args.pool_size]
    print(
        f"Pool size: {len(pool_indices)} (top by mean pairwise disagreement)"
    )

    pool_rows = []
    for i, v in enumerate(versions):
        pool_rows.append({
            "version_id": v,
            "label": format_version_label(v),
            "agent": agent_by_vid.get(v, "?"),
            "language": lang_by_vid.get(v, "?"),
            "fail_count": int(fail_counts[i]),
            "mean_disagree_rate": float(mean_rate[i]),
            "in_pool": i in set(pool_indices),
        })
    pool_df = pd.DataFrame(pool_rows).sort_values(
        "mean_disagree_rate", ascending=False
    ).reset_index(drop=True)
    pool_df.to_csv(output_dir / "n_version_units_no_oracle_pool.csv", index=False)

    # 4. Build families
    rng = np.random.default_rng(args.seed)
    families = {
        "max_disagreement_pool": select_units_anchored_disagree(
            pool_indices, n=args.n, num_units=args.num_units,
            mean_disagree_rate=mean_rate, rate=rate, objective="min",
        ),
        "max_disagreement_pool_sum": select_units_anchored_disagree(
            pool_indices, n=args.n, num_units=args.num_units,
            mean_disagree_rate=mean_rate, rate=rate, objective="sum",
        ),
        "min_disagreement_pool": select_units_anchored_disagree(
            sorted(eligible_indices,
                   key=lambda i: float(mean_rate[i]))[: args.pool_size],
            n=args.n, num_units=args.num_units,
            mean_disagree_rate=mean_rate, rate=rate, objective="min",
            minimise=True,
        ),
        "random_baseline": random_units(
            rng, list(range(N)), n=args.n, num_units=args.num_units,
        ),
    }
    if args.also_n5 and len(pool_indices) >= 5:
        families["max_disagreement_pool_n5"] = select_units_anchored_disagree(
            pool_indices, n=5, num_units=args.num_units,
            mean_disagree_rate=mean_rate, rate=rate, objective="min",
        )

    # 5. Evaluate (oracle is consulted *only* for reporting K and μ —
    # never for selection above).
    phi_dummy = np.full((N, N), np.nan, dtype=np.float64)
    # We don't load φ in this script (the whole point is to avoid the
    # oracle).  evaluate_units uses phi only for diagnostic columns; pass
    # NaN so the resulting rows simply report NaN for max/sum/within-unit φ.
    all_rows: list[dict] = []
    summary_rows: list[dict] = []
    for fam_name, units in families.items():
        rows = evaluate_units(
            units,
            family=fam_name,
            versions=versions,
            fail_sets_arrays=fail_sets,
            fail_counts=fail_counts,
            phi=phi_dummy,
            T=T,
        )
        # Augment each row with the disagreement-based selection metrics
        for row, triple in zip(rows, units):
            d_min = unit_min_disagree_rate(triple, rate)
            d_max = unit_max_disagree_rate(triple, rate)
            d_sum = unit_sum_disagree_rate(triple, rate)
            row["min_pairwise_disagree_rate"] = d_min
            row["max_pairwise_disagree_rate"] = d_max
            row["sum_pairwise_disagree_rate"] = d_sum
            row["min_pairwise_disagree_count"] = int(round(d_min * T))
            row["sum_pairwise_disagree_count"] = int(round(d_sum * T))
        all_rows.extend(rows)
        df = pd.DataFrame(rows)
        if df.empty:
            continue
        summary = family_summary(df, T=T)
        summary["family"] = fam_name
        summary["mean_min_disagree_rate"] = float(df["min_pairwise_disagree_rate"].mean())
        summary["mean_sum_disagree_rate"] = float(df["sum_pairwise_disagree_rate"].mean())
        summary_rows.append(summary)
        print(
            f"[{fam_name}] N={summary['n']} units={summary['n_units']} "
            f"mean K={summary['mean_observed']:.2f} (μ={summary['mean_expected']:.4g}) "
            f"mean min-disagree={summary['mean_min_disagree_rate']:.4g} "
            f"better-than-best-member={summary['n_units_better_than_best_member']}"
        )
        plot_unit_failures(
            df, output_dir / f"n_version_units_no_oracle_{fam_name}.pdf",
            T=T, family_label=fam_name,
        )

    units_df = pd.DataFrame(all_rows)
    units_df.to_csv(output_dir / "n_version_units_no_oracle.csv", index=False)
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(output_dir / "n_version_units_no_oracle_summary.csv", index=False)
    (output_dir / "n_version_units_no_oracle_summary.json").write_text(
        json.dumps(summary_rows, indent=2, default=str)
    )
    plot_family_summary(
        summary_df, output_dir / "n_version_units_no_oracle_summary.pdf", T=T,
    )

    write_no_oracle_markdown(
        units_df,
        output_dir / "n_version_units_no_oracle_table.md",
        T=T,
        family_order=list(families.keys()),
    )

    main_summary = next(
        (s for s in summary_rows if s["family"] == "max_disagreement_pool"), None
    )
    if main_summary is not None:
        print()
        print("=" * 72)
        print("RQ4 (no-oracle) headline — max_disagreement_pool, N=3")
        print("=" * 72)
        print(
            f"  units evaluated      : {main_summary['n_units']}\n"
            f"  zero-K units         : {main_summary['n_units_zero_failures']}\n"
            f"  units better than    : {main_summary['n_units_better_than_best_member']}\n"
            f"    best single member \n"
            f"  mean observed K      : {main_summary['mean_observed']:.2f}\n"
            f"  mean predicted μ     : {main_summary['mean_expected']:.4g}\n"
            f"  mean min-disagree    : {main_summary['mean_min_disagree_rate']:.4g}"
        )
        print("=" * 72)


def write_no_oracle_markdown(
    units_df: pd.DataFrame,
    output_path: Path,
    *,
    T: int,
    family_order: list[str],
) -> None:
    if units_df.empty:
        return
    lines: list[str] = [
        "# RQ4 (no-oracle) — N-version units selected by output disagreement",
        "",
        f"All counts are over a shared campaign of T = {T:,} test cases.",
        "Selection used **only** inter-version output comparisons; the oracle "
        "is consulted afterwards solely to compute the *Observed K* and "
        "*Predicted μ* columns reported below.  *min disagree* and *Σ disagree* "
        "are within-unit statistics over pairwise output disagreement rates.",
        "",
    ]

    descriptions = {
        "max_disagreement_pool": (
            "Anchored construction: 20 versions with the **highest** mean "
            "pairwise output-disagreement rate act as anchors; each anchor is "
            "paired with two pool members maximising the *minimum* pairwise "
            "disagreement within the unit (analog of `min max φ` from the "
            "oracle-aware analysis)."
        ),
        "max_disagreement_pool_sum": (
            "Same anchored pool as `max_disagreement_pool`, but the per-anchor "
            "objective is to maximise the **sum** of the three pairwise "
            "disagreement rates."
        ),
        "max_disagreement_pool_n5": (
            "Same as `max_disagreement_pool` with N = 5."
        ),
        "min_disagreement_pool": (
            "Sanity baseline: anchors are the versions with the *lowest* mean "
            "pairwise disagreement; each is completed with partners minimising "
            "the within-unit *min* pairwise disagreement.  Expected to mimic "
            "the high-φ baseline of the oracle-aware analysis."
        ),
        "random_baseline": (
            "Sanity baseline: 20 unit triples drawn uniformly at random from "
            "all admitted versions."
        ),
    }

    for family in family_order:
        sub = units_df[units_df["family"] == family].reset_index(drop=True)
        if sub.empty:
            continue
        n_versions = int(sub["n"].iloc[0])
        member_cols = max(
            len(str(row["member_labels"]).split("|"))
            for _, row in sub.iterrows()
        )
        lines.append(f"## Family `{family}` (N = {n_versions}, {len(sub)} units)")
        lines.append("")
        if family in descriptions:
            lines.append(descriptions[family])
            lines.append("")

        header = ["Unit"]
        for k in range(member_cols):
            header.append(f"Member {k+1}")
            header.append(f"f{k+1}")
        header.extend([
            "min disagree", "Σ disagree", "Observed K", "Predicted μ", "K/μ",
        ])
        lines.append("| " + " | ".join(header) + " |")
        right = {
            "Unit", "min disagree", "Σ disagree",
            "Observed K", "Predicted μ", "K/μ",
        }
        lines.append(
            "|" + "|".join(
                ["---:" if (h.startswith("f") or h in right) else "---"
                 for h in header]
            ) + "|"
        )

        sub = sub.sort_values("observed_unit_fail_count").reset_index(drop=True)
        for i, row in sub.iterrows():
            members = [
                part for part in str(row["member_labels"]).split("|") if part
            ]
            counts = [
                part for part in str(row["member_fail_counts"]).split("|") if part
            ]
            cells = [f"U{i+1}"]
            for k in range(member_cols):
                if k < len(members):
                    cells.append(f"`{members[k]}`")
                    cells.append(counts[k] if k < len(counts) else "")
                else:
                    cells.append("")
                    cells.append("")
            cells.append(_format_phi_label(float(row["min_pairwise_disagree_rate"])))
            cells.append(_format_phi_label(float(row["sum_pairwise_disagree_rate"])))
            cells.append(f"{int(row['observed_unit_fail_count'])}")
            cells.append(f"{float(row['expected_unit_fail_count']):.3g}")
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


if __name__ == "__main__":
    main()
