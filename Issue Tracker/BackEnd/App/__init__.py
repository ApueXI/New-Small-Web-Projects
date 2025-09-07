from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import logging, os

FORMAT = "%(filename)s - %(asctime)s - %(levelname)s - %(message)s"
DATEFMT ="%Y-%m-%d %H:%M:%S"

logging.basicConfig(level=logging.INFO, 
                    filename="Main.log", 
                    filemode="w", 
                    format= FORMAT,
                    datefmt= DATEFMT)

app = Flask(__name__)
db = SQLAlchemy()
jwt = JWTManager(app)

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
SQLITE = os.getenv("DB_NAME")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_HOST = os.getenv("MYSQL_HOST")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

logger = logging.getLogger(__name__)

def run_app():

    # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE}"

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=3)

    from .IssueTracker import issue_tracker
    from .auth import user_auth

    app.register_blueprint( issue_tracker, url_prefix="/api")
    app.register_blueprint( user_auth, url_prefix="/user")

    db.init_app(app)
    CORS(app, supports_credentials=True)

    # create_database(app)

    sqlite_database(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        logger.info("Database has been created")

def sqlite_database(app):
     db_path = Path(app.instance_path) / SQLITE
     if not db_path.exists():
        with app.app_context():
            db.create_all()
            logger.info("Database has been created")

@app.before_request
def get_localhost():
    app.logger.info(f"On localhost: {request.host}")