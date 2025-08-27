from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
import logging, os

FORMAT = "%(filename)s - %(asctime)s - %(levelname)s - %(message)s"
DATEFMT ="%Y-%M-%D %H:%M:%S"

logging.basicConfig(level=logging.INFO, 
                    filename="Main.log", 
                    filemode="w", 
                    format= FORMAT,
                    datefmt= DATEFMT)

db = SQLAlchemy()
app = Flask(__name__)

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_NAME = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")

logger = logging.getLogger(__name__)

def run_app():

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from .IssueTracker import issue_tracker
    app.register_blueprint( issue_tracker, url_prefix="/api")

    CORS(app)

    db.init_app(app)

    create_database(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

def create_database(app):
    db_path = Path(app.instance_path) / DB_NAME

    if not db_path.exists():
        with app.app_context():
            db.create_all()
            logger.info("Database has been created")

@app.before_request
def get_localhost():
    app.logger.info(f"On localhost: {request.host}")