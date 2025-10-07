from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.orm.relationships import _RelationshipDeclared
from sqlalchemy import INTEGER, VARCHAR, TIMESTAMP
from datetime import datetime
from models import Base
from typing import Any

class Users(Base):
    __tablename__ = "users"
    tasks: _RelationshipDeclared[Any] = relationship("Tasks", back_populates="users")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(64))
    role: Mapped[str] = mapped_column(VARCHAR(32))


    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role}, created_at={self.created_at})>"