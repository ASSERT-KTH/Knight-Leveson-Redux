"""
Plot LIC-specific failure counts.

By default, each bar counts how many distinct `agent | model | language`
triples have at least one failure involving that LIC, stacked by language.
The input can be either:

- `fault_events.jsonl` from `pipeline.run_campaign`
- `summary_table_cmv_oracle.csv` from `analysis.analyze_cmv_oracle`

LIC indices in the fault log are 0-based CMV positions; the plot always uses
1-based LIC labels from 1 to 15.

Usage:
    python -m analysis.plot_lic_failure_counts \
        --input results/main-spec-3/fault_events.jsonl

    python -m analysis.plot_lic_failure_counts \
        --input results/main-spec-3/fault_events.jsonl \
        --output results/main-spec-3/lic_failure_counts.pdf
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def iter_fault_events(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc


def triple_from_record(record: dict) -> str:
    agent = record.get("agent")
    language = record.get("language")
    version_id = str(record.get("version_id", ""))

    model = None
    match = re.match(r".*__m_(?P<model>.*?)__l_.*__run\d+$", version_id)
    if match:
        model = match.group("model").replace("_", "/")

    if agent and model and language:
        return f"{agent} | {model} | {language}"
    return version_id


def count_unique_triples_by_lic_and_group(
    input_path: Path,
    *,
    stack_by: str,
) -> tuple[dict[str, Counter[int]], list[str]]:
    triples_by_lic_and_group: dict[str, dict[int, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for record in iter_fault_events(input_path):
        triple = triple_from_record(record)
        group = str(record.get(stack_by, "?"))
        indices = record.get("diff", {}).get("cmv_mismatch_indices") or []
        for idx in indices:
            lic = int(idx) + 1
            if 1 <= lic <= 15:
                triples_by_lic_and_group[group][lic].add(triple)

    groups = sorted(triples_by_lic_and_group)
    counts_by_group: dict[str, Counter[int]] = {}
    for group in groups:
        counts_by_group[group] = Counter(
            {lic: len(triples_by_lic_and_group[group].get(lic, set())) for lic in range(1, 16)}
        )
    return counts_by_group, groups


def count_fault_rows_by_lic(input_path: Path) -> Counter[int]:
    counts: Counter[int] = Counter({lic: 0 for lic in range(1, 16)})
    for record in iter_fault_events(input_path):
        indices = record.get("diff", {}).get("cmv_mismatch_indices") or []
        for idx in indices:
            lic = int(idx) + 1
            if 1 <= lic <= 15:
                counts[lic] += 1
    return counts


def count_unique_triples_from_summary_csv(
    input_path: Path,
    *,
    stack_by: str,
) -> tuple[dict[str, Counter[int]], list[str]]:
    triples_by_lic_and_group: dict[str, dict[int, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    with input_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            triple = triple_from_record(row)
            group = str(row.get(stack_by, "?"))
            for lic in range(1, 16):
                key = f"lic_{lic}_mismatch_count"
                try:
                    count = int(row.get(key, "0") or 0)
                except ValueError:
                    count = 0
                if count > 0:
                    triples_by_lic_and_group[group][lic].add(triple)

    groups = sorted(triples_by_lic_and_group)
    counts_by_group: dict[str, Counter[int]] = {}
    for group in groups:
        counts_by_group[group] = Counter(
            {lic: len(triples_by_lic_and_group[group].get(lic, set())) for lic in range(1, 16)}
        )
    return counts_by_group, groups


def plot_counts_stacked(
    counts_by_group: dict[str, Counter[int]],
    groups: list[str],
    output_path: Path,
    *,
    stack_by: str,
) -> None:
    x = list(range(1, 16))
    language_colors = {
        "python": "#4c78a8",
        "rust": "#f58518",
        "pascal": "#54a24b",
    }
    agent_colors = {
        "claude_code": "#e45756",
        "codex": "#4c78a8",
        "cursor": "#72b7b2",
        "gemini": "#f58518",
        "opencode": "#54a24b",
    }
    colors = language_colors if stack_by == "language" else agent_colors

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = [0] * len(x)
    for group in groups:
        y = [counts_by_group[group][lic] for lic in x]
        bars = ax.bar(
            x,
            y,
            bottom=bottom,
            color=colors.get(group, None),
            label=group,
        )
        bottom = [a + b for a, b in zip(bottom, y)]

    ax.set_xticks(x)
    ax.set_xlabel("LIC")
    ax.set_ylabel("Distinct failing triples")
    ax.set_title(f"Failures by LIC (stacked by {stack_by})")
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend(title=stack_by.capitalize())

    totals = [sum(counts_by_group[group][lic] for group in groups) for lic in x]
    for lic, total in zip(x, totals):
        ax.text(lic, total, str(total), ha="center", va="bottom")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to fault_events.jsonl or summary_table_cmv_oracle.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path. Defaults to <input-dir>/lic_failure_counts.pdf",
    )
    parser.add_argument(
        "--mode",
        choices=("triples", "rows"),
        default="triples",
        help="Count distinct agent|model|language triples or raw fault rows per LIC.",
    )
    parser.add_argument(
        "--stack-by",
        choices=("language", "agent"),
        default="language",
        help="Color stacked segments by language or by agent.",
    )
    return parser.parse_args()


def infer_input_kind(input_path: Path) -> str:
    if input_path.suffix.lower() == ".jsonl":
        return "fault-events"
    if input_path.suffix.lower() == ".csv":
        return "summary-csv"
    raise SystemExit(
        f"Could not infer input kind from {input_path}. Expected .jsonl or .csv."
    )


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = (
        args.output.resolve()
        if args.output is not None
        else input_path.with_name("lic_failure_counts.pdf")
    )
    input_kind = infer_input_kind(input_path)

    if args.mode != "triples":
        raise SystemExit("Stacked plotting currently supports only --mode triples.")
    if input_kind == "fault-events":
        counts_by_group, groups = count_unique_triples_by_lic_and_group(
            input_path,
            stack_by=args.stack_by,
        )
    else:
        counts_by_group, groups = count_unique_triples_from_summary_csv(
            input_path,
            stack_by=args.stack_by,
        )
    total_counts = Counter(
        {
            lic: sum(counts_by_group[group][lic] for group in groups)
            for lic in range(1, 16)
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plot_counts_stacked(
        counts_by_group,
        groups,
        output_path,
        stack_by=args.stack_by,
    )

    print(f"Wrote {output_path}")
    print(f"Input kind: {input_kind}")
    print(f"Mode: {args.mode}")
    print(f"Stacked by: {args.stack_by}")
    print(f"Groups: {', '.join(groups)}")
    for lic in range(1, 16):
        parts = ", ".join(f"{group}={counts_by_group[group][lic]}" for group in groups)
        print(f"LIC {lic}: total={total_counts[lic]} ({parts})")


if __name__ == "__main__":
    main()
