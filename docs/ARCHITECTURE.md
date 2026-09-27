# Architecture

## Pipeline

Document -> MICD / UDV ingestion -> Qdrant -> retrieval -> IR -> MCG -> LLM or RPA -> MRM

## MICD

MICD handles document ingestion and creation of Verifiable Document Units (UDVs). Each UDV retains source document, source version, source type, ICD, ingestion timestamp, content, vector and metadata.

## ICD

ICD is assigned during source-document ingestion from Authenticity (A), Completeness (C), and Consensus (K). It propagates as immutable metadata to UDVs from that document version. A/C/K changes create a new document version.

## MREC and IR

IR = ICD * cosine_similarity(query, UDV)

TOP_K = 10.

## MCG

A: sufficient documentary support; LLM generation allowed.

B: partial or non-conclusive support; LLM generation allowed with qualification.

C: insufficient support; LLM invocation is suppressed and RPA responds.

Category B uses the arithmetic mean of the selected top-K IR values. ICR = sum(IR_k^2) / sum(IR_k).

## MRM

MRM records category, source IDs, IR metrics, ICR where applicable, latency and whether the LLM was invoked.

## Security Boundary

The technical core is private and must not expose patent-sensitive architecture, source code, confidential corpus material or credentials through the public Somos Felices website.
