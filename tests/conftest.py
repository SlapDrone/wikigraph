import json
import pytest


@pytest.fixture(scope="session")
def test_data():
    data = {}
    files = {
        "members_no_discard": "test_members.json",
        "members_discard_no_relationships" : "test_members_discard.json",
        "relationships_discard_no_relationships": "test_relationships_discard.json",
        "relationships_no_discard": "test_relationships.json",
    }
    for key, filename in files.items():
        with open(f"tests/test_data/{filename}", "r") as f:
            data[key] = json.load(f)
    return data
