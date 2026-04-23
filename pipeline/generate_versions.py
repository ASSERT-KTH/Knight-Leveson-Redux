"""
Pipeline stage 1: Generate versions.

For each agent listed in config, for each ``language`` in ``languages``, for each
configured model (``config.models`` or legacy ``config.model``), run ``runs`` times
in a fresh sandbox each.
Writes one JSON file per version to --output directory.

Usage:
    python -m pipeline.generate_versions \\
        --config config/pilot.yaml \\
        --output results/pilot/versions/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.registry import get_agent
from harnesses import normalize_languages
from pipeline.naming import (
    models_from_agent_config,
    slug_model,
    version_json_filename,
    version_id_from_filename,
)


def run(config_path: str, output_dir: str) -> None:
    config = yaml.safe_load(Path(config_path).read_text())
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    repo_root = Path(__file__).resolve().parents[1]
    spec_rel = config.get("agent_spec_path", "benchmarks/launch_interceptor/spec_original.md")
    spec_path = (repo_root / spec_rel).resolve()
    if not spec_path.exists() or not spec_path.is_file():
        print(f"ERROR: agent spec not found at {spec_path}", file=sys.stderr)
        sys.exit(1)
    try:
        spec_path.relative_to(repo_root)
    except ValueError:
        print(f"ERROR: agent_spec_path must resolve under repo root ({repo_root})", file=sys.stderr)
        sys.exit(1)

    timeout = config.get("agent_timeout_seconds", 300)
    agents_cfg = config.get("agents", [])
    try:
        languages = normalize_languages(config.get("languages"))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        total = sum(
            len(languages)
            * len(models_from_agent_config(a.get("config") or {}))
            * a.get("runs", 1)
            for a in agents_cfg
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Generating {total} versions for {len(agents_cfg)} agent(s)...")

    version_index: list[dict] = []
    generated = 0

    for agent_cfg in agents_cfg:
        agent_name = agent_cfg["name"]
        runs = agent_cfg.get("runs", 1)
        inner = dict(agent_cfg.get("config") or {})
        try:
            model_list = models_from_agent_config(inner)
        except ValueError as exc:
            print(f"ERROR: [{agent_name}] {exc}", file=sys.stderr)
            sys.exit(1)

        base_config = {k: v for k, v in inner.items() if k not in ("models", "model")}

        print(
            f"\n  [{agent_name}] {len(languages)} language(s) × {len(model_list)} model(s) × {runs} run(s) "
            f"= {len(languages) * len(model_list) * runs} version(s)...",
        )

        for lang in languages:
            for configured_model in model_list:
                agent_config = {"timeout_seconds": timeout, **base_config}
                if configured_model is not None:
                    agent_config["model"] = configured_model
                adapter = get_agent(agent_name, agent_config)

                display_model = configured_model if configured_model is not None else "default"
                model_slug = slug_model(configured_model)

                for run_id in range(runs):
                    print(
                        f"    lang={lang!r} model={display_model!r} run {run_id}...",
                        end=" ",
                        flush=True,
                    )
                    record = adapter.generate_version(
                        spec_path=spec_path,
                        run_id=run_id,
                        language=lang,
                    )

                    fname = version_json_filename(
                        agent_name,
                        configured_model,
                        run_id,
                        language=lang,
                    )
                    fpath = out / fname
                    record.to_json(fpath)

                    version_index.append({
                        "file": fname,
                        "version_id": version_id_from_filename(fname),
                        "agent": agent_name,
                        "run_id": run_id,
                        "language": lang,
                        "configured_model": display_model,
                        "model_slug": model_slug,
                        "build_status": record.build_status,
                        "model": record.model_name,
                        "error_message": record.error_message,
                    })

                    model_display = record.model_name
                    if (
                        record.model_name != display_model
                        and display_model != "default"
                    ):
                        model_display = f"{display_model} → {record.model_name}"

                    status_line = f"status={record.build_status} model={model_display}"
                    if record.error_message:
                        em = record.error_message
                        if len(em) > 500:
                            em = em[:500] + "… (see version JSON for full text)"
                        status_line += f"  ← {em}"
                    print(status_line)
                    generated += 1

    index_path = out / "index.json"
    index_path.write_text(json.dumps(version_index, indent=2))
    print(f"\nDone. {generated} versions written to {output_dir}")
    print(f"Index: {index_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate agent versions")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()
    run(args.config, args.output)


if __name__ == "__main__":
    main()
