import re

from app.graph.models import GraphExtraction


def normalize_name(name: str) -> str:
    """Normalize a name for duplicate detection."""
    name = name.casefold().strip()
    name = re.sub(r"\s+", " ", name)
    return name


def resolve_extractions(
    extractions: list[GraphExtraction],
) -> list[GraphExtraction]:

    canonical_entities = {}
    canonical_names = {}

    # Identify one canonical name for each normalized entity name.
    for extraction in extractions:
        for entity in extraction.entities:
            key = normalize_name(entity.name)

            if key not in canonical_entities:
                canonical_entities[key] = entity
                canonical_names[key] = entity.name

            elif (
                not canonical_entities[key].description
                and entity.description
            ):
                canonical_entities[key].description = entity.description

    # Update relationship endpoints and remove duplicate entities.
    resolved_extractions = []

    for extraction in extractions:
        updated_entities = []
        seen = set()

        for entity in extraction.entities:
            key = normalize_name(entity.name)

            if key not in seen:
                updated_entities.append(canonical_entities[key])
                seen.add(key)

        updated_relationships = []

        for relationship in extraction.relationships:
            source_key = normalize_name(relationship.source_entity)
            target_key = normalize_name(relationship.target_entity)

            updated_relationships.append(
                relationship.model_copy(
                    update={
                        "source_entity": canonical_names.get(
                            source_key, relationship.source_entity
                        ),
                        "target_entity": canonical_names.get(
                            target_key, relationship.target_entity
                        ),
                    }
                )
            )

        resolved_extractions.append(
            GraphExtraction(
                entities=updated_entities,
                relationships=updated_relationships,
            )
        )

    return resolved_extractions
