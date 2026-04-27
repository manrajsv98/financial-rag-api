from ingestion import load_pdf
from chunking import chunk_documents

if __name__ == "__main__":
    docs = load_pdf("data/raw/Boom_Supersonic.pdf")
    chunks = chunk_documents(docs, chunk_size=100, overlap=20)

    print(f"Loaded {len(docs)} pages")
    print(f"Created {len(chunks)} chunks")

    for chunk in chunks [:3]:
        print(chunk["chunk_id"])
        print(chunk["metadata"])
        print(chunk["text"][:300])
        print("-" * 50)