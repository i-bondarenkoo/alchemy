from sqlalchemy import String
from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Tag(Base):
    __tablename__ = "tags"
    name: Mapped[str] = mapped_column(String(25), unique=True)
    color: Mapped[str | None]
