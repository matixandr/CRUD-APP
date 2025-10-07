## Project Structure Setup
- [x] Create `models/` directory
- [x] Create `repositories/` directory  
- [x] Create `services/` directory
- [x] Create `routes/` directory
- [x] Add `__init__.py` files to all new directories

## Models Layer
- [ ] Create `models/task.py` - move `Tasks` class from `db.py`
- [ ] Create `models/user.py` - move `Users` class from `db.py`
- [ ] Create `models/__init__.py` - export both models
- [ ] Update imports in other files

## Repository Layer
- [ ] Create `repositories/task_repository.py`
  - [ ] Add `TaskRepository` class with `__init__(self, engine)`
  - [ ] Move `task_post_executor` → `create()` method
  - [ ] Move `task_get_executor` → `get_by_user()` method
  - [ ] Move `task_patch_executor` → `update()` method
  - [ ] Move `task_delete_executor` → `delete()` method
- [ ] Create `repositories/user_repository.py`
  - [ ] Add `UserRepository` class with `__init__(self, engine)`
  - [ ] Move `users_get_executor` → `get_all()` method
  - [ ] Move `users_post_executor` → `create()` method
  - [ ] Move `users_delete_executor` → `delete()` method
- [ ] Create `repositories/__init__.py` - export both repositories

## Service Layer
- [ ] Create `services/task_service.py`
  - [ ] Add `TaskService` class with `__init__(self, task_repository)`
  - [ ] Add `create_task(data)` method with validation
  - [ ] Add `get_user_tasks(user_id)` method
  - [ ] Add `update_task(update_fields, task_id, user_id)` method
  - [ ] Add `delete_task(user_id, task_id)` method
- [ ] Create `services/user_service.py`
  - [ ] Add `UserService` class with `__init__(self, user_repository)`
  - [ ] Add `get_all_users()` method
  - [ ] Add `create_user(data)` method with validation
  - [ ] Add `delete_user(username)` method
- [ ] Create `services/__init__.py` - export both services

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
