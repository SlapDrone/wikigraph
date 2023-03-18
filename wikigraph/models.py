import logging

import pydantic


logger = logging.getLogger(__name__)


class Person(pydantic.BaseModel):
    uri: str = pydantic.Field(alias="person")
    label: str = pydantic.Field(alias="personLabel")


class Relationship(pydantic.BaseModel):
    person_uri: str = pydantic.Field(alias="person")
    person_label: str = pydantic.Field(alias="personLabel")
    related_person_uri: str = pydantic.Field(alias="related_person")
    related_person_label: str = pydantic.Field(alias="related_personLabel")
    relationship: str


def map_to_models(
    query_results: list[dict],
    model: pydantic.BaseModel
) -> list[pydantic.BaseModel]:
    mapped_data = []

    for result in query_results:
        data = {key: value["value"] for key, value in result.items()}
        instance = model(**data)
        mapped_data.append(instance)

    return mapped_data