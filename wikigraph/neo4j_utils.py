import os
from typing import Dict, List

from neo4j import GraphDatabase, Driver

import wikigraph.models as M


NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "testpassword")


def create_connection() -> Driver:
    """
    Create a connection to the Neo4j database.

    Returns:
        Driver: A Neo4j database driver object.
    """
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return driver

def insert_members(driver: Driver, members: List[Member]):
    """
    Insert a list of Member objects into the Neo4j database.

    Args:
        driver (Driver): A Neo4j database driver object.
        members (List[Member]): A list of Member objects.
    """
    with driver.session() as session:
        for member in members:
            session.write_transaction(create_person, member.uri, member.label)

def insert_relationships(driver: Driver, relationships: List[Relationship]):
    """
    Insert a list of Relationship objects into the Neo4j database.

    Args:
        driver (Driver): A Neo4j database driver object.
        relationships (List[Relationship]): A list of Relationship objects.
    """
    with driver.session() as session:
        for relationship in relationships:
            session.write_transaction(
                create_relation,
                relationship.person,
                relationship.related_person,
                relationship.relationship
            )

def create_person(tx, uri: str, label: str):
    """
    Create a Person node in the Neo4j database.

    Args:
        tx: A transaction object.
        uri (str): The URI of the person.
        label (str): The name of the person.
    """
    query = "MERGE (p:Person {uri: $uri, name: $label}) RETURN p"
    return tx.run(query, uri=uri, label=label)

def create_relation(tx, person_uri: str, related_person_uri: str, relation_type: str):
    """
    Create a relationship between two Person nodes in the Neo4j database.

    Args:
        tx: A transaction object.
        person_uri (str): The URI of the person.
        related_person_uri (str): The URI of the related person.
        relation_type (str): The type of relationship between the two nodes.
    """
    query = """
    MATCH (p:Person {uri: $person_uri})
    MATCH (r:Person {uri: $related_person_uri})
    MERGE (p)-[:HAS_RELATION {type: $relation_type}]->(r)
    """
    return tx.run(query, person_uri=person_uri, related_person_uri=related_person_uri, relation_type=relation_type)


if __name__ == "__main__":
    print("NEO4J_URI", NEO4J_URI)
    driver = create_connection()
    print("All people in the database:")
    print(get_all_people(driver))
