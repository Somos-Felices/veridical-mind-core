from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from qdrant_client import QdrantClient

from src.config.mcg import load_mcg_config
from src.mcg.gateway import GenerationGateway
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever
from src.mrm.logger import MRMLogger
from src.service.query_service import QueryService


class StubLLMClient:
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        return f"[DEV LLM RESPONSE] {prompt}"


class QueryRequest(BaseModel):
    query: str
    prompt: str | None = None


app = FastAPI(title="Veridical Mind Core")

embedding_provider = LocalEmbeddingProvider()

qdrant_client = QdrantClient(
    url="http://localhost:6333",
)

retriever = QdrantRetriever(
    qdrant_client=qdrant_client,
    collection_name="veridical_udv",
    embedding_provider=embedding_provider,
)

mrm_logger = MRMLogger()
mcg_config = load_mcg_config()

gateway = GenerationGateway(
    llm_client=StubLLMClient(),
    mrm_logger=mrm_logger,
    theta_a=mcg_config.theta_a,
    theta_b=mcg_config.theta_b,
    top_k=mcg_config.top_k,
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
        result = query_service.handle(
            query=request.query,
            prompt=request.prompt or request.query,
        )

        return {
            "category": result.category,
            "response": result.response,
            "llm_invoked": result.llm_invoked,
            "icr": result.icr,
            "trace": result.trace,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
