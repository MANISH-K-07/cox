
import json

from app.retrieval.graph_enhanced_search import graph_enhanced_search
from app.synthesis.answer_generator import generate_answer


def main():
    question = "Why is the Orion pilot schedule at risk?"

    print("=" * 70)
    print("CO-X ANSWER SYNTHESIS TEST")
    print("=" * 70)

    # Step 1: Retrieve relevant evidence.
    print("\nRetrieving relevant documents...")

    retrieved_chunks = graph_enhanced_search(question)

    print(f"Retrieved {len(retrieved_chunks)} chunks.")

    # Step 2: Generate an answer using the retrieved evidence.
    print("\nGenerating answer using the LLM...")

    result = generate_answer(
        question=question,
        retrieved_chunks=retrieved_chunks
    )

    # Step 3: Display the answer.
    print("\n" + "=" * 70)
    print("GENERATED ANSWER")
    print("=" * 70)

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
