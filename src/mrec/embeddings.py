from sentence_transformers import SentenceTransformer

class LocalEmbeddingProvider:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    @property
    def dimension(self) -> int:
        return 384

    def embed(self, text: str) -> list[float]:
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        return self.model.encode(text, normalize_embeddings=False).tolist()
