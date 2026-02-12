from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String


class Profile(Base):
    __tablename__ = "profiles"
    first_name: Mapped[str | None] = mapped_column(String(35))
    last_name: Mapped[str | None] = mapped_column(String(35))
    bio: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
