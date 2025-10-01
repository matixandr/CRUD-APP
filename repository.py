from sqlalchemy.engine import Engine
from typing import LiteralString
from sqlalchemy import text

def task_post_executor(
        engine: Engine,
        task_name: str,
        user_id: int,
        created_at: str,
        status: str,
        due_date: str,
        priority: str
    ):
    ADD_TO_TASK = text(
    """
        INSERT INTO tasks (task_name, user_id, created_at, status, due_date, priority)
        VALUES (:task_name, :user_id, :created_at, :status, :due_date, :priority)
    """)

    with engine.connect() as conn:
        conn.execute(ADD_TO_TASK, {
            "task_name": task_name,
            "user_id": user_id,
            "created_at": created_at,
            "status": status,
            "due_date": due_date,
            "priority": priority
        })
        conn.commit()

def task_get_executor(
        engine: Engine,
        user_id: int
    ):
    QUERY = text('SELECT * FROM tasks WHERE user_id = :user_id;')
    with engine.connect() as conn:
        result = conn.execute(QUERY, {"user_id": user_id}).fetchall()

    return result

def task_delete_executor(
        engine: Engine,
        user_id: int,
        task_id: int
    ):
    QUERY = text(f"DELETE FROM tasks WHERE user_id = :user_id AND task_id = :task_id")
    with engine.connect() as conn:
        conn.execute(QUERY, {
            "user_id": user_id,
            "task_id": task_id
        })
        conn.commit()

def task_patch_executor(
        engine: Engine,
        clause: LiteralString,
        task_id: int,
        user_id: int
    ):
    QUERY = text(f"UPDATE tasks SET {clause} WHERE task_id = :task_id AND user_id = :user_id")

    with engine.connect() as conn:
        conn.execute(QUERY, {
            "task_id": task_id,
            "user_id": user_id
        })
        conn.commit()