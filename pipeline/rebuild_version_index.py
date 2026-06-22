"""
Rebuild versions/index.json from all *.json version records in that directory.

Use when index.json is missing entries or out of sync after manual file copies.

Usage:
    python -m pipeline.rebuild_version_index --versions results/main/versions/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.base import VersionRecord
from harnesses import get_harness
from pipeline.naming import slug_model, version_id_from_filename


def _configured_model_from_record(record: VersionRecord) -> str:
    gc = record.generation_config or {}
    for key in ("model", "model_passed_to_cli", "variant"):
        v = gc.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return record.model_name or "default"


def _effective_build_status(versions_dir: Path, record: VersionRecord) -> tuple[str, str]:
    language = getattr(record, "language", None) or "python"
    harness = get_harness(language)
    artifact_rel = getattr(record, "artifact_file", "") or ""
    if artifact_rel:
        artifact_path = (versions_dir / artifact_rel).resolve()
        if artifact_path.is_file():
            if language == "python":
                status = harness.check_syntax(artifact_path.read_text(encoding="utf-8", errors="replace"))
                if status == "ok":
                    return "ok", ""
                return status, "archived Python artifact failed syntax validation"
            return "ok", ""
    return record.build_status, record.error_message or ""


def index_entry(path: Path, record: VersionRecord) -> dict[str, object]:
    fname = path.name
    agent = record.agent_name
    cm = _configured_model_from_record(record)
    display = cm
    build_status, error_message = _effective_build_status(path.parent, record)
    record.build_status = build_status
    record.error_message = error_message
    return {
        "file": fname,
        "artifact_file": getattr(record, "artifact_file", "") or "",
        "trajectory_file": getattr(record, "trajectory_file", "") or "",
        "version_id": version_id_from_filename(fname),
        "agent": agent,
        "run_id": record.run_id,
        "language": getattr(record, "language", None) or "python",
        "configured_model": display,
        # Match pipeline/generate_versions.py: slug_model(configured_model)
        "model_slug": slug_model(cm),
        "build_status": build_status,
        "model": record.model_name,
        "error_message": error_message,
    }


def rebuild(versions_dir: Path) -> list[dict[str, object]]:
    versions_dir = versions_dir.resolve()
    if not versions_dir.is_dir():
        raise FileNotFoundError(f"not a directory: {versions_dir}")

    json_files = sorted(
        p for p in versions_dir.iterdir()
        if p.suffix == ".json" and p.name != "index.json" and not p.name.endswith(".trajectory.json")
    )
    entries: list[dict[str, object]] = []
    for p in json_files:
        record = VersionRecord.from_json(p)
        entries.append(index_entry(p, record))
        record.to_json(p)
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild versions/index.json from version JSON files")
    parser.add_argument(
        "--versions",
        required=True,
        type=Path,
        help="Directory containing *.json version records (writes index.json here)",
    )
    args = parser.parse_args()
    out_dir = args.versions.resolve()
    entries = rebuild(out_dir)
    index_path = out_dir / "index.json"
    index_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {index_path}")


if __name__ == "__main__":
    main()
