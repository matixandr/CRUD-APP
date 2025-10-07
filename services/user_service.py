from repositories import UserRepository
from datetime import datetime

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.ur = user_repository

    def get_all_users(self):
        return self.ur.get_all()

    def create_user(self, data: dict):
        if not data.get("username") or not data.get("role"):
            return False, "Missing required fields"

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = self.ur.create(
            username=data["username"],
            role=data["role"],
            created_at=created_at
        )
        if result == "user exists":
            return False, "User already exists"
        return True, "User created successfully"

    def delete_user(self, username: str):
        if not username:
            return False, "Username is required"
        self.ur.delete(username)
        return True, "User deleted successfully"