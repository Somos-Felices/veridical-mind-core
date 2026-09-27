# Veridical Mind Core

Private technical implementation for the Veridical Mind project.

## Purpose

Technical core for controlling generation over a documentary corpus.

## Pipeline

Document -> MICD / UDV ingestion -> Qdrant -> retrieval -> IR -> MCG -> LLM or RPA -> MRM

## Current Components

- MICD / UDV ingestion
- ICD provenance and versioning
- Qdrant retrieval
- IR calculation
- MCG A/B/C classification
- Category-C LLM suppression
- RPA
- MRM logging
- FastAPI foundation

## Development

Python 3.11
FastAPI
Qdrant
SentenceTransformers
pytest

See docs/SETUP.md for local setup and test commands.

## Validation

The current local validation includes the unit/integration test suite and a MICD -> Qdrant -> retrieval -> IR smoke test covering provenance and document-version immutability.

## Security

Never commit API keys, credentials, confidential corpus material, source documents, or patent-sensitive implementation details.

The public Somos Felices website is separate from this private technical core.

Final ICD weights and MCG thresholds remain configurable until formally aligned.
