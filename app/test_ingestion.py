from ingestion import load_pdf

if __name__ == "__main__":
    docs = load_pdf("data/raw/Boom_Supersonic.pdf")

    print(f"Loaded {len(docs)} pages")

    for doc in docs[:2]:
        print(doc["metadata"])
        print(doc["text"][:200])
        print("-" * 50)