import logging
from fastapi import FastAPI

import os
import tempfile
from fastapi import UploadFile, File 

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
async def ingest_document(
    file: UploadFile = File(...),
    chunk_size: int = 500,
    overlap: int = 100,
):
    logger.info(f"Starting ingestion for uploaded file: {file.filename}")

    if not file.filename.endswith(".pdf"):
        return {
            "status": "failed",
            "file_path": file.filename,
            "chunks_created": 0,
            "chunks_inserted": 0,
        }

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        file_contents = await file.read()
        temp_file.write(file_contents)
        temp_file_path = temp_file.name

    try:
        documents = load_pdf(temp_file_path)

        # Replace temp source path with original filename for cleaner citations
        for doc in documents:
            doc["metadata"]["source"] = file.filename

        chunks = chunk_documents(
            documents,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        logger.info(f"Created {len(chunks)} chunks")

        for chunk in chunks:
            chunk["embedding"] = create_embedding(chunk["text"])

        inserted_count = add_chunks_to_vector_store(chunks)

        logger.info(f"Inserted {inserted_count} chunks into vector store")

        return {
            "status": "success",
            "file_path": file.filename,
            "chunks_created": len(chunks),
            "chunks_inserted": inserted_count,
        }

    finally:
        os.remove(temp_file_path)