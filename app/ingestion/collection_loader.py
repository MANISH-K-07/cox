# we want all items to become the same type object.

from pathlib import Path

from app.ingestion.models import Document
from app.ingestion.loaders import load_file
from app.ingestion.json_loaders import (
    load_slack_messages,
    load_emails,
)


def load_all_documents(data_dir: Path) -> list[Document]:
    """
    Load every sample source and convert it into
    a unified list of Document objects.
    """

    documents = []

    # 1. Load Slack messages
    slack_documents = load_slack_messages(
        data_dir / "slack_messages.json"
    )
    documents.extend(slack_documents)

    # 2. Load emails
    email_documents = load_emails(
        data_dir / "emails.json"
    )
    documents.extend(email_documents)

    # 3. Load meeting transcripts
    meeting_files = [
        "meeting_2026-10-29.txt",
        "meeting_2026-11-02.txt",
    ]

    for filename in meeting_files:
        file_path = data_dir / filename
        text = load_file(file_path)

        document = Document(
            id=filename,
            source="meeting",
            source_type="meeting_transcript",
            text=text,
            metadata={
                "filename": filename,
            },
        )

        documents.append(document)

    # 4. Load PDF
    pdf_filename = "project_orion_brief.pdf"

    pdf_text = load_file(data_dir / pdf_filename)

    pdf_document = Document(
        id=pdf_filename,
        source="pdf",
        source_type="project_document",
        text=pdf_text,
        metadata={
            "filename": pdf_filename,
        },
    )

    documents.append(pdf_document)

    # 5. Load Word document
    docx_filename = "northstar_supplier_update.docx"

    docx_text = load_file(data_dir / docx_filename)

    docx_document = Document(
        id=docx_filename,
        source="docx",
        source_type="supplier_document",
        text=docx_text,
        metadata={
            "filename": docx_filename,
        },
    )

    documents.append(docx_document)

    return documents
