import chromadb

from app.config import settings

client = chromadb.PersistentClient(path=settings.chroma_db_path)

def get_collection():
    return client.get_or_create_collection(
        name=settings.chroma_collection_name
    )

def add_chunks_to_vector_store(chunks: list[dict]) -> int:
    collection = get_collection()

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])
        embeddings.append(chunk["embedding"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(ids)

def query_vector_store(query_embedding: list[float], top_k: int = 5):
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    
    return results