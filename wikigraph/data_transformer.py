from typing import List, Dict
from wikigraph.sparql import fetch_data


def process_data(members: Dict, relationships: List[Dict]) -> Dict[str, Dict]:
    graph = {}

    # Add members to the graph
    for uri, attrs in members.items():
        person = attrs["personLabel"]
        if person not in graph:
            graph[uri] = {"relations": [], "attributes": attrs}

    # Add relationships to the graph
    for entry in relationships:
        person = entry["personLabel"]["value"]
        related_person = entry["related_personLabel"]["value"]
        relation_type = entry["relationship"]["value"]

        if person not in graph:
            graph[person] = {"relations": []}

        graph[person]["relations"].append({"type": relation_type, "related_person": related_person})

    return graph



if __name__ == "__main__":
    raw_data = fetch_data()
    processed_data = process_data(raw_data)
    print(processed_data)
