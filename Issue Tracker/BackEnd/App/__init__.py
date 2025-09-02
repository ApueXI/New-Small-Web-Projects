from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
import logging, os
import mysql.connector

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

SECRET_KEY = os.getenv("SECRET_KEY")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_HOST = os.getenv("MYSQL_HOST")

logger = logging.getLogger(__name__)

def run_app():

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}"
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    from .IssueTracker import issue_tracker
    app.register_blueprint( issue_tracker, url_prefix="/api")

    db.init_app(app)
    CORS(app)

    create_database(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

def create_database(app):
        with app.app_context():
            db.create_all()
            logger.info("Database has been created")

@app.before_request
def get_localhost():
    app.logger.info(f"On localhost: {request.host}")