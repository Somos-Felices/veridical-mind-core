# Sprint 1 Results Report

## Status

Independent Sprint 1 engineering implementation and validation are complete.

## Implemented

1. MICD / UDV ingestion
2. Source governance validation
3. Immutable document versioning
4. ICD propagation
5. Local embedding and Qdrant retrieval
6. Source-filtered retrieval
7. IR ranking
8. TOP_K=10
9. MCG A/B/C classification
10. Generation Gateway enforcement
11. Category C physical LLM suppression
12. RPA fallback
13. Category B epistemic qualification and ICR
14. MRM structured traces
15. Optional MRM JSONL persistence
16. Integrated QueryService
17. FastAPI /health and /query
18. Reproducible public corpus validation

## Validation

Full test suite: 71 passed.

Public corpus validation:
1. 8 public source documents
2. 24 indexed public UDVs
3. Source filtering excludes non-public engineering fixtures
4. 6 retrieval queries executed
5. All 6 queries reached Category B under the development MCG configuration
6. All 6 recorded ICR
7. All 6 invoked the controlled LLM path
8. MRM traces were produced for all 6 decisions

MCG benchmark:
1. Iterations = 1000
2. Minimum = 0.003000 ms
3. Mean = 0.003517 ms
4. P95 = 0.005500 ms
5. Maximum = 0.049400 ms
6. Target P95 < 50 ms = passed

## Acceptance Coverage

T1: Category A generation at temperature 0.0 is covered by controlled gateway tests.

T2: Category B qualification with ICR is covered by controlled gateway tests and public corpus validation.

T3: Category C RPA with physical LLM suppression and llm_invoked=false is covered by controlled gateway tests.

T4: Required MRM trace fields without raw query storage are covered by integration and gateway tests.

Real QueryService integration through Qdrant, retrieval, IR, MCG, Gateway and MRM is validated.

## Public Corpus Boundary

The public corpus is an engineering fixture only.

Its ICD values are synthetic validation values and are not authoritative historical reliability assessments.

The public corpus must not be treated as the final project-authorized corpus.

## Remaining Project Inputs

1. Approved 12-document Isidora Goyenechea corpus
2. Authoritative corpus manifest and provenance metadata
3. Final A/C/K assignments
4. Final ICD weights
5. Final MCG thresholds
6. Approved validation queries and expected categories
7. Required production credentials and provider configuration

These values are intentionally not inferred from development defaults.

## Final Validation Path

Once authoritative project inputs are available, the official corpus is ingested and T1-T4 are rerun against that corpus.

No final authoritative corpus acceptance result is claimed before that step.
