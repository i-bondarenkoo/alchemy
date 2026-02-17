from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from app.database.base import Base
from typing import TYPE_CHECKING
from app.models.post_tag import association_table

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.tag import Tag


class Post(Base):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column(String(60))
    body: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=association_table, back_populates="posts"
    )
