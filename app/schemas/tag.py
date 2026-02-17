from pydantic import BaseModel, ConfigDict


class CreateTagSchema(BaseModel):
    name: str
    color: str | None = None


class ResponseTagSchema(CreateTagSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResponseTagForRelationship(CreateTagSchema):
    model_config = ConfigDict(from_attributes=True)
