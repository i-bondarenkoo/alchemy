from pydantic import BaseModel, ConfigDict


class CreatePostSchema(BaseModel):
    user_id: int
    body: str | None = None
    title: str


class ResponsePostSchema(CreatePostSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class ResponsePostSchemaForRelation(BaseModel):
    id: int
    body: str | None = None
    title: str
