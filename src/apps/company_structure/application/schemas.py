import uuid

from pydantic import BaseModel, ConfigDict, alias_generators


class DepartmentSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
        serialize_by_alias=True,
    )

    id: uuid.UUID
    title: str
    parent_id: uuid.UUID | None
