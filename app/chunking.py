from typing import List, Dict, Any 

def chunk_documents(
        documents: List[Dict[str,Any]],
        chunk_size: int = 500,
        overlap: int = 100,
) -> List[Dict[str,Any]]:
    
    chunks = []

    for doc in documents:
        text = doc["text"]
        metadata = doc["metadata"]

        words = text.split()

        start = 0
        chunk_index = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunk = {
                "chunk_id": f"{metadata['source']}_p{metadata['page']}_c{chunk_index}",
                "text": chunk_text,
                "metadata": {
                    **metadata,
                    "chunk_index": chunk_index,
                },
            }

            chunks.append(chunk)

            start += chunk_size - overlap
            chunk_index += 1

    return chunks