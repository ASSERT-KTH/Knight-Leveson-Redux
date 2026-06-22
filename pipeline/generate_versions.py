"""
Pipeline stage 1: Generate versions.

For each agent listed in config, for each ``language`` in ``languages``, for each
configured model (``config.models`` or legacy ``config.model``), run ``runs`` times
in a fresh sandbox each.
Writes one JSON file per version to --output directory.
"""
from __future__ import annotations

import argparse
import json
import shutil
import stat
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.registry import get_agent
from harnesses import get_harness, normalize_languages
from pipeline.naming import (
    models_from_agent_config,
    slug_model,
    version_json_filename,
    version_id_from_filename,
)

_GENERATION_WORKERS = 4


def _trajectory_filename(version_filename: str) -> str:
    return version_filename.removesuffix('.json') + '.trajectory.json'


def _artifact_filename(version_filename: str, artifact_path: Path, language: str) -> str:
    stem = version_filename.removesuffix('.json')
    suffix = artifact_path.suffix
    if language == 'python':
        return stem + '.py'
    if suffix:
        return stem + '.artifact' + suffix
    return stem + '.artifact'


def _write_trajectory_sidecar(record, output_path: Path, trajectory_filename: str) -> None:
    payload = {
        'agent': record.agent_name,
        'model': record.model_name,
        'run_id': record.run_id,
        'language': record.language,
        'sandbox_dir': record.sandbox_dir,
        'trajectory_capture_note': record.trajectory_capture_note,
        'trajectory': record.trajectory,
        'raw_agent_stdout': record.raw_agent_stdout,
        'raw_agent_stderr': record.raw_agent_stderr,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    record.trajectory_file = trajectory_filename
    record.trajectory = None
    record.raw_agent_stdout = ''
    record.raw_agent_stderr = ''


def _maybe_strip_native_artifact(destination: Path, language: str) -> None:
    if language == 'python':
        return
    strip_bin = shutil.which('strip')
    if not strip_bin:
        return
    try:
        subprocess.run(
            [strip_bin, str(destination)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            text=False,
        )
    except Exception:
        return


def _copy_primary_artifact(record, harness, output_dir: Path, version_filename: str) -> str:
    artifact_path = harness.primary_artifact_path(Path(record.sandbox_dir))
    if artifact_path is None:
        return ''
    artifact_filename = _artifact_filename(version_filename, artifact_path, record.language)
    destination = output_dir / artifact_filename
    shutil.copy2(artifact_path, destination)
    _maybe_strip_native_artifact(destination, record.language)
    mode = destination.stat().st_mode
    destination.chmod(mode | stat.S_IXUSR)
    return artifact_filename


def _generation_task_payloads(agents_cfg: list[dict], languages: list[str], timeout: int) -> list[dict]:
    tasks: list[dict] = []
    for agent_cfg in agents_cfg:
        agent_name = agent_cfg['name']
        runs = agent_cfg.get('runs', 1)
        inner = dict(agent_cfg.get('config') or {})
        model_list = models_from_agent_config(inner)
        base_config = {k: v for k, v in inner.items() if k not in ('models', 'model')}

        print(
            f"\n  [{agent_name}] {len(languages)} language(s) × {len(model_list)} model(s) × {runs} run(s) "
            f"= {len(languages) * len(model_list) * runs} version(s)...",
        )

        for lang in languages:
            for configured_model in model_list:
                agent_config = {'timeout_seconds': timeout, **base_config}
                if configured_model is not None:
                    agent_config['model'] = configured_model
                display_model = configured_model if configured_model is not None else 'default'
                model_slug = slug_model(configured_model)
                for run_id in range(runs):
                    tasks.append({
                        'agent_name': agent_name,
                        'language': lang,
                        'configured_model': configured_model,
                        'display_model': display_model,
                        'model_slug': model_slug,
                        'run_id': run_id,
                        'agent_config': dict(agent_config),
                    })
    return tasks


def _run_generation_task(task: dict, spec_path: Path, output_dir: Path) -> tuple[dict, str]:
    agent_name = task['agent_name']
    lang = task['language']
    configured_model = task['configured_model']
    display_model = task['display_model']
    run_id = task['run_id']

    harness = get_harness(lang)
    adapter = get_agent(agent_name, dict(task['agent_config']))
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
    artifact_fname = _copy_primary_artifact(record, harness, output_dir, fname)
    record.artifact_file = artifact_fname

    trajectory_fname = _trajectory_filename(fname)
    trajectory_path = output_dir / trajectory_fname
    _write_trajectory_sidecar(record, trajectory_path, trajectory_fname)

    fpath = output_dir / fname
    record.to_json(fpath)

    index_entry = {
        'file': fname,
        'artifact_file': artifact_fname,
        'trajectory_file': trajectory_fname,
        'version_id': version_id_from_filename(fname),
        'agent': agent_name,
        'run_id': run_id,
        'language': lang,
        'configured_model': display_model,
        'model_slug': task['model_slug'],
        'build_status': record.build_status,
        'model': record.model_name,
        'error_message': record.error_message,
    }

    model_display = record.model_name
    if record.model_name != display_model and display_model != 'default':
        model_display = f"{display_model} → {record.model_name}"

    status_line = f"lang={lang!r} model={display_model!r} run {run_id}... status={record.build_status} model={model_display}"
    if record.error_message:
        em = record.error_message
        if len(em) > 500:
            em = em[:500] + '… (see version JSON for full text)'
        status_line += f"  ← {em}"
    return index_entry, status_line


def run(config_path: str, output_dir: str) -> None:
    config = yaml.safe_load(Path(config_path).read_text())
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    repo_root = Path(__file__).resolve().parents[1]
    spec_rel = config.get('agent_spec_path', 'benchmarks/launch_interceptor/spec_original.md')
    spec_path = (repo_root / spec_rel).resolve()
    if not spec_path.exists() or not spec_path.is_file():
        print(f"ERROR: agent spec not found at {spec_path}", file=sys.stderr)
        sys.exit(1)
    try:
        spec_path.relative_to(repo_root)
    except ValueError:
        print(f"ERROR: agent_spec_path must resolve under repo root ({repo_root})", file=sys.stderr)
        sys.exit(1)

    timeout = config.get('agent_timeout_seconds', 300)
    agents_cfg = config.get('agents', [])
    try:
        languages = normalize_languages(config.get('languages'))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        total = sum(
            len(languages)
            * len(models_from_agent_config(a.get('config') or {}))
            * a.get('runs', 1)
            for a in agents_cfg
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Generating {total} versions for {len(agents_cfg)} agent(s)...")

    try:
        tasks = _generation_task_payloads(agents_cfg, languages, timeout)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    version_index: list[dict] = []
    generated = 0

    print(f"Running up to {_GENERATION_WORKERS} concurrent generations.")
    with ThreadPoolExecutor(max_workers=_GENERATION_WORKERS) as executor:
        futures = [executor.submit(_run_generation_task, task, spec_path, out) for task in tasks]
        for future in as_completed(futures):
            index_entry, status_line = future.result()
            version_index.append(index_entry)
            print(f"    {status_line}")
            generated += 1

    index_path = out / 'index.json'
    index_path.write_text(json.dumps(version_index, indent=2))
    print(f"\nDone. {generated} versions written to {output_dir}")
    print(f"Index: {index_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate agent versions')
    parser.add_argument('--config', required=True, help='Path to YAML config')
    parser.add_argument('--output', required=True, help='Output directory')
    args = parser.parse_args()
    run(args.config, args.output)


if __name__ == '__main__':
    main()
