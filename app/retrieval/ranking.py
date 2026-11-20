
import math

import re


from app.retrieval.embeddings import generate_embeddings


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Calculate cosine similarity between two vectors."""

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)



STOPWORDS = {
    "the", "is", "a", "an", "and", "or", "of", "to",
    "in", "on", "for", "with", "what", "why", "how",
    "does", "do", "are", "was", "were", "at", "by",
    "about", "this", "that", "it"
}


def keyword_similarity(query: str, text: str) -> float:
    """
    Calculate keyword relevance using basic query expansion.
    Related terms are grouped together.
    """
    query_words = {
        word
        for word in re.findall(r"\b[a-zA-Z0-9]+\b", query.lower())
        if word not in STOPWORDS
    }

    text_words = set(
        re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    )

    if not query_words:
        return 0.0

    expansions = {
        "risk": {
            "risk", "delay", "delayed", "late", "later",
            "slip", "slipped", "threat", "issue"
        },
        "schedule": {
            "schedule", "timeline", "timing", "shipment",
            "delivery", "arrival", "planned", "date", "deadline"
        },
        "pilot": {
            "pilot", "trial", "rollout"
        },
        "orion": {
            "orion"
        }
    }

    matched_groups = 0

    for word in query_words:
        related_words = expansions.get(word, {word})

        if related_words.intersection(text_words):
            matched_groups += 1

    return matched_groups / len(query_words)




def build_ranking_text(chunk: dict) -> str:
    """
    Combine original chunk text with its extracted graph context.
    """

    original_text = chunk["text"]

    graph_context = chunk.get("graph_context", [])

    if not graph_context:
        return original_text

    graph_lines = []

    for relationship in graph_context:
        graph_lines.append(
            f"{relationship.get('source_entity', '')} "
            f"--{relationship.get('relationship', '')}--> "
            f"{relationship.get('target_entity', '')}. "
            f"Evidence: {relationship.get('evidence', '')}"
        )

    return (
        f"Original document:\n{original_text}\n\n"
        f"Extracted knowledge graph relationships:\n"
        + "\n".join(graph_lines)
    )


def rank_chunks_by_relevance(query: str, chunks: list[dict]) -> list[dict]:
    """
    Rank graph-discovered chunks using both semantic and keyword relevance.
    """
    if not chunks:
        return []

    # Generate semantic embeddings.
    ranking_texts = [build_ranking_text(chunk) for chunk in chunks]
    texts = [query] + ranking_texts

    embeddings = generate_embeddings(texts)
    query_embedding = embeddings[0]
    chunk_embeddings = embeddings[1:]

    for chunk, chunk_embedding, ranking_text in zip(
        chunks, chunk_embeddings, ranking_texts
    ):
        # Semantic similarity: understands meaning and related concepts.
        semantic_score = cosine_similarity(
            query_embedding, chunk_embedding
        )

        # Keyword similarity: rewards direct word overlap.
        keyword_score = keyword_similarity(query, ranking_text)

        # Combine both signals.
        final_score = (
            0.7 * semantic_score
            + 0.3 * keyword_score
        )

        chunk["semantic_score"] = semantic_score
        chunk["keyword_score"] = keyword_score
        chunk["relevance_score"] = final_score

    return sorted(
        chunks,
        key=lambda chunk: chunk["relevance_score"],
        reverse=True
    )
