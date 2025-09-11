from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies, decode_token,
                                get_jwt_identity, jwt_required, get_jwt)

from .model import Users, RefreshToken
from App import db, jwt
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__) # So you can organize your logs by having each file be different
FORMAT = "%(name)s - %(asctime)s - %(funcName)s - %(lineno)d -  %(levelname)s - %(message)s " # Defines what the message should look like in the logs

handler = logging.FileHandler("Users.log", mode="a") # Creates/selects the file the logs will be in. And defines what mode will be 'a' for appending
formatter = logging.Formatter(FORMAT)

handler.setFormatter(formatter) # Sets the formatter you have have defines
logger.addHandler(handler) # Finishes the logging config by adding if in the logger variable

user_auth = Blueprint("user_auth", __name__) # Blueprint to organie your routes when you have many of them

# Automatic callback to see if the JWT is expired
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = RefreshToken.query.filter_by(jti=jti).first()
    return token is not None and token.revoked

'''
Method to register the user into the database
Only register user, this doesnt create a JWT or tokens
'''
@user_auth.route("/register", methods=["POST"])
def user_register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not validate_user(data=data, username=username, password=password):
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "Missing credentials"}), 400
        
    if Users.query.filter_by(username=username).first():
        logger.error("Username already exists")
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "Username already exists"}), 400
    
    user = Users(username=username)
    user.set_password(password)

    db.session.add(user)

    success, error = commit_session()
    if not success:
        logger.error("Failed to Commit to database")
        logger.exception(f"Error: {error}")
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "DAtabase error"}), 500
    
    logger.info("User was successfully added")

    return jsonify({"status" : "success" , "ok" : True, 
                        "from" : "Python", 
                        "message" : "User register successful"}), 201

'''
Login method
Creates a token for the each user to use
'''
@user_auth.route("/login", methods=["POST"])
def user_login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not validate_user(data, username, password):
        logger.error("Missing Credentials")
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "Missing credentials"}), 400
    
    user = Users.query.filter_by(username=username).first()
    if not user:
        logger.error("Username not found")
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "User not found"}), 401
    
    if not user.check_password(password):
        logger.error("Password not correct")
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "Password not correct"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    refresh_token_decoded = decode_token(refresh_token)
    jti = refresh_token_decoded["jti"]

    expires = datetime.now(timezone.utc) + current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    current_refresh_token = RefreshToken(jti=jti, user_id=user.id, expires_at=expires)

    db.session.add(current_refresh_token)

    success, error = commit_session()
    if not success:
        logger.error("Failed to commit to database")
        logger.exception(f"Error: {error}")

    response = jsonify({"status" : "success" , "ok" : True, 
                        "from" : "Python", 
                        "message" : "Login Successfull"})
    
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    logger.info("User logged in")

    return response, 200

@user_auth.route("/protected_test", methods=["GET"])
@jwt_required()
def protected_test():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)

    data = user.get_user()

    if not user:
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python",
                        "message" : "Login Unsuccessfull"}), 404
    
    return jsonify({"status" : "success" , "ok" : True, 
                    "from" : "Python", "user" : data,
                    "message" : "Login Successfull"}), 200

@user_auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()["jti"]
    token = RefreshToken.query.filter_by(jti=jti, revoked=False).first()

    if not token:
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "Login Unsuccessfull"})
    
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    response = jsonify({"status" : "success" , "ok" : True, 
                        "from" : "Python", 
                        "message" : "Refresh token successful"})

    set_access_cookies(response, access_token)

    return response, 200

@user_auth.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    token = RefreshToken.query.filter_by(jti=jti).first()

    if not token:
        return jsonify({"status" : "error" , "ok" : False, 
                        "from" : "Python", 
                        "message" : "Token not found"}), 404
    
    token.revoked = True
    
    success, error = commit_session()
    if not success:
        logger.error("Failed to logout the user")
        logger.exception(f"Error : {error}")

    response = jsonify({"status" : "success" , "ok" : True, 
                        "from" : "Python", 
                        "message" : "Token revoked successfully"})
    
    unset_jwt_cookies(response)

    logger.info("User has logout")

    return response, 200

def commit_session():
    try:
        db.session.commit()
        return (True, None)
    except Exception as e:
        db.session.rollback()
        return (False, str(e))
    
def validate_user(data, username, password):
    if not data or not username or not password:
        logger.error("Missing Credentials")
        return False
    return True