# Co-X — Minimum Viable Product Requirements

## 1. Project Objective

Develop an AI-powered knowledge management prototype that ingests information from multiple enterprise sources, organizes the information into a connected knowledge base, and generates concise, evidence-backed synthesis documents.

## 2. Supported Inputs

The initial prototype will support:
- Slack messages (JSON exports)
- Gmail messages (JSON exports)
- Meeting transcripts (TXT)
- PDF documents
- Microsoft Word documents (DOCX)

## 3. Core Functional Requirements

**FR-01: Multi-source ingestion**

The system shall accept and process information from all supported input formats.

**FR-02: Text extraction**

The system shall extract readable text and relevant metadata from uploaded sources.

**FR-03: Document chunking and indexing**

The system shall divide extracted text into searchable sections and generate embeddings.

**FR-04: Knowledge extraction**

The system shall identify entities, facts, people, projects, decisions, issues, and action items.

**FR-05: Knowledge graph construction**

The system shall establish relationships between extracted entities and maintain links to their original sources.

**FR-06: Hybrid retrieval**

The system shall combine keyword search, semantic search, and knowledge graph retrieval to identify relevant information.

**FR-07: Synthesis generation**

The system shall generate structured summaries containing:
- Executive summary
- Important developments
- Previously established decisions
- Unresolved questions
- Action items
- Supporting sources

**FR-08: Source attribution**

Generated claims shall be traceable to their original documents or messages.

**FR-09: Knowledge updates**

When new information is ingested, the system shall update its existing knowledge rather than treating every ingestion as an unrelated collection of documents.

**FR-10: Contradiction awareness**

The system shall identify potentially conflicting information and distinguish confirmed decisions from suggestions, estimates, and unresolved discussions.

## 4. Non-functional Requirements

- Simple and accessible user interface.
- Modular and maintainable code.
- Reasonable response time for a small demonstration dataset.
- Source traceability.
- Protection of API credentials.
- No fabricated decisions or source references.

## 5. Prototype Success Criteria

The prototype will be considered successful when it can:

1. Ingest at least three different types of information sources.
2. Extract and organize their contents.
3. Build a knowledge graph connecting relevant entities.
4. Retrieve relevant information through keyword, vector, and graph search.
5. Generate a coherent synthesis document using multiple sources.
6. Display source references supporting its conclusions.
7. Incorporate new information and reflect changes in subsequent summaries.