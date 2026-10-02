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

## MCG Latency Benchmark

Run the local classification benchmark:

    python scripts/benchmark_mcg_latency.py

The benchmark runs 1000 MCG classification iterations and reports minimum, mean, p95 and maximum latency. It measures only the classification decision boundary.

## FastAPI

    uvicorn src.main:app --reload

## Health

http://127.0.0.1:8000/health

## Secrets

Keep credentials in .env or the approved secret manager. Never commit .env, API keys, credentials, confidential corpus data or protected source material.

