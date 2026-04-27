from app.retrieval import retrieve
from app.generation import generate_answer


if __name__ == "__main__":
    question = "Which airlines have ordered Overture aircraft?"

    retrieved_chunks = retrieve(question, top_k=3)

    result = generate_answer(
        question=question,
        retrieved_chunks=retrieved_chunks,
    )

    print("Question:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(source)