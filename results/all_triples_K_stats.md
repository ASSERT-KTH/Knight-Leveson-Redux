# All-triples K statistics

## Full pool (all campaign versions)

- Versions in pool: **48**
- Triples C(48, 3): **17,296**
- T (test cases): 1,000,000

### Single-version failure counts vs triple unit K

Oracle-aware failure count: per version, number of tests where output disagrees with the oracle; per triple (N=3), *K* is the number of tests where at least two members fail (majority is wrong). Rows **P0**–**P100** are empirical percentiles over the *n* single-version counts and over the *n* triple *K* values, respectively (same labels as numpy `percentile`).

| Statistic | Single versions (n = 48) | All triples (n = 17,296) |
|---|---:|---:|
| Min | 0 (0.0000% of T) | 0 (0.0000% of T) |
| Max | 10,469 (1.0469% of T) | 419 (0.0419% of T) |
| Mean | 387.44 (0.0387% of T) | 130.99 (0.0131% of T) |
| Std dev | 1488.37 | 194.20 |
| With K = 0 (count) | 27 | 11,844 |
| With K = 0 (% of row population) | 56.25% | 68.48% |
| Unique K values | 6 | 3 |
| P0 | 0 (0.0000% of T) | 0 (0.0000% of T) |
| P1 | 0 (0.0000% of T) | 0 (0.0000% of T) |
| P5 | 0 (0.0000% of T) | 0 (0.0000% of T) |
| P10 | 0 (0.0000% of T) | 0 (0.0000% of T) |
| P25 | 0 (0.0000% of T) | 0 (0.0000% of T) |
| P50 | 0 (0.0000% of T) | 0 (0.0000% of T) |
| P75 | 419 (0.0419% of T) | 419 (0.0419% of T) |
| P90 | 419 (0.0419% of T) | 419 (0.0419% of T) |
| P95 | 429 (0.0429% of T) | 419 (0.0419% of T) |
| P99 | 6,004 (0.6004% of T) | 419 (0.0419% of T) |
| P100 | 10,469 (1.0469% of T) | 419 (0.0419% of T) |

#### Single-version failure counts (unique values)

| K | # versions | % of versions | K / T (%) |
|---:|---:|---:|---:|
| 0 | 27 | 56.25% | 0.0000% |
| 10 | 2 | 4.17% | 0.0010% |
| 419 | 16 | 33.33% | 0.0419% |
| 435 | 1 | 2.08% | 0.0435% |
| 969 | 1 | 2.08% | 0.0969% |
| 10,469 | 1 | 2.08% | 1.0469% |

### Comparison to individual members (within each triple)

- Triples with K = 0:  **11,844**  (68.48% of all triples)
- K < min(member K)  — unit beats its best member:   **37**  (0.2%)
- K > min(member K)  — unit worse than best member:  **4,464**  (25.8%)
- K < max(member K)  — unit beats its worst member:  **10,304**  (59.6%)

### Individual version K (pool)

| Version | K | K/T (%) |
|---|---:|---:|
| `claude-code-claude-haiku-4.5-l-rust` | 419 | 0.0419% |
| `claude-code-claude-opus-4.5-l-pascal` | 0 | 0.0000% |
| `claude-code-claude-opus-4.5-l-python` | 0 | 0.0000% |
| `claude-code-claude-opus-4.5-l-rust` | 0 | 0.0000% |
| `claude-code-claude-opus-4.6-l-pascal` | 0 | 0.0000% |
| `claude-code-claude-opus-4.6-l-python` | 0 | 0.0000% |
| `claude-code-claude-opus-4.6-l-rust` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.5-l-pascal` | 969 | 0.0969% |
| `claude-code-claude-sonnet-4.5-l-python` | 0 | 0.0000% |
| `claude-code-claude-sonnet-4.5-l-rust` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.6-l-pascal` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.6-l-python` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.6-l-rust` | 0 | 0.0000% |
| `codex-gpt-5.2-l-pascal` | 0 | 0.0000% |
| `codex-gpt-5.2-l-python` | 0 | 0.0000% |
| `codex-gpt-5.2-l-rust` | 0 | 0.0000% |
| `codex-gpt-5.3-codex-l-pascal` | 0 | 0.0000% |
| `codex-gpt-5.3-codex-l-python` | 0 | 0.0000% |
| `codex-gpt-5.3-codex-l-rust` | 0 | 0.0000% |
| `codex-gpt-5.4-mini-l-python` | 0 | 0.0000% |
| `codex-gpt-5.4-mini-l-rust` | 0 | 0.0000% |
| `codex-gpt-5.4-l-pascal` | 0 | 0.0000% |
| `codex-gpt-5.4-l-python` | 0 | 0.0000% |
| `codex-gpt-5.4-l-rust` | 0 | 0.0000% |
| `cursor-composer-2.5-l-pascal` | 419 | 0.0419% |
| `cursor-composer-2.5-l-python` | 0 | 0.0000% |
| `cursor-composer-2.5-l-rust` | 419 | 0.0419% |
| `cursor-composer-2-l-pascal` | 0 | 0.0000% |
| `cursor-composer-2-l-python` | 435 | 0.0435% |
| `cursor-composer-2-l-rust` | 0 | 0.0000% |
| `gemini-gemini-2.5-pro-l-python` | 419 | 0.0419% |
| `gemini-gemini-2.5-pro-l-rust` | 419 | 0.0419% |
| `gemini-gemini-3-flash-preview-l-pascal` | 0 | 0.0000% |
| `gemini-gemini-3-flash-preview-l-python` | 0 | 0.0000% |
| `gemini-gemini-3-flash-preview-l-rust` | 0 | 0.0000% |
| `gemini-gemini-3.1-pro-preview-l-pascal` | 10 | 0.0010% |
| `gemini-gemini-3.1-pro-preview-l-python` | 10 | 0.0010% |
| `gemini-gemini-3.1-pro-preview-l-rust` | 0 | 0.0000% |
| `opencode-google-gemma-4-31b-it-l-python` | 0 | 0.0000% |
| `opencode-qwen-qwen3.5-397b-a17b-l-pascal` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-397b-a17b-l-python` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-397b-a17b-l-rust` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-flash-02-23-l-python` | 10,469 | 1.0469% |
| `opencode-qwen-qwen3.5-plus-02-15-l-python` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-plus-02-15-l-rust` | 419 | 0.0419% |
| `opencode-qwen-qwen3.6-plus-l-pascal` | 419 | 0.0419% |
| `opencode-qwen-qwen3.6-plus-l-python` | 0 | 0.0000% |
| `opencode-qwen-qwen3.6-plus-l-rust` | 419 | 0.0419% |

### Best 20 triples (lowest K)

| Rank | K | K/T (%) | Members |
|---:|---:|---:|---|
| 1 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `gemini-gemini-3-flash-preview-l-rust` |
| 2 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `opencode-qwen-qwen3.6-plus-l-python` |
| 3 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2-l-pascal` · `cursor-composer-2-l-python` |
| 4 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2-l-pascal` · `cursor-composer-2-l-rust` |
| 5 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2-l-pascal` · `gemini-gemini-2.5-pro-l-python` |
| 6 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2-l-pascal` · `gemini-gemini-2.5-pro-l-rust` |
| 7 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 8 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `cursor-composer-2-l-pascal` |
| 9 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `cursor-composer-2-l-python` |
| 10 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `cursor-composer-2-l-rust` |
| 11 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `gemini-gemini-3-flash-preview-l-pascal` |
| 12 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `gemini-gemini-3-flash-preview-l-python` |
| 13 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `opencode-google-gemma-4-31b-it-l-python` |
| 14 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-rust` · `gemini-gemini-3.1-pro-preview-l-pascal` |
| 15 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-pascal` |
| 16 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-python` |
| 17 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` |
| 18 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.5-flash-02-23-l-python` |
| 19 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-python` |
| 20 | 0 | 0.0000% | `claude-code-claude-sonnet-4.5-l-python` · `cursor-composer-2.5-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |

### Worst 20 triples (highest K)

| Rank | K | K/T (%) | Members |
|---:|---:|---:|---|
| 1 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `claude-code-claude-opus-4.6-l-rust` |
| 2 | 419 | 0.0419% | `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 3 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 4 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 5 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-python` |
| 6 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 7 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 8 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-python` |
| 9 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 10 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-python` |
| 11 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 12 | 419 | 0.0419% | `opencode-qwen-qwen3.5-flash-02-23-l-python` · `opencode-qwen-qwen3.6-plus-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 13 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 14 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |
| 15 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.5-plus-02-15-l-python` |
| 16 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.5-flash-02-23-l-python` |
| 17 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` |
| 18 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.5-397b-a17b-l-python` |
| 19 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-pascal` · `opencode-qwen-qwen3.5-397b-a17b-l-pascal` |
| 20 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.5-l-python` · `claude-code-claude-sonnet-4.5-l-pascal` |

### K value breakdown (all unique values)

| K | # triples | % of total | K / T (%) |
|---:|---:|---:|---:|
| 0 | 11,844 | 68.48% | 0.0000% |
| 10 | 46 | 0.27% | 0.0010% |
| 419 | 5,406 | 31.26% | 0.0419% |

---

## Trimmed pool (no 0-fail, no mega-fail versions)

**Exclusion rule:** drop versions with **zero** oracle failures and versions with **K ≥ 10,000**.

#### Excluded: zero oracle failures

| Version | K |
|---|---:|
| `claude-code-claude-opus-4.5-l-pascal` | 0 |
| `claude-code-claude-opus-4.5-l-python` | 0 |
| `claude-code-claude-opus-4.5-l-rust` | 0 |
| `claude-code-claude-opus-4.6-l-pascal` | 0 |
| `claude-code-claude-opus-4.6-l-python` | 0 |
| `claude-code-claude-sonnet-4.5-l-python` | 0 |
| `claude-code-claude-sonnet-4.6-l-rust` | 0 |
| `codex-gpt-5.2-l-pascal` | 0 |
| `codex-gpt-5.2-l-python` | 0 |
| `codex-gpt-5.2-l-rust` | 0 |
| `codex-gpt-5.3-codex-l-pascal` | 0 |
| `codex-gpt-5.3-codex-l-python` | 0 |
| `codex-gpt-5.3-codex-l-rust` | 0 |
| `codex-gpt-5.4-mini-l-python` | 0 |
| `codex-gpt-5.4-mini-l-rust` | 0 |
| `codex-gpt-5.4-l-pascal` | 0 |
| `codex-gpt-5.4-l-python` | 0 |
| `codex-gpt-5.4-l-rust` | 0 |
| `cursor-composer-2.5-l-python` | 0 |
| `cursor-composer-2-l-pascal` | 0 |
| `cursor-composer-2-l-rust` | 0 |
| `gemini-gemini-3-flash-preview-l-pascal` | 0 |
| `gemini-gemini-3-flash-preview-l-python` | 0 |
| `gemini-gemini-3-flash-preview-l-rust` | 0 |
| `gemini-gemini-3.1-pro-preview-l-rust` | 0 |
| `opencode-google-gemma-4-31b-it-l-python` | 0 |
| `opencode-qwen-qwen3.6-plus-l-python` | 0 |

#### Excluded: K ≥ 10,000

| Version | K |
|---|---:|
| `opencode-qwen-qwen3.5-flash-02-23-l-python` | 10,469 |

**Remaining versions:** **20**

- Versions in pool: **20**
- Triples C(20, 3): **1,140**
- T (test cases): 1,000,000

### Single-version failure counts vs triple unit K

Oracle-aware failure count: per version, number of tests where output disagrees with the oracle; per triple (N=3), *K* is the number of tests where at least two members fail (majority is wrong). Rows **P0**–**P100** are empirical percentiles over the *n* single-version counts and over the *n* triple *K* values, respectively (same labels as numpy `percentile`).

| Statistic | Single versions (n = 20) | All triples (n = 1,140) |
|---|---:|---:|
| Min | 10 (0.0010% of T) | 0 (0.0000% of T) |
| Max | 969 (0.0969% of T) | 419 (0.0419% of T) |
| Mean | 406.40 (0.0406% of T) | 400.05 (0.0400% of T) |
| Std dev | 178.06 | 86.71 |
| With K = 0 (count) | 0 | 34 |
| With K = 0 (% of row population) | 0.00% | 2.98% |
| Unique K values | 4 | 3 |
| P0 | 10 (0.0010% of T) | 0 (0.0000% of T) |
| P1 | 10 (0.0010% of T) | 0 (0.0000% of T) |
| P5 | 10 (0.0010% of T) | 419 (0.0419% of T) |
| P10 | 378 (0.0378% of T) | 419 (0.0419% of T) |
| P25 | 419 (0.0419% of T) | 419 (0.0419% of T) |
| P50 | 419 (0.0419% of T) | 419 (0.0419% of T) |
| P75 | 419 (0.0419% of T) | 419 (0.0419% of T) |
| P90 | 421 (0.0421% of T) | 419 (0.0419% of T) |
| P95 | 462 (0.0462% of T) | 419 (0.0419% of T) |
| P99 | 868 (0.0868% of T) | 419 (0.0419% of T) |
| P100 | 969 (0.0969% of T) | 419 (0.0419% of T) |

#### Single-version failure counts (unique values)

| K | # versions | % of versions | K / T (%) |
|---:|---:|---:|---:|
| 10 | 2 | 10.00% | 0.0010% |
| 419 | 16 | 80.00% | 0.0419% |
| 435 | 1 | 5.00% | 0.0435% |
| 969 | 1 | 5.00% | 0.0969% |

### Comparison to individual members (within each triple)

- Triples with K = 0:  **34**  (2.98% of all triples)
- K < min(member K)  — unit beats its best member:   **34**  (3.0%)
- K > min(member K)  — unit worse than best member:  **272**  (23.9%)
- K < max(member K)  — unit beats its worst member:  **340**  (29.8%)

### Individual version K (pool)

| Version | K | K/T (%) |
|---|---:|---:|
| `claude-code-claude-haiku-4.5-l-rust` | 419 | 0.0419% |
| `claude-code-claude-opus-4.6-l-rust` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.5-l-pascal` | 969 | 0.0969% |
| `claude-code-claude-sonnet-4.5-l-rust` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.6-l-pascal` | 419 | 0.0419% |
| `claude-code-claude-sonnet-4.6-l-python` | 419 | 0.0419% |
| `cursor-composer-2.5-l-pascal` | 419 | 0.0419% |
| `cursor-composer-2.5-l-rust` | 419 | 0.0419% |
| `cursor-composer-2-l-python` | 435 | 0.0435% |
| `gemini-gemini-2.5-pro-l-python` | 419 | 0.0419% |
| `gemini-gemini-2.5-pro-l-rust` | 419 | 0.0419% |
| `gemini-gemini-3.1-pro-preview-l-pascal` | 10 | 0.0010% |
| `gemini-gemini-3.1-pro-preview-l-python` | 10 | 0.0010% |
| `opencode-qwen-qwen3.5-397b-a17b-l-pascal` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-397b-a17b-l-python` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-397b-a17b-l-rust` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-plus-02-15-l-python` | 419 | 0.0419% |
| `opencode-qwen-qwen3.5-plus-02-15-l-rust` | 419 | 0.0419% |
| `opencode-qwen-qwen3.6-plus-l-pascal` | 419 | 0.0419% |
| `opencode-qwen-qwen3.6-plus-l-rust` | 419 | 0.0419% |

### Best 20 triples (lowest K)

| Rank | K | K/T (%) | Members |
|---:|---:|---:|---|
| 1 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.5-397b-a17b-l-pascal` |
| 2 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.5-397b-a17b-l-python` |
| 3 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.5-plus-02-15-l-python` |
| 4 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` |
| 5 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-2.5-pro-l-rust` · `gemini-gemini-3.1-pro-preview-l-python` |
| 6 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-2.5-pro-l-rust` · `gemini-gemini-3.1-pro-preview-l-pascal` |
| 7 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 8 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 9 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |
| 10 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-python` |
| 11 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` |
| 12 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-python` |
| 13 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-pascal` |
| 14 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 15 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 16 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |
| 17 | 0 | 0.0000% | `cursor-composer-2.5-l-rust` · `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` |
| 18 | 0 | 0.0000% | `cursor-composer-2.5-l-rust` · `cursor-composer-2-l-python` · `gemini-gemini-3.1-pro-preview-l-python` |
| 19 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-2.5-pro-l-python` · `gemini-gemini-3.1-pro-preview-l-pascal` |
| 20 | 0 | 0.0000% | `cursor-composer-2-l-python` · `gemini-gemini-2.5-pro-l-python` · `gemini-gemini-3.1-pro-preview-l-python` |

### Worst 20 triples (highest K)

| Rank | K | K/T (%) | Members |
|---:|---:|---:|---|
| 1 | 419 | 0.0419% | `claude-code-claude-haiku-4.5-l-rust` · `claude-code-claude-opus-4.6-l-rust` · `claude-code-claude-sonnet-4.5-l-pascal` |
| 2 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 3 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 4 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 5 | 419 | 0.0419% | `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 6 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 7 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 8 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 9 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 10 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 11 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |
| 12 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 13 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 14 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 15 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 16 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 17 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-python` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |
| 18 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.6-plus-l-rust` |
| 19 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.6-plus-l-pascal` |
| 20 | 419 | 0.0419% | `opencode-qwen-qwen3.5-397b-a17b-l-python` · `opencode-qwen-qwen3.5-397b-a17b-l-rust` · `opencode-qwen-qwen3.5-plus-02-15-l-rust` |

### K value breakdown (all unique values)

| K | # triples | % of total | K / T (%) |
|---:|---:|---:|---:|
| 0 | 34 | 2.98% | 0.0000% |
| 10 | 18 | 1.58% | 0.0010% |
| 419 | 1,088 | 95.44% | 0.0419% |