# adds retrieval_methods and graph_context fields to search results.

import re

from app.graph.storage import load_graph
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.vector_store import get_collection

from app.retrieval.ranking import rank_chunks_by_relevance


def graph_enhanced_search(
    query: str,
    top_k: int = 5,
    max_graph_chunks: int = 10,
) -> list[dict]:
    """
    Combine hybrid search with one-hop knowledge graph expansion.

    Returns original hybrid results plus additional chunks
    discovered through connected graph relationships.
    """

    # 1. Run our existing hybrid search
    hybrid_results = hybrid_search(
        query=query,
        top_k=top_k,
    )

    # 2. Load the saved knowledge graph
    graph = load_graph()

    # Store results by chunk ID to avoid duplicates
    combined = {}

    for result in hybrid_results:
        combined[result["id"]] = {
            **result,
            "retrieval_methods": ["hybrid"],
            "graph_context": [],
        }

    # 3. Find graph entities mentioned in hybrid results
    matched_entities = set()

    for result in hybrid_results:
        text = result["text"].casefold()

        for entity_name in graph.nodes:
            entity_name_lower = entity_name.casefold()

            # Match complete entity names, not partial words
            pattern = (
                r"(?<!\w)"
                + re.escape(entity_name_lower)
                + r"(?!\w)"
            )

            if re.search(pattern, text):
                matched_entities.add(entity_name)

    # 4. Explore relationships connected to those entities
    graph_chunk_context = {}

    for entity_name in matched_entities:

        # Look at both incoming and outgoing relationships
        connected_edges = list(
            graph.in_edges(entity_name, data=True)
        ) + list(
            graph.out_edges(entity_name, data=True)
        )

        for source, target, data in connected_edges:

            chunk_id = data.get("source_chunk_id")

            if not chunk_id:
                continue

            context = {
                "matched_entity": entity_name,
                "source_entity": source,
                "relationship": data.get("relationship"),
                "target_entity": target,
                "evidence": data.get("evidence"),
                "confidence": data.get("confidence"),
            }

            graph_chunk_context.setdefault(
                chunk_id, []
            ).append(context)


    # check 2
    # Remove duplicate graph connections for each source chunk
    for chunk_id, contexts in graph_chunk_context.items():

        unique_contexts = {}

        for context in contexts:

            # Two graph traversals may discover the same edge.
            # Use its actual relationship and evidence to identify it.
            key = (
                context["source_entity"],
                context["relationship"],
                context["target_entity"],
                context["evidence"],
            )

            unique_contexts[key] = context

        graph_chunk_context[chunk_id] = list(
            unique_contexts.values()
        )


    # 5. Limit the number of additional graph-discovered chunks
    graph_chunk_ids = [
        chunk_id
        for chunk_id in graph_chunk_context
        if chunk_id not in combined
    ][:max_graph_chunks]

    # 6. Retrieve the original chunks from ChromaDB
    if graph_chunk_ids:

        collection = get_collection()

        retrieved = collection.get(
            ids=graph_chunk_ids,
            include=["documents", "metadatas"],
        )

        for index, chunk_id in enumerate(retrieved["ids"]):

            combined[chunk_id] = {
                "id": chunk_id,
                "text": retrieved["documents"][index],
                "metadata": retrieved["metadatas"][index],
                "retrieval_methods": ["graph"],
                "graph_context": [],
            }

    # 7. Attach graph context to hybrid results too
    for chunk_id, contexts in graph_chunk_context.items():

        if chunk_id in combined:
            result = combined[chunk_id]

            if "graph" not in result["retrieval_methods"]:
                result["retrieval_methods"].append("graph")

            result["graph_context"].extend(contexts)

    # 8. Return hybrid results first, followed by graph discoveries
    # Separate the original hybrid results from graph-only results.
    hybrid_results = [
        result
        for result in combined.values()
        if "hybrid" in result["retrieval_methods"]
    ]

    graph_results = [
        result
        for result in combined.values()
        if "hybrid" not in result["retrieval_methods"]
    ]

    # Rank graph-only results by semantic relevance to the question.
    ranked_graph_results = rank_chunks_by_relevance(
        query=query,
        chunks=graph_results,
    )

    # Keep hybrid results first, followed by ranked graph results.
    return hybrid_results + ranked_graph_results
