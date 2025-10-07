from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from services.user_service import UserService
from services.task_service import TaskService

from flask import Flask, request, jsonify, Response
from db import db_init

app = Flask(__name__)
engine = db_init()

tr = TaskRepository(engine)
ts = TaskService(tr)

ur = UserRepository(engine)
us = UserService(ur)

@app.route('/tasks/<int:user_id>/<int:task_id>', methods=['PATCH'])
def update_tasks(user_id: int, task_id: int) -> tuple[Response, int] | None:
    if request.method == "PATCH":
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Data is empty"
            }), 400

        ALLOWED = {'task_name', 'due_date', 'priority', 'status'}
        update_fields = {}

        for key, value in data.items():
            if key in ALLOWED:
                update_fields[key] = value

        if not update_fields:
            return jsonify({
                "status": "error",
                "message": "There is no fields to edit inside the database"
            }), 400

        try:
            success, msg = ts.update_task(
                update_fields,
                task_id,
                user_id
            )
            if not success:
                return jsonify({
                    "status": "error",
                    "message": msg
                }), 400
        except Exception as e:
            app.logger.error(f"err at patch executor task: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error editing task in database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Successfully updated the task in database"
        }), 200

@app.route('/tasks/<int:user_id>', methods=['GET', 'DELETE'])
def manage_tasks(user_id: int) -> None | tuple[Response, int] | str:
    if request.method == "GET":
        try:
            result = ts.get_tasks_for_user(user_id)
        except Exception as e:
            app.logger.error(f"err at get_tasks_for_user: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error getting task data from database, please check the server console"
            }), 500

        format = request.accept_mimetypes.best_match(['application/json', 'text/html'])

        if format == "text/html":
            thing = f"""
                    <h1>TASK LIST TABLE</h1>
                    <table border="1">
                        <thead>
                            <tr>
                                <th>task_id</th>
                                <th>task_name</th>
                                <th>user_id</th>
                                <th>created_at</th>
                                <th>status</th>
                                <th>due_date</th>
                                <th>priority</th>
                            </tr>
                        </thead>
                        <tbody>
                    """

            for record in result:
                thing += f"""
                            <tr>
                                <td>{record.task_id}</td>
                                <td>{record.task_name}</td>
                                <td>{record.user_id}</td>
                                <td>{record.created_at}</td>
                                <td>{record.status}</td>
                                <td>{record.due_date}</td>
                                <td>{record.priority}</td>
                            </tr>
                        """

            thing += """
                        </tbody>
                    </table>
                    """

            return thing

        task_list = []
        for record in result:
            task_list.append({
                "task_id": record.task_id,
                "task_name": record.task_name,
                "user_id": record.user_id,
                "created_at": str(record.created_at),
                "status": record.status,
                "due_date": str(record.due_date),
                "priority": record.priority
            })

        return jsonify({
            "status": "success",
            "message": "Fetch of data successful",
            "data": task_list
        }), 200

    if request.method == "DELETE":
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Data is empty"
            }), 400

        task_id = data.get("task_id")

        if not user_id or not task_id:
            return jsonify({
                "status": "error",
                "message": "One of these is missing: user_id or task_id"
            }), 400

        try:
            success, msg = ts.delete_task(
                user_id,
                task_id
            )
            if not success:
                return jsonify({"status": "error", "message": msg}), 400
        except Exception as e:
            app.logger.error(f"err at delete_task: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error deleting task from database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": f"Successfully deleted a task from database"
        }), 200

@app.route('/tasks', methods=['POST'])
def tasks() -> tuple[Response, int]:
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Data is empty"
        }), 400

    if data.get('task_id'):
        return jsonify({
            "status": "error",
            "message": "You can't pass task_id into the parameters because it's calculated automatically"
        }), 400

    if data.get('created_at'):
        return jsonify({
            "status": "error",
            "message": "You can't pass created_at into the parameters because it's calculated automatically"
        }), 400

    # Zamiast rozbijać ręcznie dane, przekaż do serwisu
    try:
        success, msg = ts.create_task(data)
        if not success:
            return jsonify({
                "status": "error",
                "message": msg
            }), 400
    except Exception as e:
        app.logger.error(f"err at post executor task: {e}")
        return jsonify({
            "status": "error",
            "message": "There was an error adding task to database, please check the server console"
        }), 500

    return jsonify({
        "status": "success",
        "message": "Successfully added task to the database"
    }), 201

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def users() -> None | tuple[Response, int] | str:
    if request.method == "GET":
        try:
            usr = us.get_all_users()
        except Exception as e:
            app.logger.error(f"err at users get executor:  {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error getting users, please check the server console"
            }), 500

        format = request.accept_mimetypes.best_match(['application/json', 'text/html'])

        if format == "text/html":
            thing = f"""
                            <h1>USER LIST TABLE</h1>
                            <table border="1">
                                <thead>
                                    <tr>
                                        <th>id</th>
                                        <th>username</th>
                                        <th>role</th>
                                        <th>created_at</th>
                                    </tr>
                                </thead>
                                <tbody>
                            """

            for record in usr:
                thing += f"""
                                    <tr>
                                        <td>{record.id}</td>
                                        <td>{record.username}</td>
                                        <td>{record.role}</td>
                                        <td>{record.created_at}</td>
                                    </tr>
                                """

            thing += """
                                </tbody>
                            </table>
                            """

            return thing

        user_list = []
        for record in usr:
            user_list.append({
                "id": record.id,
                "username": record.username,
                "role": record.role,
                "created_at": str(record.created_at),
            })

        return jsonify({
            "status": "success",
            "message": "Successfully fetched users data",
            "data": user_list
        }), 200

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Data is empty"
            }), 400

        try:
            success, msg = us.create_user(data)
            if not success:
                return jsonify({
                    "status": "error",
                    "message": msg
                }), 409
        except Exception as e:
            app.logger.error(f"err at users post executor: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error adding user to database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Successfully added a new user to database"
        }), 201

    if request.method == "DELETE":
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Data is empty"
            }), 400

        username = data.get("username")
        try:
            success, msg = us.delete_user(username)
            if not success:
                return jsonify({
                    "status": "error",
                    "message": msg
                }), 400
        except Exception as e:
            app.logger.error(f"err at users delete executor: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error deleting user from database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Successfully deleted a user from database"
        }), 200

if __name__ == "__main__":
    app.run(debug=True)