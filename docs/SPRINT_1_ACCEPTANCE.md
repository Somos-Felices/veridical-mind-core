# Sprint 1 Acceptance Evidence

## E1 Environment

Python 3.11 environment operational.

Local Qdrant operational.

FastAPI operational.

Embedding provider operational at 384 dimensions.

## E2 Integrated Runtime

Verified path:

embedding -> Qdrant -> retrieval -> IR -> Top-K -> MCG -> Gateway/RPA -> MRM

## E3 Category C

Live HTTP acceptance:

category = C

llm_invoked = false

RPA response returned.

MRM trace also recorded llm_invoked=false.

## E4 MCG Latency

Measured classification boundary:

0.0172 ms

Required target:

< 50 ms

Result:

PASS

## E5 Observability

Langfuse authenticated client:

PASS

Langfuse observer smoke:

PASS

MRM remains the source of truth.

## E6 Regression

71 automated tests passed.

## E7 Corpus Qualification

Current runtime evidence uses the provisional public Isidora corpus.

It is not represented as the final authoritative project acceptance corpus.

Final T1-T4 acceptance must be rerun against the approved corpus and project-provided expected categories.

## Evidence Rule

No final ICD weights, A/C/K values, MCG thresholds or expected categories are invented by this release package.
