import pytest
import typing as ty
import json
from unittest.mock import MagicMock
from wikigraph import sparql  # Import the module instead of the function


# def mock_fetch_data(
#     num_batches: int = 3,
#     discard_no_relationships = True,
# ):
#     if num_batches != 3:
#         raise NotImplementedError
#     if discard_no_relationships:
#         return test_data["members_discard_no_relationships"], test_data["relationships_discard_no_relationships"]
#     else:
#         return test_data["members_no_discard"], test_data["relationships_no_discard"]


# @pytest.fixture(autouse=True)
# def mock_sparql_fetch_data(monkeypatch):
#     monkeypatch.setattr(sparql, 'fetch_data', MagicMock(side_effect=mock_fetch_data))  # Use the module and function name as a string


# def test_fetch_data():
#     members, relationships = sparql.fetch_data()  # Call fetch_data from the imported module
#     assert isinstance(members, list)
#     assert len(members) > 0
#     assert isinstance(relationships, list)
#     assert len(relationships) > 0


# def test_get_relationships(mock_sparql_fetch_data):
#     members = sparql.get_members()
#     batch_size = 3
#     expected_batches = 2

#     batch_iter = 0
#     for batch in sparql.get_relationships(members, batch_size=batch_size):
#         assert len(batch) <= batch_size
#         batch_iter += 1

#     assert batch_iter == expected_batches
# # ... (other imports) ...

# Wikipedia editing changes this... need to figure out a sensible way to mock without trivialising these tests
# def test_fetch_data_no_discard(test_data):
#     # Use the test_data fixture to load the expected data from JSON files
#     expected_members = test_data["members_no_discard"]
#     expected_relationships = test_data["relationships_no_discard"]

#     members, relationships = sparql.fetch_data(num_batches=3, discard_no_relationships=False)

#     assert len(members) == len(expected_members)
#     assert len(relationships) == len(expected_relationships)


# def test_fetch_data_discard_no_relationships(test_data):
#     # Use the test_data fixture to load the expected data from JSON files
#     expected_members = test_data["members_discard_no_relationships"]
#     expected_relationships = test_data["relationships_discard_no_relationships"]

#     members, relationships = sparql.fetch_data(num_batches=3, discard_no_relationships=True)

#     assert len(members) == len(expected_members)
#     assert len(relationships) == len(expected_relationships)

    # Check that all members have at least one relationship
#    members_with_relationships = set()
#    for relationship in relationships:
#        members_with_relationships.add(relationship["person"]["value"])

#   assert len(members) == len(members_with_relationships)


def test_data_consistency(test_data):
    # the number of relationships should be the same because we discard members only
    assert len(test_data["relationships_discard_no_relationships"]) == len(test_data["relationships_no_discard"])
    # the number of members discarding those with no relationships should be less than without discard
    assert len(test_data["members_discard_no_relationships"]) < len(test_data["members_no_discard"])
