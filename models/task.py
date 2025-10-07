from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR, TIMESTAMP, DATE, ForeignKey
from sqlalchemy.orm.relationships import _RelationshipDeclared
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, date
from models import Base
from typing import Any

class Tasks(Base):
    __tablename__ = "tasks"
    users: _RelationshipDeclared[Any] = relationship("Users", back_populates="tasks")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    task_id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(INTEGER, ForeignKey('users.id'))
    task_name: Mapped[str] = mapped_column(VARCHAR(128))
    due_date: Mapped[date] = mapped_column(DATE)
    status = mapped_column(
        ENUM(
            'pending',
            'in-progress',
            'completed',
            name="status_enum",
            create_type=True),
        nullable=False,
        default='pending'
    )
    priority = mapped_column(
        ENUM(
            'low',
            'medium',
            'high',
            name="priority_enum",
            create_type=True),
        nullable=False,
        default='medium'
    )

    def __repr__(self):
        return (
            f"<Task(id={self.task_id}, name={self.task_name}, user_id={self.user_id}, "
            f"status={self.status}, due_date={self.due_date}, priority={self.priority})>"
        )