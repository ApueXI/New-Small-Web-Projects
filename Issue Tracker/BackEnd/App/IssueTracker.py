from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .model import Issues
from App import db, jwt
import logging


logger = logging.getLogger(__name__) # So you can organize your logs by having each file be different
FORMAT = "%(name)s - %(asctime)s - %(funcName)s - %(lineno)d -  %(levelname)s - %(message)s " # Defines what the message should look like in the logs

handler = logging.FileHandler("IssueTracker.log", mode="a") # Creates/selects the file the logs will be in. And defines what mode will be 'a' for appending
formatter = logging.Formatter(FORMAT) 

handler.setFormatter(formatter) # Sets the formatter you have have defines
logger.addHandler(handler) # Finishes the logging config by adding if in the logger variable

issue_tracker = Blueprint("issue_tracker", __name__) # Blueprint to organie your routes when you have many of them

# Custom error so i can flag the frontend with a Boolean for easy conditional rendering
@jwt.unauthorized_loader
def unauthorized_access(err_msg):
    logger.error(err_msg)
    return jsonify({"status" : "error", "ok" : False, 
                    "from" : "Python", "message" : "You need to log in"}), 401

'''
For getting all the issues from the database
Sorts it by the status
'''
@issue_tracker.route("/issue/get", methods=["GET"])
# @jwt_required()
def get_issues():

    sort = request.args.get("sort", "desc")
    statusD = request.args.get("query", "open")

    order = Issues.priority_level.desc() if sort == "desc" else Issues.priority_level.asc()

    issues = Issues.query.filter(Issues.status.ilike(f"{statusD}")).order_by(order).all()

    data = [issue.get_data() for issue in issues]

    logger.info(f"{issues}")

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : data}), 200

'''
Gets the issues solo by filtering the ID of the issue
This is for when the users click the issues into a new link
'''
@issue_tracker.route("/issue/get/<int:id>", methods=["GET"])
def get_issues_solo(id):

    issue = Issues.query.get_or_404(id)

    data = issue.get_data() # Helper method to get sqlalchemy object to Py Dict

    logger.info(f"{issue} {data}")

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : data}), 200

'''
To Post a new issue
validates each data from the json
'''
@issue_tracker.route("/issue/send", methods=["POST"])
def send_issues():

    data = request.get_json()

    title = data.get("title").strip()
    priority_level = data.get("priority_level")
    details = data.get("details").strip()
    status = "open"

    if not title or not priority_level or not details:
        message = "Failed to meet one of the requirements e.g. title, priority_level, details"

        logger.error(message)
        return jsonify({"status" : "error", "ok" : False, 
                    "from" : "Python", "message" : message}), 400
    
    if not title_validate(title) or not priority_level_validate(priority_level):
        message = "Title or Priority Level must be wihthin requirements"

        logger.error(message)
        return jsonify({"status" : "error", "ok" : False, 
                    "from" : "Python", "message" : message}), 400

    issue = Issues(title=title, priority_level=priority_level, details=details, status=status)

    db.session.add(issue)

    success, error = commit_session()

    if not success:
        logger.exception(f"Error occuered {error}")
        return jsonify({"status" : "error", "ok" : False, 
                    "from" : "Python", "message" : error}), 500
    
    logger.info("Send Issue is succesful")
    
    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : data}), 200

'''
Deletes the issues by getting its ID
'''
@issue_tracker.route("/issue/delete/<int:id>", methods=["DELETE"])
def delete_issue(id):

    issue = Issues.query.get_or_404(id)

    db.session.delete(issue)

    success, error = commit_session()
    
    if not success:
        logger.exception(f"Error occurred: {error}")
        return jsonify({ "status": "error", "ok": False,"message":error, "from" : "Python" }), 500

    logger.info(f"{issue} deleted")

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : "Deleted Succesfully"}), 200

'''
Have'nt testest yet
Updates specific part of the issue by using PATCH(Havent tested PATCH yet in any of my projects)
'''
@issue_tracker.route("/issue/update/<int:id>", methods=["PATCH"])
def update_issue(id):
    issue = Issues.query.get_or_404(id)

    data = request.get_json()

    if not title_validate(data.get("title")) or not priority_level_validate(data.get("priority_level")):
        message = "Title or Priority Level must be wihthin requirements"

        logger.error(message)
        return jsonify({"status" : "error", "ok" : False, 
                    "from" : "Python", "message" : message}), 400

    if "title" in data:
        issue.title = data.get("title")
    if "priority_level" in data:
        issue.priority_level = data.get("priority_level")
    if "details" in data:
        issue.details = data.get("details")
    if "status" in data:
        issue.status = data.get("status")


    success, error = commit_session()

    if not success:
        logger.exception(f"Error occurred: {error}")
        return jsonify({ "status": "error", "ok": False,"message": error, "from" : "Python" }), 500
    
    logger.info(f"{issue} updated")

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : "Updated Sccuesfully"}), 200

'''
Helper method to avoid repreadted use of try except in each method
'''
def commit_session():
    try:
        db.session.commit()
        logger.info("Succesfully commited to the database")
        return (True, None)
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to commit to the database")
        return (False, str(e))
    
'''
Helper method to validate title
'''
def title_validate(title):
    if not (4 < len(title) < 30):
        return False
    
    if not title.strip():
        return False
    
    return True

'''
Helper method to validate title
'''
def priority_level_validate(priority_level):

    if not isinstance(priority_level, int):
        return False

    if not ( 1 <= priority_level <= 10):
        return False
    
    return True