# Heatmap Table Alternatives

## Pairwise Phi Summary by Diversity Relation

| Pair relation | Pairs | Defined phi | Undefined phi | phi = 1 | 0.9 <= phi < 1 | phi <= 0 | Median phi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| same lang, same agent | 61 | 12 | 49 | 8 (66.7%) | 0 (0.0%) | 1 (8.3%) | 1.000 |
| same lang, cross agent | 306 | 52 | 254 | 32 (61.5%) | 0 (0.0%) | 15 (28.8%) | 1.000 |
| cross lang, same agent | 160 | 40 | 120 | 26 (65.0%) | 0 (0.0%) | 5 (12.5%) | 1.000 |
| cross lang, cross agent | 601 | 106 | 495 | 55 (51.9%) | 0 (0.0%) | 35 (33.0%) | 1.000 |
| all pairs | 1128 | 210 | 918 | 121 (57.6%) | 0 (0.0%) | 56 (26.7%) | 1.000 |

## Exact Failure-Profile Clusters

| Profile | Versions | Failing inputs | Languages | Agents | Representative versions |
| --- | --- | --- | --- | --- | --- |
| P1 | 27 | 0 | pascal: 7, python: 11, rust: 9 | claude-code: 7, codex: 11, cursor: 3, gemini: 4, opencode: 2 | claude-code/claude-opus-4.5/pascal; claude-code/claude-opus-4.5/python; claude-code/claude-opus-4.5/rust; +24 more |
| P2 | 16 | 419 | pascal: 4, python: 4, rust: 8 | claude-code: 5, cursor: 2, gemini: 2, opencode: 7 | claude-code/claude-haiku-4.5/rust; claude-code/claude-opus-4.6/rust; claude-code/claude-sonnet-4.5/rust; +13 more |
| P3 | 2 | 10 | pascal: 1, python: 1 | gemini: 2 | gemini/gemini-3.1-pro-preview/pascal; gemini/gemini-3.1-pro-preview/python |

## High-Correlation Components (phi >= 0.9)

| Component | Versions | Agents | Languages | Edges | phi = 1 edges | Failure-count range |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 16 | claude-code: 5, cursor: 2, gemini: 2, opencode: 7 | pascal: 4, python: 4, rust: 8 | 120 | 120 | 419-419 |
| C2 | 2 | gemini: 2 | pascal: 1, python: 1 | 1 | 1 | 10-10 |
