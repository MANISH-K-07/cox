from openai import OpenAI

from app.synthesis.llm import get_client


EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text strings into numerical vectors.
    """

    if not texts:
        return []

    client = get_client()

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    # Return vectors in the same order as the input texts
    return [
        item.embedding
        for item in response.data
    ]
