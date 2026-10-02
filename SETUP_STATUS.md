# Setup Status

Current local engineering state for Veridical Mind Core.

## Current Validation

1. Python 3.11 environment is operational.
2. Existing local Qdrant container is operational.
3. `veridical_udv` is green with 384-dimensional cosine vectors.
4. Local `all-MiniLM-L6-v2` embedding provider is operational.
5. MICD / UDV ingestion foundation is implemented.
6. Corpus source governance validation is implemented.
7. Immutable document versioning and ICD propagation are implemented.
8. MREC retrieval and IR calculation are implemented.
9. MCG A/B/C classification is implemented.
10. Category C physically suppresses LLM invocation.
11. RPA fallback is implemented.
12. MRM trace logging and structured JSONL persistence are implemented.
13. Integrated query service is implemented.
14. FastAPI `/health` and `/query` endpoints are operational.
15. Full local test suite: 69 passed.
16. Live `/health` check: successful.
17. Live `/query` smoke test: successful with Category C and `llm_invoked=false`.
18. Exact working Python dependency versions are captured in `requirements.lock.txt`.

## Latency Validation

1. Repeatable MCG classification benchmark is available at `scripts/benchmark_mcg_latency.py`.
2. Benchmark uses 1000 local classification iterations.
3. Latest local benchmark minimum: 0.003100 ms.
4. Latest local benchmark mean: 0.003301 ms.
5. Latest local benchmark p95: 0.003400 ms.
6. Latest local benchmark maximum: 0.022900 ms.
7. Latest benchmark result: p95 < 50 ms target passed.

## Current Development Configuration

1. Local embeddings use `all-MiniLM-L6-v2`.
2. Embedding dimension is 384.
3. Local Qdrant uses collection `veridical_udv`.
4. Development LLM path uses the local stub.
5. MCG thresholds remain development configuration and are not final project thresholds.
6. ICD weights remain development defaults and are not final project weights.

## External Inputs

1. Approved 12-document Isidora Goyenechea corpus.
2. Source metadata and provenance.
3. Final A/C/K assignments.
4. Final ICD weights.
5. Final MCG thresholds.
6. Approved validation queries and expected categories.
7. Required external credentials and account access.
8. Production provider configuration.
9. Langfuse credentials when activated.
10. Hosting, DNS and email administration access.

## Release State

The local implementation has completed independent Sprint 1 engineering validation. The official corpus and project-owner technical parameters remain external inputs and are not invented locally.

No production deployment should be claimed until those inputs are available and the official acceptance cases have been executed.
