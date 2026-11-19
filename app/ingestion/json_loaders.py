import json
from pathlib import Path

from app.ingestion.models import Document


def load_slack_messages(file_path: Path) -> list[Document]:
    """Load Slack messages and convert each into a Document."""

    with open(file_path, "r", encoding="utf-8") as file:
        messages = json.load(file)

    documents = []

    for message in messages:
        document = Document(
            id=message["id"],
            source="slack",
            source_type="slack_message",
            text=message["text"],
            timestamp=message.get("timestamp"),
            author=message.get("author"),
            metadata={
                "channel": message.get("channel"),
                "thread_id": message.get("thread_id"),
            },
        )

        documents.append(document)

    return documents


def load_emails(file_path: Path) -> list[Document]:
    """Load emails and convert each into a Document."""

    with open(file_path, "r", encoding="utf-8") as file:
        emails = json.load(file)

    documents = []

    for email in emails:
        document = Document(
            id=email["id"],
            source="email",
            source_type="email",
            text=email["body"],
            timestamp=email.get("timestamp"),
            author=email.get("from"),
            metadata={
                "subject": email.get("subject"),
                "to": email.get("to", []),
            },
        )

        documents.append(document)

    return documents
