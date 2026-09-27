import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
collection = os.getenv("QDRANT_COLLECTION", "veridical_udv")

if not client.collection_exists(collection):
    client.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

print(f"Collection ready: {collection}")
print(client.get_collection(collection))
