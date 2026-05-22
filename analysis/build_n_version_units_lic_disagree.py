"""
RQ4 (no-oracle, LIC-output variant) — N-version unit construction by
maximising per-LIC pairwise output disagreement.

Setup
-----
``pipeline.run_campaign_lic`` re-executed every admitted version on a
mini-campaign (default 10 000 cases, sharing the seed with the full
campaign so test ids are aligned) and recorded each version's full
15-bit CMV (Conditions Met Vector) output per case.  *No oracle is
consulted* during selection — only inter-version comparisons of the
recorded CMV bits.

For every test ``t`` and ordered pair of versions ``(i, j)`` we form the
15-bit XOR ``D_{ij}(t) = CMV_i(t) ⊕ CMV_j(t)``.  This vector flags the
LIC bits on which the two versions output different values.  We
aggregate two pairwise summary statistics from the (T × 15) tensor:

    bit_disagree[i, j]  = mean over (t, b) of D_{ij}(t)[b]
                         = total Hamming distance / (T · 15)
    any_disagree[i, j]  = mean over t of (D_{ij}(t) ≠ 0)
                         = fraction of tests on which the two CMVs differ

The first is a fine-grained, per-condition diversity measure; the second
matches the existing ``output_disagreement_matrix`` semantics.  Selection
uses ``bit_disagree`` by default (the user request — "for every test
case for every pair we create a disagreement boolean vector ... pairs
with the highest average disagree").

Selection mirrors the anchored construction of
``analysis.build_n_version_units`` but inverted: anchors are the
``--num-units`` versions with the *highest* mean pairwise per-bit
disagreement, and each anchor is completed with the ``n-1`` pool members
that maximise the within-unit *minimum* pairwise disagreement (the
no-oracle analog of "min max φ").  Globally de-duplicated.

Reporting (oracle is consulted *only* for the K / μ columns; never for
selection):
    * Observed unit failure count K on the **full 1 M-case campaign**
      (uses cached ``failure_sets.npz``).
    * Independence prediction μ from per-member failure rates.
    * Within-unit min / max / Σ pairwise CMV-bit-disagreement.

Outputs (in ``--output``, default = campaign dir):

    n_version_units_lic_disagree.csv               # one row per unit
    n_version_units_lic_disagree_summary.{csv,json}
    n_version_units_lic_disagree_table.md
    n_version_units_lic_disagree_<family>.pdf
    n_version_units_lic_disagree_pool.csv          # pool ranking
    cmv_disagreement_matrix.npz                    # cached tensors

Usage:
    python -m analysis.build_n_version_units_lic_disagree \\
        --cmv      results/main-spec-3/cmv_outputs.npz \\
        --campaign results/main-spec-3/campaign.csv \\
        --num-units 20 --n 3 --pool-size 25
"""
from __future__ import annotations

import argparse
import itertools
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
# Pairwise CMV disagreement (no oracle)
# ---------------------------------------------------------------------------

# 15 LICs occupy bits 0..14; bits 15..15 of the uint16 packing are zero.
_BIT_MASK_15 = np.uint16((1 << 15) - 1)
_POPCOUNT_LUT = np.array(
    [bin(i).count("1") for i in range(1 << 15)], dtype=np.uint8
)


def _popcount15(arr: np.ndarray) -> np.ndarray:
    """Vectorised popcount on uint16 values whose bits 15+ are zero."""
    return _POPCOUNT_LUT[arr.astype(np.int64) & int(_BIT_MASK_15)]


def compute_cmv_disagreement(
    cmv_packed: np.ndarray,
    valid: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Compute pairwise CMV disagreement statistics from the mini-campaign.

    Inputs
    ------
    cmv_packed : (V, T) uint16
        Bit ``b`` of ``cmv_packed[v, t]`` = CMV[b] of version v on test t.
    valid : (V, T) uint8
        ``1`` if the version produced a well-formed (cmv, pum, fuv,
        launch) tuple; ``0`` otherwise.  Pairs only contribute on tests
        where *both* versions are valid.

    Returns
    -------
    bit_disagree : (V, V) float64
        Mean per-(test, bit) disagreement rate over jointly-valid tests.
        The diagonal is 0 by convention.
    any_disagree : (V, V) float64
        Fraction of jointly-valid tests on which the two CMVs differ in
        at least one bit (Hamming distance > 0).
    pair_valid_count : (V, V) int64
        Number of tests where both versions produced a valid CMV.
    pair_hamming_total : (V, V) int64
        Sum over tests of Hamming distance between the two CMVs.
    """
    V, T = cmv_packed.shape
    valid_b = valid.astype(bool)
    bit_disagree = np.zeros((V, V), dtype=np.float64)
    any_disagree = np.zeros((V, V), dtype=np.float64)
    pair_valid_count = np.zeros((V, V), dtype=np.int64)
    pair_hamming_total = np.zeros((V, V), dtype=np.int64)

    for i in range(V):
        ci = cmv_packed[i]
        vi = valid_b[i]
        for j in range(i + 1, V):
            cj = cmv_packed[j]
            vj = valid_b[j]
            both = vi & vj
            n = int(both.sum())
            if n == 0:
                continue
            xor = (ci ^ cj) & _BIT_MASK_15
            xor_valid = xor[both]
            ham = _popcount15(xor_valid)
            ham_total = int(ham.sum())
            any_disagree_count = int((xor_valid != 0).sum())
            br = ham_total / (n * 15.0)
            ar = any_disagree_count / n
            bit_disagree[i, j] = br
            bit_disagree[j, i] = br
            any_disagree[i, j] = ar
            any_disagree[j, i] = ar
            pair_valid_count[i, j] = n
            pair_valid_count[j, i] = n
            pair_hamming_total[i, j] = ham_total
            pair_hamming_total[j, i] = ham_total

    return bit_disagree, any_disagree, pair_valid_count, pair_hamming_total


# ---------------------------------------------------------------------------
# Anchored selection
# ---------------------------------------------------------------------------

def unit_min_pair(triple: tuple[int, ...], M: np.ndarray) -> float:
    return float(min(M[a, b] for a, b in itertools.combinations(triple, 2)))


def unit_max_pair(triple: tuple[int, ...], M: np.ndarray) -> float:
    return float(max(M[a, b] for a, b in itertools.combinations(triple, 2)))


def unit_sum_pair(triple: tuple[int, ...], M: np.ndarray) -> float:
    return float(sum(M[a, b] for a, b in itertools.combinations(triple, 2)))


def select_units_anchored_max(
    pool: list[int],
    *,
    n: int,
    num_units: int,
    mean_score: np.ndarray,
    pair_score: np.ndarray,
    objective: str = "min",
    minimise: bool = False,
) -> list[tuple[int, ...]]:
    """One unit per anchor, globally de-duplicated.

    Anchors iterate over ``pool`` in descending ``mean_score`` order
    (highest mean per-version disagreement first) when ``minimise``
    is False, ascending otherwise (sanity baseline).  For each anchor the
    candidate triples are scored by the ``pair_score`` aggregate
    (``min`` / ``max`` / ``sum``) and the best triple not yet selected
    by an earlier anchor wins.
    """
    if len(pool) < n:
        raise ValueError(
            f"Need at least n={n} versions in the pool to build a unit; got {len(pool)}"
        )
    score_fn = {
        "min": unit_min_pair,
        "max": unit_max_pair,
        "sum": unit_sum_pair,
    }[objective]
    pool_sorted = sorted(pool, key=lambda i: float(mean_score[i]),
                         reverse=not minimise)
    anchors = pool_sorted[:num_units]
    sign = 1.0 if minimise else -1.0  # default = maximise
    seen: set[tuple[int, ...]] = set()
    units: list[tuple[int, ...]] = []
    for anchor in anchors:
        candidates = [v for v in pool if v != anchor]
        scored: list[tuple[float, tuple[int, ...]]] = []
        for combo in itertools.combinations(candidates, n - 1):
            triple = tuple(sorted((anchor,) + combo))
            scored.append((sign * score_fn(triple, pair_score), triple))
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
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--cmv", type=Path, required=True,
        help="cmv_outputs.npz from pipeline.run_campaign_lic",
    )
    p.add_argument(
        "--campaign", type=Path, required=True,
        help="campaign.csv used for K/μ reporting (oracle-aware, but not "
             "consulted during selection)",
    )
    p.add_argument(
        "--output", type=Path, default=None,
        help="Output dir (default: campaign dir)",
    )
    p.add_argument(
        "--cache", type=Path, default=None,
        help=".npz failure-set cache shared with build_n_version_units",
    )
    p.add_argument(
        "--disagree-cache", type=Path, default=None,
        help=".npz cache for the (V×V) CMV-disagreement matrices",
    )
    p.add_argument("--num-units", type=int, default=20)
    p.add_argument("--n", type=int, default=3, help="Versions per unit")
    p.add_argument(
        "--pool-size", type=int, default=25,
        help="Top-K versions by mean per-bit pairwise disagreement",
    )
    p.add_argument(
        "--also-n5", action="store_true",
        help="Also evaluate N=5 units.",
    )
    p.add_argument("--seed", type=int, default=20260507)
    args = p.parse_args()

    cmv_path = args.cmv.resolve()
    campaign_path = args.campaign.resolve()
    output_dir = (args.output or campaign_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_path = (
        args.cache or campaign_path.parent / "failure_sets.npz"
    ).resolve()
    disagree_cache = (
        args.disagree_cache
        or campaign_path.parent / "cmv_disagreement_matrix.npz"
    ).resolve()

    if not cmv_path.is_file():
        raise SystemExit(
            f"cmv_outputs.npz not found: {cmv_path}\n"
            "Run pipeline.run_campaign_lic first."
        )
    if not campaign_path.is_file():
        raise SystemExit(f"campaign.csv not found: {campaign_path}")

    # --- 1. Load mini-campaign CMV outputs ---------------------------------
    print(f"Loading {cmv_path.name}...")
    cmv_data = np.load(cmv_path, allow_pickle=True)
    cmv_versions: list[str] = cmv_data["versions"].tolist()
    cmv_packed: np.ndarray = cmv_data["cmv_packed"]
    valid: np.ndarray = cmv_data["valid"]
    T_mini = int(cmv_data["n"])
    seed_mini = int(cmv_data["seed"])
    print(
        f"  V={len(cmv_versions)} versions · T_mini={T_mini} cases "
        f"(seed={seed_mini})"
    )

    # --- 2. Align with the campaign.csv version order ----------------------
    big_versions = analysis_version_ids(
        campaign_path, read_campaign_version_order(campaign_path)
    )
    lang_by_vid, agent_by_vid = load_version_language_agent(
        campaign_path, big_versions
    )
    common = [v for v in big_versions if v in set(cmv_versions)]
    if len(common) != len(big_versions):
        missing = set(big_versions) - set(cmv_versions)
        print(
            f"  warning: {len(missing)} admitted version(s) absent from CMV "
            f"snapshot — restricting analysis to {len(common)} shared versions."
        )
    versions = common
    cmv_idx = {v: i for i, v in enumerate(cmv_versions)}
    perm = np.asarray([cmv_idx[v] for v in versions], dtype=np.int64)
    cmv_packed = cmv_packed[perm]
    valid = valid[perm]
    N = len(versions)

    # --- 3. Pairwise CMV disagreement (cached) -----------------------------
    bit_disagree = any_disagree = pair_valid = pair_hamming = None
    if disagree_cache.is_file():
        d = np.load(disagree_cache, allow_pickle=True)
        if d["versions"].tolist() == versions and int(d["T_mini"]) == T_mini:
            bit_disagree = d["bit_disagree"]
            any_disagree = d["any_disagree"]
            pair_valid = d["pair_valid"]
            pair_hamming = d["pair_hamming"]
            print(f"Loaded CMV-disagreement matrices from {disagree_cache.name}")
    if bit_disagree is None:
        print("Computing pairwise CMV-disagreement matrices...")
        bit_disagree, any_disagree, pair_valid, pair_hamming = (
            compute_cmv_disagreement(cmv_packed, valid)
        )
        np.savez(
            disagree_cache,
            versions=np.asarray(versions, dtype=object),
            T_mini=np.int64(T_mini),
            seed_mini=np.int64(seed_mini),
            bit_disagree=bit_disagree,
            any_disagree=any_disagree,
            pair_valid=pair_valid,
            pair_hamming=pair_hamming,
        )
        print(f"Cached at {disagree_cache}")

    # Mean per-version: ignore diagonal (NaN-mask).
    bit_off = bit_disagree.copy()
    np.fill_diagonal(bit_off, np.nan)
    any_off = any_disagree.copy()
    np.fill_diagonal(any_off, np.nan)
    mean_bit = np.nanmean(bit_off, axis=1)
    mean_any = np.nanmean(any_off, axis=1)

    # --- 4. Pool: top-K by mean per-bit pairwise disagreement --------------
    eligible = list(range(N))
    pool_sorted = sorted(eligible, key=lambda i: -float(mean_bit[i]))
    pool_indices = pool_sorted[: args.pool_size]
    print(
        f"Pool size: {len(pool_indices)} (top by mean per-bit pairwise "
        f"CMV-disagreement on the {T_mini}-case mini-campaign)"
    )

    # Pool CSV
    pool_rows = []
    for i, v in enumerate(versions):
        pool_rows.append({
            "version_id": v,
            "label": format_version_label(v),
            "agent": agent_by_vid.get(v, "?"),
            "language": lang_by_vid.get(v, "?"),
            "mean_bit_disagree_rate": float(mean_bit[i]),
            "mean_any_disagree_rate": float(mean_any[i]),
            "in_pool": i in set(pool_indices),
        })
    pool_df = pd.DataFrame(pool_rows).sort_values(
        "mean_bit_disagree_rate", ascending=False
    ).reset_index(drop=True)
    pool_df.to_csv(
        output_dir / "n_version_units_lic_disagree_pool.csv", index=False
    )

    # --- 5. Build families -------------------------------------------------
    rng = np.random.default_rng(args.seed)
    families: dict[str, list[tuple[int, ...]]] = {
        "max_lic_disagree_pool": select_units_anchored_max(
            pool_indices, n=args.n, num_units=args.num_units,
            mean_score=mean_bit, pair_score=bit_disagree, objective="min",
        ),
        "max_lic_disagree_pool_sum": select_units_anchored_max(
            pool_indices, n=args.n, num_units=args.num_units,
            mean_score=mean_bit, pair_score=bit_disagree, objective="sum",
        ),
        "min_lic_disagree_pool": select_units_anchored_max(
            sorted(eligible, key=lambda i: float(mean_bit[i]))[: args.pool_size],
            n=args.n, num_units=args.num_units,
            mean_score=mean_bit, pair_score=bit_disagree, objective="min",
            minimise=True,
        ),
        "random_baseline": random_units(
            rng, list(range(N)), n=args.n, num_units=args.num_units,
        ),
    }
    if args.also_n5 and len(pool_indices) >= 5:
        families["max_lic_disagree_pool_n5"] = select_units_anchored_max(
            pool_indices, n=5, num_units=args.num_units,
            mean_score=mean_bit, pair_score=bit_disagree, objective="min",
        )

    # --- 6. Evaluate against the FULL 1M-case campaign ---------------------
    T_full, fail_sets_dict = load_failure_sets(
        campaign_path, versions, cache_path=cache_path,
    )
    fail_sets_arrays = [fail_sets_dict[v] for v in versions]
    fail_counts = np.asarray([a.size for a in fail_sets_arrays], dtype=np.int64)

    # Pass NaN φ — selection used no oracle and we don't load the
    # phi matrix here.  The φ columns remain NaN in the output.
    phi_dummy = np.full((N, N), np.nan, dtype=np.float64)
    all_rows: list[dict] = []
    summary_rows: list[dict] = []
    for fam_name, units in families.items():
        rows = evaluate_units(
            units,
            family=fam_name,
            versions=versions,
            fail_sets_arrays=fail_sets_arrays,
            fail_counts=fail_counts,
            phi=phi_dummy,
            T=T_full,
        )
        for row, triple in zip(rows, units):
            row["min_bit_disagree_rate"] = unit_min_pair(triple, bit_disagree)
            row["max_bit_disagree_rate"] = unit_max_pair(triple, bit_disagree)
            row["sum_bit_disagree_rate"] = unit_sum_pair(triple, bit_disagree)
            row["min_any_disagree_rate"] = unit_min_pair(triple, any_disagree)
            row["max_any_disagree_rate"] = unit_max_pair(triple, any_disagree)
            row["sum_any_disagree_rate"] = unit_sum_pair(triple, any_disagree)
        all_rows.extend(rows)
        df = pd.DataFrame(rows)
        if df.empty:
            continue
        summary = family_summary(df, T=T_full)
        summary["family"] = fam_name
        summary["mean_min_bit_disagree"] = float(df["min_bit_disagree_rate"].mean())
        summary["mean_sum_bit_disagree"] = float(df["sum_bit_disagree_rate"].mean())
        summary_rows.append(summary)
        print(
            f"[{fam_name}] N={summary['n']} units={summary['n_units']} "
            f"mean K={summary['mean_observed']:.2f} "
            f"(μ={summary['mean_expected']:.4g}) "
            f"mean-min-bit-disagree={summary['mean_min_bit_disagree']:.4g} "
            f"better-than-best-member={summary['n_units_better_than_best_member']}"
        )
        plot_unit_failures(
            df, output_dir / f"n_version_units_lic_disagree_{fam_name}.pdf",
            T=T_full, family_label=fam_name,
        )

    units_df = pd.DataFrame(all_rows)
    units_df.to_csv(
        output_dir / "n_version_units_lic_disagree.csv", index=False
    )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(
        output_dir / "n_version_units_lic_disagree_summary.csv", index=False
    )
    (output_dir / "n_version_units_lic_disagree_summary.json").write_text(
        json.dumps(summary_rows, indent=2, default=str)
    )
    plot_family_summary(
        summary_df,
        output_dir / "n_version_units_lic_disagree_summary.pdf",
        T=T_full,
    )

    write_lic_disagree_markdown(
        units_df,
        output_dir / "n_version_units_lic_disagree_table.md",
        T_full=T_full,
        T_mini=T_mini,
        family_order=list(families.keys()),
    )

    main_summary = next(
        (s for s in summary_rows if s["family"] == "max_lic_disagree_pool"),
        None,
    )
    if main_summary is not None:
        print()
        print("=" * 72)
        print(
            "RQ4 (no-oracle, LIC-output) headline — max_lic_disagree_pool, N=3"
        )
        print("=" * 72)
        print(
            f"  units evaluated        : {main_summary['n_units']}\n"
            f"  zero-K units           : {main_summary['n_units_zero_failures']}\n"
            f"  better than best member: {main_summary['n_units_better_than_best_member']}\n"
            f"  mean observed K        : {main_summary['mean_observed']:.2f}\n"
            f"  mean predicted μ       : {main_summary['mean_expected']:.4g}\n"
            f"  mean-min bit-disagree  : {main_summary['mean_min_bit_disagree']:.4g}"
        )
        print("=" * 72)


def write_lic_disagree_markdown(
    units_df: pd.DataFrame,
    output_path: Path,
    *,
    T_full: int,
    T_mini: int,
    family_order: list[str],
) -> None:
    if units_df.empty:
        return
    lines: list[str] = [
        "# RQ4 (no-oracle, LIC-output) — N-version units selected by per-LIC disagreement",
        "",
        f"Selection signal: each version was re-executed on a "
        f"{T_mini:,}-case mini-campaign and its 15-bit CMV output was "
        "saved per test.  For every pair of versions and every test we "
        "form the bit-wise XOR of the two CMVs and compute the "
        "per-(test, bit) mean disagreement rate over jointly-valid "
        "tests.  Selection consults *only* these inter-version "
        "comparisons — the oracle is never used to label individual "
        "outputs.",
        "",
        f"K and μ columns below are computed on the **full {T_full:,}-case "
        "campaign** for fair comparison with the oracle-aware analysis "
        "(this is for reporting only; selection used the mini-campaign "
        "alone).",
        "",
    ]

    descriptions = {
        "max_lic_disagree_pool": (
            "Anchored construction: the 20 versions with the **highest** "
            "mean per-bit pairwise CMV-disagreement act as anchors; each "
            "anchor is paired with two pool members maximising the "
            "*minimum* pairwise per-bit disagreement within the unit "
            "(no-oracle analog of `min max φ`)."
        ),
        "max_lic_disagree_pool_sum": (
            "Same anchored pool as `max_lic_disagree_pool`, but the "
            "per-anchor objective is to maximise the **sum** of the "
            "three pairwise per-bit disagreement rates."
        ),
        "max_lic_disagree_pool_n5": (
            "Same as `max_lic_disagree_pool` with N = 5."
        ),
        "min_lic_disagree_pool": (
            "Sanity baseline: anchors are the versions with the *lowest* "
            "mean per-bit pairwise CMV-disagreement; each is completed "
            "with the partners minimising the within-unit minimum "
            "pairwise disagreement.  Expected to mimic the high-φ "
            "baseline of the oracle-aware analysis."
        ),
        "random_baseline": (
            "Sanity baseline: 20 unit triples drawn uniformly at random "
            "from all admitted versions."
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
            "min bit-disagree", "Σ bit-disagree", "min any-disagree",
            "Observed K", "Predicted μ", "K/μ",
        ])
        lines.append("| " + " | ".join(header) + " |")
        right = {
            "Unit", "min bit-disagree", "Σ bit-disagree", "min any-disagree",
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
            cells.append(_format_phi_label(float(row["min_bit_disagree_rate"])))
            cells.append(_format_phi_label(float(row["sum_bit_disagree_rate"])))
            cells.append(_format_phi_label(float(row["min_any_disagree_rate"])))
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
