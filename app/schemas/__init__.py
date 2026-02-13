from app.schemas.user import (
    CreateUserSchema,
    ResponseUserSchema,
    ResponseUserSchemaWithPosts,
)
from app.schemas.post import (
    CreatePostSchema,
    ResponsePostSchema,
    ResponsePostSchemaForRelation,
)
from app.schemas.profile import CreateProfileSchema

ResponseUserSchemaWithPosts.model_rebuild()
