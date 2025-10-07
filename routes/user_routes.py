from flask import Blueprint, request, jsonify, Response


def create_user_routes(user_service):
    """Factory function to create user routes blueprint with dependency injection"""
    user_bp = Blueprint('users', __name__, url_prefix='/users')

    @user_bp.route('', methods=['GET'])
    def get_users() -> None | tuple[Response, int] | str:
        try:
            usr = user_service.get_all_users()
        except Exception as e:
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

    @user_bp.route('', methods=['POST'])
    def create_user() -> tuple[Response, int]:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Data is empty"
            }), 400

        try:
            success, msg = user_service.create_user(data)
            if not success:
                return jsonify({
                    "status": "error",
                    "message": msg
                }), 409
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "There was an error adding user to database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Successfully added a new user to database"
        }), 201

    @user_bp.route('', methods=['DELETE'])
    def delete_user() -> tuple[Response, int]:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "Data is empty"
            }), 400

        username = data.get("username")
        try:
            success, msg = user_service.delete_user(username)
            if not success:
                return jsonify({
                    "status": "error",
                    "message": msg
                }), 400
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "There was an error deleting user from database, please check the server console"
            }), 500

        return jsonify({
            "status": "success",
            "message": "Successfully deleted a user from database"
        }), 200

    return user_bp

