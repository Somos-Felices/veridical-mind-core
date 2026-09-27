from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Veridical Mind local embedding smoke test"
vector = model.encode(text)

print("Local embeddings: OK")
print("Model: all-MiniLM-L6-v2")
print("Vector dimension:", len(vector))
print("First values:", vector[:3])
