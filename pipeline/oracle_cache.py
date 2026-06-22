from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from benchmarks.launch_interceptor.decide_diff import pack_case_expected_output, packed_output_digest
from benchmarks.launch_interceptor.generator import iter_campaign_cases

_CACHE_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class OracleCache:
    seed: int
    campaign_n: int
    cmv_bits: np.ndarray
    pum_rows: np.ndarray
    fuv_bits: np.ndarray
    launch_bits: np.ndarray
    digests: np.ndarray
    cache_path: Path

    def expected_at(self, test_id: int) -> tuple[int, tuple[int, ...], int, int, int]:
        return (
            int(self.cmv_bits[test_id]),
            tuple(int(v) for v in self.pum_rows[test_id]),
            int(self.fuv_bits[test_id]),
            int(self.launch_bits[test_id]),
            int(self.digests[test_id]),
        )


def oracle_cache_path(cache_dir: Path, seed: int, campaign_n: int) -> Path:
    return cache_dir / f"oracle__seed{seed}__n{campaign_n}__v{_CACHE_SCHEMA_VERSION}.npz"


def load_or_build_oracle_cache(cache_dir: Path, seed: int, campaign_n: int) -> OracleCache:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = oracle_cache_path(cache_dir, seed, campaign_n)
    if cache_path.is_file():
        with np.load(cache_path, allow_pickle=False) as data:
            meta_raw = data["meta"].item()
            meta = json.loads(str(meta_raw))
            if meta.get("schema_version") == _CACHE_SCHEMA_VERSION and meta.get("seed") == seed and meta.get("campaign_n") == campaign_n:
                return OracleCache(
                    seed=seed,
                    campaign_n=campaign_n,
                    cmv_bits=data["cmv_bits"].astype(np.uint16, copy=False),
                    pum_rows=data["pum_rows"].astype(np.uint16, copy=False),
                    fuv_bits=data["fuv_bits"].astype(np.uint16, copy=False),
                    launch_bits=data["launch_bits"].astype(np.uint8, copy=False),
                    digests=data["digests"].astype(np.uint64, copy=False),
                    cache_path=cache_path,
                )
    cmv_bits = np.zeros(campaign_n, dtype=np.uint16)
    pum_rows = np.zeros((campaign_n, 15), dtype=np.uint16)
    fuv_bits = np.zeros(campaign_n, dtype=np.uint16)
    launch_bits = np.zeros(campaign_n, dtype=np.uint8)
    digests = np.zeros(campaign_n, dtype=np.uint64)
    for idx, case in enumerate(iter_campaign_cases(seed=seed, n=campaign_n)):
        packed = pack_case_expected_output(case)
        cmv_bits[idx] = packed.cmv_bits
        pum_rows[idx, :] = packed.pum_rows
        fuv_bits[idx] = packed.fuv_bits
        launch_bits[idx] = packed.launch_bit
        digests[idx] = packed_output_digest(packed)
    meta = json.dumps({
        "schema_version": _CACHE_SCHEMA_VERSION,
        "seed": seed,
        "campaign_n": campaign_n,
    }, separators=(",", ":"))
    np.savez_compressed(
        cache_path,
        meta=np.array(meta),
        cmv_bits=cmv_bits,
        pum_rows=pum_rows,
        fuv_bits=fuv_bits,
        launch_bits=launch_bits,
        digests=digests,
    )
    return OracleCache(
        seed=seed,
        campaign_n=campaign_n,
        cmv_bits=cmv_bits,
        pum_rows=pum_rows,
        fuv_bits=fuv_bits,
        launch_bits=launch_bits,
        digests=digests,
        cache_path=cache_path,
    )
