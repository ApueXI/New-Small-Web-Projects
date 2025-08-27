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

    sort = request.args.get("sort", "asc")

    order = Issues.id.asc() if sort == "asc" else Issues.id.desc()

    issues = Issues.query.order_by(order).all()

    data = [issue.get_data() for issue in issues]

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

def commit_session():
    try:
        db.session.commit()
        logger.info("Succesfully commited to the database")
        return (True, None)
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to commit to the database")
        return (False, str(e))