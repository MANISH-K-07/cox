from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents
from app.processing.deduplication import detect_duplicates


def main():

    data_dir = Path("sample_data")

    # 1. Load documents
    documents = load_all_documents(data_dir)

    print(f"Original documents: {len(documents)}")

    # 2. Chunk documents
    chunks = chunk_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    # 3. Detect duplicates
    chunks = detect_duplicates(chunks)

    duplicates = [
        chunk for chunk in chunks
        if chunk.metadata["is_duplicate"]
    ]

    unique_chunks = [
        chunk for chunk in chunks
        if not chunk.metadata["is_duplicate"]
    ]

    print("\n" + "=" * 60)
    print("DEDUPLICATION RESULTS")
    print("=" * 60)

    print(f"Total chunks: {len(chunks)}")
    print(f"Unique chunks: {len(unique_chunks)}")
    print(f"Duplicates detected: {len(duplicates)}")

    if duplicates:

        print("\nDuplicate details:")

        for duplicate in duplicates:

            print(f"\nDuplicate ID: {duplicate.id}")

            print(
                "Original ID:",
                duplicate.metadata["duplicate_of"]
            )

            print(
                "Text:",
                duplicate.text[:150]
            )

    else:

        print("\nNo exact duplicates found in the sample dataset.")

    print("\n" + "=" * 60)
    print("DEDUPLICATION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
