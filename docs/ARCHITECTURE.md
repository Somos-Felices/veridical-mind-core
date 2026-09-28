# Architecture

## Pipeline

Document
→ MICD ingestion
→ UDV creation
→ ICD metadata
→ vector storage
→ MREC retrieval
→ IR ranking
→ MCG classification
→ generation or RPA
→ MRM trace

## MICD

MICD creates immutable document versions and semantic UDV units.

Each UDV inherits the ICD associated with its source document version.

A source-document change creates a new version; historical ICD values are not mutated.

## MREC

MREC retrieves candidate UDVs using semantic similarity.

Information Relevance is:

`IR = ICD × cosine_similarity`

The current implementation preserves cosine similarity directly.

## MCG

MCG operates before LLM generation.

- Category A: sufficient documentary support; generation permitted.
- Category B: partial/non-conclusive support; generation permitted with epistemic qualification.
- Category C: insufficient support; LLM invocation is suppressed and RPA responds.

Category C is therefore a control-flow decision, not merely a response-generation instruction.

## MRM

MRM records the classification decision and associated metrics.

The runtime trace includes:

- timestamp
- query vector
- category
- source IDs
- IR maximum
- IR average
- ICR where applicable
- classification latency
- LLM invocation status

Raw query text is not required in the MRM trace.

## Development limitations

Current local development components include a local embedding model and development LLM stub. These are implementation/testing choices and are not final production-provider decisions.
