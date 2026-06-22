"""
Generate three alternatives to the pairwise phi heatmap:

1. clustered collapsed heatmap
2. high-phi correlation graph
3. ranked strongest-pairs plot
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform


LANG_COLORS = {
    "pascal": "#54a24b",
    "python": "#4c78a8",
    "rust": "#f58518",
}

AGENT_SHAPES = {
    "claude_code": "o",
    "cursor": "s",
    "gemini": "^",
    "opencode": "D",
    "codex": "P",
}

PAIR_COLORS = {
    "same language, same agent": "#8c564b",
    "same language, cross agent": "#4c78a8",
    "cross language, same agent": "#54a24b",
    "cross language, cross agent": "#e45756",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pairwise", type=Path, required=True, help="Path to pairwise_table.csv")
    parser.add_argument("--failure-sets", type=Path, required=True, help="Path to failure_sets.npz")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for output PDFs")
    parser.add_argument("--graph-threshold", type=float, default=0.9, help="Minimum phi for graph edges")
    parser.add_argument("--top-n", type=int, default=30, help="Number of ranked pairs to plot")
    return parser.parse_args()


def parse_version_id(version_id: str) -> dict[str, str]:
    parts = version_id.split("__")
    agent = parts[0]
    model = "unknown"
    language = "unknown"
    for part in parts[1:]:
        if part.startswith("m_"):
            model = part[2:]
        if part.startswith("l_"):
            language = part[2:]
    return {"agent": agent, "model": model, "language": language}


def format_label(version_id: str) -> str:
    meta = parse_version_id(version_id)
    agent = meta["agent"].replace("_", "-")
    model = meta["model"].replace("_", "-")
    return f"{agent}:{model}"


def load_pairwise(path: Path) -> tuple[list[str], dict[tuple[str, str], dict[str, float]]]:
    versions: set[str] = set()
    rows: dict[tuple[str, str], dict[str, float]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            vi = str(row["version_i"])
            vj = str(row["version_j"])
            versions.add(vi)
            versions.add(vj)
            phi_raw = (row.get("phi_correlation") or "").strip()
            obs_raw = (row.get("observed_cofailures") or "0").strip()
            rows[(vi, vj)] = {
                "phi": float(phi_raw) if phi_raw else float("nan"),
                "observed": float(obs_raw) if obs_raw else 0.0,
            }
    ordered = sorted(versions)
    return ordered, rows


def load_failure_sets(path: Path) -> dict[str, np.ndarray]:
    data = np.load(path, allow_pickle=True)
    versions = [str(v) for v in data["versions"]]
    failure_sets: dict[str, np.ndarray] = {}
    for idx, version_id in enumerate(versions):
        failure_sets[version_id] = np.array(data[f"f_{idx}"], dtype=np.int64)
    return failure_sets


def lookup_pair(rows: dict[tuple[str, str], dict[str, float]], a: str, b: str) -> dict[str, float]:
    if a == b:
        return {"phi": 1.0, "observed": float("nan")}
    return rows.get((a, b)) or rows.get((b, a)) or {"phi": float("nan"), "observed": 0.0}


def build_collapsed_groups(versions: list[str], failure_sets: dict[str, np.ndarray]) -> list[list[str]]:
    grouped: dict[bytes, list[str]] = defaultdict(list)
    for version_id in versions:
        grouped[failure_sets[version_id].tobytes()].append(version_id)
    groups = list(grouped.values())
    groups.sort(key=lambda members: (-len(members), members[0]))
    return groups


def plot_clustered_collapsed_heatmap(
    versions: list[str],
    rows: dict[tuple[str, str], dict[str, float]],
    failure_sets: dict[str, np.ndarray],
    output_path: Path,
) -> None:
    groups = build_collapsed_groups(versions, failure_sets)
    n = len(groups)
    mat = np.zeros((n, n), dtype=float)
    for i, gi in enumerate(groups):
        for j, gj in enumerate(groups):
            if i == j:
                mat[i, j] = 1.0 if failure_sets[gi[0]].size > 0 else 0.0
            else:
                mat[i, j] = lookup_pair(rows, gi[0], gj[0])["phi"]
    sim = np.nan_to_num(mat, nan=0.0, posinf=1.0, neginf=0.0)
    if n >= 2:
        dist = 1.0 - np.clip(sim, 0.0, 1.0)
        np.fill_diagonal(dist, 0.0)
        order = leaves_list(linkage(squareform(dist, checks=False), method="average"))
        groups = [groups[i] for i in order]
        sim = sim[np.ix_(order, order)]
    labels = []
    for members in groups:
        meta = parse_version_id(members[0])
        agent = meta["agent"].replace("_", "-")
        language = meta["language"]
        if len(members) == 1:
            labels.append(f"{agent}/{language}")
        else:
            labels.append(f"{agent}/{language} x{len(members)}")

    fig, ax = plt.subplots(figsize=(8.6, 7.4))
    im = ax.imshow(sim, cmap="YlOrRd", vmin=0.0, vmax=1.0, aspect="equal")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_title("Collapsed Clustered Phi Heatmap", fontsize=15, pad=14)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Phi correlation", fontsize=11)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_threshold_graph(
    versions: list[str],
    rows: dict[tuple[str, str], dict[str, float]],
    output_path: Path,
    threshold: float,
) -> None:
    graph = nx.Graph()
    for version_id in versions:
        meta = parse_version_id(version_id)
        graph.add_node(version_id, **meta)
    for i, vi in enumerate(versions):
        for vj in versions[i + 1:]:
            pair = lookup_pair(rows, vi, vj)
            phi = pair["phi"]
            if not math.isnan(phi) and phi >= threshold:
                graph.add_edge(vi, vj, phi=phi)

    pos = nx.spring_layout(graph, seed=7, weight="phi", k=1.4 / math.sqrt(max(len(graph.nodes), 1)))
    fig, ax = plt.subplots(figsize=(9.2, 7.0))
    edge_widths = [1.0 + 4.0 * (graph[u][v]["phi"] - threshold) / max(1e-6, 1.0 - threshold) for u, v in graph.edges()]
    nx.draw_networkx_edges(graph, pos, ax=ax, width=edge_widths, edge_color="#999999", alpha=0.6)

    for agent, marker in AGENT_SHAPES.items():
        agent_nodes = [n for n, data in graph.nodes(data=True) if data["agent"] == agent]
        if not agent_nodes:
            continue
        node_colors = [LANG_COLORS.get(graph.nodes[n]["language"], "#cccccc") for n in agent_nodes]
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=agent_nodes,
            node_shape=marker,
            node_color=node_colors,
            edgecolors="black",
            linewidths=0.5,
            node_size=110,
            ax=ax,
        )

    labels = {n: format_label(n) for n in graph.nodes() if graph.degree(n) > 0}
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=7, ax=ax)

    lang_handles = [Patch(facecolor=color, edgecolor="black", label=lang.capitalize()) for lang, color in LANG_COLORS.items()]
    agent_handles = [Line2D([0], [0], marker=marker, color="black", linestyle="", markersize=7, label=agent.replace("_", "-")) for agent, marker in AGENT_SHAPES.items() if any(data["agent"] == agent for _, data in graph.nodes(data=True))]
    legend1 = ax.legend(handles=lang_handles, title="Language", loc="upper left", bbox_to_anchor=(0.01, 0.99), frameon=True, fancybox=False)
    ax.add_artist(legend1)
    ax.legend(handles=agent_handles, title="Agent", loc="upper left", bbox_to_anchor=(0.20, 0.99), frameon=True, fancybox=False)
    ax.set_title(f"High-Correlation Graph (phi >= {threshold:.2f})", fontsize=15, pad=12)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def pair_relation(a: str, b: str) -> str:
    ma = parse_version_id(a)
    mb = parse_version_id(b)
    same_language = ma["language"] == mb["language"]
    same_agent = ma["agent"] == mb["agent"]
    if same_language and same_agent:
        return "same language, same agent"
    if same_language and not same_agent:
        return "same language, cross agent"
    if not same_language and same_agent:
        return "cross language, same agent"
    return "cross language, cross agent"


def plot_ranked_pairs(
    versions: list[str],
    rows: dict[tuple[str, str], dict[str, float]],
    output_path: Path,
    top_n: int,
) -> None:
    points: list[dict[str, object]] = []
    for i, vi in enumerate(versions):
        for vj in versions[i + 1:]:
            pair = lookup_pair(rows, vi, vj)
            phi = pair["phi"]
            if math.isnan(phi):
                continue
            points.append(
                {
                    "pair": f"{format_label(vi)} / {format_label(vj)}",
                    "phi": phi,
                    "observed": pair["observed"],
                    "relation": pair_relation(vi, vj),
                }
            )
    points.sort(key=lambda item: (float(item["phi"]), float(item["observed"])), reverse=True)
    points = points[:top_n]
    labels = [str(item["pair"]) for item in points][::-1]
    xs = [float(item["phi"]) for item in points][::-1]
    sizes = [40 + 0.25 * float(item["observed"]) for item in points][::-1]
    colors = [PAIR_COLORS[str(item["relation"])] for item in points][::-1]

    fig_h = max(6.0, 0.27 * len(points) + 1.6)
    fig, ax = plt.subplots(figsize=(9.4, fig_h))
    y = np.arange(len(points))
    ax.hlines(y, xmin=0.0, xmax=xs, color="#bbbbbb", linewidth=1.0)
    ax.scatter(xs, y, s=sizes, c=colors, edgecolors="black", linewidths=0.4)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Phi correlation")
    ax.set_xlim(-0.02, 1.02)
    ax.set_title(f"Top {len(points)} Strongest Pairwise Phi Matches", fontsize=15, pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.35)
    legend_handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markeredgecolor="black", markersize=8, label=label) for label, color in PAIR_COLORS.items()]
    ax.legend(handles=legend_handles, title="Pair type", loc="lower right", frameon=True, fancybox=False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    versions, rows = load_pairwise(args.pairwise.resolve())
    failure_sets = load_failure_sets(args.failure_sets.resolve())
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_clustered_collapsed_heatmap(
        versions,
        rows,
        failure_sets,
        output_dir / "heatmap_alt_clustered_collapsed.pdf",
    )
    plot_threshold_graph(
        versions,
        rows,
        output_dir / "heatmap_alt_threshold_graph.pdf",
        threshold=args.graph_threshold,
    )
    plot_ranked_pairs(
        versions,
        rows,
        output_dir / "heatmap_alt_ranked_pairs.pdf",
        top_n=args.top_n,
    )


if __name__ == "__main__":
    main()
