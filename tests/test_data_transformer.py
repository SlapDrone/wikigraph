import pytest
from src.data_transformer import process_data

def test_process_data():
    sample_data = [
        {
            "personLabel": {"value": "Person A"},
            "relationLabel": {"value": "Relation X"},
        },
        {
            "personLabel": {"value": "Person A"},
            "relationLabel": {"value": "Relation Y"},
        },
        {
            "personLabel": {"value": "Person B"},
            "relationLabel": {"value": "Relation X"},
        },
    ]

    processed_data = process_data(sample_data)
    assert isinstance(processed_data, dict)
    assert len(processed_data) == 2

    assert "Person A" in processed_data
    assert "Person B" in processed_data

    assert processed_data["Person A"]["relations"] == ["Relation X", "Relation Y"]
    assert processed_data["Person B"]["relations"] == ["Relation X"]
