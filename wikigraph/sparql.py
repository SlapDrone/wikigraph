import json
import logging
import sys
import time
import typing as ty
from SPARQLWrapper import SPARQLWrapper, JSON

import wikigraph.models as M


logger = logging.getLogger(__name__)

wikidata_endpoint = "https://query.wikidata.org/sparql"
sparql = SPARQLWrapper(wikidata_endpoint)
sparql.setReturnFormat(JSON)


# Query to get the Nazi Party members
def create_persons_query(offset: int, limit: int) -> str:
    """
    Builds a SPARQL query string to get the `offset`-th to the (`offset` + `limit`)-th person
    """
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?person ?personLabel
    WHERE {{
      ?person wdt:P31/wdt:P279* wd:Q5 .  # Instance of human or subclass of human
      ?person wdt:P102 wd:Q7320 .  # Member of: Nazi Party
      ?person rdfs:label ?personLabel .
      FILTER (LANG(?personLabel) = "en").
    }}
    OFFSET {offset}
    LIMIT {limit}
    """
    return query


# {{wdt:P40 wdt:P22 wdt:P25 wdt:P3373 wdt:P1038}}
def build_relationships_query(
    offset: int,
    limit: int,
    persons_clause: str,
    relationships_clause: str
) -> str:
    return f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?person ?personLabel ?related_person ?related_personLabel ?relationship
    WHERE {{
      VALUES ?person {{{persons}}}
      ?person wdt:P31/wdt:P279* wd:Q5 .  # Instance of human or subclass of human
      ?person rdfs:label ?personLabel .
      FILTER (LANG(?personLabel) = "en").

      VALUES ?relationship {{{relationships}}}  # Family relationship properties
      ?person ?relationship ?related_person . 
      ?related_person wdt:P31/wdt:P279* wd:Q5 .  # Instance of human or subclass of human
      ?related_person rdfs:label ?related_personLabel .
      FILTER (LANG(?related_personLabel) = "en").
    }}
    OFFSET {offset}
    LIMIT {limit}
    """


def execute_query(query: str) -> list[dict]:
    sparql.setQuery(query)
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    return bindings


def get_persons(offset: int, limit: int) -> list[M.Person]:
    query = create_persons_query(offset, limit)
    bindings = execute_query(query)
    return M.map_to_models(bindings, M.Person)


def get_relationships(
    offset: int,
    limit: int,
    persons: list[M.Person],
    relationships: list[str]
) -> list[M.Relationship]:
    persons_clause = " ".join(f"wd:{member.uri.split('/')[-1]}" for member in members)
    relationships_clause = " ".join([f"wdt:{r}" for r in relationship_types])
    query = build_relationships_query(offset, limit, persons_clause, relationships_clause)
    bindings = execute_query(query)
    return M.map_to_models(bindings, M.Relationship)



if __name__ == "__main__":
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

