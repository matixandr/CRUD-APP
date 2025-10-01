from repository import task_post_executor,task_delete_executor,task_get_executor,task_patch_executor
from flask import Flask, request, jsonify
from db import db_init

app = Flask(__name__)
engine = db_init()

@app.route('/tasks/<int:user_id>/<int:task_id>', methods=['PATCH'])
def update_tasks(user_id: int, task_id: int):
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
            ex = task_patch_executor(
                engine,
                update_fields,
                task_id,
                user_id
            )
            if type(ex) == str:
                return jsonify({
                    "status": "error",
                    "message": "There is no safe fields to update inside database"
                }), 400
        except Exception as e:
            print(f"err in patch executor task: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error editing task in database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Successfully updated the task in database"
        }), 200

@app.route('/tasks/<int:user_id>', methods=['GET','DELETE'])
def manage_tasks(user_id: int):
    if request.method == "GET":
        try:
            result = task_get_executor(
                engine,
                user_id
            )
        except Exception as e:
            print(f"err in delete executor task: {e}")
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
                                <td>{record[0]}</td>
                                <td>{record[1]}</td>
                                <td>{record[2]}</td>
                                <td>{record[3]}</td>
                                <td>{record[4]}</td>
                                <td>{record[5]}</td>
                                <td>{record[6]}</td>
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
                "task_id": record[0],
                "task_name": record[1],
                "user_id": record[2],
                "created_at": str(record[3]),
                "status": record[4],
                "due_date": str(record[5]),
                "priority": record[6]
            })

        return jsonify({
            "status": "success",
            "message": "Fetch of data successful",
            "data": task_list
        })


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
            task_delete_executor(
                engine,
                user_id,
                task_id
            )
        except Exception as e:
            print(f"err in delete executor task: {e}")
            return jsonify({
                "status": "error",
                "message": "There was an error deleting task from database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": f"Successfully deleted an task from database"
        }), 200

@app.route('/tasks', methods=['POST'])
def tasks():
    data = request.get_json()

    if data.get('task_id'):
        return jsonify({
            "status": "error",
            "message": "You can't pass task_id into the parameters because it's calculated automatically"
        }), 400

    created_at = data.get('created_at')
    task_name = data.get('task_name')
    due_date = data.get('due_date')
    priority = data.get('priority')
    user_id = data.get('user_id')
    status = data.get('status')

    if (
            not task_name or
            not user_id or
            not created_at or
            not status or
            not due_date or
            not priority
    ):
        return jsonify({
            "status": "error",
            "message": "One of the values for inserting into tasks is not present in the request"
        }), 400

    try:
        task_post_executor(
            engine,
            task_name,
            user_id,
            created_at,
            status,
            due_date,
            priority
        )
    except Exception as e:
        print(f"err in post executor task: {e}")
        return jsonify({
            "status": "error",
            "message": "There was an error adding task to database, please check the server console"
        }), 500

    return jsonify({
        "status": "success",
        "message": "Successfully added task to the database"
    }), 201

# TODO: add endpoints for users: GET, POST, DELETE
# TODO: fix foreign key constraint violation for adding tasks (user doesn't exist)
# TODO: add .http tests for new users endpoints
# TODO: code quality refactor
# TODO: code quality refactor part two -> change logs (currently print) to flask logging system
# TODO: new README.md with description and instructions how to run etc.
# TODO: requirements.txt file with required packages for project

if __name__ == "__main__":
    app.run(debug=True)