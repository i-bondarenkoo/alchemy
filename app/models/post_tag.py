from sqlalchemy import ForeignKey, Table, Column, Integer
from app.database.base import Base

association_table = Table(
    "post_tag_table",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
