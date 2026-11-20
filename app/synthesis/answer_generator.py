# takes 2 inputs
# 1. question: what the user wants to know
# 2. retrieved_chunks: the relevant documents returned by our retrieval pipeline.


import json

from app.synthesis.llm import ask_llm


def generate_answer(question: str, retrieved_chunks: list[dict]) -> dict:
    """
    Generate an evidence-based answer using retrieved documents.
    """

    evidence = []

    for chunk in retrieved_chunks:
        evidence.append({
            "source": chunk.get("metadata", {}).get("source", "Unknown"),
            "chunk_id": chunk.get("id", "Unknown"),
            "text": chunk.get("text", ""),
            "graph_context": chunk.get("graph_context", [])
        })

    prompt = f"""
You are an AI assistant helping employees understand project information.

Answer the user's question using ONLY the evidence provided below.

Rules:
1. Do not invent facts or make unsupported assumptions.
2. Distinguish confirmed facts from estimates and potential risks.
3. Mention relevant dates, people, and dependencies.
4. Cite the source documents supporting your answer.
5. If the evidence is insufficient, clearly say so.

User question:
{question}

Retrieved evidence:
{json.dumps(evidence, indent=2)}

Return your response as valid JSON with this structure:

{{
    "answer": "Your clear, concise answer",
    "key_points": [
        "Important finding 1",
        "Important finding 2"
    ],
    "risks": [
        "Identified risk 1"
    ],
    "action_items": [
        "Recommended or explicitly assigned action"
    ],
    "sources": [
        "Source document name"
    ]
}}

Return ONLY valid JSON. Do not include markdown code fences.
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "answer": response,
            "key_points": [],
            "risks": [],
            "action_items": [],
            "sources": []
        }
