from sqlalchemy import Column, INTEGER, VARCHAR, TIMESTAMP, DATE, ForeignKey, Engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ENUM
import sqlalchemy
import dotenv
import os

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(INTEGER, primary_key=True, autoincrement=True)
    users = relationship("Users", back_populates="tasks")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    user_id = Column(INTEGER, ForeignKey('users.id'))
    task_name = Column(VARCHAR(128))
    due_date = Column(DATE)
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
    tasks = relationship("Tasks", back_populates="users")
    id = Column(INTEGER, primary_key=True)
    created_at = Column(TIMESTAMP)
    username = Column(VARCHAR(64))
    role = Column(VARCHAR(32))

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