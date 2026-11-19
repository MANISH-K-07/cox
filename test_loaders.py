from pathlib import Path

from app.ingestion.collection_loader import load_all_documents


def main():
    data_dir = Path("sample_data")

    documents = load_all_documents(data_dir)

    print("=" * 60)
    print("CO-X UNIFIED INGESTION TEST")
    print("=" * 60)

    print(f"\nTotal documents loaded: {len(documents)}")

    # Count documents by source
    source_counts = {}

    for document in documents:
        source_counts[document.source] = (
            source_counts.get(document.source, 0) + 1
        )

    print("\nDocuments by source:")

    for source, count in source_counts.items():
        print(f"  {source}: {count}")

    print("\n--- First document ---")

    print(documents[0].model_dump_json(indent=2))

    print("\n--- Last document ---")

    print(documents[-1].model_dump_json(indent=2))

    print("\n--- All document IDs ---")

    for document in documents:
        print(f"{document.id} | {document.source_type}")

    print("\n" + "=" * 60)

    if len(documents) == 15:
        print("SUCCESS: All 15 documents are unified!")
    else:
        print(f"WARNING: Expected 15 documents, got {len(documents)}")

    print("=" * 60)


if __name__ == "__main__":
    main()
    