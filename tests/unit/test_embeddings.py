from src.mrec.embeddings import LocalEmbeddingProvider


def test_embedding_dimension():
    provider = LocalEmbeddingProvider()

    assert provider.dimension == 384


def test_embedding_returns_expected_vector():
    provider = LocalEmbeddingProvider()

    vector = provider.embed("Isidora Goyenechea was a Chilean historical figure.")

    assert len(vector) == provider.dimension
    assert any(value != 0 for value in vector)


def test_embedding_is_deterministic():
    provider = LocalEmbeddingProvider()

    text = "Isidora Goyenechea was a Chilean historical figure."

    first = provider.embed(text)
    second = provider.embed(text)

    assert first == second
