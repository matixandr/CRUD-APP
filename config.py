from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from services.task_service import TaskService
from services.user_service import UserService
from db import db_init

from sqlalchemy.engine import Engine

class AppConfig:
    def __init__(self):
        self.engine: Engine = db_init()

        self.task_repository = TaskRepository(self.engine)
        self.user_repository = UserRepository(self.engine)

        self.task_service = TaskService(self.task_repository)
        self.user_service = UserService(self.user_repository)
