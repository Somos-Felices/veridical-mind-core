from fastapi import FastAPI

app = FastAPI(title="Veridical Mind Core")

@app.get("/health")
def health():
    return {"status": "ok"}
