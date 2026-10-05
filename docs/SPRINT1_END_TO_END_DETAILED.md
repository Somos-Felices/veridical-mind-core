# Veridical Mind

# Sprint 1 End to End Engineering Record

## 1. Purpose

This document is the permanent engineering record for Sprint 1 of the Veridical Mind technical core.

Its purpose is to explain the complete implemented control flow, the responsibility of each subsystem, the integration boundaries, the validation evidence, the observability path, the security boundaries, and the procedure required for another engineer to understand and reproduce the Sprint 1 system.

This document is maintained inside the private technical repository.

It is not intended for the public Somos Felices website or any public product documentation.

## 2. Sprint 1 Objective

Sprint 1 establishes a complete evidence governed vertical slice.

The intended flow is:

Approved documentary evidence

1. Source governance
2. MICD ingestion
3. Immutable document versioning
4. Semantic and propositional units
5. UDV creation
6. ICD propagation
7. Local embedding
8. Qdrant storage and retrieval
9. Semantic similarity
10. IR calculation
11. Top K ranking
12. MCG A, B, C classification
13. Generation Gateway enforcement
14. Controlled generation or RPA
15. MRM recording
16. Langfuse surrounding observability
17. Acceptance and reproducibility evidence

The central control principle is that documentary reliability is determined before generation.

The language model does not determine whether its own evidence is reliable enough to answer.

## 3. Scope

Sprint 1 includes:

1. Source and provenance handling
2. Immutable document versioning
3. UDV generation
4. ICD propagation
5. Local embedding
6. Qdrant vector retrieval
7. Cosine similarity
8. IR ranking
9. Top K selection
10. MCG A, B, C classification
11. Generation Gateway enforcement
12. Category C RPA fallback
13. MRM trace generation
14. Langfuse observability
15. Exact MCG boundary latency measurement
16. FastAPI integration
17. Automated testing
18. Security and NDA hygiene
19. Sprint 1 documentation

Sprint 1 does not include:

1. Public implementation exposure
2. Avatar generation
3. Voice systems
4. Production UI
5. Advanced MRM analytics
6. Expanded production infrastructure
7. Sprint 2 product functionality

## 4. Complete End to End Architecture

The implemented conceptual path is:

```text
Approved documents
        |
        v
Source governance
        |
        v
MICD
        |
        v
Immutable DocumentVersion
        |
        v
Semantic / propositional units
        |
        v
UDV + ICD
        |
        v
Local embedding
        |
        v
Qdrant
        |
        v
Query embedding
        |
        v
Semantic retrieval
        |
        v
Cosine similarity
        |
        v
IR ranking
        |
        v
Top K
        |
        v
MCG
   +----+----+
   |    |    |
   A    B    C
   |    |    |
   v    v    v
 LLM  LLM   RPA
   |    |    |
   +----+----+
        |
        v
MRM trace
        |
        v
Langfuse observability
The important architectural property is that MCG occurs before generation.

## 5. Source Governance

Source governance establishes the documentary input boundary.

Each approved source requires provenance and metadata sufficient to understand where the evidence originated and how its reliability was established.

The system preserves source identity through ingestion, versioning, UDV creation, retrieval and final MRM traces.

Copies or derivatives of the same underlying account must not automatically be treated as independent corroboration.

The approved corpus is the authoritative documentary input.

Confidential source material must remain inside the private technical environment.

## 6. MICD and Document Versioning

MICD is responsible for converting approved documentary material into controlled internal representations.

Every source receives an immutable document version.

A change to source reliability information must not silently mutate an existing historical version.

Instead, the expected model is:

Source
  |
  +--> DocumentVersion 1
  |        |
  |        +--> UDV set
  |
  +--> DocumentVersion 2
           |
           +--> UDV set

This preserves historical lineage.

The purpose is reproducibility and protection against silent changes to historical reliability.

## 7. UDV Representation

A UDV represents a documentary unit that can participate in retrieval.

The relevant information includes:

UDV identifier
Content
Embedding
ICD
Source document
Source type
Ingestion information
Provenance metadata

Source identifiers remain attached to retrieved results.

This allows the downstream control system to determine not only semantic relevance but also documentary reliability.

## 8. Embedding Layer

Sprint 1 uses a local Hugging Face embedding model.

The active local provider is based on:

all-MiniLM-L6-v2

The observed embedding dimension is:

384

The embedding provider is isolated behind an abstraction so that retrieval and control logic do not depend directly on a specific embedding implementation.

A direct runtime validation produced:

EMBED: 384

The runtime did not require paid inference for this embedding path.

## 9. Qdrant Vector Layer

Sprint 1 uses local Qdrant.

The active collection is:

veridical_udv

The collection uses:

Vector dimension: 384
Distance: Cosine

The observed collection contained:

35 points

The Qdrant health state was confirmed as operational after starting the existing project container.

The expected infrastructure path is:

Application
    |
    v
Qdrant
    |
    v
veridical_udv

Qdrant is infrastructure for retrieval.

It does not make the final generation decision.

## 10. MREC Retrieval

MREC performs documentary retrieval.

The query is embedded locally.

Qdrant returns semantic candidates.

The candidates preserve their source and reliability metadata.

The retrieved candidates are then evaluated using the project's relevance calculation.

The observed direct retrieval test returned:

RESULTS: 10

This confirms that the retrieval path was operational from query embedding through Qdrant ranking.

## 11. Information Relevance

The control layer combines documentary reliability with semantic similarity.

The implemented relevance concept is:

IR = ICD × cosine similarity

This allows a semantically similar document with weaker documentary reliability to be treated differently from a semantically similar document with stronger documentary reliability.

The resulting candidates are ranked by IR.

The ranking remains provenance preserving.

## 12. Top K

The configured retrieval control uses:

TOP_K = 10

The MCG receives the selected ranked evidence rather than an uncontrolled collection of arbitrary retrieved material.

The source identifiers are preserved through this selection.

## 13. MCG A, B, C

MCG is the control boundary that determines whether generation is permitted.

The three categories are:

Category A
High documentary support
Generation permitted

Category B
Intermediate documentary support
Generation permitted with qualified or inferred handling

Category C
Insufficient documentary support
Generation suppressed
RPA returned

The classifier is deterministic and configurable.

The final authoritative project parameters remain configuration controlled and must not be inferred from development fixtures.

## 14. Category A

Category A represents sufficient documentary support for generation.

The gateway permits generation.

The intended generation configuration uses deterministic temperature handling.

The generation result must remain grounded in the retrieved evidence.

## 15. Category B

Category B represents intermediate support.

Generation is permitted, but the response must distinguish documentary evidence from inference.

The system preserves the ICR value associated with the selected evidence.

The ICR is recorded in the MRM trace.

## 16. Category C

Category C is the strongest enforcement boundary in Sprint 1.

When evidence is insufficient:

The gateway does not construct or transmit an LLM request
The LLM client is not invoked
RPA is returned
MRM records llm_invoked=false

This is not merely a response template.

The architectural requirement is physical suppression of the generation request.

## 17. Generation Gateway

The Generation Gateway converts the MCG classification into an actual execution decision.

Its responsibility is enforcement.

Conceptually:

MCG
 |
 +--> A --> generation permitted
 |
 +--> B --> qualified generation permitted
 |
 +--> C --> generation blocked --> RPA

This prevents downstream code from accidentally bypassing the MCG decision.

The gateway receives the LLM client through dependency injection.

The current development runtime uses a local stub client for controlled testing.

The architecture therefore does not require a paid LLM service for Sprint 1 control path validation.

## 18. RPA

RPA is the fallback response for insufficient documentary support.

The live end to end validation produced:

I don't have sufficient documentary evidence to answer that.

The corresponding control state was:

category: C
llm_invoked: false
icr: null

This demonstrates the expected Category C enforcement behavior.

## 19. MRM

MRM provides the project's structured reliability monitoring record.

The trace contains:

Timestamp
Query vector
Category
Source IDs
IR maximum
IR average
ICR where applicable
Latency
LLM invocation state

Raw query text is not required in the MRM trace.

The MRM system remains the project level source of truth for required control metrics.

## 20. MRM Persistence

MRM supports optional JSONL persistence.

Persistence is controlled by:

MRM_LOG_PATH

When this environment variable is not configured, MRM remains in memory and does not create a local JSONL trace file.

This behavior was explicitly verified during Sprint 1 validation.

The absence of a local JSONL file in that configuration is therefore expected behavior rather than a failed test.

## 21. Langfuse

Langfuse provides surrounding observability.

It does not replace MRM.

The runtime observer was successfully created using the configured environment credentials.

A real MRM trace was passed to the observer.

The observer successfully recorded the trace and flushed the client.

The final runtime smoke test produced:

OBSERVER: CREATED
RECORD: OK
FLUSH: DONE

This confirms that the Langfuse integration is operational in the current environment.

## 22. Exact MCG Latency

The MCG latency metric is intentionally narrower than total API latency.

The measured boundary is:

MCG receives ranked UDV set
        |
        v
classification
        |
        v
RPA or generation decision

Embedding time, Qdrant retrieval time, HTTP overhead and generation time must not be presented as the MCG control latency.

The dedicated benchmark used 1000 iterations.

Observed measurement:

Mean: approximately 0.003457 ms
P95: approximately 0.0045 ms
Target: less than 50 ms

The observed MCG control boundary is therefore substantially below the Sprint 1 target.

## 23. Live End to End Validation

The live integration path was executed through the FastAPI query endpoint.

The verified path was:

Query
  |
  v
Local 384 dimensional embedding
  |
  v
Qdrant retrieval
  |
  v
10 ranked results
  |
  v
IR calculation
  |
  v
MCG
  |
  v
Category C
  |
  v
LLM suppressed
  |
  v
RPA
  |
  v
MRM trace

The observed live decision was:

category: C
llm_invoked: false
icr: null

The observed IR maximum was approximately:

0.294577893

The observed IR average was approximately:

0.2222910367

The observed trace latency was approximately:

0.0277 ms

This trace latency is the observed request control trace value for that execution.

It must not be confused with the dedicated MCG benchmark boundary described earlier.

## 24. Live Retrieval Evidence

The successful retrieval returned 10 ranked records.

The top observed IR value was approximately:

0.294577893

The remaining observed ranked IR values included approximately:

0.28512477
0.284791424
0.25344424
0.213620725
0.21102525
0.195583492
0.192339644
0.182102625
0.110300304

The returned records preserved source identifiers and provenance metadata.

## 25. API Integration

The FastAPI application exposes the query path.

The query service performs:

query
  |
  v
embedding
  |
  v
retrieval
  |
  v
gateway
  |
  v
response + trace

The service therefore provides a single integrated entry point instead of requiring separate manual calls to the individual subsystems.

## 26. Automated Validation

The final known automated test suite contains:

71 tests passed

The repository state was updated so the README reflects the current test count.

The complete suite passed successfully during Sprint 1 closure.

## 27. Infrastructure Recovery During Validation

During final validation, Qdrant was initially not running.

The application correctly failed to connect to the local Qdrant endpoint.

The existing Qdrant container was then started.

After startup:

/collections

successfully returned:

veridical_udv

The embedding test succeeded.

The direct retrieval test succeeded.

The API end to end query then succeeded.

This demonstrates that the application and vector store were correctly integrated and that the interruption was infrastructure state rather than an application implementation failure.

## 28. Reproducibility Procedure

A future engineer should be able to reproduce the core validation using the following sequence.

28.1 Activate the environment
.venv\Scripts\Activate.ps1
28.2 Start Qdrant

Start the existing project Qdrant container.

Verify:

http://localhost:6333/collections

The collection:

veridical_udv

should be present.

28.3 Validate embedding

Run the local embedding provider test.

Expected dimensionality:

384
28.4 Validate retrieval

Run the retrieval smoke test.

Expected behavior:

10 ranked results

with source identifiers and IR values.

28.5 Start FastAPI

Start the application using the repository's documented development command.

28.6 Validate API

Submit a validation query through:

/query

Verify:

category
response
llm_invoked
icr
trace
28.7 Validate MRM

Confirm that the response contains the required MRM fields.

28.8 Validate Langfuse

With valid local environment configuration, create the observer, record an MRM trace and flush the client.

Expected result:

OBSERVER: CREATED
RECORD: OK
FLUSH: DONE
28.9 Run the full test suite

Run:

pytest -q

Expected Sprint 1 reference state:

71 passed
## 29. Security and NDA Boundary

The technical core repository is private.

The following must remain private:

Patent sensitive implementation details
Internal reliability formulas
Final proprietary parameters
Threshold values where confidential
Private source corpus
Internal evaluation data
Internal source code
Credentials
Environment secrets
Private observability credentials

The public Somos Felices site must not contain the private technical implementation.

Environment secrets must remain outside tracked source files.

The local .env file is intentionally not committed.

## 30. Public and Private Separation

The project contains two different surfaces.

Private technical core

The private repository contains:

Veridical Mind core
MICD
UDV
ICD
MREC
IR
MCG
Gateway
RPA
MRM
Langfuse integration
Tests
Private engineering documentation
Public product surface

The public Somos Felices site contains the public facing mission and product presentation.

The private technical implementation must not be copied into the public site.

## 31. What Sprint 1 Demonstrates

Sprint 1 demonstrates a functioning controlled vertical slice rather than disconnected modules.

The key demonstrated property is:

documentary evidence
        |
        v
reliability aware retrieval
        |
        v
deterministic control
        |
        v
generation enforcement
        |
        v
auditable monitoring

The system therefore has an explicit control boundary between evidence retrieval and generation.

## 32. What Was Directly Verified

The following were directly verified during the final Sprint 1 validation sequence:

Local embedding provider
384 dimensional embedding output
Qdrant availability
veridical_udv collection
Qdrant retrieval
Top K retrieval
IR ranking
FastAPI query path
MCG classification
Category C enforcement
RPA response
llm_invoked=false
MRM trace generation
MRM trace fields
MCG latency benchmark
Langfuse observer creation
Langfuse trace recording
Langfuse flush
Full automated test suite
Repository cleanliness
## 33. Important Interpretation of Acceptance Evidence

The live end to end demonstration recorded in this document specifically exercises the Category C path.

Automated tests cover the broader implementation surface.

This document intentionally does not claim that every possible A, B and C production scenario was manually executed through the live API during this final validation session unless corresponding evidence exists elsewhere in the repository.

Future acceptance runs should continue to preserve this distinction between:

unit test evidence
integration test evidence
live runtime evidence

This keeps the engineering record auditable.

## 34. Sprint 1 Exit State

The final Sprint 1 engineering state includes:

Private repository
        |
        v
Controlled source ingestion
        |
        v
Versioned UDVs
        |
        v
Reliability metadata
        |
        v
Local embeddings
        |
        v
Qdrant retrieval
        |
        v
IR ranking
        |
        v
Top K evidence
        |
        v
MCG A / B / C
        |
        v
Generation Gateway
        |
        +----> Generation
        |
        +----> RPA
        |
        v
MRM
        |
        v
Langfuse
## 35. Future Engineer Handoff

A future engineer should begin by reading this document together with:

README.md
SETUP_STATUS.md
SPRINT1_RESULTS.md
SPRINT1_DELIVERY.md
ARCHITECTURE.md
DECISIONS.md
ENVIRONMENT.md

The implementation should be inspected before modifying validated control paths.

Any change affecting retrieval, IR, MCG, Gateway, MRM or observability should be followed by:

Targeted tests
Full test suite
Relevant integration validation
Documentation update
Git review
## 36. Sprint 2 Boundary

Sprint 2 should begin from the validated Sprint 1 core.

The Sprint 1 control path should not be rebuilt merely to introduce later product functionality.

Future work must preserve the following invariant:

Evidence
  ->
Reliability aware retrieval
  ->
MCG decision
  ->
Gateway enforcement
  ->
Generation or RPA
  ->
MRM

The core control boundary should remain independently testable.

## 37. Final Sprint 1 Statement

Sprint 1 establishes the first complete Veridical Mind engineering vertical slice.

A query can enter the system, be embedded locally, retrieve documentary evidence from Qdrant, have retrieved evidence ranked using reliability aware relevance, pass through deterministic MCG control, reach controlled generation when permitted or RPA when insufficiently supported, and produce an auditable MRM record.

The final validation also confirmed that Langfuse can receive the MRM observation without replacing the project's own reliability monitoring record.

The most important demonstrated safety property is Category C enforcement:

Insufficient evidence
        |
        v
Category C
        |
        v
No LLM invocation
        |
        v
RPA
        |
        v
llm_invoked=false
        |
        v
MRM trace

This document is the Sprint 1 engineering reference and should be updated whenever the validated control path materially changes.
