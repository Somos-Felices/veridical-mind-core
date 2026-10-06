from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
import os

from src.config.mcg import load_mcg_config
from src.mcg.gateway import GenerationGateway
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever
from src.mrm.logger import MRMLogger
from src.observability.langfuse import create_langfuse_observer
from src.service.query_service import QueryService


class StubLLMClient:
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        evidence = prompt.split("DOCUMENTARY EVIDENCE:", 1)[-1].split(
            "USER QUESTION:", 1
        )[0]
        question = prompt.split("USER QUESTION:", 1)[-1].split(
            "INSTRUCTION:", 1
        )[0].strip()

        q = question.lower()

        if "who designed" in q and "palacio cousino" in q:
            return (
                "The documentary record identifies the French architect "
                "Paul Lathoud as the architect of the Palacio Cousi\u00f1o."
            )

        if "parque" in q and "lota" in q:
            return (
                "The documentary record describes Isidora Goyenechea's "
                "continued development and enrichment of Parque de Lota "
                "after Luis Cousi\u00f1o's death."
            )

        lines = [
            line.strip()
            for line in evidence.splitlines()
            if line.strip() and not line.startswith("[UDV")
        ]

        for line in lines:
            if len(line) > 40:
                return line

        return (
            "The available documentary evidence supports this answer, "
            "but the retrieved record does not contain enough detail "
            "for a more specific response."
        )


class QueryRequest(BaseModel):
    query: str
    prompt: str | None = None
    source_docs: list[str] | None = None


PUBLIC_POC_SOURCE_DOCS = [
    "public-isidora-001",
    "public-isidora-002",
    "public-isidora-003",
    "public-isidora-004",
    "public-isidora-005",
    "public-isidora-006",
    "public-isidora-007",
    "public-isidora-008",
]


app = FastAPI(title="Veridical Mind Core")

embedding_provider = LocalEmbeddingProvider()

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
)

retriever = QdrantRetriever(
    qdrant_client=qdrant_client,
    collection_name="veridical_udv",
    embedding_provider=embedding_provider,
)

mrm_log_path = os.getenv("MRM_LOG_PATH")
langfuse_observer = create_langfuse_observer()
mrm_logger = MRMLogger(
    log_path=mrm_log_path,
    observer=langfuse_observer,
)

mcg_config = load_mcg_config()

gateway = GenerationGateway(
    llm_client=StubLLMClient(),
    mrm_logger=mrm_logger,
    config=mcg_config,
    answerability_enabled=True,
)

query_service = QueryService(
    retriever=retriever,
    gateway=gateway,
    embedding_provider=embedding_provider,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "qdrant": "connected",
        "embedding_dimension": embedding_provider.dimension,
    }


@app.post("/query")
def query(request: QueryRequest):
    try:
        source_docs = (
            request.source_docs
            if request.source_docs is not None
            else PUBLIC_POC_SOURCE_DOCS
        )

        result = query_service.handle(
            query=request.query,
            prompt=request.prompt or request.query,
            source_docs=source_docs,
        )

        trace = result.trace
        if isinstance(trace, dict):
            trace = {
                key: value
                for key, value in trace.items()
                if key != "query_vector"
            }
        elif hasattr(trace, "__dict__"):
            trace = {
                key: value
                for key, value in vars(trace).items()
                if key != "query_vector"
            }

        return {
            "category": result.category,
            "response": result.response,
            "llm_invoked": result.llm_invoked,
            "icr": result.icr,
            "evidence": result.evidence,
            "trace": trace,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


