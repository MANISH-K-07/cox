# Relationship model requires source_chunk_id
# we aren't asking the AI to generate IDs (intentional design decision)
# program knows which chunk the AI is reading
# so it should add the ID automatically

import json

from app.synthesis.llm import ask_llm
from app.graph.models import GraphExtraction


# we are not expecting the extraction quality to be perfect!
# the following prompt is just for evaluation.

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
2. Do not invent facts, entities, or relationships.
3. Use consistent entity names. Use the full name when available.
4. Do not create separate entities for the same thing using different names.
5. Use the entity types listed above. Do not invent new types.
6. Relationship names must be short, uppercase, and descriptive.
7. Relationships must have the correct direction.
8. Include an exact supporting quote for every relationship.
9. Confidence must be between 0 and 1.
10. Preserve uncertainty:
    - "may" means possible
    - "expected" means an estimate
    - "confirmed" means explicitly confirmed
    - "target" does not mean a guaranteed date
11. Do not turn a risk into a confirmed event.
12. Extract people and their roles when explicitly mentioned.
13. Extract dates with the year when the year is explicitly available.
14. If the year is not available, do not invent it.
15. Tasks should include the responsible person if the text identifies them.
16. Avoid creating entities for generic words unless they are
    meaningful to the project.
17. Return valid JSON only. No markdown or explanation.

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
