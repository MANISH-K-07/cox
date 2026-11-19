# Co-X Phase 1 Starter Dataset

This is a synthetic dataset for building and testing a Co-X knowledge-management prototype. It is not Honda internal information.

## Files
- `sample_data/slack_messages.json`: sample Slack channel messages
- `sample_data/emails.json`: sample email messages
- `sample_data/meeting_2026-10-29.txt`: meeting transcript 1
- `sample_data/meeting_2026-11-02.txt`: meeting transcript 2
- `sample_data/project_orion_brief.pdf`: project brief PDF
- `sample_data/northstar_supplier_update.docx`: supplier update Word document
- `docs/ground_truth.md`: expected facts and test questions

## Scenario
Project Orion is a fictional automotive infotainment pilot. Its working target is January 18, 2027. A supplier shipment estimate creates schedule risk, but no revised pilot date has been approved.

## Phase 1 rule
Keep source files unchanged. Any extracted facts, chunks, graph entities, and generated summaries should be stored separately and linked back to these source files.
