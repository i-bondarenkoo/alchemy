from app.crud.user import (
    create_user_crud,
    get_user_by_id_crud,
    get_list_users_crud,
    delete_user_crud,
    get_user_with_posts_crud,
    get_user_with_profile_crud,
    get_user_with_posts_and_posts_with_tags_crud,
    update_user_crud,
    get_user_by_id_dep,
)
from app.crud.post import (
    create_post_crud,
    get_post_by_id_crud,
    get_post_with_user_crud,
    add_tag_to_post_crud,
    get_post_with_tags_crud,
)
from app.crud.profile import (
    create_profile_crud,
    get_profile_by_id_crud,
    get_profile_with_user_crud,
)

from app.crud.tag import (
    create_tag_crud,
    get_tag_by_id_crud,
    get_tag_with_posts_crud,
    get_tag_with_posts_and_user_crud,
)
from app.crud.post_tag import create_post_tag_crud
