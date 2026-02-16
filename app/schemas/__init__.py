from app.schemas.user import (
    CreateUserSchema,
    ResponseUserSchema,
    ResponseUserSchemaWithPosts,
    ResponseUserSchemaWithProfiles,
    ResponseUserForOtherRelationship,
)
from app.schemas.post import (
    CreatePostSchema,
    ResponsePostSchema,
    ResponsePostSchemaForRelation,
    ResponsePostWithUser,
)
from app.schemas.profile import (
    CreateProfileSchema,
    ResponseProfileRelationForUser,
    ResponseProfileSchema,
    ResponseProfileWithUser,
)

ResponseUserSchemaWithPosts.model_rebuild()
ResponseUserSchemaWithProfiles.model_rebuild()
ResponsePostWithUser.model_rebuild()
ResponseProfileWithUser.model_rebuild()
