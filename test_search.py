from app.retrieval.search import semantic_search


def main():

    query = "Why is the Orion pilot schedule at risk?"

    print("=" * 60)
    print("CO-X SEMANTIC SEARCH TEST")
    print("=" * 60)

    print(f"\nQuery: {query}")

    results = semantic_search(
        query=query,
        top_k=5,
    )

    print(f"\nResults returned: {len(results)}")

    for index, result in enumerate(results, start=1):

        print("\n" + "-" * 60)

        print(f"Result {index}")
        print(f"ID: {result['id']}")
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']:.4f}")

        print("\nText:")
        print(result["text"])

    print("\n" + "=" * 60)
    print("SEARCH TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
