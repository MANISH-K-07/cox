from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents
from app.processing.deduplication import detect_duplicates

from app.retrieval.embeddings import generate_embeddings
from app.retrieval.vector_store import save_documents, get_collection


def main():

    print("=" * 60)
    print("CO-X VECTOR DATABASE TEST")
    print("=" * 60)

    # 1. Load
    documents = load_all_documents(
        Path("sample_data")
    )

    print(f"\nLoaded documents: {len(documents)}")

    # 2. Chunk
    chunks = chunk_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    # 3. Deduplicate
    chunks = detect_duplicates(chunks)

    unique_chunks = [
        chunk
        for chunk in chunks
        if not chunk.metadata["is_duplicate"]
    ]

    print(f"Unique chunks: {len(unique_chunks)}")

    # 4. Generate embeddings
    print("\nGenerating embeddings...")

    texts = [
        chunk.text
        for chunk in unique_chunks
    ]

    embeddings = generate_embeddings(texts)

    print(f"Embeddings generated: {len(embeddings)}")

    if embeddings:
        print(
            "Dimensions of first embedding:",
            len(embeddings[0])
        )

    # 5. Save to ChromaDB
    print("\nSaving to ChromaDB...")

    total_saved = save_documents(
        unique_chunks,
        embeddings,
    )

    print(f"Documents in database: {total_saved}")

    # 6. Verify
    collection = get_collection()

    print("\nChecking stored data...")

    stored_data = collection.get(
        limit=3,
        include=["documents", "metadatas"],
    )

    for index, document_id in enumerate(stored_data["ids"]):

        print(f"\nID: {document_id}")

        print(
            "Text:",
            stored_data["documents"][index][:150]
        )

        print(
            "Source:",
            stored_data["metadatas"][index]["source"]
        )

    print("\n" + "=" * 60)
    print("VECTOR DATABASE TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
