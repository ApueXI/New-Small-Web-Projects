from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import logging, os

"""
FORMAT > cuztomizes how the messeage in the logging should look like
DATEFMT > formtas how the date should look like

basicConfig
    level > sets the level at what should the logging accept (default is logging.ERROR)
    filename > The name of the file where the logs should be
    filemode > 'w' is overwrite, craete a new log, 'w' is the default. you could use 'a' to append in the log file avoiding rewriting
    format, datefmt > sets what the message in the log should look like
"""
FORMAT = "%(filename)s - %(asctime)s - %(levelname)s - %(message)s"
DATEFMT ="%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.INFO, 
                    filename="Main.log", 
                    filemode="w", 
                    format= FORMAT,
                    datefmt= DATEFMT)

'''
app > initializes the flask app
db > initializes the sqlalchemy
jwt > initializes the JWT 
'''
app = Flask(__name__)
db = SQLAlchemy()
jwt = JWTManager(app)

'''
env_path > gets/sets the absolute file dir/path of where you have the .env file
load_dotenv() > library where it loads the env for easy use

os.getenv > gets the env variable. you need to insert the exact string of the name
'''
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

    '''
    first two config > initialzes the Databse e.g. SQLITE or MySQL
    '''
    # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}/{MYSQL_DB}"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{SQLITE}"

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # incresaes performance
    
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"] # Sets the location where the jwt should be sent
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_COOKIE_SECURE"] = False # should be true in production 
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False # should be true in production
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=15) # short lived token
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=3) # lobe lived token to refresh the access token

    '''
    initializes the blueprint
    meaning to organize your files
    '''
    from .IssueTracker import issue_tracker
    from .auth import user_auth

    app.register_blueprint( issue_tracker, url_prefix="/api")
    app.register_blueprint( user_auth, url_prefix="/user")

    db.init_app(app)
    CORS(app, supports_credentials=True) # Enables CORS and lets you send JWT thorough cookieHTTP

    # create_database(app)
    sqlite_database(app)

    '''
    Automatically closes every session opened 
    No need for db.session.close() for every sqlalechemy interaction
    '''
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

# logs where the locahost is
@app.before_request
def get_localhost():
    app.logger.info(f"On localhost: {request.host}")