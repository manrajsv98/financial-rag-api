import json

from app.retrieval import retrieve
from app.generation import generate_answer


def load_eval_questions(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)


def keyword_match(answer: str, expected_keywords: list[str]) -> float:
    answer_lower = answer.lower()

    matches = 0

    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            matches += 1

    return matches / len(expected_keywords)


def retrieval_hit(retrieved_chunks: list[dict], expected_page: int) -> bool:
    for chunk in retrieved_chunks:
        if chunk["metadata"].get("page") == expected_page:
            return True

    return False


def run_evaluation(eval_file_path: str = "data/eval/eval_questions.json"):
    questions = load_eval_questions(eval_file_path)

    results = []

    for item in questions:
        question = item["question"]
        expected_keywords = item["expected_keywords"]
        expected_page = item["expected_page"]

        retrieved_chunks = retrieve(question, top_k=3)
        answer_result = generate_answer(question, retrieved_chunks)

        answer = answer_result["answer"]

        result = {
            "question": question,
            "answer": answer,
            "keyword_score": keyword_match(answer, expected_keywords),
            "retrieval_hit": retrieval_hit(retrieved_chunks, expected_page),
        }

        results.append(result)

    return results


if __name__ == "__main__":
    eval_results = run_evaluation()

    for result in eval_results:
        print("\nQuestion:", result["question"])
        print("Answer:", result["answer"])
        print("Keyword Score:", result["keyword_score"])
        print("Retrieval Hit:", result["retrieval_hit"])