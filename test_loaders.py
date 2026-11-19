from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents


def main():

    data_dir = Path("sample_data")

    # Load original documents
    documents = load_all_documents(data_dir)

    print(f"Original documents: {len(documents)}")

    # Chunk documents
    chunks = chunk_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    print("\n" + "=" * 60)
    print("CHUNK BREAKDOWN")
    print("=" * 60)

    for chunk in chunks:

        print(f"\nID: {chunk.id}")
        print(f"Source: {chunk.source}")
        print(f"Chunk: {chunk.metadata['chunk_index'] + 1} "
              f"of {chunk.metadata['total_chunks']}")
        print(f"Characters: {len(chunk.text)}")

        print("\nText preview:")
        print(chunk.text[:250])

        print("-" * 60)

    print("\nCHUNKING TEST COMPLETED")


if __name__ == "__main__":
    main()
