# most useful documents are now appearing at the top,
# even though neither search method alone ranked everything perfectly.

from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents
from app.processing.deduplication import detect_duplicates

from app.retrieval.keyword_search import build_keyword_index
from app.retrieval.hybrid_search import hybrid_search


def main():

    print("=" * 60)
    print("CO-X HYBRID SEARCH TEST")
    print("=" * 60)

    # Load all sample documents
    documents = load_all_documents(
        Path("sample_data")
    )

    # Chunk them
    chunks = chunk_documents(documents)

    # Deduplicate
    chunks = detect_duplicates(chunks)

    unique_chunks = [
        chunk for chunk in chunks
        if not chunk.metadata["is_duplicate"]
    ]

    # Build keyword index
    build_keyword_index(unique_chunks)

    # Search
    query = "Why is the Orion pilot schedule at risk?"

    print(f"\nQuery: {query}")

    results = hybrid_search(
        query=query,
        top_k=5,
    )

    print(f"\nResults returned: {len(results)}")

    for rank, result in enumerate(results, start=1):

        print("\n" + "-" * 60)

        print(f"FINAL RANK: {rank}")
        print(f"ID: {result['id']}")
        print(f"Source: {result['metadata']['source']}")

        print(
            f"Semantic rank: {result['semantic_rank']}"
        )

        print(
            f"Keyword rank: {result['keyword_rank']}"
        )

        print(
            f"Hybrid score: {result['hybrid_score']:.6f}"
        )

        print("\nText:")
        print(result["text"][:500])

    print("\n" + "=" * 60)
    print("HYBRID SEARCH TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
