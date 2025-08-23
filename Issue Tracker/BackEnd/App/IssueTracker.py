from flask import Blueprint, request, jsonify
from .model import Issues
from App import db
import logging

logger = logging.getLogger(__name__)

handler = logging.FileHandler("IssueTracker.log")
formatter = logging.Formatter("%(name)s - %(asctime)s - %(funcName)s - %(lineno)d -  %(levelname)s - %(message)s ")
handler.setFormatter(formatter)
logger.addHandler(handler)

issue_tracker = Blueprint("issue_tracker", __name__)

@issue_tracker.route("/issues/data", methods=["GET"])
def get_issues():

    sort = request.args.get("sort", "asc").strip()

    order = Issues.id.asc() if sort == "asc" else Issues.id.desc()

    issues = Issues.query.order_by(order).all()

    data = [issue.get_data() for issue in issues]

    return jsonify({"status" : "success", "ok" : True, 
                    "from" : "Python", "result" : data}), 200

def commit_session():
    try:
        db.session.commit()
        logger.info("Succesfully commited to the database")
        return (True, None)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to commit to the database\nError: {e}")
        return (False, str(e))