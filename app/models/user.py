from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, func
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(35), unique=True)
    email: Mapped[str] = mapped_column(String(35), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
