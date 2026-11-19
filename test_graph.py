from app.graph.models import Entity, Relationship, GraphExtraction
from app.graph.graph_builder import build_graph


def main():
    # Create sample entities
    entities = [
        Entity(
            name="Project Orion",
            entity_type="Project",
            description="Automotive infotainment pilot",
        ),
        Entity(
            name="Northstar",
            entity_type="Supplier",
            description="Supplier of the display controller",
        ),
        Entity(
            name="Display Controller",
            entity_type="Component",
            description="Hardware component required for Orion",
        ),
    ]

    # Create sample relationships
    relationships = [
        Relationship(
            source_entity="Project Orion",
            relationship="DEPENDS_ON",
            target_entity="Northstar",
            evidence="The Orion pilot depends on Northstar's delivery.",
            source_chunk_id="sample_chunk_001",
        ),
        Relationship(
            source_entity="Northstar",
            relationship="SUPPLIES",
            target_entity="Display Controller",
            evidence="Northstar supplies the display controller.",
            source_chunk_id="sample_chunk_001",
        ),
    ]

    # Put them into our extraction object
    extraction = GraphExtraction(
        entities=entities,
        relationships=relationships,
    )

    # Build the graph
    graph = build_graph([extraction])

    print("=" * 50)
    print("KNOWLEDGE GRAPH TEST")
    print("=" * 50)

    print(f"\nNumber of entities: {graph.number_of_nodes()}")
    print(f"Number of relationships: {graph.number_of_edges()}")

    print("\nENTITIES:")
    for node, data in graph.nodes(data=True):
        print(f"- {node} ({data['entity_type']})")

    print("\nRELATIONSHIPS:")
    for source, target, data in graph.edges(data=True):
        print(f"- {source} --{data['relationship']}--> {target}")
        print(f"  Evidence: {data['evidence']}")
        print(f"  Source: {data['source_chunk_id']}")

    print("\nGraph test completed successfully!")


if __name__ == "__main__":
    main()
