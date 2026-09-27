from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

print("Qdrant:", client.get_collections())
print("Collection:", os.getenv("QDRANT_COLLECTION"))
print("OpenAI key configured:", bool(os.getenv("OPENAI_API_KEY")))
