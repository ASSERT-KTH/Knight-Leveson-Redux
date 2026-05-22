"""
UpSet plot — LIC-level version signatures, three modes:

  --source fault   (default)
      Sets: oracle-based. Version v ∈ LIC-k set iff it produced at
      least one cmv_mismatch on LIC k over the full campaign
      (from fault_events.jsonl).

  --source fault-modes
      Like 'fault', but each distinct failure fingerprint (the exact set
      of test IDs where a version fails LIC k) becomes its own row.
      Rows are labelled 'LIC k·A', 'LIC k·B', … ordered by frequency.
      Two versions in the same mode share identical failing test inputs —
      their failures are maximally correlated and they should NOT be
      combined in an N-version unit.

  --source cmv
      Sets: oracle-free. Version v ∈ LIC-k set iff its CMV bit k
      disagrees with at least one other version on at least one test
      (from cmv_outputs.npz).

      Add --split to further de-aggregate each LIC by direction:
        LIC k↑  version says 1 while majority says 0
        LIC k↓  version says 0 while majority says 1

Intersection bars: number of implementations whose *exact* signature
matches that combination.

Usage:
    python -m analysis.plot_lic_upset \\
        --fault-events results/main-spec-3/fault_events.jsonl \\
        --output       results/main-spec-3/lic_upset.pdf

    python -m analysis.plot_lic_upset --source fault-modes \\
        --fault-events results/main-spec-3/fault_events.jsonl \\
        --output       results/main-spec-3/lic_upset_modes.pdf

    python -m analysis.plot_lic_upset --source cmv \\
        --cmv     results/main-spec-3/cmv_outputs_1M.npz \\
        --output  results/main-spec-3/lic_upset_disagree.pdf

    python -m analysis.plot_lic_upset --source cmv --split \\
        --cmv     results/main-spec-3/cmv_outputs_1M.npz \\
        --output  results/main-spec-3/lic_upset_disagree_split.pdf
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np


# ---------------------------------------------------------------------------
# Loaders — both return frozenset[str] label keys
# ---------------------------------------------------------------------------

def load_lic_sets_from_faults(
    fault_events_path: Path,
) -> tuple[dict[str, frozenset[str]], int]:
    """Oracle-based: {version_id: frozenset(label strings like 'LIC 10')}."""
    by_version: dict[str, set[str]] = collections.defaultdict(set)
    with fault_events_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            vid = rec.get("version_id")
            if not vid:
                continue
            for k in (rec.get("diff") or {}).get("cmv_mismatch_indices") or []:
                by_version[vid].add(f"LIC {int(k) + 1}")
    result = {v: frozenset(s) for v, s in by_version.items() if s}
    return result, len(result)


def load_lic_sets_from_fault_modes(
    fault_events_path: Path,
) -> tuple[dict[str, frozenset[str]], int]:
    """Oracle-based, failure-mode-disaggregated.

    For each LIC k, every distinct *failure fingerprint* — the exact
    frozenset of test IDs where a version fails that LIC — becomes its
    own row, labelled 'LIC k·A', 'LIC k·B', … (A = most common mode).

    Two versions sharing a mode label have identical failing inputs for
    that LIC; their failures are perfectly correlated.  Versions that
    never fail LIC k do not appear in any mode for that LIC.
    """
    _LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Step 1: per-version, per-LIC failure sets
    fail: dict[str, dict[int, set]] = collections.defaultdict(
        lambda: collections.defaultdict(set)
    )
    all_vids: set[str] = set()
    with fault_events_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            vid = rec.get("version_id")
            tid = rec.get("test_id")
            if not vid:
                continue
            all_vids.add(vid)
            if tid is None:
                continue
            for k in (rec.get("diff") or {}).get("cmv_mismatch_indices") or []:
                fail[vid][int(k)].add(int(tid))

    # Step 2: for each LIC, assign mode labels sorted by descending frequency
    lic_mode_label: dict[int, dict[frozenset, str]] = {}
    for lic in sorted({lic for v in fail.values() for lic in v}):
        fp_counts: dict[frozenset, int] = collections.Counter(
            frozenset(fail[vid][lic])
            for vid in fail
            if lic in fail[vid]
        )
        fps_sorted = sorted(fp_counts, key=lambda fp: -fp_counts[fp])
        lic_mode_label[lic] = {
            fp: f"LIC {lic + 1}\u00b7{_LETTERS[i] if i < len(_LETTERS) else str(i)}"
            for i, fp in enumerate(fps_sorted)
        }

    # Step 3: assign labels to versions
    result: dict[str, set[str]] = collections.defaultdict(set)
    for vid, lic_dict in fail.items():
        for lic, test_set in lic_dict.items():
            label = lic_mode_label[lic][frozenset(test_set)]
            result[vid].add(label)

    return {v: frozenset(s) for v, s in result.items()}, len(all_vids)


def load_lic_sets_from_cmv_modes(
    cmv_path: Path,
) -> tuple[dict[str, frozenset[str]], int]:
    """Oracle-free failure-mode disaggregation.

    For each LIC k, versions are grouped by their exact CMV[k] output
    vector across all tests (their *behavior fingerprint* for that LIC).
    The most common fingerprint is treated as the canonical (likely
    correct) behavior and excluded from the plot.  Every distinct
    minority fingerprint becomes its own row: 'LIC k·A' (largest
    minority), 'LIC k·B', … — mirroring fault-modes without an oracle.

    Two versions that share a row have identical outputs on every test
    for that LIC; their failures (whatever they may be) are perfectly
    correlated and they should not be combined in an N-version unit.
    """
    _LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    data = np.load(cmv_path, allow_pickle=True)
    versions: list[str] = data["versions"].tolist()
    cmv_packed: np.ndarray = data["cmv_packed"]   # (V, T) uint16
    valid: np.ndarray = data["valid"].astype(np.uint8)  # (V, T)
    V, _T = cmv_packed.shape

    result: dict[str, set[str]] = {v: set() for v in versions}

    for b in range(15):
        bit_mat = ((cmv_packed >> b) & 1).astype(np.uint8)  # (V, T)

        # Fingerprint each version's output vector as packed bytes
        fp_to_vidx: dict[bytes, list[int]] = collections.defaultdict(list)
        for vi in range(V):
            # Zero out invalid tests so they don't create spurious differences
            vec = bit_mat[vi] * valid[vi]
            fp = np.packbits(vec).tobytes()
            fp_to_vidx[fp].append(vi)

        if len(fp_to_vidx) <= 1:
            continue  # unanimous on this LIC — nothing to show

        # Largest group = canonical (best proxy for oracle); exclude it
        canon_fp = max(fp_to_vidx, key=lambda fp: len(fp_to_vidx[fp]))
        minority_fps = sorted(
            (fp for fp in fp_to_vidx if fp != canon_fp),
            key=lambda fp: -len(fp_to_vidx[fp]),
        )

        lic_num = b + 1
        for i, fp in enumerate(minority_fps):
            letter = _LETTERS[i] if i < len(_LETTERS) else str(i)
            label = f"LIC {lic_num}\u00b7{letter}"
            for vi in fp_to_vidx[fp]:
                result[versions[vi]].add(label)

    return {v: frozenset(s) for v, s in result.items() if s}, V


def load_lic_sets_from_cmv(
    cmv_path: Path,
    split_direction: bool = False,
) -> tuple[dict[str, frozenset[str]], int]:
    """Oracle-free: {version_id: frozenset(label strings)}.

    Without split_direction: label is 'LIC k' for each deviating bit k.
    With    split_direction: label is 'LIC k↑' (over-fires vs majority)
                             or     'LIC k↓' (under-fires vs majority).
    A version can appear in both ↑ and ↓ for the same LIC if it deviates
    in both directions across different test cases.
    """
    data = np.load(cmv_path, allow_pickle=True)
    versions: list[str] = data["versions"].tolist()
    cmv_packed: np.ndarray = data["cmv_packed"]   # (V, T) uint16
    valid: np.ndarray = data["valid"].astype(bool) # (V, T)
    V, _T = cmv_packed.shape

    disagree_sets: dict[str, set[str]] = {v: set() for v in versions}

    for b in range(15):
        bit_mat = ((cmv_packed >> b) & 1).astype(np.int8)  # (V, T)
        valid_count = valid.sum(axis=0)
        ones = (bit_mat * valid).sum(axis=0)
        majority = (2 * ones > valid_count).astype(np.int8)  # (T,)

        if split_direction:
            # over-fires: version=1, majority=0
            over  = valid & (bit_mat == 1) & (majority[None, :] == 0)
            # under-fires: version=0, majority=1
            under = valid & (bit_mat == 0) & (majority[None, :] == 1)
            for vi, v in enumerate(versions):
                if over[vi].any():
                    disagree_sets[v].add(f"LIC {b + 1}\u2191")   # ↑
                if under[vi].any():
                    disagree_sets[v].add(f"LIC {b + 1}\u2193")   # ↓
        else:
            deviates = valid & (bit_mat != majority[None, :])
            any_dev = deviates.any(axis=1)
            for vi, v in enumerate(versions):
                if any_dev[vi]:
                    disagree_sets[v].add(f"LIC {b + 1}")

    result = {v: frozenset(s) for v, s in disagree_sets.items() if s}
    return result, V


# ---------------------------------------------------------------------------
# Shared UpSet renderer
# ---------------------------------------------------------------------------

def _lic_label_sort_key(label: str) -> tuple[int, int, str]:
    """Sort labels: 'LIC 10' → (10,0,''), 'LIC 10↑' → (10,1,''),
    'LIC 10↓' → (10,2,''), 'LIC 10·A' → (10,3,'A')."""
    m = re.match(r"LIC\s+(\d+)(.*)", label)
    if not m:
        return (999, 0, "")
    n = int(m.group(1))
    suffix = m.group(2).strip()
    if not suffix:
        return (n, 0, "")
    if suffix == "\u2191":
        return (n, 1, "")
    if suffix == "\u2193":
        return (n, 2, "")
    if suffix.startswith("\u00b7"):        # ·A, ·B, …
        return (n, 3, suffix[1:])
    return (n, 4, suffix)


def _render_upset(
    lic_sets: dict[str, frozenset[str]],
    n_versions_total: int,
    output_path: Path,
    title: str,
    totals_xlabel: str,
) -> None:
    active_lics = sorted({k for s in lic_sets.values() for k in s},
                         key=_lic_label_sort_key)
    n_lics = len(active_lics)
    lic_labels = active_lics  # strings are already the labels

    sig_counts: collections.Counter = collections.Counter(lic_sets.values())
    sigs_sorted = sorted(sig_counts.items(), key=lambda x: -x[1])
    n_sigs = len(sigs_sorted)

    lic_totals = [sum(1 for s in lic_sets.values() if k in s) for k in active_lics]
    lic_order = sorted(range(n_lics), key=lambda i: -lic_totals[i])
    active_lics_ord = [active_lics[i] for i in lic_order]
    lic_labels_ord = [lic_labels[i] for i in lic_order]
    lic_totals_ord = [lic_totals[i] for i in lic_order]

    membership = np.array(
        [[k in sig for k in active_lics_ord] for sig, _ in sigs_sorted],
        dtype=bool,
    )
    counts_arr = np.array([c for _, c in sigs_sorted])

    bar_h  = 3.0
    matrix_h = 0.45 * n_lics
    left_w  = 1.6
    main_w  = max(7.0, 0.7 * n_sigs)

    fig = plt.figure(figsize=(left_w + main_w + 0.4, bar_h + matrix_h + 1.0))
    gs = gridspec.GridSpec(
        2, 2,
        width_ratios=[left_w, main_w],
        height_ratios=[bar_h, matrix_h],
        hspace=0.05, wspace=0.03,
    )
    ax_bar    = fig.add_subplot(gs[0, 1])
    ax_totals = fig.add_subplot(gs[1, 0])
    ax_mat    = fig.add_subplot(gs[1, 1])
    fig.add_subplot(gs[0, 0]).set_visible(False)

    x = np.arange(n_sigs)
    bar_color = "#4878cf"

    # top bar chart
    ax_bar.bar(x, counts_arr, color=bar_color, width=0.65, zorder=3)
    for xi, c in zip(x, counts_arr):
        ax_bar.text(xi, c + 0.15, str(c), ha="center", va="bottom",
                    fontsize=8, fontweight="bold")
    ax_bar.set_xlim(-0.6, n_sigs - 0.4)
    ax_bar.set_ylim(0, max(counts_arr) * 1.22)
    ax_bar.set_xticks([])
    ax_bar.set_ylabel("Implementations\n(exact signature)", fontsize=9)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    ax_bar.spines["bottom"].set_visible(False)
    ax_bar.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax_bar.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax_bar.set_title(title, fontsize=10, pad=6)

    # dot matrix
    dot_size = 140
    ax_mat.set_xlim(-0.6, n_sigs - 0.4)
    ax_mat.set_ylim(-0.6, n_lics - 0.4)
    for yi in range(n_lics):
        ax_mat.axhline(yi, color="#e0e0e0", linewidth=0.8, zorder=0)
    for xi, row in enumerate(membership):
        active_rows = np.where(row)[0]
        for yi in range(n_lics):
            ax_mat.scatter(xi, yi, s=dot_size, color="#d8d8d8",
                           zorder=1, linewidths=0)
        if len(active_rows) > 0:
            ax_mat.plot([xi, xi], [active_rows.min(), active_rows.max()],
                        color=bar_color, linewidth=2.5, zorder=2)
            for yi in active_rows:
                ax_mat.scatter(xi, yi, s=dot_size, color=bar_color,
                               zorder=3, linewidths=0)
    ax_mat.set_yticks(range(n_lics))
    ax_mat.set_yticklabels([])
    ax_mat.set_xticks([])
    ax_mat.spines["top"].set_visible(False)
    ax_mat.spines["right"].set_visible(False)
    ax_mat.spines["bottom"].set_visible(False)
    ax_mat.spines["left"].set_visible(False)
    ax_mat.tick_params(left=False)

    # left totals bar
    y = np.arange(n_lics)
    ax_totals.barh(y, lic_totals_ord, color="#888888", height=0.55, zorder=3)
    for yi, v in enumerate(lic_totals_ord):
        ax_totals.text(v + 0.3, yi, str(v), va="center",
                       fontsize=8, fontweight="bold")
    ax_totals.set_ylim(-0.6, n_lics - 0.4)
    ax_totals.set_xlim(max(lic_totals_ord) * 1.25, 0)
    ax_totals.set_yticks(y)
    ax_totals.set_yticklabels(lic_labels_ord, fontsize=8)
    ax_totals.set_xlabel(totals_xlabel, fontsize=9)
    ax_totals.spines["top"].set_visible(False)
    ax_totals.spines["right"].set_visible(False)
    ax_totals.spines["left"].set_visible(False)
    ax_totals.tick_params(left=False)
    ax_totals.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=4))
    ax_totals.grid(axis="x", linestyle="--", alpha=0.4, zorder=0)

    fig.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Wrote {output_path}")

    # text summary
    print(f"\nVersions in ≥1 LIC set: {len(lic_sets)} / {n_versions_total}")
    print(f"Active LIC keys ({n_lics}): {active_lics}")
    print("\nPer-LIC version counts (ordered):")
    for label, total in zip(active_lics_ord, lic_totals_ord):
        print(f"  {label}: {total:3d} versions")
    print(f"\nDistinct signatures: {n_sigs}")
    print("Signature breakdown (sorted by count):")
    for sig, n in sigs_sorted:
        keys = sorted(sig, key=_lic_label_sort_key)
        print(f"  {n:3d} versions: {keys}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--source", choices=["fault", "fault-modes", "cmv", "cmv-modes"], default="fault",
        help="'fault'       = oracle-based, one row per LIC (default); "
             "'fault-modes' = oracle-based, one row per distinct failure fingerprint; "
             "'cmv'         = oracle-free, one row per LIC (majority-deviation); "
             "'cmv-modes'   = oracle-free, one row per distinct behavior fingerprint",
    )
    p.add_argument(
        "--fault-events", type=Path,
        default=Path("results/main-spec-3/fault_events.jsonl"),
    )
    p.add_argument(
        "--cmv", type=Path,
        default=Path("results/main-spec-3/cmv_outputs_1M.npz"),
    )
    p.add_argument(
        "--split", action="store_true",
        help="(cmv source only) de-aggregate each LIC into ↑ (over-fires vs "
             "majority) and ↓ (under-fires vs majority) sub-entries",
    )
    p.add_argument(
        "--output", type=Path, default=None,
        help="Output PDF path (default depends on --source and --split)",
    )
    args = p.parse_args()

    if args.source == "fault":
        if not args.fault_events.is_file():
            sys.exit(f"fault_events.jsonl not found: {args.fault_events}")
        lic_sets, n_total = load_lic_sets_from_faults(args.fault_events)
        out = args.output or Path("results/main-spec-3/lic_upset.pdf")
        title = (
            f"LIC-failure UpSet — {n_total} implementations "
            f"({len(lic_sets)} with ≥1 LIC failure)"
        )
        xlabel = "Implementations\n(any failure in LIC)"
    elif args.source == "fault-modes":
        if not args.fault_events.is_file():
            sys.exit(f"fault_events.jsonl not found: {args.fault_events}")
        lic_sets, n_total = load_lic_sets_from_fault_modes(args.fault_events)
        out = args.output or Path("results/main-spec-3/lic_upset_modes.pdf")
        title = (
            f"LIC failure-mode UpSet — {n_total} implementations "
            f"({len(lic_sets)} with ≥1 failure)\n"
            "Each row = a distinct failure fingerprint  ·  same row = identical failing inputs"
        )
        xlabel = "Implementations\n(in failure mode)"
    elif args.source == "cmv-modes":
        if not args.cmv.is_file():
            sys.exit(f"cmv file not found: {args.cmv}")
        lic_sets, n_total = load_lic_sets_from_cmv_modes(args.cmv)
        out = args.output or Path("results/main-spec-3/lic_upset_cmv_modes.pdf")
        title = (
            f"LIC behavior-mode UpSet (oracle-free) — {n_total} implementations "
            f"({len(lic_sets)} in a minority mode)\n"
            "Each row = a distinct output fingerprint  ·  same row = identical outputs on all tests"
        )
        xlabel = "Implementations\n(in minority mode)"
    else:
        if not args.cmv.is_file():
            sys.exit(f"cmv_outputs.npz not found: {args.cmv}")
        lic_sets, n_total = load_lic_sets_from_cmv(args.cmv, split_direction=args.split)
        if args.split:
            out = args.output or Path("results/main-spec-3/lic_upset_disagree_split.pdf")
            title = (
                f"LIC-disagreement UpSet (by direction) — {n_total} implementations "
                f"({len(lic_sets)} disagreeing on ≥1 LIC)\n"
                r"↑ fires when majority doesn't  ·  ↓ silent when majority fires"
            )
            xlabel = "Implementations\n(disagree on LIC direction)"
        else:
            out = args.output or Path("results/main-spec-3/lic_upset_disagree.pdf")
            title = (
                f"LIC-disagreement UpSet — {n_total} implementations "
                f"({len(lic_sets)} disagreeing on ≥1 LIC)"
            )
            xlabel = "Implementations\n(disagree on LIC with ≥1 other)"

    out.parent.mkdir(parents=True, exist_ok=True)
    _render_upset(lic_sets, n_total, out, title, xlabel)


if __name__ == "__main__":
    main()
