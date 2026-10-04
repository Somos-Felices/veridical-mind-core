# Sprint 1 Results Report

## Status

Sprint 1 engineering implementation, integration, observability wiring, runtime validation and regression testing are complete.

The remaining project-owned acceptance dependency is the approved authoritative corpus and its final A/C/K, ICD weight, threshold and expected-category inputs. These values are intentionally not inferred.

## Implemented

1. MICD / UDV ingestion foundation
2. Source governance and provenance validation
3. Immutable document versioning
4. ICD propagation
5. Local embedding provider
6. Qdrant retrieval
7. IR ranking
8. TOP_K=10
9. Deterministic MCG A/B/C classification
10. Generation Gateway enforcement
11. Category C physical LLM suppression
12. RPA fallback
13. Category B qualification and ICR
14. MRM structured traces
15. Optional JSONL MRM persistence
16. Langfuse surrounding observability
17. Integrated QueryService
18. FastAPI /health and /query
19. Source-document filtering through the query API

## Runtime Validation

FastAPI health check passed.

Qdrant connected successfully.

Embedding dimension: 384.

Live Category C request returned:

category = C
llm_invoked = false
icr = null
RPA response returned

The live MRM trace recorded:

category = C
llm_invoked = false
IR maximum = 0.35181619
IR average = 0.2502539641
MCG classification latency = 0.0172 ms

The measured MCG boundary latency is below the required 50 ms target.

## Regression Validation

Full automated test suite:

71 passed

Langfuse observer smoke test:

PASS

Langfuse authenticated client initialization:

PASS

## Observability

MRM remains the project reliability record.

Langfuse is used as surrounding observability and receives MRM-derived control metadata without raw query, prompt or document content.

Category C records llm_invoked=false.

## Security

Secrets remain in environment configuration and are not part of the repository.

Patent-sensitive implementation, private evaluation material and confidential source material must remain outside public product surfaces.

The authoritative corpus must only be ingested after project approval.

## Formal Acceptance Dependency

Final corpus-based T1-T4 acceptance requires:

1. Approved 12-document corpus
2. Corpus manifest and provenance metadata
3. Final A/C/K assignments
4. Final ICD weights
5. Final MCG thresholds
6. Approved validation queries and expected categories

No unresolved project parameters are inferred by the engineering implementation.

## Sprint 1 Engineering Conclusion

The Sprint 1 technical vertical slice is implementation-complete and validated.

Once the authoritative project inputs are supplied, the same acceptance path can be rerun without rebuilding the core.
