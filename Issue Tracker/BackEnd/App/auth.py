from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from .model import Users, RefreshToken
from App import db, jwt
import logging

logger = logging.getLogger(__name__)
FORMAT = "%(name)s - %(asctime)s - %(funcName)s - %(lineno)d -  %(levelname)s - %(message)s "

handler = logging.FileHandler("Users.log", mode="a")
formatter = logging.Formatter(FORMAT)

handler.setFormatter(formatter)
logger.addHandler(handler)

user_auth = Blueprint("user_auth", __name__)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = RefreshToken.query.filter_by(jti=jti).first()
    return token is not None and token.revoked


@user_auth.route("/register", methods=["POST"])
def user_register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not data or not data.get("username") or not data.get("password"):
        logger.error("Missing Credentials")
        return jsonify({"msg": "Username and password required"}), 400
        
    if Users.query.filter_by(username=data["username"]).first():
        logger.error("Username already exists")
        return jsonify({"msg": "Username already exists"}), 400
    
    user = Users(usrename= username)
    user.set_password(password)

    db.session.add(user)

    success, error = commit_session()

    if not success:
        logger.exception("Failed to commit tot the database")
        return jsonify({"msg" : "Faled to commit to the database"})
    


def commit_session():
    try:
        db.session.commit()
        logger.info("Succesfully commited to the database")
        return (True, None)
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to commit to the database")
        return (False, str(e))