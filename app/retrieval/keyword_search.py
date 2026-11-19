# using FTS5, built-in search feature in SQLite.

import sqlite3
import json
import re
from pathlib import Path

from app.ingestion.models import Document


DB_PATH = Path("storage/keyword_search.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    return connection


def build_keyword_index(documents: list[Document]):
    """
    Build a full-text search index from document chunks.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # Create the full-text search table
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
        USING fts5(
            id UNINDEXED,
            text,
            source UNINDEXED,
            metadata UNINDEXED
        )
    """)

    # Rebuild the index from scratch for this dataset
    cursor.execute("DELETE FROM chunks_fts")

    # Insert documents
    for document in documents:

        metadata = document.metadata.copy()

        metadata["author"] = document.author
        metadata["timestamp"] = document.timestamp
        metadata["source_type"] = document.source_type

        cursor.execute(
            """
            INSERT INTO chunks_fts
            (id, text, source, metadata)
            VALUES (?, ?, ?, ?)
            """,
            (
                document.id,
                document.text,
                document.source,
                json.dumps(metadata),
            ),
        )

    connection.commit()
    connection.close()

    print(f"Keyword index built with {len(documents)} chunks.")


def keyword_search(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Search chunks using SQLite full-text search.
    """

    # Extract words from the user's query
    words = re.findall(r"\w+", query.lower())

    if not words:
        return []

    # OR means a document can match any query word
    search_query = " OR ".join(words)

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id,
                text,
                source,
                metadata,
                bm25(chunks_fts) AS score
            FROM chunks_fts
            WHERE chunks_fts MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (search_query, top_k),
        )

        rows = cursor.fetchall()

    except sqlite3.OperationalError:
        rows = []

    connection.close()

    results = []

    for row in rows:

        results.append({
            "id": row[0],
            "text": row[1],
            "metadata": {
                **json.loads(row[3]),
                "source": row[2],
            },
            "keyword_score": row[4],
        })

    return results
