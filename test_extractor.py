from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents
from app.processing.deduplication import detect_duplicates

from app.graph.extractor import extract_graph_from_chunk


def main():
    print("=" * 60)
    print("CO-X AI GRAPH EXTRACTION TEST")
    print("=" * 60)

    # Load all sample documents
    documents = load_all_documents(Path("sample_data"))

    # Split documents into chunks
    chunks = chunk_documents(documents)

    # Detect duplicates
    chunks = detect_duplicates(chunks)

    # Select one chunk for our first AI extraction test
    test_chunk = next(
        chunk for chunk in chunks
        if "Northstar" in chunk.text
        and "January 18" in chunk.text
    )

    print("\nSelected chunk:")
    print(f"ID: {test_chunk.id}")
    print(f"Source: {test_chunk.source}")
    print("\nText:")
    print(test_chunk.text)

    # Send the chunk to the AI
    print("\nExtracting entities and relationships...")
    extraction = extract_graph_from_chunk(test_chunk)

    # Display extracted entities
    print("\n" + "=" * 60)
    print("ENTITIES")
    print("=" * 60)

    for entity in extraction.entities:
        print(f"\nName: {entity.name}")
        print(f"Type: {entity.entity_type}")
        print(f"Description: {entity.description}")

    # Display extracted relationships
    print("\n" + "=" * 60)
    print("RELATIONSHIPS")
    print("=" * 60)

    for relationship in extraction.relationships:
        print(
            f"\n{relationship.source_entity}"
            f" --{relationship.relationship}--> "
            f"{relationship.target_entity}"
        )

        print(f"Evidence: {relationship.evidence}")
        print(f"Confidence: {relationship.confidence}")
        print(f"Source chunk: {relationship.source_chunk_id}")

    print("\n" + "=" * 60)
    print("AI EXTRACTION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
