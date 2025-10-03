# CRUD-APP

A RESTful task and user management API built with Flask and PostgreSQL

> [!WARNING]
> This CRUD app is for a school project and it's not intended for comercial use. Please do NOT reference anything from here

## Features

- **User Management**: Create, read, and delete users
- **Task Management**: Full CRUD operations with status tracking (pending, in-progress, completed)
- **Priority Levels**: Organize tasks by priority (low, medium, high)
- **Content Negotiation**: JSON and HTML response formats
- **Input Validation**: Request validation and error handling

## Tech Stack

1. Python **3.13.2**
2. Flask **2.3.3**
3. PostgreSQL **18.0**
4. SQLAlchemy **2.0.43**
5. python-dotenv **1.0.1**

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file**
   ```env
   POSTGRES_USERNAME=your_username
   POSTGRES_PASSWD=your_password
   POSTGRES_SERVER=your_server_ip
   POSTGRES_PORT=your_port
   POSTGRES_DB_NAME=your_database_name
   ```

3. **Run**
   ```bash
   python app.py
   ```
   Server starts at `http://localhost:5000`

## API Reference

### Users

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| GET | `/users` | - | Get all users |
| POST | `/users` | `{"username": "matt", "role": "admin"}` | Create user |
| DELETE | `/users` | `{"username": "matt"}` | Delete user |

### Tasks

| Method | Endpoint | Body | Description |
|--------|----------|------|-------------|
| GET | `/tasks/{user_id}` | - | Get user's tasks |
| POST | `/tasks` | See below* | Create task |
| PATCH | `/tasks/{user_id}/{task_id}` | Any allowed field** | Update task |
| DELETE | `/tasks/{user_id}` | `{"task_id": 1}` | Delete task |

> *POST /tasks required fields:
```json
{
  "task_name": "Complete homework",
  "user_id": 1,
  "status": "pending",
  "due_date": "2025-10-10",
  "priority": "high"
}
```

> **PATCH allowed fields: `task_name`, `status`, `due_date`, `priority`

### Response Format

**Success:**
```json
{
  "status": "success",
  "message": "Operation completed",
  "data": [...]
}
```

**Error:**
```json
{
  "status": "error",
  "message": "Error description"
}
```

### Status Codes
- `200` - Success (GET/PATCH/DELETE)
- `201` - Created (POST)
- `400` - Bad Request
- `409` - Conflict
- `500` - Server Error

## Testing

Tests inside request_tests are made for PyCharm to test the endpoints
