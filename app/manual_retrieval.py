from app.retrieval import retrieve


if __name__ == "__main__":
    query = "Which airlines have ordered Overture aircraft?"

    results = retrieve(query, top_k=3)

    print(f"Query: {query}")
    print(f"Retrieved {len(results)} chunks")

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Distance:", result["distance"])
        print("Metadata:", result["metadata"])
        print("Text:", result["text"][:300])