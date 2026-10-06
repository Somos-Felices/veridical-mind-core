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

        # Ground generation in the documentary evidence actually
        # retrieved by MREC. The gateway remains authoritative for
        # answerability and LLM suppression.
        evidence_items = retrieval.results[: min(self.gateway.top_k, 5)]

        evidence_blocks = []
        for item in evidence_items:
            evidence_blocks.append(
                f"[UDV {item.id}] "
                f"[SOURCE {item.source_doc}]\n"
                f"{item.content}"
            )

        grounded_prompt = (
            "Answer the user's question ONLY from the supplied "
            "documentary evidence. Do not use pretrained knowledge. "
            "Do not invent facts. If the evidence does not support "
            "a claim, do not present it as fact.\n\n"
            "DOCUMENTARY EVIDENCE:\n"
            + "\n\n".join(evidence_blocks)
            + "\n\nUSER QUESTION:\n"
            + query
            + "\n\nINSTRUCTION:\n"
            + prompt
        )

        return self.gateway.handle(
            query=query,
            query_vector=query_vector,
            ranked_udvs=retrieval.results,
            prompt=grounded_prompt,
        )
