from flask import Flask
from config import AppConfig
from routes import create_task_routes, create_user_routes

def create_app() -> Flask:
    app = Flask(__name__)

    config = AppConfig()

    task_routes = create_task_routes(config.task_service)
    user_routes = create_user_routes(config.user_service)

    app.register_blueprint(task_routes)
    app.register_blueprint(user_routes)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)