from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents
from app.processing.deduplication import detect_duplicates

from app.graph.extractor import extract_graph_from_chunk
from app.graph.graph_builder import build_graph

from app.graph.entity_resolution import resolve_extractions

from app.graph.storage import (
    save_extraction,
    load_extraction,
    save_graph,
    load_graph,
)


def main():
    print("=" * 60)
    print("CO-X FULL KNOWLEDGE GRAPH BUILD")
    print("=" * 60)

    # 1. Load all sample documents
    documents = load_all_documents(Path("sample_data"))
    print(f"\nDocuments loaded: {len(documents)}")

    # 2. Split documents into chunks
    chunks = chunk_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    # 3. Remove exact duplicates from processing
    chunks = detect_duplicates(chunks)

    unique_chunks = [
        chunk for chunk in chunks
        if not chunk.metadata["is_duplicate"]
    ]

    print(f"Unique chunks to process: {len(unique_chunks)}")

    # 4. Extract entities and relationships from each chunk
    extractions = []

    cached_count = 0
    newly_processed_count = 0

    for index, chunk in enumerate(unique_chunks, start=1):
        print("\n" + "-" * 60)
        print(f"Processing chunk {index}/{len(unique_chunks)}")
        print(f"Source: {chunk.source}")
        print(f"Chunk ID: {chunk.id}")

        try:
            # First, check whether this chunk was processed before
            extraction = load_extraction(chunk.id)

            if extraction is not None:
                print("Using cached extraction.")
                cached_count += 1

            else:
                print("No cached extraction found. Calling LLM...")

                extraction = extract_graph_from_chunk(chunk)

                # Save the extraction for future runs
                save_extraction(extraction, chunk.id)

                newly_processed_count += 1

            extractions.append(extraction)

            print(f"Entities extracted: {len(extraction.entities)}")
            print(
                "Relationships extracted: "
                f"{len(extraction.relationships)}"
            )

        except Exception as error:
            print(f"ERROR processing this chunk: {error}")

    print("\nEXTRACTION CACHE RESULTS")
    print(f"Loaded from cache: {cached_count}")
    print(f"Newly processed: {newly_processed_count}")

    # 5. Resolve duplicate entities
    resolved_extractions = resolve_extractions(extractions)

    print("\nEntity resolution completed.")

    # Count entities before and after resolution
    before_count = sum(
        len(extraction.entities)
        for extraction in extractions
    )

    after_count = len({
        entity.name
        for extraction in resolved_extractions
        for entity in extraction.entities
    })

    print(f"Entity mentions before resolution: {before_count}")
    print(f"Unique entity names after resolution: {after_count}")

    # 6. Build the consolidated graph
    graph = build_graph(resolved_extractions)


    # Save the consolidated graph
    save_graph(graph)

    # Load it again to verify persistence
    loaded_graph = load_graph()

    print("\nGRAPH STORAGE VERIFICATION")
    print(f"Original nodes: {graph.number_of_nodes()}")
    print(f"Loaded nodes: {loaded_graph.number_of_nodes()}")
    print(f"Original edges: {graph.number_of_edges()}")
    print(f"Loaded edges: {loaded_graph.number_of_edges()}")

    assert graph.number_of_nodes() == loaded_graph.number_of_nodes()
    assert graph.number_of_edges() == loaded_graph.number_of_edges()

    print("Graph saved and loaded successfully!")


    # 7. Display graph statistics
    print("\n" + "=" * 60)
    print("KNOWLEDGE GRAPH RESULTS")
    print("=" * 60)

    print(f"\nSuccessful chunks: {len(extractions)}")
    print(f"Entities (nodes): {graph.number_of_nodes()}")
    print(f"Relationships (edges): {graph.number_of_edges()}")

    print("\nENTITY TYPES:")

    entity_types = {}

    for _, data in graph.nodes(data=True):
        entity_type = data.get("entity_type", "Unknown")
        entity_types[entity_type] = entity_types.get(entity_type, 0) + 1

    for entity_type, count in sorted(entity_types.items()):
        print(f"- {entity_type}: {count}")

    print("\nSAMPLE RELATIONSHIPS:")

    for source, target, data in list(graph.edges(data=True))[:15]:
        print(
            f"- {source} "
            f"--{data['relationship']}--> "
            f"{target}"
        )

    print("\n" + "=" * 60)
    print("FULL GRAPH BUILD COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
