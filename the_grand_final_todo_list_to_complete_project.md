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
- [ ] Create `config.py`
  - [ ] Add `AppConfig` class
  - [ ] Initialize `engine` in constructor
  - [ ] Initialize `task_repository` with engine
  - [ ] Initialize `user_repository` with engine
  - [ ] Initialize `task_service` with task_repository
  - [ ] Initialize `user_service` with user_repository

## Routes Layer
- [ ] Create `routes/task_routes.py`
  - [ ] Add `create_task_routes(task_service)` factory function
  - [ ] Create Blueprint for `/tasks`
  - [ ] Move `POST /tasks` endpoint
  - [ ] Move `GET /tasks/<user_id>` endpoint
  - [ ] Move `PATCH /tasks/<user_id>/<task_id>` endpoint
  - [ ] Move `DELETE /tasks/<user_id>` endpoint
  - [ ] Update all endpoints to use `task_service`
- [ ] Create `routes/user_routes.py`
  - [ ] Add `create_user_routes(user_service)` factory function
  - [ ] Create Blueprint for `/users`
  - [ ] Move `GET /users` endpoint
  - [ ] Move `POST /users` endpoint
  - [ ] Move `DELETE /users` endpoint
  - [ ] Update all endpoints to use `user_service`
- [ ] Create `routes/__init__.py` - export route factories

## Refactor Main Application
- [ ] Update `app.py`
  - [ ] Import `AppConfig` from `config.py`
  - [ ] Create `create_app()` factory function
  - [ ] Initialize `config = AppConfig()` inside factory
  - [ ] Register task routes blueprint with DI
  - [ ] Register user routes blueprint with DI
  - [ ] Update `if __name__ == "__main__"` block
  - [ ] Remove old global `engine` variable
  - [ ] Remove old route definitions

## Cleanup
- [ ] Delete old `repository.py` file (or keep as backup)
- [ ] Update `db.py` if needed (or move to config)
- [ ] Check all imports are correct
- [ ] Remove unused imports

## Testing & Verification
- [ ] Test `POST /tasks` endpoint
- [ ] Test `GET /tasks/<user_id>` endpoint
- [ ] Test `PATCH /tasks/<user_id>/<task_id>` endpoint
- [ ] Test `DELETE /tasks/<user_id>` endpoint
- [ ] Test `GET /users` endpoint
- [ ] Test `POST /users` endpoint
- [ ] Test `DELETE /users` endpoint
- [ ] Verify database connection works
- [ ] Check error handling works correctly
