from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pathlib import Path
import logging

db = SQLAlchemy()
DB_NAME = "IssueTracker.db"

logging.basicConfig(level=logging.info, filename="Main.log", filemode="w", 
                    format="%(filename)s - %(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%M-%D %H:%M:%S")

logger = logging.getLogger(__name__)

def run_app():
    app = Flask(__name__)

    app.config("SQLALCHEMY_DATABASE_URI") = f"sqlite:///{DB_NAME}"
    app.config("SECRET_KEY") = "4f7690667988b8124afae2b90bd62432"
    app.config("SQLALCHEMY_TRACK_MODIFICATIONS") = False

    CORS(app)

    db.init_app(app)

    create_database(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

def create_database(app):
    db_path = Path(app.root_path) / DB_NAME

    if not db_path.exists():
        with app.app_context():
            db.create_all()
            logger.info("Database has been created")