from openai import OpenAI

from app.config import settings


client = OpenAI(api_key=settings.openai_api_key)


def build_context(retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        metadata = chunk["metadata"]

        source = metadata.get("source", "unknown")
        page = metadata.get("page", "unknown")

        context_blocks.append(
            f"Source {i}: {source}, page {page}\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_blocks)


def generate_answer(question: str, retrieved_chunks: list[dict]) -> dict:
    context = build_context(retrieved_chunks)

    prompt = f"""
You are a financial document assistant.

Answer the user's question using only the provided context.

If the answer is not available in the context, say:
"I could not find enough information in the provided documents to answer this question."

Question:
{question}

Context:
{context}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    sources = []

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        sources.append(
            {
                "source": metadata.get("source"),
                "page": metadata.get("page"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": chunk.get("distance"),
            }
        )

    return {
        "answer": response.output_text,
        "sources": sources,
    }