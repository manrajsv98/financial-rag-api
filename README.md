# Financial Document Intelligence RAG API

## Overview
End-to-end Retrieval-Augmented Generation (RAG) system for querying financial documents.

## Features
- PDF ingestion and preprocessing
- Text chunking with overlap
- OpenAI embeddings
- Vector search with ChromaDB
- LLM-based answer generation
- FastAPI REST API

## Architecture
PDF → Chunking → Embeddings → Vector DB → Retrieval → LLM → API

## Example Query
POST /ask

{
  "question": "Which airlines have ordered Overture aircraft?"
}

## Example Response
{
  "answer": "American Airlines, United Airlines, and Japan Airlines...",
  "sources": [...]
}

## Tech Stack
- Python
- FastAPI
- OpenAI API
- ChromaDB

## How to Run
uvicorn app.main:app --reload