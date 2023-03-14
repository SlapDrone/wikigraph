import pytest
import typing as ty
from unittest.mock import MagicMock
from src import sparql  # Import the module instead of the function

# Mock the fetch_data function to return a sample result
MEMBERS = [
    'http://www.wikidata.org/entity/Q43067', 'http://www.wikidata.org/entity/Q2571',
    'http://www.wikidata.org/entity/Q28147', 'http://www.wikidata.org/entity/Q41749',
    'http://www.wikidata.org/entity/Q38573', 'http://www.wikidata.org/entity/Q48301',
    'http://www.wikidata.org/entity/Q31793', 'http://www.wikidata.org/entity/Q352',
    'http://www.wikidata.org/entity/Q47906', 'http://www.wikidata.org/entity/Q38302',
    'http://www.wikidata.org/entity/Q28085'
]
# first 5 relationships put in file
RELATIONSHIPS = [
    {'person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q352'}, 'relationship': {'type': 'uri', 'value': 'http://www.wikidata.org/prop/direct/P1038'}, 'related_person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q64799'}, 'personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Adolf Hitler'}, 'related_personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Heinz Hitler'}},
    {'person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q352'}, 'relationship': {'type': 'uri', 'value': 'http://www.wikidata.org/prop/direct/P3373'}, 'related_person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q66225'}, 'personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Adolf Hitler'}, 'related_personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Alois Hitler, Jr.'}},
    {'person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q352'}, 'relationship': {'type': 'uri', 'value': 'http://www.wikidata.org/prop/direct/P451'}, 'related_person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q76106'}, 'personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Adolf Hitler'}, 'related_personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Maria Reiter'}},
    {'person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q352'}, 'relationship': {'type': 'uri', 'value': 'http://www.wikidata.org/prop/direct/P451'}, 'related_person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q76433'}, 'personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Adolf Hitler'}, 'related_personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Eva Braun'}},
    {'person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q352'}, 'relationship': {'type': 'uri', 'value': 'http://www.wikidata.org/prop/direct/P22'}, 'related_person': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q78500'}, 'personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Adolf Hitler'}, 'related_personLabel': {'xml:lang': 'en', 'type': 'literal', 'value': 'Alois Hitler'}}
]

def mock_fetch_data(num_batches: ty.Optional[int] = None, discard_no_relationships: ty.Optional[bool] = None):
    return MEMBERS, RELATIONSHIPS

@pytest.fixture(autouse=True)
def mock_sparql_fetch_data(monkeypatch):
    monkeypatch.setattr(sparql, 'fetch_data', MagicMock(side_effect=mock_fetch_data))  # Use the module and function name as a string

def test_fetch_data():
    members, relationships = sparql.fetch_data()  # Call fetch_data from the imported module
    assert isinstance(members, list)
    assert len(members) > 0
    assert isinstance(relationships, list)
    assert len(relationships) > 0


def test_get_relationships(mock_sparql_fetch_data):
    members = sparql.get_members()
    batch_size = 3
    expected_batches = 2

    batch_iter = 0
    for batch in sparql.get_relationships(members, batch_size=batch_size):
        assert len(batch) <= batch_size
        batch_iter += 1

    assert batch_iter == expected_batches


def test_fetch_data_num_batches(mock_sparql_fetch_data):
    num_batches = 2
    members, relationships = sparql.fetch_data(num_batches=num_batches)

    assert len(members) > 0
    assert len(relationships) > 0
    assert len(relationships) == num_batches * 3  # Assumes each batch has 3 relationships


def test_fetch_data_discard_no_relationships(mock_sparql_fetch_data):
    members, relationships = sparql.fetch_data(num_batches=1, discard_no_relationships=True)

    members_with_relationships = set()
    for relationship in relationships:
        members_with_relationships.add(relationship["person"]["value"])

    assert len(members) == len(members_with_relationships)