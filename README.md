# Document Intelligence

A full-stack Retrieval-Augmented Generation (RAG) application for querying PDF documents using natural language.

Built using FastAPI, Streamlit, OpenAI embeddings, and ChromaDB.


---------------> USE IT HERE rag-app.manrajvirdee.dev <---------------

---

# Overview

This project allows users to upload PDF documents, process them into semantic vector embeddings, and ask grounded questions over the document content.

The system uses a Retrieval-Augmented Generation (RAG) pipeline:

1. PDF documents are uploaded and processed
2. Text is extracted and split into chunks
3. Embeddings are generated using OpenAI
4. Chunks are stored in ChromaDB vector database
5. User questions are embedded and semantically matched against stored chunks
6. Relevant context is retrieved and passed to the LLM
7. The LLM generates grounded answers with sources

---

# Features

* PDF document upload and ingestion
* Semantic search using vector embeddings
* Grounded answer generation
* Source attribution for retrieved chunks
* Configurable chunk size and overlap
* Responsive Streamlit frontend
* FastAPI backend API
* ChromaDB vector storage
* Dockerised backend deployment
* Cloud deployment using Render and Streamlit Community Cloud
* Custom domain routing via Cloudflare
* Error handling for API quota and ingestion failures

---

# Architecture

```text
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
PDF Processing + Chunking
        ↓
OpenAI Embeddings
        ↓
ChromaDB Vector Store
        ↓
Semantic Retrieval
        ↓
LLM Answer Generation
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

## Frontend

* Streamlit

## AI / ML

* OpenAI API
* Embeddings
* Retrieval-Augmented Generation (RAG)

## Database

* ChromaDB

## DevOps & Deployment

* Docker
* GitHub
* Render
* Streamlit Community Cloud
* Cloudflare

## Testing

* pytest

---

# Example Workflow

## Upload Document

Users upload a PDF document through the Streamlit interface.

## Ingestion Pipeline

The backend:

* extracts text from the PDF
* splits the document into chunks
* generates embeddings for each chunk
* stores embeddings in ChromaDB

## Ask Questions

Users can ask natural language questions such as:

```text
Which airlines have ordered Overture aircraft?
```

The system retrieves relevant chunks and generates a grounded response.

---

# Project Structure

```text
financial-rag-api/
│
├── app/
│   ├── main.py
│   ├── generation.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── ingestion.py
│   └── config.py
│
├── ui/
│   └── streamlit_app.py
│
├── tests/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Local Development

## Clone Repository

```bash
git clone https://github.com/yourusername/financial-rag-api.git
cd financial-rag-api
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# Run Frontend

```bash
streamlit run ui/streamlit_app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

# Deployment

## Backend

The FastAPI backend is containerised using Docker and deployed on Render.

## Frontend

The Streamlit frontend is deployed using Streamlit Community Cloud.

## Domain Routing

Custom domain routing and redirects are configured using Cloudflare.

---

# Challenges & Learnings

This project involved:

* understanding RAG architecture
* handling document chunking and semantic retrieval
* deploying frontend and backend services separately
* managing OpenAI API usage and rate limits
* debugging deployment and networking issues
* designing responsive Streamlit UI components
* integrating cloud services and custom domains

---

# Future Improvements

Potential future improvements include:

* OCR support for scanned PDFs
* asynchronous ingestion jobs
* user authentication
* multi-document collections
* chat history and conversational memory
* evaluation metrics dashboard
* advanced retrieval and reranking
* migration to PostgreSQL-backed metadata storage

---

# Disclaimer

This project was built as a learning-focused AI engineering project exploring modern Retrieval-Augmented Generation workflows and cloud deployment practices.
