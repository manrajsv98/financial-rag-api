from app.chunking import chunk_documents


def test_chunk_documents_creates_chunks():
    documents = [
        {
            "text": "one two three four five six seven eight nine ten",
            "metadata": {
                "source": "test.pdf",
                "page": 1,
            },
        }
    ]

    chunks = chunk_documents(
        documents,
        chunk_size=5,
        overlap=2,
    )

    assert len(chunks) > 1
    assert chunks[0]["metadata"]["source"] == "test.pdf"
    assert chunks[0]["metadata"]["page"] == 1
    assert "chunk_id" in chunks[0]
    assert "text" in chunks[0]