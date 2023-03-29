import os
from typing import Dict, List

from neo4j import GraphDatabase, Driver

import wikigraph.models as M
import wikigraph.config as C
from wikigraph.logger import get_logger

logger = get_logger(__name__)


def create_connection(settings: C.Settings) -> Driver:
    """
    Create a connection to the Neo4j database.

    Returns:
        Driver: A Neo4j database driver object.
    """
    driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
    logger.debug(f"Created Neo4j database driver {driver}")
    return driver

def insert_persons(driver: Driver, persons: List[M.Person]):
    """
    Insert a list of Member objects into the Neo4j database.

    Args:
        driver (Driver): A Neo4j database driver object.
        persons (List[Person]): A list of Person objects.
    """
    with driver.session() as session:
        logger.debug(f"Writing {len(persons)} to database")
        for person in persons:
            session.write_transaction(create_person, person.uri, person.label)

def insert_relationships(driver: Driver, relationships: List[M.Relationship]):
    """
    Insert a list of Relationship objects into the Neo4j database.

    Args:
        driver (Driver): A Neo4j database driver object.
        relationships (List[Relationship]): A list of Relationship objects.
    """
    with driver.session() as session:
        logger.debug(f"Writing {len(relationships)} relationships to database")
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
    logger.debug(query)
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
    logger.debug(query)
    return tx.run(query, person_uri=person_uri, related_person_uri=related_person_uri, relation_type=relation_type)


if __name__ == "__main__":
    pass
