from sqlalchemy import text, Sequence, Row
from typing import Any

class TaskRepository:
    def __init__(self, engine):
        self.engine = engine

    def create(
            self,
            task_name: str,
            user_id: int,
            created_at: str,
            status: str,
            due_date: str,
            priority: str
        ) -> None:
        ADD_TO_TASK = text(
            """
            INSERT INTO tasks (task_name, user_id, created_at, status, due_date, priority)
            VALUES (:task_name, :user_id, :created_at, :status, :due_date, :priority)
            """)

        with self.engine.connect() as conn:
            conn.execute(ADD_TO_TASK, {
                "task_name": task_name,
                "user_id": user_id,
                "created_at": created_at,
                "status": status,
                "due_date": due_date,
                "priority": priority
            })
            conn.commit()

    def get_by_user(
            self,
            user_id: int
        ) -> Sequence[Row[Any]]:
        QUERY = text('SELECT * FROM tasks WHERE user_id = :user_id;')
        with self.engine.connect() as conn:
            result = conn.execute(QUERY, {"user_id": user_id}).fetchall()

        return result

    def update(
            self,
            update_fields: dict,
            task_id: int,
            user_id: int
        ) -> str | None:
        ALLOWED_FIELDS = {'task_name', 'due_date', 'priority', 'status'}
        safe_fields = {k: v for k, v in update_fields.items() if k in ALLOWED_FIELDS}

        if not safe_fields:
            return "nice try with that sql injection"

        set_clauses = [f"{field} = :{field}" for field in safe_fields.keys()]
        set_clause = ", ".join(set_clauses)

        QUERY = text(f"UPDATE tasks SET {set_clause} WHERE task_id = :task_id AND user_id = :user_id")

        params = {**safe_fields, "task_id": task_id, "user_id": user_id}

        with self.engine.connect() as conn:
            conn.execute(QUERY, params)
            conn.commit()

    def delete(
            self,
            user_id: int,
            task_id: int
        ) -> None:
        QUERY = text(f"DELETE FROM tasks WHERE user_id = :user_id AND task_id = :task_id")
        with self.engine.connect() as conn:
            conn.execute(QUERY, {
                "user_id": user_id,
                "task_id": task_id
            })
            conn.commit()