
from pathlib import Path

from app.ingestion.collection_loader import load_all_documents
from app.processing.chunking import chunk_documents
from app.processing.deduplication import detect_duplicates

from app.retrieval.embeddings import generate_embeddings
from app.retrieval.vector_store import save_documents
from app.retrieval.keyword_search import build_keyword_index

from app.graph.extractor import extract_graph_from_chunk
from app.graph.entity_resolution import resolve_extractions
from app.graph.graph_builder import build_graph
from app.graph.storage import (
    save_extraction,
    load_extraction,
    save_graph,
)


def initialize_sample_data():
    """
    Load, process, index, and graph all sample data.
    """

    data_dir = Path("sample_data")

    # 1. Load documents
    documents = load_all_documents(data_dir)
    print(f"Documents loaded: {len(documents)}")

    # 2. Chunk documents
    chunks = chunk_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    # 3. Detect duplicates
    chunks = detect_duplicates(chunks)

    unique_chunks = [
        chunk for chunk in chunks
        if not chunk.metadata["is_duplicate"]
    ]

    print(f"Unique chunks: {len(unique_chunks)}")

    # 4. Generate embeddings and populate vector database
    embeddings = generate_embeddings([
        chunk.text for chunk in unique_chunks
    ])

    vector_count = save_documents(
        unique_chunks,
        embeddings
    )

    print(f"Vector database records: {vector_count}")

    # 5. Build keyword search index
    build_keyword_index(unique_chunks)

    # 6. Extract graph information
    extractions = []

    for chunk in unique_chunks:
        extraction = load_extraction(chunk.id)

        if extraction is None:
            extraction = extract_graph_from_chunk(chunk)
            save_extraction(extraction, chunk.id)

        extractions.append(extraction)

    # 7. Resolve entities and build graph
    resolved_extractions = resolve_extractions(extractions)

    graph = build_graph(resolved_extractions)

    # 8. Save graph
    save_graph(graph)

    return {
        "status": "success",
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
        "unique_chunks": len(unique_chunks),
        "vector_records": vector_count,
        "keyword_records": len(unique_chunks),
        "graph_nodes": graph.number_of_nodes(),
        "graph_relationships": graph.number_of_edges()
    }
