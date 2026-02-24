from sqlalchemy import String
from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models.post_tag import association_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # from app.models.post import Post
    from app.models.post_tag import PostTag


class Tag(Base):
    __tablename__ = "tags"
    name: Mapped[str] = mapped_column(String(25), unique=True)
    color: Mapped[str | None]

    # posts: Mapped[list["Post"]] = relationship(
    #     "Post", secondary=association_table, back_populates="tags"
    # )
    posts: Mapped[list["PostTag"]] = relationship(
        "PostTag", cascade="all, delete-orphan", back_populates="tag"
    )
