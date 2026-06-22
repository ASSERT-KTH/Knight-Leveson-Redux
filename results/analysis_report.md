# NVP AI Agent Fault-Independence Experiment — Results

## Pilot Summary

- **Benchmark**: Launch Interceptor Program (Knight & Leveson 1986)
- **Admitted versions**: 48
- **Campaign test cases**: 1000000
- **Observed simultaneous failures (K)**: 429
- **Expected under independence (μ)**: 115.36
- **K&L z-statistic**: 29.2032
- **p-value**: 0.0000e+00
- **Reject H0 at 99% (|z|>2.576)**: YES

## Per-Version Failure Rates

| Version | Agent | Total Tests | Failures | Failure Rate |
|---------|-------|-------------|----------|--------------|
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code | 1000000 | 419 | 0.0004 |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code | 1000000 | 0 | 0.0000 |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code | 1000000 | 0 | 0.0000 |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code | 1000000 | 0 | 0.0000 |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code | 1000000 | 0 | 0.0000 |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code | 1000000 | 0 | 0.0000 |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code | 1000000 | 419 | 0.0004 |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | claude_code | 1000000 | 969 | 0.0010 |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code | 1000000 | 0 | 0.0000 |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | claude_code | 1000000 | 419 | 0.0004 |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | claude_code | 1000000 | 419 | 0.0004 |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | claude_code | 1000000 | 419 | 0.0004 |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | claude_code | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.2__l_pascal__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.2__l_python__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.2__l_rust__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.3-codex__l_python__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.3-codex__l_rust__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.4-mini__l_python__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.4-mini__l_rust__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.4__l_pascal__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.4__l_python__run000 | codex | 1000000 | 0 | 0.0000 |
| codex__m_gpt-5.4__l_rust__run000 | codex | 1000000 | 0 | 0.0000 |
| cursor__m_composer-2.5__l_pascal__run000 | cursor | 1000000 | 419 | 0.0004 |
| cursor__m_composer-2.5__l_python__run000 | cursor | 1000000 | 0 | 0.0000 |
| cursor__m_composer-2.5__l_rust__run000 | cursor | 1000000 | 419 | 0.0004 |
| cursor__m_composer-2__l_pascal__run000 | cursor | 1000000 | 0 | 0.0000 |
| cursor__m_composer-2__l_python__run000 | cursor | 1000000 | 435 | 0.0004 |
| cursor__m_composer-2__l_rust__run000 | cursor | 1000000 | 0 | 0.0000 |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini | 1000000 | 419 | 0.0004 |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini | 1000000 | 419 | 0.0004 |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini | 1000000 | 0 | 0.0000 |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini | 1000000 | 0 | 0.0000 |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | gemini | 1000000 | 0 | 0.0000 |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | gemini | 1000000 | 10 | 0.0000 |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | gemini | 1000000 | 10 | 0.0000 |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | gemini | 1000000 | 0 | 0.0000 |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode | 1000000 | 0 | 0.0000 |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode | 1000000 | 419 | 0.0004 |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode | 1000000 | 419 | 0.0004 |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode | 1000000 | 419 | 0.0004 |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode | 1000000 | 10469 | 0.0105 |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode | 1000000 | 419 | 0.0004 |
| opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | opencode | 1000000 | 419 | 0.0004 |
| opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | opencode | 1000000 | 419 | 0.0004 |
| opencode__m_qwen_qwen3.6-plus__l_python__run000 | opencode | 1000000 | 0 | 0.0000 |
| opencode__m_qwen_qwen3.6-plus__l_rust__run000 | opencode | 1000000 | 419 | 0.0004 |

## Pairwise Co-failure Analysis

| Version i | Version j | Observed | Expected | Ratio | Phi | Binomial p | Sig? |
|-----------|-----------|----------|----------|-------|-----|------------|------|
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-opus-4.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-opus-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-opus-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-opus-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-opus-4.6__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-haiku-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-opus-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-opus-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-opus-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-opus-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-opus-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-opus-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_pascal__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.42 | 0.00 | -0.0006 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.01 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.01 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 10.14 | 41.30 | 0.1291 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.41 | 1031.99 | 0.6574 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5.4-mini__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | codex__m_gpt-5.4__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | cursor__m_composer-2.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | cursor__m_composer-2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | cursor__m_composer-2.5__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2.5__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| cursor__m_composer-2.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_python__run000 | cursor__m_composer-2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2.5__l_rust__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| cursor__m_composer-2.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | cursor__m_composer-2__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 4.55 | 0.00 | -0.0021 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.18 | 0.00 | -0.0004 | 1.000e+00 | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-2.5-pro__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-2.5-pro__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-pro__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini__m_gemini-3-flash-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 10 | 0.00 | 100000.00 | 1.0000 | 2.755e-47 | **YES** |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.10 | 0.00 | -0.0003 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.10 | 0.00 | -0.0003 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 4.39 | 95.52 | 0.1990 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 419 | 0.18 | 2386.63 | 1.0000 | 0.000e+00 | **YES** |
| opencode__m_qwen_qwen3.6-plus__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |

> Bonferroni-corrected α = 0.0000

## Statistical Methodology

Following Knight & Leveson (1986) exactly:

```
P_0 = ∏(1 - p_i)
P_1 = Σ p_i · ∏_{j≠i}(1 - p_j)
P_m = 1 - P_0 - P_1
μ = T · P_m = 1000000 · 0.000115 = 115.36
z = (K - μ) / σ = (429 - 115.36) / 10.7399 = 29.2032
```

## Interpretation

> **H0 rejected** at 99% confidence (z=29.20). The observed coincident failures significantly exceed what independence would predict. This is consistent with the original Knight & Leveson finding for human programmers.

## Cross-Language Fault Dependence (matched pairs)

Pairs are versions with the same agent/model/run but different `language` (see `match_base_key` in `analysis/analyze_results.py`).

- **Matched pairs analyzed**: 42
- **Mean phi**: 0.9657

| version_i (lang) | version_j (lang) | Observed co-fails | Expected | Phi |
|-------------------|------------------|---------------------|----------|-----|
| claude_code__m_claude-opus-4.5__l_pascal__run000 (pascal) | claude_code__m_claude-opus-4.5__l_python__run000 (python) | 0 | 0.00 | nan |
| claude_code__m_claude-opus-4.5__l_pascal__run000 (pascal) | claude_code__m_claude-opus-4.5__l_rust__run000 (rust) | 0 | 0.00 | nan |
| claude_code__m_claude-opus-4.5__l_python__run000 (python) | claude_code__m_claude-opus-4.5__l_rust__run000 (rust) | 0 | 0.00 | nan |
| claude_code__m_claude-opus-4.6__l_pascal__run000 (pascal) | claude_code__m_claude-opus-4.6__l_python__run000 (python) | 0 | 0.00 | nan |
| claude_code__m_claude-opus-4.6__l_pascal__run000 (pascal) | claude_code__m_claude-opus-4.6__l_rust__run000 (rust) | 0 | 0.00 | nan |
| claude_code__m_claude-opus-4.6__l_python__run000 (python) | claude_code__m_claude-opus-4.6__l_rust__run000 (rust) | 0 | 0.00 | nan |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 (pascal) | claude_code__m_claude-sonnet-4.5__l_python__run000 (python) | 0 | 0.00 | nan |
| claude_code__m_claude-sonnet-4.5__l_pascal__run000 (pascal) | claude_code__m_claude-sonnet-4.5__l_rust__run000 (rust) | 419 | 0.41 | 0.6574 |
| claude_code__m_claude-sonnet-4.5__l_python__run000 (python) | claude_code__m_claude-sonnet-4.5__l_rust__run000 (rust) | 0 | 0.00 | nan |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 (pascal) | claude_code__m_claude-sonnet-4.6__l_python__run000 (python) | 419 | 0.18 | 1.0000 |
| claude_code__m_claude-sonnet-4.6__l_pascal__run000 (pascal) | claude_code__m_claude-sonnet-4.6__l_rust__run000 (rust) | 0 | 0.00 | nan |
| claude_code__m_claude-sonnet-4.6__l_python__run000 (python) | claude_code__m_claude-sonnet-4.6__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.2__l_pascal__run000 (pascal) | codex__m_gpt-5.2__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5.2__l_pascal__run000 (pascal) | codex__m_gpt-5.2__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.2__l_python__run000 (python) | codex__m_gpt-5.2__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.3-codex__l_pascal__run000 (pascal) | codex__m_gpt-5.3-codex__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5.3-codex__l_pascal__run000 (pascal) | codex__m_gpt-5.3-codex__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.3-codex__l_python__run000 (python) | codex__m_gpt-5.3-codex__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.4-mini__l_python__run000 (python) | codex__m_gpt-5.4-mini__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.4__l_pascal__run000 (pascal) | codex__m_gpt-5.4__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5.4__l_pascal__run000 (pascal) | codex__m_gpt-5.4__l_rust__run000 (rust) | 0 | 0.00 | nan |
| codex__m_gpt-5.4__l_python__run000 (python) | codex__m_gpt-5.4__l_rust__run000 (rust) | 0 | 0.00 | nan |
| cursor__m_composer-2.5__l_pascal__run000 (pascal) | cursor__m_composer-2.5__l_python__run000 (python) | 0 | 0.00 | nan |
| cursor__m_composer-2.5__l_pascal__run000 (pascal) | cursor__m_composer-2.5__l_rust__run000 (rust) | 419 | 0.18 | 1.0000 |
| cursor__m_composer-2.5__l_python__run000 (python) | cursor__m_composer-2.5__l_rust__run000 (rust) | 0 | 0.00 | nan |
| cursor__m_composer-2__l_pascal__run000 (pascal) | cursor__m_composer-2__l_python__run000 (python) | 0 | 0.00 | nan |
| cursor__m_composer-2__l_pascal__run000 (pascal) | cursor__m_composer-2__l_rust__run000 (rust) | 0 | 0.00 | nan |
| cursor__m_composer-2__l_python__run000 (python) | cursor__m_composer-2__l_rust__run000 (rust) | 0 | 0.00 | nan |
| gemini__m_gemini-2.5-pro__l_python__run000 (python) | gemini__m_gemini-2.5-pro__l_rust__run000 (rust) | 419 | 0.18 | 1.0000 |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 (pascal) | gemini__m_gemini-3-flash-preview__l_python__run000 (python) | 0 | 0.00 | nan |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 (pascal) | gemini__m_gemini-3-flash-preview__l_rust__run000 (rust) | 0 | 0.00 | nan |
| gemini__m_gemini-3-flash-preview__l_python__run000 (python) | gemini__m_gemini-3-flash-preview__l_rust__run000 (rust) | 0 | 0.00 | nan |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 (pascal) | gemini__m_gemini-3.1-pro-preview__l_python__run000 (python) | 10 | 0.00 | 1.0000 |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 (pascal) | gemini__m_gemini-3.1-pro-preview__l_rust__run000 (rust) | 0 | 0.00 | nan |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 (python) | gemini__m_gemini-3.1-pro-preview__l_rust__run000 (rust) | 0 | 0.00 | nan |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 (pascal) | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 (python) | 419 | 0.18 | 1.0000 |
| opencode__m_qwen_qwen3.5-397b-a17b__l_pascal__run000 (pascal) | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 (rust) | 419 | 0.18 | 1.0000 |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 (python) | opencode__m_qwen_qwen3.5-397b-a17b__l_rust__run000 (rust) | 419 | 0.18 | 1.0000 |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 (python) | opencode__m_qwen_qwen3.5-plus-02-15__l_rust__run000 (rust) | 419 | 0.18 | 1.0000 |
| opencode__m_qwen_qwen3.6-plus__l_pascal__run000 (pascal) | opencode__m_qwen_qwen3.6-plus__l_python__run000 (python) | 0 | 0.00 | nan |
| … | … | (2 more rows in cross_language_pairwise.csv) | | |


## Caveats

- If this run used mock agents only, these results **validate the framework infrastructure**, not empirical claims about real AI coding agent behavior.
- Real-agent runs require API keys (ANTHROPIC_API_KEY, CURSOR_API_KEY, CODEX_API_KEY).
- Campaign size (1,000) is much smaller than K&L (1,000,000); statistical power is limited.
- See `docs/experiment_design.md` for full discussion of confounders and threats to validity.

## Files

| File | Description |
|------|-------------|
| `results/campaign.csv` | Raw pass/fail matrix (test × version) |
| `results/analysis/stats.json` | Full statistics in machine-readable format |
| `results/analysis/summary_table.csv` | Per-version summary |
| `results/analysis/failure_heatmap_{observed,expected,phi}.pdf` | Pairwise matrices (3 PDFs) |
| `results/analysis/failure_rates.pdf` | Per-version failure rate bar chart |
| `results/analysis/failures_by_language_stacked.pdf` | Stacked bars: tests with >20 failures × counts per language |

## Reference

Knight, J. C. & Leveson, N. G. (1986). An experimental evaluation of the assumption of independence in multiversion programming. *IEEE Transactions on Software Engineering*, 12(1), 96–109.