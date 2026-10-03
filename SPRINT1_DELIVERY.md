# Veridical Mind
# Sprint 1 Engineering Delivery

## 1. Delivery status

Sprint 1 independent engineering implementation is complete as a reproducible public-source engineering release.

Repository state:
1. Current delivery commit is tracked by Git history.
2. Full automated suite: 71 passed.
3. Local Qdrant retrieval path operational.
4. Local MiniLM embedding path operational.
5. MICD, UDV, IR, MCG, Gateway, RPA and MRM integrated.
6. Source-filtered retrieval is operational.
7. Category C physical LLM suppression validated.
8. Category B qualified generation and ICR validated.
9. Category A generation path validated through controlled acceptance fixtures.
10. MCG boundary latency benchmark is below the required 50 ms target.
11. Public corpus validation is reproducible through `scripts/validate_public_corpus.py`.

## 2. Delivered engineering chain

Public or approved source documents
→ MICD
→ immutable DocumentVersion
→ semantic/propositional UDV chunks
→ ICD propagation
→ local embeddings
→ Qdrant
→ source filtering
→ cosine similarity
→ IR
→ Top-K
→ deterministic MCG
→ Category A/B/C
→ Generation Gateway or RPA
→ MRM trace

## 3. Public-source engineering corpus

The current engineering corpus uses publicly available Chilean historical and archival material.

It is explicitly marked as a public-source engineering fixture.

It is not represented as the final project-authorized historical corpus.

Current public fixture:
1. 8 public source documents
2. 24 indexed UDVs
3. Source provenance retained
4. Source URLs recorded
5. Synthetic ICD values used only for engineering validation
6. Non-public engineering fixtures excluded from public validation through source filtering
7. No confidential project corpus is required for this release

## 4. MCG validation

Development validation configuration:
1. thetaA = 0.80
2. thetaB = 0.30
3. TOP_K = 10
4. Temperature = 0.0

These values are engineering validation parameters and are not claimed to be final project parameters.

Controlled Category A:
1. Covered by gateway acceptance tests.
2. LLM invoked = true.
3. Temperature = 0.0.

Controlled Category B:
1. Covered by gateway acceptance tests.
2. LLM invoked = true.
3. ICR calculated.
4. Temperature = 0.0.
5. Epistemic qualification applied.

Controlled Category C:
1. Covered by gateway acceptance tests.
2. LLM invoked = false.
3. LLM call count remains zero.
4. RPA returned.
5. MRM records `llm_invoked=false`.

Public corpus validation:
1. 6 queries executed against the 8-source public corpus.
2. All 6 reached Category B under the development configuration.
3. ICR was recorded for all 6.
4. All 6 invoked the controlled LLM path.
5. Source filtering excluded unrelated engineering fixtures.

## 5. Latest public validation

Query 1:
`What was Isidora Goyenechea role in Lota?`
Category = B
IR max = 0.485953
IR average = 0.360211
ICR = 0.3674240298056943

Query 2:
`What did Isidora Goyenechea do with Parque de Lota?`
Category = B
IR max = 0.529558
IR average = 0.454160
ICR = 0.4591158974211881

Query 3:
`Who designed Palacio Cousino?`
Category = B
IR max = 0.625740
IR average = 0.426529
ICR = 0.45428535262705255

Query 4:
`When was Palacio Cousino constructed?`
Category = B
IR max = 0.643792
IR average = 0.439751
ICR = 0.46679093037143177

Query 5:
`What features did Parque de Lota have?`
Category = B
IR max = 0.524319
IR average = 0.443307
ICR = 0.44855299886958283

Query 6:
`When was Parque de Lota declared a Historic Monument?`
Category = B
IR max = 0.616794
IR average = 0.484182
ICR = 0.4976343488071014

## 6. Latency

Dedicated MCG benchmark:
1. Iterations = 1000
2. Minimum = 0.003000 ms
3. Mean = 0.003517 ms
4. P95 = 0.005500 ms
5. Maximum = 0.049400 ms
6. Target = less than 50 ms
7. Result = PASS

The benchmark measures the MCG control boundary rather than end-to-end HTTP, embedding, Qdrant or LLM latency.

## 7. MRM

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

Category C records `llm_invoked=false`.

## 8. Security and reproducibility

1. Secrets remain outside tracked source.
2. Confidential project corpus is not included.
3. Patent-sensitive project data is not included.
4. Public historical sources are separated from project-authoritative inputs.
5. Local Qdrant is used for engineering validation.
6. Local MiniLM is used for engineering validation.
7. The complete automated test suite passes.
8. Public validation is reproducible through `scripts/validate_public_corpus.py`.

## 9. Final replacement path

When the project-authoritative corpus becomes available:

1. Replace the public-source fixture with the approved corpus.
2. Apply authoritative source metadata.
3. Apply authoritative A/C/K values and ICD weights.
4. Apply authoritative MCG thresholds.
5. Run approved T1 through T4 queries.
6. Regenerate acceptance evidence.
7. Update the final release record.

The Sprint 1 engineering implementation is therefore complete independently of that later corpus substitution.

## 10. Definition of delivered engineering work

Document source
→ ingestion
→ ICD
→ UDV
→ embeddings
→ Qdrant
→ source filtering
→ retrieval
→ IR
→ Top-K
→ MCG
→ Gateway
→ RPA
→ MRM
→ acceptance tests

Full suite result: 71 passed.
