from pydantic import Tag
from sqlalchemy import ForeignKey, Table, Column, Integer, func, UniqueConstraint
from app.database.base import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.tag import Tag
# association_table = Table(
#     "post_tag_table",
#     Base.metadata,
#     Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
#     Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
# )


class PostTag(Base):
    __tablename__ = "post_tags"
    __table_args__ = (UniqueConstraint("post_id", "tag_id"),)
    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
    )
    tag_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    post: Mapped["Post"] = relationship("Post", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="posts")
