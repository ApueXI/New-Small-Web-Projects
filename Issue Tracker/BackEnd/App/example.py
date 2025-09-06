from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies,
    decode_token
)
from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"  # Change in production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jwt_demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-jwt"  # Change in production
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Enable in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ----------------- Models -----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    revoked = db.Column(db.Boolean, default=False)
    expires_at = db.Column(db.DateTime, nullable=False)

# Create tables within app context
with app.app_context():
    db.create_all()

# ----------------- JWT Handlers -----------------
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = RefreshToken.query.filter_by(jti=jti).first()
    return token is not None and token.revoked

# ----------------- Routes -----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Username and password required"}), 400
        
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Username already exists"}), 400
        
    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

# ----------------- Login -----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Username and password required"}), 400
        
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Decode the refresh token to get its JTI
    refresh_token_decoded = decode_token(refresh_token)
    jti = refresh_token_decoded["jti"]

    # Save refresh token in DB
    expires = datetime.now(datetime.timezone.utc) + app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    db.session.add(RefreshToken(jti=jti, user_id=user.id, expires_at=expires))
    db.session.commit()

    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response

# ----------------- Protected -----------------
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify({"msg": f"Hello {user.username}!"})

# ----------------- Refresh -----------------
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    jti = get_jwt()["jti"]
    token = RefreshToken.query.filter_by(jti=jti, revoked=False).first()
    if not token:
        return jsonify({"msg": "Refresh token revoked"}), 401

    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    response = jsonify({"msg": "Access token refreshed"})
    set_access_cookies(response, access_token)
    return response

# ----------------- Logout -----------------
@app.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    token = RefreshToken.query.filter_by(jti=jti).first()
    if token:
        token.revoked = True
        db.session.commit()

    response = jsonify({"msg": "Logged out"})
    unset_jwt_cookies(response)
    return response

# ----------------- Run App -----------------
if __name__ == "__main__":
    app.run(debug=True)