from typing import List, Dict
from .sparql import fetch_data

def process_data(data: List[Dict]) -> Dict[str, Dict]:
    graph = {}

    for entry in data:
        person = entry["personLabel"]["value"]
        relation = entry["relationLabel"]["value"]

        if person not in graph:
            graph[person] = {"relations": []}

        graph[person]["relations"].append(relation)

    return graph

if __name__ == "__main__":
    raw_data = fetch_data()
    processed_data = process_data(raw_data)
    print(processed_data)
