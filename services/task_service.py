from repositories import TaskRepository
from datetime import datetime

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.repo = task_repository

    def get_tasks_for_user(self, user_id: int):
        return self.repo.get_by_user(user_id)

    def create_task(self, data: dict):
        required = ['task_name', 'user_id', 'status', 'due_date', 'priority']
        if not all(data.get(field) for field in required):
            return False, "Missing required fields"

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.repo.create(
            task_name=data['task_name'],
            user_id=data['user_id'],
            created_at=created_at,
            status=data['status'],
            due_date=data['due_date'],
            priority=data['priority']
        )
        return True, "Task created successfully"

    def update_task(self, update_fields: dict, task_id: int, user_id: int):
        result = self.repo.update(update_fields, task_id, user_id)
        if isinstance(result, str):
            return False, result
        return True, "Task updated successfully"

    def delete_task(self, user_id: int, task_id: int):
        self.repo.delete(user_id, task_id)
        return True, "Task deleted successfully"