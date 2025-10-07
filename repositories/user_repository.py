from sqlalchemy import text, Sequence, Row
from typing import Any

class UserRepository:
    def __init__(self, engine):
        self.engine = engine

    def get_all(self) -> Sequence[Row[Any]]:
        QUERY = text("SELECT * FROM users;")
        with self.engine.connect() as conn:
            result = conn.execute(QUERY).fetchall()

        return result

    def create(
            self,
            username: str,
            role: str,
            created_at: str
        ) -> str | None:
        QUERY_FIND = text("SELECT * FROM users WHERE username = :username")
        with self.engine.connect() as conn:
            result = conn.execute(QUERY_FIND, {
                "username": username
            })

        if result.fetchone() is not None:
            return "user exists"

        QUERY_ADD = text("""
                         INSERT INTO users (username, role, created_at)
                         VALUES (:username, :role, :created_at)
                         """)
        with self.engine.connect() as conn:
            conn.execute(QUERY_ADD, {
                "username": username,
                "role": role,
                "created_at": created_at
            })
            conn.commit()

    def delete(
            self,
            username: str
        ) -> None:
        QUERY = text("""
                     DELETE
                     FROM users
                     WHERE username = :username
                     """)
        with self.engine.connect() as conn:
            conn.execute(QUERY, {
                "username": username
            })
            conn.commit()