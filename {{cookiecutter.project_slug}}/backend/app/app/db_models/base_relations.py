# Import installed packages
# Import app code
from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)
