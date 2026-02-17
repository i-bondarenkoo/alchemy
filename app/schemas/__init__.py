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
    ResponsePostWithTags,
)
from app.schemas.profile import (
    CreateProfileSchema,
    ResponseProfileRelationForUser,
    ResponseProfileSchema,
    ResponseProfileWithUser,
)
from app.schemas.tag import (
    CreateTagSchema,
    ResponseTagSchema,
    ResponseTagForRelationship,
)

ResponseUserSchemaWithPosts.model_rebuild()
ResponseUserSchemaWithProfiles.model_rebuild()
ResponsePostWithUser.model_rebuild()
ResponseProfileWithUser.model_rebuild()
ResponsePostWithTags.model_rebuild()
