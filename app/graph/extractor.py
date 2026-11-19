# Relationship model requires source_chunk_id
# we aren't asking the AI to generate IDs (intentional design decision)
# program knows which chunk the AI is reading
# so it should add the ID automatically

import json

from app.synthesis.llm import ask_llm
from app.graph.models import GraphExtraction


def extract_graph_from_chunk(chunk) -> GraphExtraction:
    """
    Extract entities and relationships from a single document chunk.
    """

    prompt = f"""
You are an information extraction system for a workplace knowledge graph.

Extract important entities and relationships from the text below.

ENTITY TYPES:
- Person
- Project
- Organization
- Supplier
- Product
- Component
- Meeting
- Decision
- Task
- Date
- Risk
- Event

RULES:
1. Extract only information explicitly supported by the text.
2. Do not invent facts or relationships.
3. Use consistent entity names.
4. Relationship names should be short, uppercase, and descriptive.
5. Include supporting evidence for every relationship.
6. Confidence must be between 0 and 1.
7. Preserve uncertainty.
8. Do not turn a possible risk into a confirmed fact.
9. Do not create unsupported relationships.
10. Return valid JSON only. No markdown or explanation.

REQUIRED JSON FORMAT:

{{
    "entities": [
        {{
            "name": "Entity name",
            "entity_type": "Entity type",
            "description": "Short description"
        }}
    ],
    "relationships": [
        {{
            "source_entity": "Entity name",
            "relationship": "RELATIONSHIP_TYPE",
            "target_entity": "Entity name",
            "evidence": "Supporting text",
            "confidence": 0.95
        }}
    ]
}}

DOCUMENT INFORMATION:
Source: {chunk.source}
Chunk ID: {chunk.id}

DOCUMENT TEXT:
{chunk.text}
"""

    # 1. Ask the AI to extract information
    response_text = ask_llm(prompt)

    # check 2
    response_text = response_text.strip()

    if response_text.startswith("```"):
        response_text = (
            response_text
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

    # 2. Parse the returned JSON
    data = json.loads(response_text)

    # 3. Attach the chunk ID ourselves
    for relationship in data.get("relationships", []):
        relationship["source_chunk_id"] = chunk.id

    # 4. Validate everything using Pydantic
    extraction = GraphExtraction.model_validate(data)

    return extraction
