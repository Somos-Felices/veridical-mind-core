class LocalEmbeddingProvider:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    @property
    def dimension(self) -> int:
        return 384

    def embed(self, text: str) -> list[float]:
        if self.model is None:
            from fastembed import TextEmbedding
            self.model = TextEmbedding(model_name=self.model_name)
        return next(self.model.embed([text])).tolist()


