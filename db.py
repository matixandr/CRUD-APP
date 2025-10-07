from sqlalchemy.engine import Engine
from models import Base
from app import app
import sqlalchemy
import dotenv
import os

def db_init() -> Engine:
    dotenv.load_dotenv()
    app.logger.info("loaded .env file")

    USERNAME = os.getenv("POSTGRES_USERNAME")
    PASSWORD = os.getenv("POSTGRES_PASSWD")
    SERVER = os.getenv("POSTGRES_SERVER")
    PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB_NAME")

    engine = sqlalchemy.create_engine(
        f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}"
    )
    app.logger.info("created engine (auth successful)")

    Base.metadata.create_all(engine, checkfirst=True)
    app.logger.info("database create_all executed successfully")
    return engine