from app.ingestion import load_pdf
from app.chunking import chunk_documents
from app.embeddings import create_embedding
from app.vector_store import add_chunks_to_vector_store, query_vector_store


if __name__ == "__main__":
    docs = load_pdf("data/raw/Boom_Supersonic.pdf")
    chunks = chunk_documents(docs, chunk_size=100, overlap=20)

    # Keep this small for testing to avoid cost/time
    chunks = chunks[:5]

    for chunk in chunks:
        chunk["embedding"] = create_embedding(chunk["text"])

    inserted_count = add_chunks_to_vector_store(chunks)
    print(f"Inserted {inserted_count} chunks into vector store")

    query = "What airlines have ordered Overture aircraft?"
    query_embedding = create_embedding(query)

    results = query_vector_store(query_embedding, top_k=3)

    print("Query:", query)
    print("Results:")

    for i, document in enumerate(results["documents"][0]):
        print(f"\nResult {i + 1}")
        print("Distance:", results["distances"][0][i])
        print("Metadata:", results["metadatas"][0][i])
        print("Text:", document[:300])