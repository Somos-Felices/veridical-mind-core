from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

print("Qdrant:", client.get_collections())
