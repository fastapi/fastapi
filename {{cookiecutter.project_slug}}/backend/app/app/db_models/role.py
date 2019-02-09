# Import standard library packages
from datetime import datetime

# Import app code
from app.db.base_class import Base
from app.models.base_relations import users_roles

# Import installed packages
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class Role(Base):
    # Own properties
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow(), index=True)
    name = Column(String, index=True)
    # Relationships
    users = relationship("User", secondary=users_roles, back_populates="roles")
