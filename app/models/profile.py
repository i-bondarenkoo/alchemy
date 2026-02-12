from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Profile(Base):
    __tablename__ = "profiles"
    first_name: Mapped[str | None] = mapped_column(String(35))
    last_name: Mapped[str | None] = mapped_column(String(35))
    bio: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped["User"] = relationship("User", back_populates="profile")
