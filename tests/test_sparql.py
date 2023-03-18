import pytest
import typing as ty
import json
from unittest.mock import MagicMock

import wikigraph.sparql as S
import wikigraph.models as M


def test_create_persons_query():
    offset = 10
    limit = 5
    query = S.create_persons_query(offset, limit)
    assert f"OFFSET {offset}" in query
    assert f"LIMIT {limit}" in query


def test_build_relationships_query():
    offset = 10
    limit = 5
    members = "wd:Q1 wd:Q2 wd:Q3"
    relationship_types = "wdt:P22 wdt:P25 wdt:P3373"

    query = S.build_relationships_query(offset, limit, members, relationship_types)
    assert f"OFFSET {offset}" in query
    assert f"LIMIT {limit}" in query
    assert f"{{{members}}}" in query
    assert f"{{{relationship_types}}}" in query


def test_execute_query():
    query = S.create_persons_query(0, 1)
    bindings = S.execute_query(query)
    assert isinstance(bindings, list)
    assert len(bindings) == 1


def test_get_persons_offset_limit():
    persons_1 = S.get_persons(0, 2)
    persons_2 = S.get_persons(2, 2)

    assert len(persons_1) == 2
    assert len(persons_2) == 2
    assert persons_1 != persons_2


def test_get_relationships_offset_limit():
    persons = S.get_persons(0, 2)
    relationships_1 = S.get_relationships(0, 1, persons)
    relationships_2 = S.get_relationships(1, 1, persons)

    assert len(relationships_1) == 1
    assert len(relationships_2) == 1
    assert relationships_1 != relationships_2