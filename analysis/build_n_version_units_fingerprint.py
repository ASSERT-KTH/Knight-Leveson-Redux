"""
Oracle-free N-version unit selection — three strategies.

STRATEGY 1 – Fingerprint diversity (original)
  Assign versions to per-LIC fingerprint groups (most-common = group 0).
  Maximise distinct groups per contested LIC.

STRATEGY 2 – Weighted + one-canonical
  Fingerprint diversity with minority-count weighting; force one all-canonical
  member per triple.

STRATEGY 3 – Co-failure rate minimisation (oracle-free, no canonical assumption)
  For each pair (i,j) and LIC bit k, estimate the pairwise *co-failure* rate
  without any oracle or canonical assumption:

    E[cofail(i,j,k)] ≈ cofire(i,j,k)·(1 − f̄_k)  +  cononfire(i,j,k)·f̄_k

  where  cofire   = P(version i fires AND version j fires on LIC k)
         cononfire = P(version i does NOT fire AND version j does NOT fire)
         f̄_k      = mean firing rate of ALL versions on LIC k  (used as a
                    prior for oracle-1 probability — no label required)

  Interpretation:
  · For a LIC that rarely fires (e.g. LIC-14, ~0.1 %), most co-fires are
    likely false positives (both wrong); co-nonfire is fine.
  · For a LIC that fires often (e.g. LIC-9, ~97 %), most co-nonfires are
    likely false negatives; co-fire is normal correct behaviour.
  The formula weights accordingly without any per-test oracle.

  Triple score = –∑_pairs ∑_k  E[cofail(pair,k)]   (negate → minimise)

Usage:
    python -m analysis.build_n_version_units_fingerprint \\
        --cmv        results/main-spec-3/cmv_outputs_1M.npz \\
        --campaign   results/main-spec-3
"""
from __future__ import annotations

import argparse
import collections
import itertools
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

from analysis.build_n_version_units import (  # noqa: E402
    load_failure_sets,
    load_phi_matrix,
    unit_observed_failure_count,
    independence_unit_failure_prob,
    evaluate_units,
    plot_unit_failures,
    write_units_markdown,
    family_summary,
)
from analysis.analyze_results import (  # noqa: E402
    analysis_version_ids,
    format_version_label,
    read_campaign_version_order,
)


# ---------------------------------------------------------------------------
# Fingerprint group computation
# ---------------------------------------------------------------------------

def compute_fingerprint_groups(
    cmv_path: Path,
) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray]:
    """Return (versions, groups, contested, minority_count) where:

    groups[v, k]        fingerprint group index for version v on LIC bit k
                        (0 = canonical / most common, 1 = largest minority, …)
    contested[k]        True iff LIC k has more than one distinct fingerprint.
    minority_count[k]   Number of non-canonical versions on LIC k (= weight
                        used in the diversity score: larger minority → more
                        important to achieve distinct-group coverage there).
    """
    data = np.load(cmv_path, allow_pickle=True)
    versions: list[str] = data["versions"].tolist()
    cmv_packed: np.ndarray = data["cmv_packed"]   # (V, T) uint16
    valid: np.ndarray = data["valid"].astype(np.uint8)  # (V, T)
    V, _T = cmv_packed.shape

    groups = np.zeros((V, 15), dtype=np.int8)
    contested = np.zeros(15, dtype=bool)
    minority_count = np.zeros(15, dtype=np.int32)

    for b in range(15):
        bit_mat = ((cmv_packed >> b) & 1).astype(np.uint8)

        fp_to_vidx: dict[bytes, list[int]] = collections.defaultdict(list)
        for vi in range(V):
            fp = np.packbits(bit_mat[vi] * valid[vi]).tobytes()
            fp_to_vidx[fp].append(vi)

        contested[b] = len(fp_to_vidx) > 1

        fps_sorted = sorted(fp_to_vidx, key=lambda fp: -len(fp_to_vidx[fp]))
        canon_size = len(fp_to_vidx[fps_sorted[0]])
        minority_count[b] = V - canon_size

        for g, fp in enumerate(fps_sorted):
            for vi in fp_to_vidx[fp]:
                groups[vi, b] = g

    return versions, groups, contested, minority_count


# ---------------------------------------------------------------------------
# Triple scoring
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Strategy 3 – Co-failure rate minimisation (oracle-free, no canonical)
# ---------------------------------------------------------------------------

def compute_pairwise_cofail(
    cmv_path: Path,
    contested: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute oracle-free pairwise expected co-failure rates.

    Returns
    -------
    pair_cofail : np.ndarray  shape (V, V, 15)  float32
        pair_cofail[i, j, k] = E[cofail(i,j,k)] using mean-fire-rate prior.
    mean_fire   : np.ndarray  shape (15,)  float64
        Mean firing rate per LIC bit across all versions.
    """
    data = np.load(cmv_path, allow_pickle=True)
    versions: list[str] = data["versions"].tolist()
    cmv_packed: np.ndarray = data["cmv_packed"]   # (V, T)
    V, T = cmv_packed.shape

    pair_cofail = np.zeros((V, V, 15), dtype=np.float32)
    mean_fire   = np.zeros(15, dtype=np.float64)

    for k in range(15):
        if not contested[k]:
            continue
        bk = ((cmv_packed >> k) & 1).astype(np.float32)  # (V, T) ∈ {0,1}

        fire_v = bk.mean(axis=1)          # (V,) fire rate per version
        f_mean = float(fire_v.mean())     # scalar mean fire rate = oracle-1 prior
        mean_fire[k] = f_mean

        # co_fire[i,j]    = P(i=1 AND j=1) = bk[i] · bk[j] / T
        # co_nonfire[i,j] = P(i=0 AND j=0) = (1-bk[i]) · (1-bk[j]) / T
        #                 = 1 - fire_v[i] - fire_v[j] + co_fire[i,j]
        co_fire = (bk @ bk.T) / T       # (V, V)  — fast matrix multiply

        co_nonfire = (
            1.0
            - fire_v[:, None]
            - fire_v[None, :]
            + co_fire
        )

        # Expected co-failure under mean-fire prior
        #   = cofire * P(oracle=0) + cononfire * P(oracle=1)
        #   = cofire * (1-f) + cononfire * f
        pair_cofail[:, :, k] = (
            co_fire    * (1.0 - f_mean)
            + co_nonfire * f_mean
        ).astype(np.float32)

    return pair_cofail, mean_fire


def select_units_mincofail(
    versions: list[str],
    pair_cofail: np.ndarray,
    contested: np.ndarray,
    num_units: int,
) -> list[tuple[int, int, int]]:
    """Enumerate all C(V,3) triples and pick the ones with lowest total
    oracle-free estimated pairwise co-failure rate.

    The score for a triple (A,B,C) is:
        sum over contested LICs of [cofail(A,B,k) + cofail(A,C,k) + cofail(B,C,k)]
    Smaller = better (less expected correlated failure).
    """
    V = len(versions)
    # Precompute pairwise sums over contested LICs: agg[i,j] = sum_k cofail[i,j,k]
    agg = pair_cofail[:, :, contested].sum(axis=2)   # (V, V)

    scored: list[tuple[float, tuple[int,int,int]]] = []
    for A, B, C in itertools.combinations(range(V), 3):
        score = float(agg[A, B] + agg[A, C] + agg[B, C])
        scored.append((score, (A, B, C)))

    scored.sort()
    seen: set[frozenset[int]] = set()
    units: list[tuple[int, int, int]] = []
    for score, triple in scored:
        if len(units) >= num_units:
            break
        key = frozenset(triple)
        if key not in seen:
            seen.add(key)
            units.append(triple)
    return units


def score_triple_cofail(
    triple: tuple[int, int, int],
    pair_cofail: np.ndarray,
    contested: np.ndarray,
) -> float:
    """Return sum of pairwise expected co-failure across contested LICs."""
    A, B, C = triple
    return float(pair_cofail[A, B, contested].sum()
                 + pair_cofail[A, C, contested].sum()
                 + pair_cofail[B, C, contested].sum())


def score_triple_weighted(
    triple: tuple[int, int, int],
    groups: np.ndarray,
    contested: np.ndarray,
    minority_count: np.ndarray,
) -> tuple[float, int]:
    """Weighted variant: each contested LIC contributes
    ``n_distinct_groups × minority_count[LIC]`` to the primary score.

    LICs with more minority versions (more real-world disagreement) count
    proportionally more.  Tiebreaker = number of LICs where all 3 are
    in distinct groups (unweighted).
    """
    i, j, k = triple
    primary = 0.0
    secondary = 0
    for b in range(15):
        if not contested[b]:
            continue
        gi, gj, gk = int(groups[i, b]), int(groups[j, b]), int(groups[k, b])
        n_distinct = len({gi, gj, gk})
        primary += n_distinct * int(minority_count[b])
        if n_distinct == 3:
            secondary += 1
    return -primary, -secondary


def score_triple(
    triple: tuple[int, int, int],
    groups: np.ndarray,
    contested: np.ndarray,
) -> tuple[int, int]:
    """Return (-distinct_groups_total, -full_diversity_count) for a triple.

    For each contested LIC, count the number of distinct fingerprint groups
    among the three members (1, 2, or 3).  The ideal is 3: one member in the
    canonical group, one in ·A, one in ·B — perfectly non-overlapping
    behaviors.  Canonical counts as a group like any other.

    primary   = total distinct-group count summed over all contested LICs
                (max = 3 × #contested LICs)
    secondary = # contested LICs where all three are in *different* groups
                (i.e. full per-LIC diversity)

    Both are negated so that (ascending) sorting gives the best triple first.
    """
    i, j, k = triple
    primary = 0
    secondary = 0
    for b in range(15):
        if not contested[b]:
            continue
        gi, gj, gk = int(groups[i, b]), int(groups[j, b]), int(groups[k, b])
        n_distinct = len({gi, gj, gk})
        primary += n_distinct
        if n_distinct == 3:
            secondary += 1
    return -primary, -secondary


# ---------------------------------------------------------------------------
# Anchored unit selection
# ---------------------------------------------------------------------------

def _anchor_priority(vi: int, groups: np.ndarray) -> int:
    """Versions in more minority modes make better anchors (more informative)."""
    return int((groups[vi] > 0).sum())


_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _mode_label(group: int) -> str:
    """Return '—' for canonical (0) or '·A', '·B', … for minorities."""
    if group == 0:
        return "—"
    idx = group - 1
    return f"\u00b7{_LETTERS[idx] if idx < len(_LETTERS) else str(group)}"


def write_mode_table(
    units: list[tuple[int, int, int]],
    versions: list[str],
    groups: np.ndarray,
    contested: np.ndarray,
    eval_rows: list[dict],
    output_path: Path,
    T: int,
) -> None:
    """Write a markdown table showing, for each unit member, their
    fingerprint mode on every contested LIC.  '—' = canonical."""
    contested_bits = [b for b in range(15) if contested[b]]
    contested_lics = [b + 1 for b in contested_bits]
    max_primary = 3 * len(contested_bits)

    first_row = eval_rows[0] if eval_rows else {}
    is_weighted = "fp_wscore" in first_row
    if is_weighted:
        title = "# Oracle-free fingerprint unit selection — weighted + one-canonical — minority-mode table"
        desc  = ("Selection: exactly one all-canonical member per triple; "
                 "score weighted by minority-version count per LIC.")
    else:
        title = "# Oracle-free fingerprint unit selection — minority-mode table"
        desc  = ("Selection maximises distinct fingerprint groups per contested LIC "
                 "(ideal: one member per distinct group).")

    lines: list[str] = [
        title,
        "",
        "Each cell shows the fingerprint group for that member on that LIC:  ",
        "`—` = canonical (most common behavior);  "
        "`·A` = largest minority, `·B` = second, etc.  ",
        desc,
        "",
    ]

    lic_header = " | ".join(f"LIC {l}" for l in contested_lics)
    col_sep    = " | ".join("------" for _ in contested_lics)

    for u_idx, (triple, row) in enumerate(zip(units, eval_rows)):
        obs_k      = row["observed_unit_fail_count"]
        obs_rate   = row["observed_unit_fail_rate"]
        phi_max    = row["max_pairwise_phi"]
        full_div   = row.get("fp_full_diversity", "?")

        if "fp_wscore" in row:
            score_str = f"wscore={row['fp_wscore']}, full-div {full_div}/{len(contested_bits)}"
        else:
            distinct = row.get("fp_distinct_total", "?")
            score_str = f"distinct {distinct}/{max_primary}, full-div {full_div}/{len(contested_bits)}"

        lines.append(
            f"## U{u_idx+1:02d} — {score_str}, "
            f"K={obs_k} ({obs_rate*100:.4f}%), "
            f"max-φ={phi_max:.3f}"
        )
        lines.append("")
        lines.append(f"| Member | {lic_header} |")
        lines.append(f"|--------|{col_sep}|")

        for vi in triple:
            label = format_version_label(versions[vi])
            modes = " | ".join(
                _mode_label(int(groups[vi, b])) for b in contested_bits
            )
            lines.append(f"| `{label}` | {modes} |")

        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output_path}")


def select_units_fingerprint(
    versions: list[str],
    groups: np.ndarray,
    contested: np.ndarray,
    num_units: int,
) -> list[tuple[int, int, int]]:
    """Full enumeration, unweighted score, no canonical constraint."""
    V = len(versions)
    scored = []
    for triple in itertools.combinations(range(V), 3):
        scored.append((*score_triple(triple, groups, contested), triple))
    scored.sort()
    seen: set[frozenset[int]] = set()
    units: list[tuple[int, int, int]] = []
    for *_, triple in scored:
        if len(units) >= num_units:
            break
        key = frozenset(triple)
        if key not in seen:
            seen.add(key)
            units.append(triple)
    return units


def select_units_weighted_canonical(
    versions: list[str],
    groups: np.ndarray,
    contested: np.ndarray,
    minority_count: np.ndarray,
    num_units: int,
) -> list[tuple[int, int, int]]:
    """Full enumeration with two changes vs select_units_fingerprint:

    1. **Weighted score**: each contested LIC contributes
       ``n_distinct_groups × minority_count[LIC]`` so that LICs with more
       real-world disagreement drive the optimisation more strongly.

    2. **One-canonical constraint**: every triple must contain at least one
       *all-canonical* version (group 0 on every contested LIC).  This
       ensures each unit has one member that matches the majority on all
       LICs — acting as a reliable anchor.
    """
    V = len(versions)
    all_canonical_set = {
        vi for vi in range(V)
        if all(int(groups[vi, b]) == 0 for b in range(15) if contested[b])
    }

    scored = []
    for triple in itertools.combinations(range(V), 3):
        if not any(vi in all_canonical_set for vi in triple):
            continue   # enforce one-canonical constraint
        scored.append((*score_triple_weighted(triple, groups, contested, minority_count), triple))

    scored.sort()
    seen: set[frozenset[int]] = set()
    units: list[tuple[int, int, int]] = []
    for *_, triple in scored:
        if len(units) >= num_units:
            break
        key = frozenset(triple)
        if key not in seen:
            seen.add(key)
            units.append(triple)
    return units


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cmv", type=Path,
                   default=Path("results/main-spec-3/cmv_outputs_1M.npz"))
    p.add_argument("--campaign", type=Path,
                   default=Path("results/main-spec-3/campaign.csv"))
    p.add_argument("--pairwise", type=Path, default=None)
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--cache", type=Path, default=None)
    p.add_argument("--num-units", type=int, default=20)
    p.add_argument("--seed", type=int, default=20260507)
    args = p.parse_args()

    # --campaign can be either a directory (containing campaign.csv) or the CSV itself
    campaign_arg = args.campaign.resolve()
    if campaign_arg.is_dir():
        campaign_path = campaign_arg
    else:
        campaign_path = campaign_arg.parent
    output_dir = (args.output or campaign_path).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    pairwise_path = (args.pairwise or campaign_path / "cross_language_pairwise.csv").resolve()
    cache_path = (args.cache or campaign_path / "failure_sets.npz").resolve()

    # -----------------------------------------------------------------------
    # 1. Oracle-free fingerprint groups (from CMV outputs)
    # -----------------------------------------------------------------------
    print("Computing fingerprint groups from CMV outputs …")
    cmv_versions, groups, contested, minority_count = compute_fingerprint_groups(args.cmv)
    n_contested = int(contested.sum())
    print(f"Contested LICs (>1 fingerprint): {n_contested}/15 "
          f"→ {[b+1 for b in range(15) if contested[b]]}")
    print("Minority counts (= diversity weight):")
    for b in range(15):
        if contested[b]:
            print(f"  LIC {b+1:2d}: {minority_count[b]:3d} minority versions  (weight={minority_count[b]})")

    # -----------------------------------------------------------------------
    # 1b. Co-failure rate precomputation (Strategy 3)
    # -----------------------------------------------------------------------
    print("\nComputing oracle-free pairwise co-failure rates …")
    pair_cofail_cmv, mean_fire = compute_pairwise_cofail(args.cmv, contested)
    print("Mean fire rates per contested LIC (= oracle-1 prior):")
    for b in range(15):
        if contested[b]:
            print(f"  LIC {b+1:2d}: mean_fire={mean_fire[b]*100:.2f}%")

    # -----------------------------------------------------------------------
    # 2. Oracle-aware campaign data (for evaluation only)
    # -----------------------------------------------------------------------
    all_versions = analysis_version_ids(campaign_path, read_campaign_version_order(campaign_path / "campaign.csv"))
    T, fail_sets = load_failure_sets(campaign_path / "campaign.csv", all_versions, cache_path=cache_path)
    fail_arrays = [fail_sets[v] for v in all_versions]
    fail_counts = np.array([len(fs) for fs in fail_arrays], dtype=np.int64)
    phi = load_phi_matrix(pairwise_path, all_versions)

    # Align CMV version list with campaign version list
    cmv_idx = {v: i for i, v in enumerate(cmv_versions)}
    camp_idx = {v: i for i, v in enumerate(all_versions)}

    # Versions present in both CMV data and campaign
    common = [v for v in all_versions if v in cmv_idx]
    print(f"Versions in both CMV file and campaign: {len(common)} / {len(all_versions)}")

    # Build groups matrix aligned to campaign order
    V_camp = len(all_versions)
    groups_aligned = np.zeros((V_camp, 15), dtype=np.int8)
    minority_aligned = minority_count.copy()
    # Align co-failure matrix to campaign order
    pair_cofail = np.zeros((V_camp, V_camp, 15), dtype=np.float32)
    for v in common:
        ci, mi = camp_idx[v], cmv_idx[v]
        groups_aligned[ci] = groups[mi]
        for v2 in common:
            ci2, mi2 = camp_idx[v2], cmv_idx[v2]
            pair_cofail[ci, ci2] = pair_cofail_cmv[mi, mi2]

    # -----------------------------------------------------------------------
    # 3. Unit selection — three oracle-free strategies
    # -----------------------------------------------------------------------
    # 3a. Original selection (unweighted, no canonical constraint)
    print("\nSelecting units — unweighted, no canonical constraint …")
    units_raw = select_units_fingerprint(common, groups_aligned, contested, args.num_units)
    max_primary = 3 * n_contested
    for u_idx, triple in enumerate(units_raw):
        neg_prim, neg_sec = score_triple(triple, groups_aligned, contested)
        labels = " | ".join(format_version_label(all_versions[i]) for i in triple)
        print(f"  U{u_idx+1:02d}: distinct={-neg_prim}/{max_primary}  full_div={-neg_sec}/{n_contested}  [{labels}]")

    # -----------------------------------------------------------------------
    # 3b. Weighted + one-canonical selection
    # -----------------------------------------------------------------------
    print("\nSelecting units — weighted by minority count, one-canonical constraint …")
    units_wc = select_units_weighted_canonical(
        common, groups_aligned, contested, minority_aligned, args.num_units,
    )
    max_weighted = sum(3 * int(minority_aligned[b]) for b in range(15) if contested[b])
    for u_idx, triple in enumerate(units_wc):
        neg_prim, neg_sec = score_triple_weighted(triple, groups_aligned, contested, minority_aligned)
        labels = " | ".join(format_version_label(all_versions[i]) for i in triple)
        print(f"  U{u_idx+1:02d}: wscore={-neg_prim}/{max_weighted}  full_div={-neg_sec}/{n_contested}  [{labels}]")

    # 3c. Co-failure minimisation (Strategy 3 — no canonical assumption)
    print("\nSelecting units — oracle-free co-failure rate minimisation (no canonical) …")
    units_mcf = select_units_mincofail(common, pair_cofail, contested, args.num_units)
    for u_idx, triple in enumerate(units_mcf):
        score = score_triple_cofail(triple, pair_cofail, contested)
        labels = " | ".join(format_version_label(all_versions[i]) for i in triple)
        print(f"  U{u_idx+1:02d}: cofail_score={score:.6f}  [{labels}]")

    # -----------------------------------------------------------------------
    # 4. Evaluate oracle-aware — both families
    # -----------------------------------------------------------------------
    rows_fp = evaluate_units(
        units_raw,
        family="fingerprint_diversity",
        versions=all_versions,
        fail_sets_arrays=fail_arrays,
        fail_counts=fail_counts,
        phi=phi,
        T=T,
    )

    for row, triple in zip(rows_fp, units_raw):
        neg_prim, neg_sec = score_triple(triple, groups_aligned, contested)
        row["fp_distinct_total"] = -neg_prim
        row["fp_full_diversity"] = -neg_sec

    rows_mcf = evaluate_units(
        units_mcf,
        family="cofail_minimisation",
        versions=all_versions,
        fail_sets_arrays=fail_arrays,
        fail_counts=fail_counts,
        phi=phi,
        T=T,
    )
    for row, triple in zip(rows_mcf, units_mcf):
        row["fp_cofail_score"] = score_triple_cofail(triple, pair_cofail, contested)

    rows_wc = evaluate_units(
        units_wc,
        family="fingerprint_weighted_canonical",
        versions=all_versions,
        fail_sets_arrays=fail_arrays,
        fail_counts=fail_counts,
        phi=phi,
        T=T,
    )
    for row, triple in zip(rows_wc, units_wc):
        neg_prim, neg_sec = score_triple_weighted(triple, groups_aligned, contested, minority_aligned)
        row["fp_wscore"] = -neg_prim
        row["fp_full_diversity"] = -neg_sec

    # Random baseline
    rng = np.random.default_rng(args.seed)
    rand_idx = list(range(V_camp))
    rand_triples = []
    seen: set[frozenset[int]] = set()
    while len(rand_triples) < args.num_units:
        t = tuple(sorted(rng.choice(rand_idx, size=3, replace=False).tolist()))
        key = frozenset(t)
        if key not in seen:
            seen.add(key)
            rand_triples.append(t)
    rows_rand = evaluate_units(
        rand_triples,
        family="random_baseline",
        versions=all_versions,
        fail_sets_arrays=fail_arrays,
        fail_counts=fail_counts,
        phi=phi,
        T=T,
    )

    all_rows = pd.DataFrame(rows_fp + rows_wc + rows_mcf + rows_rand)

    # -----------------------------------------------------------------------
    # 5. Output
    # -----------------------------------------------------------------------
    csv_path = output_dir / "n_version_units_fingerprint.csv"
    all_rows.to_csv(csv_path, index=False)
    print(f"\nWrote {csv_path}")

    pdf_path = output_dir / "n_version_units_fingerprint.pdf"
    fp_df = all_rows[all_rows["family"] == "fingerprint_diversity"].copy()
    plot_unit_failures(fp_df, pdf_path, T=T, family_label="fingerprint_diversity")
    print(f"Wrote {pdf_path}")

    md_path = output_dir / "n_version_units_fingerprint_table.md"
    write_units_markdown(
        all_rows, md_path,
        family_order=["fingerprint_diversity", "fingerprint_weighted_canonical",
                      "cofail_minimisation", "random_baseline"],
        T=T,
    )
    print(f"Wrote {md_path}")

    mode_table_path = output_dir / "n_version_units_fingerprint_modes.md"
    write_mode_table(
        units_raw, all_versions, groups_aligned, contested,
        rows_fp, mode_table_path, T=T,
    )

    wc_table_path = output_dir / "n_version_units_fingerprint_weighted_canonical_modes.md"
    write_mode_table(
        units_wc, all_versions, groups_aligned, contested,
        rows_wc, wc_table_path, T=T,
    )

    # Summary
    for family, grp in all_rows.groupby("family"):
        s = family_summary(grp, T=T)
        print(f"\n--- {family} ---")
        print(f"  mean observed K  : {s['mean_observed']:.2f}")
        print(f"  zero-K units     : {s['n_units_zero_failures']}")
        print(f"  beats best member: {s['n_units_better_than_best_member']}")
        print(f"  mean max phi     : {s['max_internal_phi_mean']:.4f}")


if __name__ == "__main__":
    main()
