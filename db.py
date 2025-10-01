from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped
from sqlalchemy import INTEGER, VARCHAR, TIMESTAMP, DATE, ForeignKey, Engine
from sqlalchemy.orm.relationships import _RelationshipDeclared
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, date
from typing import Any
import sqlalchemy
import dotenv
import os


Base = declarative_base()

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

class Users(Base):
    __tablename__ = "users"
    tasks: _RelationshipDeclared[Any] = relationship("Tasks", back_populates="users")
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    username: Mapped[str] = mapped_column(VARCHAR(64))
    role: Mapped[str] = mapped_column(VARCHAR(32))

def db_init() -> Engine:
    dotenv.load_dotenv()
    print("[LOG] loaded .env file")

    USERNAME = os.getenv("POSTGRES_USERNAME")
    PASSWORD = os.getenv("POSTGRES_PASSWD")
    SERVER = os.getenv("POSTGRES_SERVER")
    PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB_NAME")

    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}")
    print("[LOG] created engine (auth successful")

    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table('users'):
        Users.__table__.create(engine)
        print("[LOG] Table Users does not exist, creating it...")

    if not inspector.has_table('tasks'):
        Tasks.__table__.create(engine)
        print("[LOG] Table Tasks does not exist, creating it...")

    return engine