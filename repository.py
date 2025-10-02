from sqlalchemy import text, Sequence, Row
from sqlalchemy.engine import Engine
from typing import Any

def task_post_executor(
        engine: Engine,
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
    ) -> Sequence[Row[Any]]:
    QUERY = text('SELECT * FROM tasks WHERE user_id = :user_id;')
    with engine.connect() as conn:
        result = conn.execute(QUERY, {"user_id": user_id}).fetchall()

    return result

def task_delete_executor(
        engine: Engine,
        user_id: int,
        task_id: int
    ) -> None:
    QUERY = text(f"DELETE FROM tasks WHERE user_id = :user_id AND task_id = :task_id")
    with engine.connect() as conn:
        conn.execute(QUERY, {
            "user_id": user_id,
            "task_id": task_id
        })
        conn.commit()

def task_patch_executor(
        engine: Engine,
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

    with engine.connect() as conn:
        conn.execute(QUERY, params)
        conn.commit()

def users_get_executor(engine: Engine) -> Sequence[Row[Any]]:
    QUERY = text("SELECT * FROM users;")
    with engine.connect() as conn:
        result = conn.execute(QUERY).fetchall()

    return result

def users_post_executor(
        engine: Engine,
        username: str,
        role: str,
        created_at: str
    ) -> str | None:
    QUERY_FIND = text("SELECT * FROM users WHERE username = :username")
    with engine.connect() as conn:
        result = conn.execute(QUERY_FIND, {
            "username": username
        })

    if result:
        return "user exists"

    QUERY_ADD = text("""
     INSERT INTO users (username, role, created_at) 
     VALUES (:username, :role, :created_at)
     """)
    with engine.connect() as conn:
        conn.execute(QUERY_ADD, {
            "username": username,
            "role": role,
            "created_at": created_at
        })
        conn.commit()

def users_delete_executor(
        engine: Engine,
        username: str
    ) -> None:
    QUERY = text("""
        DELETE FROM users WHERE username = :username
    """)
    with engine.connect() as conn:
        conn.execute(QUERY, {
            "username": username
        })
        conn.commit()