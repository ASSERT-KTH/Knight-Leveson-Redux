"""
RQ4 (no-oracle, consensus pseudo-oracle) — N-version unit construction
that mirrors the oracle-aware low-φ pipeline using only inter-version
CMV comparisons.

Motivation
----------
The "max bit-disagreement" no-oracle proxy is biased: it ranks
unreliable versions highest because their CMV deviates from the (mostly
correct) majority on many tests.  The consensus pseudo-oracle removes
this bias.  For every test ``t`` and LIC bit ``b``, define

    M[t, b] = majority_{v ∈ valid versions} CMV_v(t)[b]

This is a labelling derived purely from inter-version comparisons.  Two
versions ``i`` and ``j`` then have a pseudo-failure on test ``t`` iff
their CMV differs from ``M[t]``::

    pf_v(t) = 𝟙[CMV_v(t) ≠ M(t) and v is valid on t]

We then compute the standard Pearson φ between binary pseudo-failure
vectors — the *pseudo-φ matrix* — and run the oracle-aware low-φ
pipeline (`select_units_anchored`) on it.

Pool selection.  Buggy outliers must be excluded *before* any φ-based
ranking, because their pseudo-φ with reliable versions is moderate
(near zero) and would otherwise smuggle them into the low-mean-φ pool.
We therefore form the pool from the ``--pool-size`` versions with the
**lowest pseudo-failure rate** — the consensus's "reliable core" — and
do all subsequent ranking strictly within that pool.

Selection mirrors `analysis.build_n_version_units`:

    low_pseudo_phi_pool         — anchored low-max-pseudo-φ
    low_pseudo_phi_pool_sum     — anchored low-Σ-pseudo-φ
    high_pseudo_phi_baseline    — sanity (anchors with highest mean
                                  pseudo-φ; partners maximising max
                                  pseudo-φ)
    random_baseline             — uniform-random triples

Reporting.  K and μ are evaluated against the **full 1 M-case
campaign** (oracle-aware) — the oracle is consulted only for these two
columns; selection used the 10 000-case mini-campaign alone.

Outputs (in ``--output``, default = campaign dir):

    n_version_units_consensus.csv               # one row per unit
    n_version_units_consensus_summary.{csv,json}
    n_version_units_consensus_table.md
    n_version_units_consensus_<family>.pdf
    n_version_units_consensus_pool.csv          # pool ranking
    n_version_units_consensus_summary.pdf
    consensus_pseudo_phi.npz                    # cached matrices

Usage:
    python -m analysis.build_n_version_units_consensus \\
        --cmv      results/main-spec-3/cmv_outputs.npz \\
        --campaign results/main-spec-3/campaign.csv \\
        --num-units 20 --n 3 --pool-size 25
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
    select_units_anchored,
    unit_max_phi,
    unit_sum_phi,
    write_units_markdown,
)


_BIT_MASK_15 = np.uint16((1 << 15) - 1)


# ---------------------------------------------------------------------------
# Consensus pseudo-oracle
# ---------------------------------------------------------------------------

def consensus_cmv(
    cmv_packed: np.ndarray, valid: np.ndarray
) -> np.ndarray:
    """Per-(test, LIC bit) majority over valid versions.

    Inputs ``cmv_packed`` is ``(V, T)`` ``uint16`` (bit ``b`` = CMV[b]),
    ``valid`` is ``(V, T)`` ``uint8``.  Returns the consensus CMV
    packed as a ``uint16`` array of shape ``(T,)``.

    Tie-handling: with all 59 admitted versions valid on every test the
    valid count is odd and ties cannot occur.  In the rare ``valid``
    even case ties resolve to ``0`` (strict majority required).
    """
    V, T = cmv_packed.shape
    valid_b = valid.astype(bool)
    valid_count = valid_b.sum(axis=0).astype(np.int64)  # (T,)
    M = np.zeros(T, dtype=np.uint16)
    for b in range(15):
        bit_v = ((cmv_packed >> b) & 1).astype(np.int64) * valid_b.astype(np.int64)
        ones = bit_v.sum(axis=0)  # (T,)
        # Strict majority: 2·ones > valid_count.  Ties resolve to 0.
        majority_b = (2 * ones > valid_count).astype(np.uint16)
        M |= (majority_b << b)
    return M


def pseudo_failure(
    cmv_packed: np.ndarray, valid: np.ndarray, M: np.ndarray
) -> np.ndarray:
    """``(V, T)`` boolean array; ``True`` iff version v is valid on t and
    its CMV differs from the consensus on at least one LIC bit."""
    valid_b = valid.astype(bool)
    xor = (cmv_packed ^ M[None, :]) & _BIT_MASK_15
    return (xor != 0) & valid_b


def pseudo_phi_matrix(pseudo_fail: np.ndarray) -> np.ndarray:
    """Pearson φ between binary pseudo-failure vectors over all T tests.

    Constant-pseudo-failure rows (variance 0 — versions that *never*
    deviate from the consensus on the mini-campaign) yield ``NaN``
    correlations from ``np.corrcoef``; these are substituted with ``0``,
    which mirrors the convention used by :func:`unit_max_phi` for
    failure-free pairs in the oracle-aware analysis.
    """
    pf = pseudo_fail.astype(np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        phi = np.corrcoef(pf)
    if phi.ndim == 0:
        return np.array([[1.0]])
    phi = np.where(np.isnan(phi), 0.0, phi)
    np.fill_diagonal(phi, 1.0)
    return phi


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cmv", type=Path, required=True,
                   help="cmv_outputs.npz from pipeline.run_campaign_lic")
    p.add_argument("--campaign", type=Path, required=True,
                   help="campaign.csv used for K/μ reporting only")
    p.add_argument("--output", type=Path, default=None,
                   help="Output dir (default: campaign dir)")
    p.add_argument("--cache", type=Path, default=None,
                   help=".npz failure-set cache shared with build_n_version_units")
    p.add_argument("--phi-cache", type=Path, default=None,
                   help=".npz cache for the consensus pseudo-φ matrix")
    p.add_argument("--num-units", type=int, default=20)
    p.add_argument("--n", type=int, default=3, help="Versions per unit")
    p.add_argument(
        "--pool-size", type=int, default=25,
        help="Top-K versions by lowest pseudo-failure rate (the "
             "consensus's reliable core)",
    )
    p.add_argument("--also-n5", action="store_true")
    p.add_argument("--seed", type=int, default=20260507)
    args = p.parse_args()

    cmv_path = args.cmv.resolve()
    campaign_path = args.campaign.resolve()
    output_dir = (args.output or campaign_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_path = (
        args.cache or campaign_path.parent / "failure_sets.npz"
    ).resolve()
    phi_cache = (
        args.phi_cache or campaign_path.parent / "consensus_pseudo_phi.npz"
    ).resolve()

    if not cmv_path.is_file():
        raise SystemExit(f"cmv_outputs.npz not found: {cmv_path}")
    if not campaign_path.is_file():
        raise SystemExit(f"campaign.csv not found: {campaign_path}")

    # --- 1. Load mini-campaign CMV outputs ---------------------------------
    print(f"Loading {cmv_path.name}...")
    cmv_data = np.load(cmv_path, allow_pickle=True)
    cmv_versions: list[str] = cmv_data["versions"].tolist()
    cmv_packed: np.ndarray = cmv_data["cmv_packed"]
    valid: np.ndarray = cmv_data["valid"]
    T_mini = int(cmv_data["n"])
    print(
        f"  V={len(cmv_versions)} versions · T_mini={T_mini} cases"
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
            f"  warning: {len(missing)} admitted version(s) absent from "
            f"CMV snapshot — restricting analysis to {len(common)} shared "
            "versions."
        )
    versions = common
    cmv_idx = {v: i for i, v in enumerate(cmv_versions)}
    perm = np.asarray([cmv_idx[v] for v in versions], dtype=np.int64)
    cmv_packed = cmv_packed[perm]
    valid = valid[perm]
    N = len(versions)

    # --- 3. Consensus pseudo-oracle, pseudo-failures, pseudo-φ -------------
    pseudo_fail = pseudo_phi = pf_rate = None
    if phi_cache.is_file():
        d = np.load(phi_cache, allow_pickle=True)
        if d["versions"].tolist() == versions and int(d["T_mini"]) == T_mini:
            pseudo_phi = d["pseudo_phi"]
            pf_rate = d["pf_rate"]
            valid_count_per_v = d["valid_count_per_v"]
            print(f"Loaded pseudo-φ matrix from {phi_cache.name}")
        else:
            pseudo_phi = None
    if pseudo_phi is None:
        print("Computing consensus pseudo-oracle and pseudo-φ matrix...")
        M = consensus_cmv(cmv_packed, valid)
        pseudo_fail = pseudo_failure(cmv_packed, valid, M)
        valid_count_per_v = valid.astype(bool).sum(axis=1).astype(np.int64)
        pf_rate = pseudo_fail.sum(axis=1).astype(np.float64) / np.maximum(
            valid_count_per_v, 1
        )
        pseudo_phi = pseudo_phi_matrix(pseudo_fail)
        np.savez(
            phi_cache,
            versions=np.asarray(versions, dtype=object),
            T_mini=np.int64(T_mini),
            pseudo_phi=pseudo_phi,
            pf_rate=pf_rate,
            valid_count_per_v=valid_count_per_v,
        )
        print(f"Cached pseudo-φ at {phi_cache}")

    # --- 4. Pool: reliable core (lowest pseudo-failure rate) ---------------
    pool_size = max(args.n, args.pool_size)
    pool_indices = sorted(range(N), key=lambda i: float(pf_rate[i]))[:pool_size]
    print(
        f"Pool size: {len(pool_indices)} (lowest pseudo-failure rate on the "
        f"{T_mini}-case mini-campaign)"
    )

    # Mean pseudo-φ used for anchor ordering.  We compute one variant
    # restricted to pool members (used by the low-pseudo-φ pool
    # families: anchors should be the pool members with the smallest
    # average correlation against the rest of the *reliable core*) and
    # one over the full version list (used by the high-pseudo-φ sanity
    # baseline, which draws from the full population).
    pool_set = set(pool_indices)
    mean_phi_pool = np.zeros(N, dtype=np.float64)
    for i in range(N):
        others = [j for j in pool_indices if j != i]
        if not others:
            mean_phi_pool[i] = 0.0
        else:
            mean_phi_pool[i] = float(
                np.mean([pseudo_phi[i, j] for j in others])
            )
    phi_off = pseudo_phi.copy()
    np.fill_diagonal(phi_off, np.nan)
    mean_phi_all = np.nanmean(phi_off, axis=1)

    # Pool ranking CSV
    pool_rows = []
    for i, v in enumerate(versions):
        pool_rows.append({
            "version_id": v,
            "label": format_version_label(v),
            "agent": agent_by_vid.get(v, "?"),
            "language": lang_by_vid.get(v, "?"),
            "pseudo_failure_rate": float(pf_rate[i]),
            "mean_pseudo_phi_in_pool": float(mean_phi_pool[i]),
            "mean_pseudo_phi_all": float(mean_phi_all[i]),
            "in_pool": i in pool_set,
        })
    pool_df = pd.DataFrame(pool_rows).sort_values(
        ["in_pool", "pseudo_failure_rate"],
        ascending=[False, True],
    ).reset_index(drop=True)
    pool_df.to_csv(
        output_dir / "n_version_units_consensus_pool.csv", index=False
    )

    # --- 5. Build families (selection uses pseudo-φ only) ------------------
    rng = np.random.default_rng(args.seed)
    families: dict[str, list[tuple[int, ...]]] = {
        "low_pseudo_phi_pool": select_units_anchored(
            pseudo_phi, pool_indices,
            n=args.n, num_units=args.num_units,
            mean_phi=mean_phi_pool, score_fn=unit_max_phi, minimise=True,
        ),
        "low_pseudo_phi_pool_sum": select_units_anchored(
            pseudo_phi, pool_indices,
            n=args.n, num_units=args.num_units,
            mean_phi=mean_phi_pool, score_fn=unit_sum_phi, minimise=True,
        ),
        "high_pseudo_phi_baseline": select_units_anchored(
            pseudo_phi, list(range(N)),
            n=args.n, num_units=args.num_units,
            mean_phi=mean_phi_all, score_fn=unit_max_phi, minimise=False,
        ),
        "random_baseline": random_units(
            rng, list(range(N)), n=args.n, num_units=args.num_units,
        ),
    }
    if args.also_n5 and len(pool_indices) >= 5:
        families["low_pseudo_phi_pool_n5"] = select_units_anchored(
            pseudo_phi, pool_indices,
            n=5, num_units=args.num_units,
            mean_phi=mean_phi_pool, score_fn=unit_max_phi, minimise=True,
        )

    # --- 6. Evaluate against the FULL 1M-case campaign ---------------------
    T_full, fail_sets_dict = load_failure_sets(
        campaign_path, versions, cache_path=cache_path,
    )
    fail_sets_arrays = [fail_sets_dict[v] for v in versions]
    fail_counts = np.asarray(
        [a.size for a in fail_sets_arrays], dtype=np.int64
    )

    all_rows: list[dict] = []
    summary_rows: list[dict] = []
    for fam_name, units in families.items():
        rows = evaluate_units(
            units,
            family=fam_name,
            versions=versions,
            fail_sets_arrays=fail_sets_arrays,
            fail_counts=fail_counts,
            phi=pseudo_phi,    # report pseudo-φ in the φ columns
            T=T_full,
        )
        # Augment with pseudo-failure-rate book-keeping (no oracle).
        for row, triple in zip(rows, units):
            members_pf = [float(pf_rate[i]) for i in triple]
            row["member_pseudo_fail_rates"] = "|".join(
                f"{r:.4g}" for r in members_pf
            )
            row["member_max_pseudo_fail_rate"] = float(max(members_pf))
        all_rows.extend(rows)
        df = pd.DataFrame(rows)
        if df.empty:
            continue
        summary = family_summary(df, T=T_full)
        summary["family"] = fam_name
        summary["mean_max_pseudo_phi"] = float(df["max_pairwise_phi"].mean())
        summary["mean_sum_pseudo_phi"] = float(df["sum_pairwise_phi"].mean())
        summary["mean_member_max_pseudo_fail_rate"] = float(
            df["member_max_pseudo_fail_rate"].mean()
        )
        summary_rows.append(summary)
        print(
            f"[{fam_name}] N={summary['n']} units={summary['n_units']} "
            f"mean K={summary['mean_observed']:.2f} "
            f"(μ={summary['mean_expected']:.4g}) "
            f"mean max-pseudo-φ={summary['mean_max_pseudo_phi']:.4g} "
            f"better-than-best-member={summary['n_units_better_than_best_member']}"
        )
        plot_unit_failures(
            df, output_dir / f"n_version_units_consensus_{fam_name}.pdf",
            T=T_full, family_label=fam_name,
        )

    units_df = pd.DataFrame(all_rows)
    units_df.to_csv(
        output_dir / "n_version_units_consensus.csv", index=False
    )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(
        output_dir / "n_version_units_consensus_summary.csv", index=False
    )
    (output_dir / "n_version_units_consensus_summary.json").write_text(
        json.dumps(summary_rows, indent=2, default=str)
    )
    plot_family_summary(
        summary_df,
        output_dir / "n_version_units_consensus_summary.pdf",
        T=T_full,
    )

    write_consensus_markdown(
        units_df,
        output_dir / "n_version_units_consensus_table.md",
        T_full=T_full,
        T_mini=T_mini,
        family_order=list(families.keys()),
    )

    main_summary = next(
        (s for s in summary_rows if s["family"] == "low_pseudo_phi_pool"),
        None,
    )
    if main_summary is not None:
        print()
        print("=" * 72)
        print(
            "RQ4 (no-oracle, consensus pseudo-oracle) — low_pseudo_phi_pool, N=3"
        )
        print("=" * 72)
        print(
            f"  units evaluated        : {main_summary['n_units']}\n"
            f"  zero-K units           : {main_summary['n_units_zero_failures']}\n"
            f"  better than best member: {main_summary['n_units_better_than_best_member']}\n"
            f"  mean observed K        : {main_summary['mean_observed']:.2f}\n"
            f"  mean predicted μ       : {main_summary['mean_expected']:.4g}\n"
            f"  mean max-pseudo-φ      : {main_summary['mean_max_pseudo_phi']:.4g}"
        )
        print("=" * 72)


def write_consensus_markdown(
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
        "# RQ4 (no-oracle, consensus pseudo-oracle) — N-version units",
        "",
        f"Selection signal: each version was re-executed on a "
        f"{T_mini:,}-case mini-campaign and its 15-bit CMV output saved "
        "per test.  For every test we take the per-LIC-bit majority "
        "across all valid versions as a *pseudo-oracle*; a version's "
        "*pseudo-failure* on a test is then the indicator that its CMV "
        "differs from this majority.  Pseudo-φ is the Pearson φ between "
        "binary pseudo-failure vectors — the no-oracle analog of the "
        "RQ2 φ matrix.  The pool is the reliable core (lowest "
        "pseudo-failure rate); selection within the pool minimises "
        "max / Σ pseudo-φ.  No oracle is consulted during selection.",
        "",
        f"K and μ columns below are computed on the **full {T_full:,}-case "
        "campaign** for fair comparison with the oracle-aware analysis "
        "(this is for reporting only; selection used the mini-campaign "
        "alone).",
        "",
    ]

    descriptions = {
        "low_pseudo_phi_pool": (
            "Anchored construction within the reliable core: 20 "
            "versions with the **lowest** mean pseudo-φ (over pool "
            "members) act as anchors; each anchor is paired with two "
            "pool members minimising the *worst* pairwise pseudo-φ "
            "within the unit (no-oracle analog of `low_phi_pool` from "
            "the oracle-aware analysis)."
        ),
        "low_pseudo_phi_pool_sum": (
            "Same anchors as `low_pseudo_phi_pool`, but the per-anchor "
            "objective is to minimise the **sum** of the three pairwise "
            "pseudo-φ values."
        ),
        "low_pseudo_phi_pool_n5": (
            "Same as `low_pseudo_phi_pool` with N = 5."
        ),
        "high_pseudo_phi_baseline": (
            "Sanity baseline drawn from the **full** version list "
            "(no reliability filter): anchors are the highest-mean "
            "pseudo-φ versions, partners *maximise* max pseudo-φ.  "
            "Expected to surface heavily co-failing triples."
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
            "max ψ-φ", "Σ ψ-φ", "max ψ-fail rate",
            "Observed K", "Predicted μ", "K/μ",
        ])
        lines.append("| " + " | ".join(header) + " |")
        right = {
            "Unit", "max ψ-φ", "Σ ψ-φ", "max ψ-fail rate",
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
            cells.append(_format_phi_label(float(row["max_pairwise_phi"])))
            cells.append(_format_phi_label(float(row["sum_pairwise_phi"])))
            cells.append(
                _format_phi_label(float(row["member_max_pseudo_fail_rate"]))
            )
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
