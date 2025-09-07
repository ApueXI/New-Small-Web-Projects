from App import db
from werkzeug.security import generate_password_hash, check_password_hash

# Issues table
class Issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    priority_level = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"No.{self.id}"

    def get_data(self):
        return{
            "id" : self.id,
            "title" : self.title,
            "priority_level" : self.priority_level,
            "details" : self.details,
            "status" : self.status
        }

# Users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    _password = db.Column(db.String(256), nullable=False)
    issues = db.relationship("Issues", backref="author", lazy=True)

    def __repr__(self):
        return f"No. {self.id}"
    
    def get_user(self):
        return{
            "id" : self.id,
            "username" : self.username
        }
    
    def set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)
    
# Refreshtokens table
class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    revoked = db.Column(db.Boolean, default=False, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)