# Technical Decisions

## Confirmed

- Local Qdrant is used for development.
- TOP_K is 10.
- IR = ICD multiplied by cosine similarity.
- Cosine similarity is not normalized.
- Category B uses arithmetic mean over the selected top-K IR values.
- ICR uses sum(IR squared) divided by sum(IR).
- Category C physically suppresses the LLM request.
- Category C records llm_invoked=false.
- ICD is immutable for a document version.
- A/C/K changes create a new document version.
- MRM records the generation-control decision.

## Development Configuration

Local development uses SentenceTransformers all-MiniLM-L6-v2 because the OpenAI embedding API is not currently available in the development account.

Development MCG thresholds are configurable and are not final project thresholds.

ICD weights are not final project weights until technical alignment is completed.

## Sprint 1 Validation

The local A/B/C gateway paths have been exercised with controlled evidence. Category C physically suppresses the LLM and records llm_invoked=false. A and B invoke the LLM at temperature 0.0, with B applying epistemic qualification. A provisional corpus has also been exercised through retrieval, IR and MCG without treating it as authoritative.

## Pending Alignment

- Final ICD weights p_A, p_C and p_K.
- Final MCG thresholds theta_A and theta_B.
- Production embedding configuration.
- Final Isidora Goyenechea corpus and source evaluation.
- Sprint 2 formulas including TRV, TRI and TAD.
