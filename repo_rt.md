# NVP AI Agent Fault-Independence Experiment — Results

## Pilot Summary

- **Benchmark**: Launch Interceptor Program (Knight & Leveson 1986)
- **Admitted versions**: 45
- **Campaign test cases**: 10000
- **Observed simultaneous failures (K)**: 3
- **Expected under independence (μ)**: 0.80
- **K&L z-statistic**: 2.4519
- **p-value**: 1.4212e-02
- **Reject H0 at 99% (|z|>2.576)**: NO

## Per-Version Failure Rates

| Version | Agent | Total Tests | Failures | Failure Rate |
|---------|-------|-------------|----------|--------------|
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code | 10000 | 3 | 0.0003 |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code | 10000 | 3 | 0.0003 |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code | 10000 | 0 | 0.0000 |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code | 10000 | 0 | 0.0000 |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code | 10000 | 1 | 0.0001 |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | claude_code | 10000 | 0 | 0.0000 |
| claude_code__m_claude-sonnet-4__l_python__run000 | claude_code | 10000 | 3 | 0.0003 |
| codex__m_gpt-5-codex__l_pascal__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5-codex__l_python__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5.1-codex__l_python__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5.1__l_pascal__run000 | codex | 10000 | 3 | 0.0003 |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.2-codex__l_python__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.2__l_pascal__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.2__l_python__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.3-codex__l_python__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.4-mini__l_pascal__run000 | codex | 10000 | 2 | 0.0002 |
| codex__m_gpt-5.4-mini__l_python__run000 | codex | 10000 | 101 | 0.0101 |
| codex__m_gpt-5.4__l_pascal__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5.4__l_python__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5__l_pascal__run000 | codex | 10000 | 0 | 0.0000 |
| codex__m_gpt-5__l_python__run000 | codex | 10000 | 0 | 0.0000 |
| cursor__m_composer-1.5__l_pascal__run000 | cursor | 10000 | 0 | 0.0000 |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor | 10000 | 0 | 0.0000 |
| cursor__m_composer-2-fast__l_python__run000 | cursor | 10000 | 0 | 0.0000 |
| cursor__m_composer-2__l_pascal__run000 | cursor | 10000 | 3 | 0.0003 |
| cursor__m_composer-2__l_python__run000 | cursor | 10000 | 0 | 0.0000 |
| cursor__m_grok-4-20__l_python__run000 | cursor | 10000 | 3 | 0.0003 |
| cursor__m_kimi-k2.5__l_python__run000 | cursor | 10000 | 3 | 0.0003 |
| cursor__m_kimi-k2.5__l_rust__run000 | cursor | 10000 | 3 | 0.0003 |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | gemini | 10000 | 3 | 0.0003 |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini | 10000 | 0 | 0.0000 |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini | 10000 | 0 | 0.0000 |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | gemini | 10000 | 0 | 0.0000 |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | gemini | 10000 | 0 | 0.0000 |
| opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | opencode | 10000 | 0 | 0.0000 |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode | 10000 | 0 | 0.0000 |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode | 10000 | 3 | 0.0003 |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode | 10000 | 8 | 0.0008 |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode | 10000 | 3 | 0.0003 |
| opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | opencode | 10000 | 0 | 0.0000 |

## Pairwise Co-failure Analysis

| Version i | Version j | Observed | Expected | Ratio | Phi | Binomial p | Sig? |
|-----------|-----------|----------|----------|-------|-----|------------|------|
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code__m_claude-opus-4.5__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code__m_claude-opus-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | claude_code__m_claude-sonnet-4__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.1__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | claude_code__m_claude-sonnet-4__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-opus-4.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-opus-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | claude_code__m_claude-sonnet-4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | claude_code__m_claude-sonnet-4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-opus-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code__m_claude-sonnet-4.6__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | claude_code__m_claude-sonnet-4__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5-codex__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0001 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.01 | 0.00 | -0.0010 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | 0.00 | -0.0003 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | 0.00 | -0.0002 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | claude_code__m_claude-sonnet-4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4.6__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| claude_code__m_claude-sonnet-4__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| claude_code__m_claude-sonnet-4__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.1-codex-max__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.1-codex-max__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.1-codex__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex-max__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex-max__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.1-codex__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.1__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.2-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.1__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| codex__m_gpt-5.1__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.2-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.3-codex__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.3-codex__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.3-codex__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | codex__m_gpt-5.4-mini__l_python__run000 | 0 | 0.02 | 0.00 | -0.0014 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 1 | 0.00 | 625.00 | 0.2497 | 1.599e-03 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 1 | 0.00 | 1666.67 | 0.4081 | 5.998e-04 | no |
| codex__m_gpt-5.4-mini__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5.4__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.08 | 0.00 | -0.0029 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.03 | 0.00 | -0.0017 | 1.000e+00 | no |
| codex__m_gpt-5.4-mini__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | codex__m_gpt-5.4__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | codex__m_gpt-5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5.4__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | codex__m_gpt-5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_composer-1.5__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| codex__m_gpt-5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_composer-2-fast__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-1.5__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor__m_composer-2-fast__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | cursor__m_composer-2__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2-fast__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | cursor__m_composer-2__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | cursor__m_grok-4-20__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_composer-2__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | cursor__m_grok-4-20__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_composer-2__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | cursor__m_kimi-k2.5__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_grok-4-20__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_grok-4-20__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_grok-4-20__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_grok-4-20__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_grok-4-20__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| cursor__m_grok-4-20__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_grok-4-20__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | cursor__m_kimi-k2.5__l_rust__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_python__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| cursor__m_kimi-k2.5__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | gemini__m_gemini-2.5-flash__l_pascal__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| cursor__m_kimi-k2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| cursor__m_kimi-k2.5__l_rust__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| cursor__m_kimi-k2.5__l_rust__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| gemini__m_gemini-2.5-flash__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3-flash-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3-flash-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | gemini__m_gemini-3.1-pro-preview__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| gemini__m_gemini-3.1-pro-preview__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | opencode__m_google_gemma-4-31b-it__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-26b-a4b-it__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_google_gemma-4-31b-it__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 3333.33 | 1.0000 | 1.214e-10 | **YES** |
| opencode__m_qwen_qwen3.5-397b-a17b__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | 3 | 0.00 | 1250.00 | 0.6122 | 2.299e-09 | **YES** |
| opencode__m_qwen_qwen3.5-flash-02-23__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |
| opencode__m_qwen_qwen3.5-plus-02-15__l_python__run000 | opencode__m_qwen_qwen3.6-plus__l_pascal__run000 | 0 | 0.00 | N/A | N/A | N/A | no |

> Bonferroni-corrected α = 0.0001

## Statistical Methodology

Following Knight & Leveson (1986) exactly:

```
P_0 = ∏(1 - p_i)
P_1 = Σ p_i · ∏_{j≠i}(1 - p_j)
P_m = 1 - P_0 - P_1
μ = T · P_m = 10000 · 0.000080 = 0.80
z = (K - μ) / σ = (3 - 0.80) / 0.8961 = 2.4519
```

## Interpretation

> **H0 not rejected** at 99% confidence (z=2.45, |z| < 2.576). The observed coincident failures are consistent with independent failures.

## Cross-Language Fault Dependence (matched pairs)

Pairs are versions with the same agent/model/run but different `language` (see `match_base_key` in `analysis/analyze_results.py`).

- **Matched pairs analyzed**: 15
- **Mean phi**: 0.7997

| version_i (lang) | version_j (lang) | Observed co-fails | Expected | Phi |
|-------------------|------------------|---------------------|----------|-----|
| claude_code__m_claude-opus-4.5__l_pascal__run000 (pascal) | claude_code__m_claude-opus-4.5__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5-codex__l_pascal__run000 (pascal) | codex__m_gpt-5-codex__l_python__run000 (python) | 3 | 0.00 | 1.0000 |
| codex__m_gpt-5.1-codex-max__l_pascal__run000 (pascal) | codex__m_gpt-5.1-codex-max__l_python__run000 (python) | 3 | 0.00 | 1.0000 |
| codex__m_gpt-5.1-codex__l_pascal__run000 (pascal) | codex__m_gpt-5.1-codex__l_python__run000 (python) | 3 | 0.00 | 1.0000 |
| codex__m_gpt-5.2-codex__l_pascal__run000 (pascal) | codex__m_gpt-5.2-codex__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5.2__l_pascal__run000 (pascal) | codex__m_gpt-5.2__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5.3-codex__l_pascal__run000 (pascal) | codex__m_gpt-5.3-codex__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5.4-mini__l_pascal__run000 (pascal) | codex__m_gpt-5.4-mini__l_python__run000 (python) | 0 | 0.02 | -0.0014 |
| codex__m_gpt-5.4__l_pascal__run000 (pascal) | codex__m_gpt-5.4__l_python__run000 (python) | 0 | 0.00 | nan |
| codex__m_gpt-5__l_pascal__run000 (pascal) | codex__m_gpt-5__l_python__run000 (python) | 0 | 0.00 | nan |
| cursor__m_composer-2-fast__l_pascal__run000 (pascal) | cursor__m_composer-2-fast__l_python__run000 (python) | 0 | 0.00 | nan |
| cursor__m_composer-2__l_pascal__run000 (pascal) | cursor__m_composer-2__l_python__run000 (python) | 0 | 0.00 | nan |
| cursor__m_kimi-k2.5__l_python__run000 (python) | cursor__m_kimi-k2.5__l_rust__run000 (rust) | 3 | 0.00 | 1.0000 |
| gemini__m_gemini-3-flash-preview__l_pascal__run000 (pascal) | gemini__m_gemini-3-flash-preview__l_python__run000 (python) | 0 | 0.00 | nan |
| gemini__m_gemini-3.1-pro-preview__l_pascal__run000 (pascal) | gemini__m_gemini-3.1-pro-preview__l_python__run000 (python) | 0 | 0.00 | nan |


## Caveats

- If this run used mock agents only, these results **validate the framework infrastructure**, not empirical claims about real AI coding agent behavior.
- Real-agent runs require API keys (ANTHROPIC_API_KEY, CURSOR_API_KEY, CODEX_API_KEY).
- Campaign size (1,000) is much smaller than K&L (1,000,000); statistical power is limited.
- See `docs/experiment_design.md` for full discussion of confounders and threats to validity.

## Files

| File | Description |
|------|-------------|
| `results/pilot/campaign.csv` | Raw pass/fail matrix (test × version) |
| `results/pilot/stats.json` | Full statistics in machine-readable format |
| `results/pilot/summary_table.csv` | Per-version summary |
| `results/pilot/failure_heatmap.pdf` | Pairwise co-failure heatmap |
| `results/pilot/failure_rates.pdf` | Per-version failure rate bar chart |

## Reference

Knight, J. C. & Leveson, N. G. (1986). An experimental evaluation of the assumption of independence in multiversion programming. *IEEE Transactions on Software Engineering*, 12(1), 96–109.