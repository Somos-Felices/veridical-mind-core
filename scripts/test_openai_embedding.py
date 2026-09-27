from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if not key:
    raise RuntimeError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=key)

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Veridical Mind embedding smoke test"
)

vector = response.data[0].embedding

print("OpenAI:", "OK")
print("Model:", response.model)
print("Vector dimension:", len(vector))
print("First values:", vector[:3])
