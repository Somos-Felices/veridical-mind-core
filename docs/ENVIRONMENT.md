# Environment

## Runtime

- Python 3.11
- FastAPI
- Pydantic
- Qdrant Client
- SentenceTransformers
- Pytest

## Local Services

Qdrant runs locally through Docker as veridical-qdrant.

Endpoint: http://localhost:6333

## Embeddings

Development model: all-MiniLM-L6-v2
Vector dimension: 384

## Repository

Private repository: veridical-mind-core

## Configuration

Environment-specific secrets belong in .env and must never be committed.

The repository must remain free of confidential source documents, raw corpus files, API credentials and deployment credentials.

## External Services

OpenAI embeddings and Langfuse are planned integration points. Production configuration depends on valid credentials and final project alignment.

Qdrant Cloud may be used later for production infrastructure.
