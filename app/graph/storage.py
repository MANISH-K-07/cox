import json
from pathlib import Path

import networkx as nx

from app.graph.models import GraphExtraction


GRAPH_DIR = Path("storage/graph")
EXTRACTIONS_DIR = GRAPH_DIR / "extractions"


def save_extraction(extraction, chunk_id: str):
    """Save one chunk's AI extraction as JSON."""

    EXTRACTIONS_DIR.mkdir(parents=True, exist_ok=True)

    path = EXTRACTIONS_DIR / f"{chunk_id}.json"

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            extraction.model_dump(),
            file,
            indent=2,
            ensure_ascii=False,
        )


# receives a chunk ID.
# checks whether a JSON file for that chunk exists.
# if the file doesn't exist, it returns None.
# if the file exists, it reads the JSON and converts it back into a GraphExtraction object using Pydantic.

def load_extraction(chunk_id: str) -> GraphExtraction | None:
    """Load a previously saved extraction for a chunk."""

    path = EXTRACTIONS_DIR / f"{chunk_id}.json"

    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        extraction_data = json.load(file)

    return GraphExtraction.model_validate(extraction_data)


def save_graph(graph: nx.MultiDiGraph):
    """Save graph nodes and relationships as JSON."""

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    graph_data = {
        "nodes": [
            {
                "id": node,
                **data,
            }
            for node, data in graph.nodes(data=True)
        ],
        "relationships": [
            {
                "source": source,
                "target": target,
                **data,
            }
            for source, target, data in graph.edges(data=True)
        ],
    }

    path = GRAPH_DIR / "knowledge_graph.json"

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            graph_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nKnowledge graph saved to: {path}")


def load_graph() -> nx.MultiDiGraph:
    """Load the saved graph from JSON."""

    path = GRAPH_DIR / "knowledge_graph.json"

    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge graph not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        graph_data = json.load(file)

    graph = nx.MultiDiGraph()

    for node in graph_data["nodes"]:
        node_id = node.pop("id")
        graph.add_node(node_id, **node)

    for relationship in graph_data["relationships"]:
        source = relationship.pop("source")
        target = relationship.pop("target")

        graph.add_edge(
            source,
            target,
            **relationship,
        )

    return graph
