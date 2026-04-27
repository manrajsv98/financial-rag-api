from fastapi import FastAPI

app = FastAPI(
    title="Financial Document Intelligence RAG API",
    description="A production-style RAG API for querying financial documents.",
    version='0.1.0',
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "financial-rag-api",
        "version": "0.1.0",
    }