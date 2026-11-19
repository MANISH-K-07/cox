import networkx as nx

from app.graph.models import GraphExtraction


def build_graph(extractions: list[GraphExtraction]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()

    for extraction in extractions:

        # Add entities as nodes
        for entity in extraction.entities:
            graph.add_node(
                entity.name,
                entity_type=entity.entity_type,
                description=entity.description,
            )

        # Add relationships as edges
        for relationship in extraction.relationships:
            graph.add_edge(
                relationship.source_entity,
                relationship.target_entity,
                relationship=relationship.relationship,
                evidence=relationship.evidence,
                source_chunk_id=relationship.source_chunk_id,
                confidence=relationship.confidence,
            )

    return graph
