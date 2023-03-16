import json
import sys
import time
import typing as ty
from SPARQLWrapper import SPARQLWrapper, JSON

import wikigraph.models as M

wikidata_endpoint = "https://query.wikidata.org/sparql"
sparql = SPARQLWrapper(wikidata_endpoint)
sparql.setReturnFormat(JSON)

# Query to get the Nazi Party members
members_query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?personLabel
WHERE {
  ?person wdt:P31/wdt:P279* wd:Q5 .  # Instance of human or subclass of human
  ?person wdt:P102 wd:Q7320 .  # Member of: Nazi Party
  ?person rdfs:label ?personLabel .
  FILTER (LANG(?personLabel) = "en").
}
LIMIT 100
"""

# Query to get the family relationships of Nazi Party members
relationship_types = [
    "P40",   # Child
    "P22",   # Father
    "P25",   # Mother
    "P3373", # Sibling
    "P1038", # Relative
    "P1037", # Employer
    "P106",  # Occupation
    "P108",  # Employer
    "P1347", # Participant of
    "P551",  # Residence
    "P1313", # Position held
    "P1026", # Diplomatic relation
    "P1441", # Present in work
    "P1269", # Facet of
    "P451"  # Romantic partner
]

# {{wdt:P40 wdt:P22 wdt:P25 wdt:P3373 wdt:P1038}}
relationships_query_template = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?personLabel ?related_person ?related_personLabel ?relationship
WHERE {{
  VALUES ?person {{{members}}}
  ?person wdt:P31/wdt:P279* wd:Q5 .  # Instance of human or subclass of human
  ?person rdfs:label ?personLabel .
  FILTER (LANG(?personLabel) = "en").
  
  VALUES ?relationship {{{relationship_types}}}  # Family relationship properties
  ?person ?relationship ?related_person . 
  ?related_person wdt:P31/wdt:P279* wd:Q5 .  # Instance of human or subclass of human
  ?related_person rdfs:label ?related_personLabel .
  FILTER (LANG(?related_personLabel) = "en").
}}
"""

def get_members() -> list[M.Member]:
    sparql.setQuery(members_query)
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    return M.map_to_models(bindings, M.Member)


def get_relationships(
    members: list[M.Member],
    relationship_types=relationship_types
) -> list[M.Relationship]:
    member_values = " ".join(f"wd:{member.uri.split('/')[-1]}" for member in members)
    relationship_values = " ".join([f"wdt:{r}" for r in relationship_types])
    relationships_query = relationships_query_template.format(
        members=member_values,
        relationship_types=relationship_values
    )
    sparql.setQuery(relationships_query)
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    print(bindings[:2])
    return M.map_to_models(bindings, M.Relationship)


def fetch_relationships_in_batches(
    members: list[M.Member],
    batch_size: int = 10,
    relationship_types=relationship_types
) -> list[M.Relationship]:
    all_relationships = []

    for i in range(0, len(members), batch_size):
        batch = members[i:i + batch_size]
        batch_relationships = get_relationships(batch, relationship_types)
        all_relationships.extend(batch_relationships)

    return all_relationships


# def fetch_data(num_batches=1, discard_no_relationships=True):
#     members_data = get_members()
#     relationships = []

#     # Fetch the specified number of batches
#     batch_iter = 0
#     members = [uri for uri, _ in members_data]
#     for batch in get_relationships(members, batch_size=10):
#         relationships.extend(batch)
#         time.sleep(1)  # Add a delay to avoid overloading the endpoint
#         batch_iter += 1
#         if batch_iter >= num_batches:
#             break

#     if discard_no_relationships:
#         # Keep only members with relationships
#         members_with_relationships = set()
#         for relationship in relationships:
#             members_with_relationships.add(relationship["person"]["value"])
#         members_data = [(uri, attrs) for uri, attrs in members_data if uri in members_with_relationships]

#     members = {uri: attrs for uri, attrs in members_data}

#     return members, relationships


if __name__ == "__main__":
    m = get_members()
    r = get_relationships(m[:10])
    print(m)
    print(r)
    pass
    # m, r = fetch_data()
    # print(m)
    # members_discard, relationships_discard = fetch_data(num_batches=3, discard_no_relationships=True)
    # print(f"{len(members_discard)} MEMBERS (discard)")
    # print(members_discard)
    # print(f"{len(relationships_discard)} RELATIONSHIPS (discard):")
    # print(relationships_discard)

    # members, relationships = fetch_data(num_batches=3, discard_no_relationships=False)
    # print(f"{len(members)} MEMBERS")
    # print(members)
    # print(f"{len(relationships)} RELATIONSHIPS:")
    # print(relationships)
    
    # with open("./test_members_discard.json", "w") as fp:
    #     fp.write(json.dumps(members_discard))
    # with open("./test_relationships_discard.json", "w") as fp:
    #     fp.write(json.dumps(relationships_discard))

    # with open("./test_members.json", "w") as fp:
    #     fp.write(json.dumps(members))
    # with open("./test_relationships.json", "w") as fp:
    #     fp.write(json.dumps(relationships))
    # Process and store the relationships data as required

