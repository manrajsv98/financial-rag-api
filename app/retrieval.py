from app.embeddings import create_embedding
from app.vector_store import query_vector_store

def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = create_embedding(query)

    results = query_vector_store(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(documents, metadatas, distances):
        retrieved_chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_chunks