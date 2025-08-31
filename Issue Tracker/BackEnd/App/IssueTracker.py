from flask import Blueprint, request, jsonify
from .model import Issues
from App import db
import logging

logger = logging.getLogger(__name__)
FORMAT = "%(name)s - %(asctime)s - %(funcName)s - %(lineno)d -  %(levelname)s - %(message)s "

handler = logging.FileHandler("IssueTracker.log", mode="a")
formatter = logging.Formatter(FORMAT)

handler.setFormatter(formatter)
logger.addHandler(handler)

issue_tracker = Blueprint("issue_tracker", __name__)

@issue_tracker.route("/issue/get", methods=["GET"])
def get_issues():

    sort = request.args.get("sort", "desc")
    statusD = request.args.get("query", "open")

    order = Issues.id.desc() if sort == "asc" else Issues.id.asc()

    issues = Issues.query.filter(Issues.status.ilike(f"{statusD}")).order_by(order).all()

    data = [issue.get_data() for issue in issues]

    logger.info(f"{issues}")

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : data}), 200

@issue_tracker.route("/issue/get/<int:id>", methods=["GET"])
def get_issues_solo(id):

    issue = Issues.query.get_or_404(id)

    data = issue.get_data()

    logger.info(f"{issue} {data}")

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "message" : data}), 200

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

def commit_session():
    try:
        db.session.commit()
        logger.info("Succesfully commited to the database")
        return (True, None)
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to commit to the database")
        return (False, str(e))
    

def title_validate(title):
    if not (4 < len(title) < 30):
        return False
    
    if not title.strip():
        return False
    
    return True

def priority_level_validate(priority_level):

    if not isinstance(priority_level, int):
        return False

    if not ( 1 <= priority_level <= 10):
        return False
    
    return True