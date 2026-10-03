# Veridical Mind
# Sprint 1 Engineering Delivery

## 1. Delivery status

Sprint 1 independent engineering implementation is complete as a reproducible public-source engineering release.

Repository state:
1. Commit: 2eb26f6
2. Full automated suite: 69 passed
3. Local Qdrant retrieval path operational
4. Local MiniLM embedding path operational
5. MICD, UDV, IR, MCG, Gateway, RPA and MRM integrated
6. Category C physical LLM suppression validated
7. Category B qualified generation and ICR validated
8. Category A generation path validated through controlled acceptance fixtures
9. MCG boundary latency benchmark is below the required 50 ms target
10. Working tree clean before this delivery documentation

## 2. Delivered engineering chain

Approved or public source documents
→ MICD
→ immutable DocumentVersion
→ semantic/propositional UDV chunks
→ ICD propagation
→ local embeddings
→ Qdrant
→ cosine similarity
→ IR
→ Top-K
→ deterministic MCG
→ Category A/B/C
→ Generation Gateway or RPA
→ MRM trace

## 3. Public-source engineering corpus

The current engineering corpus uses publicly available Chilean historical and archival material.

The corpus is explicitly marked as a public-source engineering fixture.

It is not represented as the final project-authorized historical corpus.

Current public fixture:
1. Four public source documents
2. Eight indexed UDVs
3. Source provenance retained
4. Source URLs recorded
5. Synthetic ICD values used only for engineering validation
6. No confidential project corpus is required for this release

## 4. MCG validation

Development validation configuration:
1. thetaA = 0.80
2. thetaB = 0.30
3. TOP_K = 10
4. Temperature = 0.0

These values are engineering validation parameters and are not claimed to be the final project parameters.

Controlled Category A:
1. IR inputs = [0.90, 0.20]
2. Category = A
3. LLM invoked = true
4. Temperature = 0.0

Controlled Category B:
1. IR inputs = [0.60, 0.50, 0.40, 0.30]
2. Category = B
3. LLM invoked = true
4. ICR = 0.47777777777777775
5. Temperature = 0.0
6. Epistemic qualification applied

Public-source Category C:
1. Query = What was Isidora Goyenechea's role in Lota?
2. Category = C
3. IR max = 0.486332345
4. IR average = 0.299343553
5. LLM invoked = false
6. LLM calls added = 0
7. RPA returned
8. MRM recorded llm_invoked=false
9. MCG boundary latency = 0.0343 ms

Public-source Category B:
1. Query = What did Isidora Goyenechea do with Parque de Lota?
2. Category = B
3. IR max = 0.52955804
4. IR average = 0.35164249475
5. ICR = 0.3861366170637631
6. LLM invoked = true
7. Temperature = 0.0
8. MRM recorded the decision

## 5. Latency

Dedicated MCG benchmark:
1. Iterations = 1000
2. Minimum = 0.0031 ms
3. Mean = 0.003417 ms
4. P95 = 0.0051 ms
5. Maximum = 0.0250 ms
6. Target = less than 50 ms
7. Result = PASS

The benchmark measures the MCG control boundary rather than end-to-end HTTP, embedding, Qdrant or LLM latency.

## 6. MRM

MRM records:
1. Query vector
2. Category
3. Source IDs
4. IR max
5. IR average
6. ICR where applicable
7. Latency
8. Timestamp
9. llm_invoked

Raw user query text is not stored in the MRM trace.

Category C records llm_invoked=false.

## 7. Security and reproducibility

1. Secrets remain outside tracked source.
2. Confidential project corpus is not included.
3. Patent-sensitive project data is not included.
4. Public historical sources are separated from project-authoritative inputs.
5. Local Qdrant is used for engineering validation.
6. Local MiniLM is used for engineering validation.
7. The complete automated test suite passes.

## 8. Acceptance mapping

T1:
Controlled high-support case reaches Category A and invokes the LLM at temperature 0.0.

T2:
Controlled partial-support case reaches Category B, invokes the LLM at temperature 0.0 and records ICR.

T3:
Public-source insufficient-support case reaches Category C, returns RPA and physically suppresses the LLM request.

T4:
A complete MRM trace is produced for every control decision.

## 9. Final replacement path

When the project-authoritative corpus becomes available, the existing engineering pipeline does not need architectural replacement.

The replacement operation is:

1. Replace the public-source fixture with the approved corpus.
2. Apply the authoritative source metadata.
3. Apply the authoritative A/C/K values and ICD weights.
4. Apply the authoritative MCG thresholds.
5. Run the approved T1 through T4 queries.
6. Regenerate acceptance evidence.
7. Update the final release record.

The Sprint 1 engineering implementation is therefore complete independently of that later corpus substitution.

## 10. Definition of delivered engineering work

The current repository contains the complete independently executable vertical slice:

Document source
→ ingestion
→ ICD
→ UDV
→ embeddings
→ Qdrant
→ retrieval
→ IR
→ Top-K
→ MCG
→ Gateway
→ RPA
→ MRM
→ acceptance tests

Full suite result: 69 passed.
