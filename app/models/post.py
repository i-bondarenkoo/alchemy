from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from app.database.base import Base


class Post(Base):
    __tablename__ = "posts"
    title: Mapped[str] = mapped_column(String(60))
    body: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
