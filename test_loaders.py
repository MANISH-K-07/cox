from pathlib import Path

from app.ingestion.loaders import load_file
from app.ingestion.json_loaders import load_slack_messages, load_emails


DATA_DIR = Path("sample_data")


def main():
    # Load Slack messages
    slack_documents = load_slack_messages(
        DATA_DIR / "slack_messages.json"
    )

    # Load emails
    email_documents = load_emails(
        DATA_DIR / "emails.json"
    )

    # Load meeting transcripts
    meeting_1 = load_file(
        DATA_DIR / "meeting_2026-10-29.txt"
    )

    meeting_2 = load_file(
        DATA_DIR / "meeting_2026-11-02.txt"
    )

    # Load PDF
    pdf_text = load_file(
        DATA_DIR / "project_orion_brief.pdf"
    )

    # Load Word document
    docx_text = load_file(
        DATA_DIR / "northstar_supplier_update.docx"
    )

    print("=" * 60)
    print("CO-X DATA LOADER TEST")
    print("=" * 60)

    print(f"\nSlack messages loaded: {len(slack_documents)}")
    print(f"Emails loaded: {len(email_documents)}")

    print("\n--- First Slack message ---")
    print(slack_documents[0].model_dump_json(indent=2))

    print("\n--- First email ---")
    print(email_documents[0].model_dump_json(indent=2))

    print("\n--- Meeting transcript 1 ---")
    print(meeting_1[:500])

    print("\n--- Meeting transcript 2 ---")
    print(meeting_2[:500])

    print("\n--- PDF ---")
    print(pdf_text[:500])

    print("\n--- DOCX ---")
    print(docx_text[:500])

    print("\n" + "=" * 60)
    print("ALL FILES LOADED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
    