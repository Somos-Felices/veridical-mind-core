# Security and Confidentiality

## Repository rules

Never commit:

- `.env`
- API keys
- access tokens
- passwords
- private credentials
- raw confidential source documents
- private corpus data
- local Qdrant storage
- virtual environments
- model caches

The repository `.gitignore` excludes the relevant local artifacts.

## Secrets

Local secrets belong in `.env` or the approved secret-management system.

`.env.example` contains configuration placeholders only.

Production secrets must be supplied through the approved deployment secret manager.

## Confidential project boundary

Patent-sensitive implementation details, protected source material, internal formulas, thresholds, private datasets and credentials must remain within the authorized private development environment.

Public-facing material must not expose confidential implementation details.

## Current verification

The repository security audit confirmed:

- working tree clean
- `.env` exists locally but is not tracked
- `.env.example` is the only tracked environment file
- no tracked files above the local large-file audit threshold
- raw/processed data directories are ignored
- local Qdrant storage is ignored
- virtual environment is ignored
