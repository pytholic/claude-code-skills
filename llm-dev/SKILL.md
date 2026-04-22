---
name: llm-dev
description: Expert guidance for Large Language Model development — architectures, training, inference, and production applications. Use when working with transformer internals, pretraining/fine-tuning pipelines, RAG systems, agentic workflows, evals, tool use, structured outputs, reasoning models, MCP integrations, or shipping LLM features to production. Combines deep-learning expertise with modern engineering practices (Python 3.13+, pytest, eval-driven development).
---

# LLM Development

Expert help across the full LLM stack — from architecture internals to production systems.

## Core areas

### Architectures & internals
- Transformer families: GPT, Claude, Llama 3/4, Qwen 2.5/3, Gemini 2.5, DeepSeek V3/R1, Mistral, GPT-OSS.
- Attention variants: MHA, MQA, GQA, sliding-window, FlashAttention-2/3, PagedAttention.
- Positional schemes: RoPE (and YaRN / NTK scaling), ALiBi, learned absolute.
- Tokenization: BPE, WordPiece, SentencePiece, byte-level fallback. Know when vocab choice matters.
- Mixture-of-Experts: routing, load balancing, expert parallelism.
- Reasoning models: extended thinking / chain-of-thought budgets, when reasoning helps vs. hurts.

### Training & alignment
- Pretraining: data curation, deduplication, tokenization, curriculum, checkpointing.
- Fine-tuning: full-param, LoRA, QLoRA, DoRA, adapter stacking — pick based on VRAM, data size, drift tolerance.
- Preference optimization: RLHF (PPO), DPO, KTO, GRPO, constitutional AI.
- Evaluation: task-specific benchmarks (MMLU, GSM8K, HumanEval, SWE-Bench, MT-Bench), domain evals, LLM-as-judge pitfalls.

### Inference & serving
- Frameworks: vLLM, SGLang, TGI, TensorRT-LLM, llama.cpp, MLX (Apple Silicon).
- Quantization: GPTQ, AWQ, GGUF (Q4_K_M etc.), FP8, INT4. Trade quality vs. throughput vs. memory.
- Runtime tricks: KV-cache reuse, prefix caching, continuous batching, speculative decoding.
- Structured outputs: JSON schema, grammar-constrained decoding (Outlines, xgrammar), tool-call formats.

### Applications
- **RAG**: chunking strategy, embedding model choice, hybrid (BM25 + vector) retrieval, reranking (cross-encoders, ColBERT), query rewriting, evaluation of the retriever separately from the generator.
- **Agents**: ReAct, plan-execute, reflection, multi-agent patterns. Know when *not* to use an agent (simple pipelines beat agents for well-defined tasks).
- **Tool use**: function calling, MCP (Model Context Protocol) servers, tool-result handling, error recovery.
- **Prompt engineering**: system prompts, few-shot selection, output steering, prompt caching (Anthropic), context-window management.
- **Long context**: needle-in-haystack evals are insufficient — test multi-hop reasoning and distractor tolerance.

### Production concerns
- Cost: token accounting, caching (prompt cache, semantic cache), routing (small model first, escalate).
- Latency: time-to-first-token vs. total time, streaming, parallel tool calls.
- Observability: trace every call, log prompts + responses (with PII controls), track eval drift.
- Safety: jailbreak robustness, prompt-injection defenses, PII filtering, refusal calibration.

## Engineering approach

**Eval-driven development.** Define the eval *before* you tune the prompt or model. Without an eval, you're vibes-coding.

**Plan before coding.** For non-trivial LLM systems: architecture → component interfaces → failure modes → eval plan → implementation.

**Standards**
- Python 3.13+ with full type hints (`str | None`, not `Optional[str]`).
- Pydantic for configs, request/response schemas, and tool-input validation.
- Modular components: retriever, reranker, generator, evaluator as separate testable units.
- Memory-efficient: stream tokens, don't materialize full responses when piping.
- Device-agnostic where practical (CPU / CUDA / MPS / ROCm).
- Use Context7 MCP for up-to-date SDK docs (Anthropic, OpenAI, vLLM, etc.) before quoting API details — SDKs change fast.

**Testing**
- pytest with numerical tolerances for flaky LLM outputs (temperature > 0) — prefer assertions on structure + invariants over exact string match.
- Golden-set evals committed to the repo.
- Test edge cases: empty input, max-context, OOV tokens, malformed tool calls, refusals.

**Documentation**
- Record model version, sampling params, and prompt in every eval run — reproducibility matters.
- Document why a model/technique was chosen, not just what.

## Deliverables

For LLM features, provide:
1. Design rationale (model choice, RAG vs. fine-tune vs. prompt, tradeoffs).
2. Eval plan — what "good" looks like, how it's measured.
3. Modular implementation with clear component boundaries.
4. Cost + latency estimates.
5. Failure modes and how they're detected.
