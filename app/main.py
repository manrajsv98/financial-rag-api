import logging
from fastapi import FastAPI

from app.schemas import AskRequest, AskResponse, IngestRequest, IngestResponse
from app.retrieval import retrieve
from app.generation import generate_answer
from app.ingestion import load_pdf
from app.chunking import chunk_documents
from app.embeddings import create_embedding
from app.vector_store import add_chunks_to_vector_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    logger.info(f"Received question: {request.question}")
    
    try:

        retrieved_chunks = retrieve(
            query=request.question,
            top_k=request.top_k,
        )

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")

        result = generate_answer(
            question=request.question,
            retrieved_chunks=retrieved_chunks,
        )
        
        logger.info("Answer generated successfully")

        return result
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")

        return {
            "answer": "An error occurred while processing the request.",
            "sources": []
        }

@app.post("/ingest", response_model=IngestResponse)
def ingest_document(request: IngestRequest):
    logger.info(f"Starting ingestion for file: {request.file_path}")

    documents = load_pdf(request.file_path)
    chunks = chunk_documents(
        documents,
        chunk_size=request.chunk_size,
        overlap=request.overlap,
    )

    logger.info(f"Created {len(chunks)} chunks")

    for chunk in chunks:
        chunk["embedding"] = create_embedding(chunk["text"])

    inserted_count = add_chunks_to_vector_store(chunks)

    logger.info(f"Inserted {inserted_count} chunks into vector store")

    return {
        "status": "success",
        "file_path": request.file_path,
        "chunks_created": len(chunks),
        "chunks_inserted": inserted_count,
    }