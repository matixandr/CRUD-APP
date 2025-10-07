from flask import Flask
from config import AppConfig
from routes import create_task_routes, create_user_routes

app = Flask(__name__)
cfg = AppConfig()

task_routes = create_task_routes(cfg.task_service)
user_routes = create_user_routes(cfg.user_service)

app.register_blueprint(task_routes)
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run(debug=True)