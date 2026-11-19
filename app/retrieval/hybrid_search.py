from app.retrieval.search import semantic_search
from app.retrieval.keyword_search import keyword_search


def hybrid_search(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Combine semantic and keyword search
    using Reciprocal Rank Fusion (RRF).
    """

    # Get results from both search engines
    semantic_results = semantic_search(
        query=query,
        top_k=top_k,
    )

    keyword_results = keyword_search(
        query=query,
        top_k=top_k,
    )

    # Store combined scores
    combined = {}

    # each search engine votes for its best results,
    # and we combine those votes.

    # RRF (Reciprocal Rank Fusion) constant
    k = 60

    # Add semantic rankings
    for rank, result in enumerate(semantic_results, start=1):

        document_id = result["id"]

        if document_id not in combined:

            combined[document_id] = {
                **result,
                "hybrid_score": 0,
                "semantic_rank": None,
                "keyword_rank": None,
            }

        combined[document_id]["semantic_rank"] = rank

        combined[document_id]["hybrid_score"] += (
            1 / (k + rank)
        )

    # Add keyword rankings
    for rank, result in enumerate(keyword_results, start=1):

        document_id = result["id"]

        if document_id not in combined:

            combined[document_id] = {
                **result,
                "hybrid_score": 0,
                "semantic_rank": None,
                "keyword_rank": None,
            }

        combined[document_id]["keyword_rank"] = rank

        combined[document_id]["hybrid_score"] += (
            1 / (k + rank)
        )

    # Sort by combined score, highest first
    ranked_results = sorted(
        combined.values(),
        key=lambda result: result["hybrid_score"],
        reverse=True,
    )

    return ranked_results[:top_k]
