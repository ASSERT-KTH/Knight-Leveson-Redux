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
from pipeline.naming import slug_model, version_id_from_filename


def _configured_model_from_record(record: VersionRecord) -> str:
    gc = record.generation_config or {}
    for key in ("model", "model_passed_to_cli", "variant"):
        v = gc.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return record.model_name or "default"


def index_entry(path: Path, record: VersionRecord) -> dict[str, object]:
    fname = path.name
    agent = record.agent_name
    cm = _configured_model_from_record(record)
    display = cm
    return {
        "file": fname,
        "version_id": version_id_from_filename(fname),
        "agent": agent,
        "run_id": record.run_id,
        "language": getattr(record, "language", None) or "python",
        "configured_model": display,
        # Match pipeline/generate_versions.py: slug_model(configured_model)
        "model_slug": slug_model(cm),
        "build_status": record.build_status,
        "model": record.model_name,
        "error_message": record.error_message or "",
    }


def rebuild(versions_dir: Path) -> list[dict[str, object]]:
    versions_dir = versions_dir.resolve()
    if not versions_dir.is_dir():
        raise FileNotFoundError(f"not a directory: {versions_dir}")

    json_files = sorted(
        p for p in versions_dir.iterdir()
        if p.suffix == ".json" and p.name != "index.json"
    )
    entries: list[dict[str, object]] = []
    for p in json_files:
        record = VersionRecord.from_json(p)
        entries.append(index_entry(p, record))
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
