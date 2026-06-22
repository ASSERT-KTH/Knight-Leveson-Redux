"""
Generate table-based alternatives to the pairwise phi heatmap.

The tables summarize the same information as the dense heatmap:
- pairwise phi counts by diversity relation
- exact failure-profile clusters
- high-correlation connected components
"""
from __future__ import annotations

import argparse
import csv
import math
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairwise", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument("--failure-sets", type=Path, required=True, help="Path to failure_sets.npz")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for table PDFs")
    parser.add_argument("--threshold", type=float, default=0.9, help="High-correlation threshold")
    return parser.parse_args()


def parse_version_id(version_id: str) -> dict[str, str]:
    parts = version_id.split("__")
    meta = {"agent": "unknown", "model": "unknown", "language": "unknown"}
    if parts:
        meta["agent"] = parts[0]
    for part in parts[1:]:
        if part.startswith("m_"):
            meta["model"] = part[2:]
        elif part.startswith("l_"):
            meta["language"] = part[2:]
    return meta


def compact_label(version_id: str) -> str:
    meta = parse_version_id(version_id)
    agent = meta["agent"].replace("_", "-")
    model = meta["model"].replace("_", "-")
    language = meta["language"]
    return f"{agent}/{model}/{language}"


def count_labels(values: list[str]) -> str:
    counts = Counter(values)
    return ", ".join(f"{key}: {counts[key]}" for key in sorted(counts))


def pct(count: int, total: int) -> str:
    if total == 0:
        return "0"
    return f"{count} ({100 * count / total:.1f}%)"


def fmt_float(value: float) -> str:
    if math.isnan(value):
        return "-"
    return f"{value:.3f}"


def load_pairwise(path: Path) -> tuple[list[str], list[dict[str, object]]]:
    versions: set[str] = set()
    rows: list[dict[str, object]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            vi = str(row["version_i"])
            vj = str(row["version_j"])
            versions.add(vi)
            versions.add(vj)
            phi_raw = (row.get("phi_correlation") or "").strip()
            rows.append(
                {
                    "version_i": vi,
                    "version_j": vj,
                    "phi": float(phi_raw) if phi_raw else float("nan"),
                    "observed": int(float(row.get("observed_cofailures") or 0)),
                }
            )
    return sorted(versions), rows


def load_failure_sets(path: Path) -> dict[str, np.ndarray]:
    data = np.load(path, allow_pickle=True)
    versions = [str(v) for v in data["versions"]]
    return {
        version_id: np.array(data[f"f_{idx}"], dtype=np.int64)
        for idx, version_id in enumerate(versions)
    }


def relation_label(vi: str, vj: str) -> str:
    mi = parse_version_id(vi)
    mj = parse_version_id(vj)
    lang = "same lang" if mi["language"] == mj["language"] else "cross lang"
    agent = "same agent" if mi["agent"] == mj["agent"] else "cross agent"
    return f"{lang}, {agent}"


def diversity_table(rows: list[dict[str, object]]) -> tuple[list[str], list[list[str]]]:
    headers = [
        "Pair relation",
        "Pairs",
        "Defined phi",
        "Undefined phi",
        "phi = 1",
        "0.9 <= phi < 1",
        "phi <= 0",
        "Median phi",
    ]
    order = [
        "same lang, same agent",
        "same lang, cross agent",
        "cross lang, same agent",
        "cross lang, cross agent",
        "all pairs",
    ]
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[relation_label(str(row["version_i"]), str(row["version_j"]))].append(row)
        grouped["all pairs"].append(row)

    table_rows: list[list[str]] = []
    for label in order:
        group_rows = grouped[label]
        total = len(group_rows)
        phis = [float(row["phi"]) for row in group_rows if not math.isnan(float(row["phi"]))]
        defined = len(phis)
        exact = sum(1 for phi in phis if abs(phi - 1.0) <= 1e-12)
        high_non_exact = sum(1 for phi in phis if 0.9 <= phi < 1.0)
        non_positive = sum(1 for phi in phis if phi <= 0.0)
        median = float(np.median(phis)) if phis else float("nan")
        table_rows.append(
            [
                label,
                str(total),
                str(defined),
                str(total - defined),
                pct(exact, defined),
                pct(high_non_exact, defined),
                pct(non_positive, defined),
                fmt_float(median),
            ]
        )
    return headers, table_rows


def failure_profile_table(
    versions: list[str],
    failure_sets: dict[str, np.ndarray],
) -> tuple[list[str], list[list[str]]]:
    headers = [
        "Profile",
        "Versions",
        "Failing inputs",
        "Languages",
        "Agents",
        "Representative versions",
    ]
    grouped: dict[bytes, list[str]] = defaultdict(list)
    for version_id in versions:
        grouped[failure_sets[version_id].tobytes()].append(version_id)

    groups = sorted(
        grouped.values(),
        key=lambda members: (-len(members), -len(failure_sets[members[0]]), members[0]),
    )
    table_rows: list[list[str]] = []
    profile_id = 1
    for members in groups:
        if len(members) == 1:
            continue
        langs = [parse_version_id(member)["language"] for member in members]
        agents = [parse_version_id(member)["agent"].replace("_", "-") for member in members]
        reps = "; ".join(compact_label(member) for member in members[:3])
        if len(members) > 3:
            reps += f"; +{len(members) - 3} more"
        table_rows.append(
            [
                f"P{profile_id}",
                str(len(members)),
                str(len(failure_sets[members[0]])),
                count_labels(langs),
                count_labels(agents),
                reps,
            ]
        )
        profile_id += 1
    return headers, table_rows


def high_phi_component_table(
    versions: list[str],
    rows: list[dict[str, object]],
    failure_sets: dict[str, np.ndarray],
    threshold: float,
) -> tuple[list[str], list[list[str]]]:
    graph = nx.Graph()
    for version_id in versions:
        graph.add_node(version_id)
    for row in rows:
        phi = float(row["phi"])
        if math.isnan(phi) or phi < threshold:
            continue
        graph.add_edge(str(row["version_i"]), str(row["version_j"]), phi=phi)

    headers = [
        "Component",
        "Versions",
        "Agents",
        "Languages",
        "Edges",
        "phi = 1 edges",
        "Failure-count range",
    ]
    components = [sorted(comp) for comp in nx.connected_components(graph) if len(comp) > 1]
    components.sort(key=lambda comp: (-len(comp), comp[0]))
    table_rows: list[list[str]] = []
    for idx, members in enumerate(components, 1):
        subgraph = graph.subgraph(members)
        edge_phis = [float(data["phi"]) for _, _, data in subgraph.edges(data=True)]
        exact_edges = sum(1 for phi in edge_phis if abs(phi - 1.0) <= 1e-12)
        fail_counts = [len(failure_sets[member]) for member in members]
        langs = [parse_version_id(member)["language"] for member in members]
        agents = [parse_version_id(member)["agent"].replace("_", "-") for member in members]
        table_rows.append(
            [
                f"C{idx}",
                str(len(members)),
                count_labels(agents),
                count_labels(langs),
                str(subgraph.number_of_edges()),
                str(exact_edges),
                f"{min(fail_counts)}-{max(fail_counts)}",
            ]
        )
    return headers, table_rows


def wrap_cell(value: str, width: int) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False)) or value


def draw_table_pdf(
    headers: list[str],
    rows: list[list[str]],
    output_path: Path,
    title: str,
    *,
    wrap_widths: list[int],
    col_widths: list[float],
) -> None:
    wrapped_rows = [
        [wrap_cell(str(value), wrap_widths[col_idx]) for col_idx, value in enumerate(row)]
        for row in rows
    ]
    fig_height = max(3.2, 1.15 + 0.42 * max(len(rows), 1))
    fig, ax = plt.subplots(figsize=(11.0, fig_height))
    ax.axis("off")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    table = ax.table(
        cellText=wrapped_rows,
        colLabels=headers,
        cellLoc="left",
        colLoc="left",
        colWidths=col_widths,
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.6)
    table.scale(1.0, 1.6)
    for (row_idx, _), cell in table.get_celld().items():
        cell.set_edgecolor("#555555")
        cell.set_linewidth(0.5)
        if row_idx == 0:
            cell.set_facecolor("#e9eef3")
            cell.set_text_props(weight="bold")
        else:
            cell.set_facecolor("#ffffff" if row_idx % 2 else "#f7f7f7")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    versions, rows = load_pairwise(args.pairwise.resolve())
    failure_sets = load_failure_sets(args.failure_sets.resolve())
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    div_headers, div_rows = diversity_table(rows)
    profile_headers, profile_rows = failure_profile_table(versions, failure_sets)
    component_headers, component_rows = high_phi_component_table(
        versions,
        rows,
        failure_sets,
        args.threshold,
    )

    draw_table_pdf(
        div_headers,
        div_rows,
        output_dir / "heatmap_table_diversity_summary.pdf",
        "Pairwise Phi Summary by Diversity Relation",
        wrap_widths=[18, 8, 10, 10, 12, 14, 12, 10],
        col_widths=[0.22, 0.08, 0.10, 0.11, 0.12, 0.15, 0.12, 0.10],
    )
    draw_table_pdf(
        profile_headers,
        profile_rows,
        output_dir / "heatmap_table_failure_profiles.pdf",
        "Exact Failure-Profile Clusters",
        wrap_widths=[8, 8, 12, 20, 22, 45],
        col_widths=[0.07, 0.08, 0.12, 0.17, 0.20, 0.36],
    )
    draw_table_pdf(
        component_headers,
        component_rows,
        output_dir / "heatmap_table_high_phi_components.pdf",
        f"High-Correlation Components (phi >= {args.threshold:.1f})",
        wrap_widths=[10, 8, 24, 18, 8, 12, 16],
        col_widths=[0.10, 0.09, 0.28, 0.20, 0.08, 0.12, 0.13],
    )

    report = "\n\n".join(
        [
            "# Heatmap Table Alternatives",
            "## Pairwise Phi Summary by Diversity Relation",
            markdown_table(div_headers, div_rows),
            "## Exact Failure-Profile Clusters",
            markdown_table(profile_headers, profile_rows),
            f"## High-Correlation Components (phi >= {args.threshold:.1f})",
            markdown_table(component_headers, component_rows),
        ]
    )
    (output_dir / "heatmap_table_summary.md").write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
