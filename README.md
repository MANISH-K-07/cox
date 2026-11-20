# Co-X knowledge-management prototype
built by Manish Krishna Kandrakota, for Carnegie Mellon University Tepper School of Business MSPM Capstone Project - Honda Research


## Backend Demo:

```
(.venv) PS E:\Workspace\cox> python demo_backend.py

   ____ ___       __  __
  / ___/ _ \      \ \/ /
 | |  | | | |______\  /
 | |__| |_| |______/  \
  \____\___/      /_/\_\

  CO-X | BACKEND SYSTEM DEMONSTRATION
  Knowledge Synthesis & Hybrid RAG Prototype
  Demo started: November 19, 2026 | 08:46:32 PM

============================================================================
                          1. BACKEND CONNECTIVITY
============================================================================
  [PASS] FastAPI application
         API is responding

============================================================================
                       2. LANGUAGE MODEL CONNECTIVITY
============================================================================
  [PASS] LLM connection
         Model: gpt-6-luna

  Response: The Co-X language model is responding.

============================================================================
                      3. KNOWLEDGE BASE INITIALIZATION
============================================================================
  [PASS] Sample data ingestion
         15 documents loaded
  Chunks created                    : 15
  Unique chunks                     : 15
  Vector database records           : 15
  Keyword index records             : 15
  Knowledge graph nodes             : 71
  Knowledge graph relationships     : 92

============================================================================
                     4. AI-POWERED KNOWLEDGE SYNTHESIS
============================================================================

  Query: Why is the Orion pilot schedule at risk, and what actions need to happen to keep it on track?
  [PASS] Brief generation
         Retrieved information and generated synthesis

EXECUTIVE SUMMARY
----------------------------------------------------------------------------
  1. The January 18, 2027 pilot is at risk because it depends on Northstar’s display controller, whose expected shipment departure is December 16, 2026—but that date is an estimate, not guaranteed. The integration team estimates five business days for installation and validation before system testing; whether the schedule can absorb that work is not yet known because the detailed test plan, test-team capacity, and effect of a partial shipment still need assessment. The schedule impact is a risk, not a confirmed delay, and no revised pilot date has been approved.

KEY FINDINGS
----------------------------------------------------------------------------
  1. Northstar’s November 2 estimate is for the controller to leave its facility on December 16, 2026; it is not a guaranteed delivery date.
  2. A prior risk assessment said a controller arrival after December 12 could cost about a week of integration testing. This is an estimate, not a confirmed schedule impact.
  3. The controller requires an estimated five business days of installation and validation before system testing; the effect on the January 18, 2027 target depends on test capacity, the detailed test plan, and whether partial shipment changes the sequence.
  4. January 18 remains the working target, and no revised pilot date has been approved.

IDENTIFIED RISKS
----------------------------------------------------------------------------
  1. The supplier shipment may depart later than estimated or arrive too late to support integration and system testing.
  2. Test-team capacity and the detailed testing sequence have not yet been confirmed, so the schedule impact is uncertain.
  3. It is not yet known whether Northstar can arrange a partial shipment.

ACTION ITEMS
----------------------------------------------------------------------------
  1. Leo Martinez: obtain Northstar’s confirmation on whether partial shipment is possible by November 5, 2026.
  2. Priya Nair: provide the test-capacity impact assessment by November 6, 2026, including the detailed test-plan and sequencing implications.
  3. Maya Chen: after receiving both inputs, decide whether to retain or revise the January 18, 2027 pilot target; do not treat a date change as approved before that decision.
  4. Assess the schedule against the December 16 shipment estimate and a one-week-slip scenario.

SOURCE DOCUMENTS
----------------------------------------------------------------------------
  1. Project Orion Supplier and Schedule Check-in, meeting, November 2, 2026 (meeting_2026-11-02.txt_chunk_0)
  2. Project Orion Weekly Review, meeting, October 29, 2026 (meeting_2026-10-29.txt_chunk_0)
  3. Project Orion — Infotainment Pilot Brief, PDF (project_orion_brief.pdf_chunk_0)
  4. Northstar Supplier Update — Project Orion, November 2, 2026 (northstar_supplier_update.docx_chunk_0)
  5. Slack update on the December 16 arrival and one-week-slip scenario (slack-006_chunk_0)

============================================================================
                       5. FINAL SYSTEM HEALTH REPORT
============================================================================

  Project                 : Co-X
  Backend                 : FastAPI
  Retrieval architecture  : Hybrid RAG + Knowledge Graph
  Vector storage          : ChromaDB
  Keyword storage         : SQLite FTS5
  Graph storage           : NetworkX
  LLM integration         : gpt-6-luna
----------------------------------------------------------------------------
  Successful checks       : 4
  Failed checks           : 0
  Execution time          : 10.04 seconds
============================================================================


       ALL SYSTEM CHECKS PASSED
       CO-X BACKEND DEMONSTRATION SUCCESSFUL


  API documentation: http://127.0.0.1:8000/docs
  Demo completed: 08:46:42 PM
============================================================================
(.venv) PS E:\Workspace\cox>

```
