import json
from pathlib import Path

import chromadb

from app.ingestion.models import Document


# Where ChromaDB will store its database on your computer
DB_PATH = Path("storage/chroma_db")

COLLECTION_NAME = "co_x_documents"


def get_collection():
    """
    Connect to persistent ChromaDB storage
    and return our document collection.
    """

    DB_PATH.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "Co-X document chunks"
        },
    )

    return collection


def prepare_metadata(document: Document) -> dict:
    """
    Convert metadata into a format ChromaDB accepts.
    """

    metadata = document.metadata.copy()

    # Chroma metadata supports primitive values.
    # Convert lists/dictionaries into JSON strings.
    for key, value in metadata.items():

        if isinstance(value, (list, dict)):
            metadata[key] = json.dumps(value)

        elif value is None:
            metadata[key] = ""

    # Add standard fields
    metadata["source"] = document.source
    metadata["source_type"] = document.source_type

    if document.timestamp:
        metadata["timestamp"] = document.timestamp

    if document.author:
        metadata["author"] = document.author

    return metadata


def save_documents(
    documents: list[Document],
    embeddings: list[list[float]],
):
    """
    Store document chunks and their vectors in ChromaDB.
    """

    if len(documents) != len(embeddings):
        raise ValueError(
            "Number of documents and embeddings must match."
        )

    collection = get_collection()

# add inserts new records, and may complain if an ID already exists.
# upsert inserts new records or updates an existing record with the same ID.

    collection.upsert(
        ids=[
            document.id
            for document in documents
        ],
        documents=[
            document.text
            for document in documents
        ],
        metadatas=[
            prepare_metadata(document)
            for document in documents
        ],
        embeddings=embeddings,
    )

    return collection.count()
