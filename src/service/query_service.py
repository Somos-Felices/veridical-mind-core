from dataclasses import dataclass

from src.mcg.gateway import GenerationGateway, GatewayResponse
from src.mrec.embeddings import LocalEmbeddingProvider
from src.mrec.retriever import QdrantRetriever


@dataclass
class QueryService:
    retriever: QdrantRetriever
    gateway: GenerationGateway
    embedding_provider: LocalEmbeddingProvider

    def handle(
        self,
        query: str,
        prompt: str,
        source_docs: list[str] | None = None,
    ) -> GatewayResponse:
        query_vector = self.embedding_provider.embed(query)

        retrieval = self.retriever.retrieve(
            query,
            top_k=self.gateway.top_k,
            source_docs=source_docs,
        )

        return self.gateway.handle(
            query=query,
            query_vector=query_vector,
            ranked_udvs=retrieval.results,
            prompt=prompt,
        )
