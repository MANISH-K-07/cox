# exact-text deduplication:
# 1. normalize text (lowercase, remove unnecessary whitespace).
# 2. calculate fingerprint/hash of the text.
# 3. compare fingerprints.
# 4. if two chunks are identical, mark them as duplicates.
# 5. preserve original documents and their sources.

import hashlib
import re

from app.ingestion.models import Document


def normalize_text(text: str) -> str:
    """
    Normalize text for exact duplicate comparison.
    """

    text = text.lower()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def create_fingerprint(text: str) -> str:
    """
    Create a unique hash fingerprint for normalized text.
    """

    normalized = normalize_text(text)

    fingerprint = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()

    return fingerprint


def detect_duplicates(
    documents: list[Document],
) -> list[Document]:
    """
    Identify exact duplicates while preserving all documents.

    Duplicate documents are marked in metadata.
    They are NOT deleted.
    """

    seen = {}

    for document in documents:

        fingerprint = create_fingerprint(document.text)

        document.metadata["fingerprint"] = fingerprint
        document.metadata["is_duplicate"] = False
        document.metadata["duplicate_of"] = None

        if fingerprint in seen:

            original_document_id = seen[fingerprint]

            document.metadata["is_duplicate"] = True
            document.metadata["duplicate_of"] = (
                original_document_id
            )

        else:

            seen[fingerprint] = document.id

    return documents
