# Setup Guide

## Requirements

1. Python 3.11
2. Docker Desktop
3. Git

## Existing Environment

Use the existing .venv. Do not recreate the environment unless explicitly required.

## Qdrant

The project uses the existing local veridical-qdrant container on port 6333.

## Tests

    python -m pytest -q

## FastAPI

    uvicorn src.main:app --reload

## Health

http://127.0.0.1:8000/health

## Secrets

Keep credentials in .env or the approved secret manager. Never commit .env, API keys, credentials, confidential corpus data or protected source material.
