#!/usr/bin/env python3
"""Build the static GitHub Pages site in ``docs/`` from ``results/main/versions/``.

This script:
  * Copies every per-version JSON file into ``docs/data/versions/``.
  * Produces an enriched ``docs/data/index.json`` (list of summaries) and
    ``docs/data/facets.json`` (agents / models / languages / statuses) that
    powers the filter UI.

The site itself is fully static; after running this script, commit the
contents of ``docs/`` and enable GitHub Pages with "Deploy from branch ->
main /docs".
"""
from __future__ import annotations

import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "results" / "main" / "versions"
OUT_DATA_DIR = ROOT / "docs" / "data"
OUT_VERSIONS_DIR = OUT_DATA_DIR / "versions"


# Build statuses to exclude from the site (runs where the agent never
# produced any code because the upstream API was down / timed out).
EXCLUDED_BUILD_STATUSES = {"api_unavailable", "no_output"}


SUMMARY_FIELDS = (
    "version_id",
    "agent",
    "agent_name",
    "model",
    "configured_model",
    "model_slug",
    "language",
    "run_id",
    "build_status",
    "acceptance_passed",
    "timestamp",
    "error_message",
)


def build() -> None:
    if not SOURCE_DIR.exists():
        raise SystemExit(f"Source directory not found: {SOURCE_DIR}")

    OUT_VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

    # Start clean so deleted upstream files disappear from the site too.
    for stale in OUT_VERSIONS_DIR.glob("*.json"):
        stale.unlink()

    # Upstream index.json carries extra fields (configured_model, model_slug)
    # that are not present in per-version files; merge them in when available.
    upstream_index_path = SOURCE_DIR / "index.json"
    upstream_by_id: dict[str, dict] = {}
    if upstream_index_path.exists():
        try:
            upstream = json.loads(upstream_index_path.read_text(encoding="utf-8"))
            for entry in upstream:
                vid = entry.get("version_id")
                if vid:
                    upstream_by_id[vid] = entry
        except Exception as exc:  # noqa: BLE001
            print(f"warning: could not read upstream index.json: {exc}")

    summaries: list[dict] = []
    agents: Counter[str] = Counter()
    models: Counter[str] = Counter()
    languages: Counter[str] = Counter()
    statuses: Counter[str] = Counter()

    for src in sorted(SOURCE_DIR.glob("*.json")):
        if src.name == "index.json":
            continue
        try:
            payload = json.loads(src.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"skip {src.name}: {exc}")
            continue

        version_id = src.stem  # filename without .json
        extra = upstream_by_id.get(version_id, {})

        build_status_raw = (
            payload.get("build_status") or extra.get("build_status") or "unknown"
        )
        if build_status_raw in EXCLUDED_BUILD_STATUSES:
            continue

        shutil.copyfile(src, OUT_VERSIONS_DIR / src.name)

        agent = payload.get("agent_name") or payload.get("agent") or extra.get("agent") or "unknown"
        # Prefer `configured_model` (what the experiment asked for) so that
        # failed runs still report a meaningful model rather than the CLI's
        # fallback string like "claude" or "gemini".
        model = (
            extra.get("configured_model")
            or payload.get("model_name")
            or payload.get("model")
            or "unknown"
        )
        language = payload.get("language") or extra.get("language") or "unknown"
        build_status = build_status_raw

        source_code = payload.get("source_code") or ""
        prompt = payload.get("prompt") or ""
        summary = {
            "version_id": version_id,
            "file": src.name,
            "agent": agent,
            "model": model,
            "language": language,
            "run_id": payload.get("run_id", 0),
            "build_status": build_status,
            "acceptance_passed": bool(payload.get("acceptance_passed")),
            "timestamp": payload.get("timestamp", ""),
            "error_message": payload.get("error_message", ""),
            "source_lines": source_code.count("\n") + (1 if source_code else 0),
            "source_bytes": len(source_code),
            "prompt_bytes": len(prompt),
        }
        summaries.append(summary)
        agents[agent] += 1
        models[model] += 1
        languages[language] += 1
        statuses[build_status] += 1

    # Sort: language, then agent, then model, then run.
    summaries.sort(
        key=lambda s: (s["language"], s["agent"], s["model"], s["run_id"])
    )

    (OUT_DATA_DIR / "index.json").write_text(
        json.dumps(summaries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    facets = {
        "agents": sorted(agents.items(), key=lambda kv: (-kv[1], kv[0])),
        "models": sorted(models.items(), key=lambda kv: (-kv[1], kv[0])),
        "languages": sorted(languages.items(), key=lambda kv: (-kv[1], kv[0])),
        "build_statuses": sorted(statuses.items(), key=lambda kv: (-kv[1], kv[0])),
        "totals": {
            "versions": len(summaries),
            "accepted": sum(1 for s in summaries if s["acceptance_passed"]),
            "built_ok": sum(1 for s in summaries if s["build_status"] == "ok"),
        },
    }
    (OUT_DATA_DIR / "facets.json").write_text(
        json.dumps(facets, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(
        f"Wrote {len(summaries)} versions -> {OUT_VERSIONS_DIR.relative_to(ROOT)}\n"
        f"  accepted: {facets['totals']['accepted']}  built_ok: {facets['totals']['built_ok']}\n"
        f"  agents:    {dict(agents)}\n"
        f"  languages: {dict(languages)}\n"
        f"  statuses:  {dict(statuses)}"
    )


if __name__ == "__main__":
    build()
