from sqlalchemy.orm import declarative_base

from .user import Users
from .task import Tasks

Base = declarative_base()

__all__ = ['Users', 'Tasks']