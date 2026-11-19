# user prompts a question:
# 1. convert question into a vector using the embedding model.
# 2. ask ChromaDB to find vectors closest to that question vector.
# 3. retrieve corresponding text chunks.
# 4. return chunks, their metadata and similarity distance.

from app.retrieval.embeddings import generate_embeddings
from app.retrieval.vector_store import get_collection


def semantic_search(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Search the vector database for chunks
    semantically related to the user's query.
    """

    # 1. Convert the user's question into an embedding
    query_embedding = generate_embeddings([query])[0]

    # 2. Connect to our database
    collection = get_collection()

    # 3. Search for the most similar vectors
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    # 4. Convert database results into a clean structure
    search_results = []

    for index in range(len(results["ids"][0])):

        search_results.append({
            "id": results["ids"][0][index],
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index],
        })

    return search_results
