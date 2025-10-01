from flask import Flask, request, jsonify
from sqlalchemy import text
from db import engine

app = Flask(__name__)

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
        params = {"task_id": task_id, "user_id": user_id}
        fields = []

        for key, value in data.items():
            if key in ALLOWED:
                fields.append(f"{key} = :{key}")
                params[key] = value

        if not fields:
            return jsonify({
                "status": "error",
                "message": "There is no fields to edit inside the database"
            }), 400

        clause = ", ".join(fields)
        QUERY = text(f"UPDATE tasks SET {clause} WHERE task_id = :task_id AND user_id = :user_id")

        with engine.connect() as conn:
            conn.execute(QUERY, {
                "task_id":task_id,
                "user_id": user_id
            })
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Successfully updated the task in database"
        }), 200

@app.route('/tasks/<int:user_id>', methods=['GET','DELETE'])
def manage_tasks(user_id: int):
    if request.method == "GET":
        QUERY = text('SELECT * FROM tasks WHERE user_id = :user_id;')
        with engine.connect() as conn:
            result = conn.execute(QUERY, {"user_id": user_id}).fetchall()

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

        QUERY = text(f"DELETE FROM tasks WHERE user_id = :user_id AND task_id = :task_id")
        with engine.connect() as conn:
            conn.execute(QUERY, {
                "user_id": user_id,
                "task_id": task_id
            })
            conn.commit()

        return jsonify({
            "status": "success",
            "message": f"Successfully deleted an task from database ({user_id}:{task_id})"
        }), 200

@app.route('/tasks', methods=['POST'])
def tasks():
    if request.method == "POST":
        data = request.get_json()

        if data.get('task_id'):
            return jsonify({
                "status": "error",
                "message": "You can't pass task id into the parameters because it's calculated automatically"
            }), 400

        QUERY = text('SELECT COUNT(task_id) FROM tasks;')
        with engine.connect() as conn:
            fetch_ids = conn.execute(QUERY).fetchall()

        task_id = int(str(fetch_ids).split("(")[1].split(",")[0])  # calculate the next id for task to be inserted

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

        ADD_TO_TASK = text("""
            INSERT INTO tasks (task_id, task_name, user_id, created_at, status, due_date, priority)
            VALUES (:task_id, :task_name, :user_id, :created_at, :status, :due_date, :priority)
        """)

        with engine.connect() as conn:
            conn.execute(ADD_TO_TASK, {
                "task_id": task_id,
                "task_name": task_name,
                "user_id": user_id,
                "created_at": created_at,
                "status": status,
                "due_date": due_date,
                "priority": priority
            })
            conn.commit()

        return jsonify({
            "status": "success",
            "message": "Successfully added task to the database"
        }), 200

if __name__ == "__main__":
    app.run(debug=True)