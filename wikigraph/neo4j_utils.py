from neo4j import GraphDatabase, Driver
from typing import Dict, List
import os

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "testpassword")

def create_connection():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return driver

def insert_data(driver: Driver, data: Dict[str, Dict]):
    with driver.session() as session:
        for uri, info in data.items():
            print("*" * 50)
            print(uri, info)
            session.write_transaction(create_person, uri, info["personLabel"])

            for relation in info["relations"]:
                session.write_transaction(create_relation, uri, relation)

def create_person(tx, uri, label):
    query = "MERGE (p:Person {uri: $uri, name: $label}) RETURN p"
    return tx.run(query, uri=uri, label=label)

def create_relation(tx, person_uri, relation):
    query = """
    MATCH (p:Person {uri: $person_uri})
    MERGE (p)-[:HAS_RELATION {type: $relation}]->(:Relation {type: $relation})
    """
    return tx.run(query, person_uri=person_uri, relation=relation)


def get_all_people(driver: Driver) -> List[str]:
    with driver.session() as session:
        result = session.read_transaction(fetch_all_people)
        people = [record["name"] for record in result]
        return people

def fetch_all_people(tx):
    query = "MATCH (p:Person) RETURN p.name as name"
    return tx.run(query)

if __name__ == "__main__":
    print("NEO4J_URI", NEO4J_URI)
    driver = create_connection()
    print("All people in the database:")
    print(get_all_people(driver))
