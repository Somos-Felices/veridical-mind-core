# Deployment Readiness

## Current local state

The Sprint 1 core runs locally with:

- Python 3.11
- FastAPI
- local Qdrant
- local `all-MiniLM-L6-v2` embeddings
- MICD ingestion and UDV creation
- ICD metadata propagation
- MREC retrieval and IR calculation
- MCG A/B/C classification
- Category C physical LLM suppression
- RPA fallback
- MRM trace logging

## Runtime dependencies

The application expects:

- Qdrant at `http://localhost:6333`
- collection `veridical_udv`
- local embedding model `all-MiniLM-L6-v2`

Configuration is loaded from environment variables where applicable.

## External provider

OpenAI integration exists in the dependency/configuration layer, but the current local development path uses local embeddings and a development LLM stub.

Production provider credentials must never be committed to the repository.

## Deployment prerequisites

Before production deployment:

1. Confirm final ICD weights from the technical owner.
2. Confirm final MCG thresholds.
3. Load the official 12-document Isidora Goyenechea corpus.
4. Validate A/B/C acceptance cases against that corpus.
5. Configure the approved production embedding provider.
6. Configure the approved production LLM provider.
7. Configure production secrets through the deployment secret manager.
8. Run the full acceptance suite.
9. Verify Category C produces no LLM request.
10. Perform latency and operational validation.

## Current blockers

The following require external/project-owner inputs and are intentionally not invented locally:

- official corpus and document-level A/C/K assignments
- final ICD weights
- final MCG thresholds
- production credentials
- production observability credentials
- production hosting/infrastructure credentials
