# Import standard library packages
from datetime import datetime

# Typings, for autocompletion (VS Code with Python plug-in)
from typing import List  # noqa

# Import app code
from app.db.base_class import Base
from app.models.base_relations import users_roles

# Import installed packages
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    # Own properties
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow(), index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    # Relationships
    roles = relationship(
        "Role", secondary=users_roles, back_populates="users"
    )  # type: List[role.Role]
