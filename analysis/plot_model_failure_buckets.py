"""
Plot a bar chart of version-triple counts by failed-test bucket.

Reads either:

- a `campaign.csv` file produced by `pipeline.run_campaign`, or
- a `summary_table_cmv_oracle.csv` file produced by `analysis.analyze_cmv_oracle`

and groups
unique `agent, model, language` triples by how many campaign test cases they
failed. Buckets are `0`, `<10`, `<100`, `<1000`, `<10000`, ...

When `versions_meta.json` exists alongside the CSV, it is used to map each
`version_id` to a canonical `agent/model/language` triple. Otherwise the script
falls back to parsing those fields from `version_id`.

Usage:
    python -m analysis.plot_model_failure_buckets results/main-spec/campaign.csv
    python -m analysis.plot_model_failure_buckets results/main-spec/campaign.csv \
        --output results/main-spec/model_failure_buckets.png
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def configure_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 13,
            "axes.titlesize": 15,
            "axes.labelsize": 15,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 11.5,
            "legend.title_fontsize": 12,
        }
    )


def _parse_passed_cell(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "t", "yes", "y"}


def _fallback_triple_from_version_id(version_id: str) -> str:
    match = re.match(r"(?P<agent>.*?)__m_(?P<model>.*?)__l_(?P<language>.*?)__run\d+$", version_id)
    if not match:
        return version_id
    agent = match.group("agent")
    model = match.group("model").replace("_", "/")
    language = match.group("language")
    return f"{agent} | {model} | {language}"


def load_version_to_triple(path: Path) -> dict[str, str]:
    meta_path = path.with_name("versions_meta.json")
    if not meta_path.exists():
        return {}

    data = json.loads(meta_path.read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for row in data:
        version_id = row.get("version_id")
        agent = row.get("agent")
        model = row.get("model")
        language = row.get("language")
        if version_id and agent and model and language:
            mapping[version_id] = f"{agent} | {model} | {language}"
    return mapping


def count_failures_by_triple_from_campaign(campaign_csv: Path) -> dict[str, int]:
    version_to_triple = load_version_to_triple(campaign_csv)
    failures_by_triple: dict[str, int] = {}

    with campaign_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"version_id", "passed"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            missing_str = ", ".join(sorted(missing))
            raise ValueError(f"campaign CSV is missing required columns: {missing_str}")

        for row in reader:
            version_id = row["version_id"]
            triple = version_to_triple.get(version_id) or _fallback_triple_from_version_id(version_id)
            failures_by_triple.setdefault(triple, 0)
            if not _parse_passed_cell(row["passed"]):
                failures_by_triple[triple] += 1

    return failures_by_triple


def count_failures_by_triple_from_summary(summary_csv: Path) -> dict[str, int]:
    failures_by_triple: dict[str, int] = {}
    with summary_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"version_id", "failed_count"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            missing_str = ", ".join(sorted(missing))
            raise ValueError(f"summary CSV is missing required columns: {missing_str}")

        for row in reader:
            version_id = row["version_id"]
            triple = _fallback_triple_from_version_id(version_id)
            failures_by_triple[triple] = int(row["failed_count"])
    return failures_by_triple


def build_bucket_labels(max_failures: int) -> list[tuple[str, int]]:
    labels: list[tuple[str, int]] = []
    bound = 10
    while bound <= max_failures:
        labels.append((f"<{bound}", bound))
        bound *= 10
    labels.append((f"<{bound}", bound))
    return labels


def bucket_counts(failures_by_triple: dict[str, int]) -> Counter[str]:
    max_failures = max(failures_by_triple.values(), default=0)
    bucket_defs = build_bucket_labels(max_failures)
    counts: Counter[str] = Counter({"0": 0})
    counts.update({label: 0 for label, _ in bucket_defs})

    for failures in failures_by_triple.values():
        if failures == 0:
            counts["0"] += 1
            continue
        for label, upper in bucket_defs:
            if failures < upper:
                counts[label] += 1
                break

    return counts


def plot_bucket_counts(bucketed: Counter[str], output_path: Path) -> None:
    configure_plot_style()
    labels = list(bucketed.keys())
    values = [bucketed[label] for label in labels]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, values, color="#1f77b4")
    ax.set_title("Agent/Model/Language Triples by Failed-Test Bucket")
    ax.set_xlabel("Failed test cases")
    ax.set_ylabel("Triple count")
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=12,
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input_path",
        help="Path to campaign.csv or summary_table_cmv_oracle.csv",
    )
    parser.add_argument(
        "--output",
        help="Output image path. Defaults to <campaign-dir>/model_failure_buckets.png",
    )
    return parser.parse_args()


def infer_input_kind(input_path: Path) -> str:
    if input_path.name == "campaign.csv":
        return "campaign"
    if input_path.name.startswith("summary_table_cmv_oracle") and input_path.suffix.lower() == ".csv":
        return "summary"
    if input_path.suffix.lower() == ".csv":
        with input_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cols = set(reader.fieldnames or [])
        if {"version_id", "passed"} <= cols:
            return "campaign"
        if {"version_id", "failed_count"} <= cols:
            return "summary"
    raise SystemExit(
        f"Could not infer input type from {input_path}; expected campaign.csv or summary_table_cmv_oracle.csv"
    )


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_path).resolve()
    output_path = (
        Path(args.output).resolve()
        if args.output
        else input_path.with_name("model_failure_buckets.png")
    )

    input_kind = infer_input_kind(input_path)
    if input_kind == "campaign":
        failures_by_triple = count_failures_by_triple_from_campaign(input_path)
    else:
        failures_by_triple = count_failures_by_triple_from_summary(input_path)
    if not failures_by_triple:
        raise SystemExit("No versions found in the input file.")

    bucketed = bucket_counts(failures_by_triple)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plot_bucket_counts(bucketed, output_path)

    print(f"Wrote {output_path}")
    print(f"Input kind: {input_kind}")
    print(f"Total triples: {len(failures_by_triple)}")
    for label, count in bucketed.items():
        print(f"{label}: {count}")


if __name__ == "__main__":
    main()
