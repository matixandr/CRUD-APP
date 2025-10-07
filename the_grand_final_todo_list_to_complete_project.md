## Project Structure Setup
- [x] ~~Create `models/` directory~~
- [x] ~~Create `repositories/` directory~~  
- [x] ~~Create `services/` directory~~
- [x] ~~Create `routes/` directory~~
- [x] ~~Add `__init__.py` files to all new directories~~

## Models Layer
- [x] ~~Create `models/task.py` - move `Tasks` class from `db.py`~~
- [x] ~~Create `models/user.py` - move `Users` class from `db.py`~~
- [x] ~~Create `models/__init__.py` - export both models~~
- [x] ~~Update imports in other files~~

## Repository Layer
- [x] ~~Create `repositories/task_repository.py`~~
  - [x] ~~Add `TaskRepository` class with `__init__(self, engine)`~~
  - [x] ~~Move `task_post_executor` → `create()` method~~
  - [x] ~~Move `task_get_executor` → `get_by_user()` method~~
  - [x] ~~Move `task_patch_executor` → `update()` method~~
  - [x] ~~Move `task_delete_executor` → `delete()` method~~
- [x] ~~Create `repositories/user_repository.py`~~
  - [x] ~~Add `UserRepository` class with `__init__(self, engine)`~~
  - [x] ~~Move `users_get_executor` → `get_all()` method~~
  - [x] ~~Move `users_post_executor` → `create()` method~~
  - [x] ~~Move `users_delete_executor` → `delete()` method~~
- [x] ~~Create `repositories/__init__.py` - export both repositories~~

## Service Layer
- [x] ~~Create `services/task_service.py`~~
  - [x] ~~Add `TaskService` class with `__init__(self, task_repository)`~~
  - [x] ~~Add `create_task(data)` method with validation~~
  - [x] ~~Add `get_user_tasks(user_id)` method~~
  - [x] ~~Add `update_task(update_fields, task_id, user_id)` method~~
  - [x] ~~Add `delete_task(user_id, task_id)` method~~
- [x] ~~Create `services/user_service.py`~~
  - [x] ~~Add `UserService` class with `__init__(self, user_repository)`~~
  - [x] ~~Add `get_all_users()` method~~
  - [x] ~~Add `create_user(data)` method with validation~~
  - [x] ~~Add `delete_user(username)` method~~
- [x] ~~Create `services/__init__.py` - export both services~~

## Dependency Injection Container
- [x] ~~Create `config.py`~~
  - [x] ~~Add `AppConfig` class~~
  - [x] ~~Initialize `engine` in constructor~~
  - [x] ~~Initialize `task_repository` with engine~~
  - [x] ~~Initialize `user_repository` with engine~~
  - [x] ~~Initialize `task_service` with task_repository~~
  - [x] ~~Initialize `user_service` with user_repository~~

## Routes Layer
- [x] ~~Create `routes/task_routes.py`~~
  - [x] ~~Add `create_task_routes(task_service)` factory function~~
  - [x] ~~Create Blueprint for `/tasks`~~
  - [x] ~~Move `POST /tasks` endpoint~~
  - [x] ~~Move `GET /tasks/<user_id>` endpoint~~
  - [x] ~~Move `PATCH /tasks/<user_id>/<task_id>` endpoint~~
  - [x] ~~Move `DELETE /tasks/<user_id>` endpoint~~
  - [x] ~~Update all endpoints to use `task_service`~~
- [x] ~~Create `routes/user_routes.py`~~
  - [x] ~~Add `create_user_routes(user_service)` factory function~~
  - [x] ~~Create Blueprint for `/users`~~
  - [x] ~~Move `GET /users` endpoint~~
  - [x] ~~Move `POST /users` endpoint~~
  - [x] ~~Move `DELETE /users` endpoint~~
  - [x] ~~Update all endpoints to use `user_service`~~
- [x] ~~Create `routes/__init__.py` - export route factories~~

## Refactor Main Application
- [x] ~~Update `app.py`~~
  - [x] ~~Import `AppConfig` from `config.py`~~
  - [x] ~~Create `create_app()` factory function~~
  - [x] ~~Initialize `config = AppConfig()` inside factory~~
  - [x] ~~Register task routes blueprint with DI~~
  - [x] ~~Register user routes blueprint with DI~~
  - [x] ~~Update `if __name__ == "__main__"` block~~
  - [x] ~~Remove old global `engine` variable~~
  - [x] ~~Remove old route definitions~~

## Cleanup
- [x] ~~Delete old `repository.py` file (or keep as backup)~~
- [x] ~~Update `db.py` if needed (or move to config)~~
- [x] ~~Check all imports are correct~~
- [x] ~~Remove unused imports~~

## Testing & Verification
- [x] ~~Test `POST /tasks` endpoint~~
- [x] ~~Test `GET /tasks/<user_id>` endpoint~~
- [x] ~~Test `PATCH /tasks/<user_id>/<task_id>` endpoint~~
- [x] ~~Test `DELETE /tasks/<user_id>` endpoint~~
- [x] ~~Test `GET /users` endpoint~~
- [x] ~~Test `POST /users` endpoint~~
- [x] ~~Test `DELETE /users` endpoint~~
- [x] ~~Verify database connection works~~
- [x] ~~Check error handling works correctly~~
