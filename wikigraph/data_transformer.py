from typing import List, Dict
from wikigraph.sparql import fetch_data


def process_data(members: List[str], relationships: List[Dict]) -> Dict[str, Dict]:
    graph = {}

    # Initialize all members in the graph with an empty list of relations
    for member in members:
        graph[member] = {"relations": []}

    # Add relationships to the corresponding members in the graph
    for entry in relationships:
        person = entry["personLabel"]["value"]
        relation = entry["relationLabel"]["value"]
        graph[person]["relations"].append(relation)

    return graph

if __name__ == "__main__":
    raw_data = fetch_data()
    processed_data = process_data(raw_data)
    print(processed_data)
