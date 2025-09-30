import os

from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP, DATE
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base
import sqlalchemy
import dotenv

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(INTEGER, primary_key=True)
    task_name = Column(VARCHAR(128))
    user_id = Column(INTEGER)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(
        ENUM(
            'pending',
            'in-progress',
            'completed',
            name="status_enum",
            create_type=True),
        nullable=False,
        default='pending'
    )
    due_date = Column(DATE)
    priority = Column(
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
    id = Column(INTEGER, primary_key=True)
    username = Column(VARCHAR(64))
    role = Column(VARCHAR(32))
    created_at = Column(TIMESTAMP)

dotenv.load_dotenv()
USERNAME = os.getenv("POSTGRES_USERNAME")
PASSWORD = os.getenv("POSTGRES_PASSWD")
SERVER = os.getenv("POSTGRES_SERVER")
PORT = os.getenv("POSTGRES_ENV")
DB_NAME = os.getenv("POSTGRES_DB_NAME")

engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}" )
inspector = sqlalchemy.inspect(engine)

if not inspector.has_table('users'):
    Users.__table__.create(engine)
    print("[LOG] Table Users does not exist, creating it...")

if not inspector.has_table('tasks'):
    Tasks.__table__.create(engine)
    print("[LOG] Table Tasks does not exist, creating it...")
