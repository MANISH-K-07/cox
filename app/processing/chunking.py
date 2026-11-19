from app.ingestion.models import Document


# Approximate token count using character count
CHUNK_SIZE = 3200
CHUNK_OVERLAP = 400


def split_text(text: str) -> list[str]:
    """
    Split long text into paragraph-aware chunks.
    Short text remains as one chunk.
    """

    text = text.strip()

    if not text:
        return []

    # Keep short documents intact
    if len(text) <= CHUNK_SIZE:
        return [text]

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If a paragraph itself is too long, split it
        if len(paragraph) > CHUNK_SIZE:

            # Save whatever we have accumulated
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            start = 0

            while start < len(paragraph):

                end = start + CHUNK_SIZE

                piece = paragraph[start:end]
                chunks.append(piece.strip())

                start = end - CHUNK_OVERLAP

            continue

        # Try adding the next paragraph
        candidate = (
            current_chunk + "\n\n" + paragraph
            if current_chunk
            else paragraph
        )

        # If adding it exceeds our limit, save current chunk
        if len(candidate) > CHUNK_SIZE:

            chunks.append(current_chunk.strip())

            # Carry some context into the next chunk
            overlap = current_chunk[-CHUNK_OVERLAP:]

            current_chunk = overlap + "\n\n" + paragraph

        else:
            current_chunk = candidate

    # Save the final remaining chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks


def chunk_documents(
    documents: list[Document],
) -> list[Document]:
    """
    Convert full documents into smaller Documents (chunks).
    """

    chunked_documents = []

    for document in documents:

        text_chunks = split_text(document.text)

        # If the document is short, this produces one chunk.
        for index, chunk_text in enumerate(text_chunks):

            chunk_document = Document(
                id=f"{document.id}_chunk_{index}",
                source=document.source,
                source_type=document.source_type,
                text=chunk_text,
                timestamp=document.timestamp,
                author=document.author,
                metadata={
                    **document.metadata,
                    "original_document_id": document.id,
                    "chunk_index": index,
                    "total_chunks": len(text_chunks),
                },
            )

            chunked_documents.append(chunk_document)

    return chunked_documents
