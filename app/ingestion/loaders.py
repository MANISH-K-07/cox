# gives us readers for the three document types. 
# JSON will have its own processing 
# because it's structured data rather than a normal document.

import json
from pathlib import Path

from docx import Document as WordDocument
import fitz

from app.ingestion.models import Document


def load_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def load_pdf(file_path: Path) -> str:
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text() + "\n"

    pdf.close()

    return text


def load_docx(file_path: Path) -> str:
    doc = WordDocument(file_path)

    paragraphs = []

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            paragraphs.append(paragraph.text)

    return "\n".join(paragraphs)


def load_json(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_file(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".txt":
        return load_txt(file_path)

    elif extension == ".pdf":
        return load_pdf(file_path)

    elif extension == ".docx":
        return load_docx(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")
    