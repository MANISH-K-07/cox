
from app.retrieval.graph_enhanced_search import graph_enhanced_search


def main():
    query = "Why is the Orion pilot schedule at risk?"

    print("=" * 70)
    print("CO-X GRAPH-ENHANCED RETRIEVAL TEST")
    print("=" * 70)

    results = graph_enhanced_search(
        query=query,
        top_k=5,
        max_graph_chunks=10,
    )

    print(f"\nQuestion: {query}")
    print(f"Total chunks retrieved: {len(results)}")

    for index, result in enumerate(results, start=1):

        print("\n" + "-" * 70)
        print(f"RESULT {index}")
        print("-" * 70)

        print(f"Chunk ID: {result['id']}")
        print(f"Source: {result['metadata'].get('source')}")
        print(f"Retrieval methods: {result['retrieval_methods']}")
        if "relevance_score" in result:
            print(f"Final relevance score: {result['relevance_score']:.4f}")
            print(f"Semantic score:        {result['semantic_score']:.4f}")
            print(f"Keyword score:         {result['keyword_score']:.4f}")


        print("\nOriginal text:")
        print(result["text"][:700])

        if result["graph_context"]:
            print("\nGraph connections:")

            for context in result["graph_context"][:5]:
                print(
                    f"- {context['source_entity']} "
                    f"--{context['relationship']}--> "
                    f"{context['target_entity']}"
                )
                print(f"  Evidence: {context['evidence']}")


if __name__ == "__main__":
    main()
