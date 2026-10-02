# Veridical Mind Core

Private technical implementation for the Veridical Mind project.

## Purpose

Technical core for controlling generation over a documentary corpus.

## Pipeline

Document -> MICD / UDV ingestion -> Qdrant -> retrieval -> IR -> MCG -> LLM or RPA -> MRM

## Current Components

- MICD / UDV ingestion
- Corpus source governance and validation
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

The current local validation includes 69 automated tests, corpus-governance validation, embedding validation, a repeatable MCG latency benchmark, and live MICD -> Qdrant -> retrieval -> IR -> MCG runtime validation. A provisional corpus has also been exercised through the complete retrieval -> IR -> MCG -> MRM path, including physical Category C LLM suppression. The provisional corpus is not authoritative project evidence.

## Security

Never commit API keys, credentials, confidential corpus material, source documents, or patent-sensitive implementation details.

The public Somos Felices website is separate from this private technical core.

Final ICD weights and MCG thresholds remain configurable until formally aligned.
