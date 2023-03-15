import pytest
from wikigraph.neo4j_utils import create_connection, get_all_people

@pytest.fixture
def driver():
    return create_connection()

def test_get_all_people(driver):
    people = get_all_people(driver)
    assert isinstance(people, list)
    assert len(people) >= 0
