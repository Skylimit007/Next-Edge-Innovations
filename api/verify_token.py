from flask import Flask, request, jsonify, session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from functools import wraps
import os

app = Flask(__name__)

# Use an environment variable for secret key in production
app.secret_key = os.environ.get("99aab60423441c01d2256e8280a0a7e3c86597734310b5515db195a37361426f", "supersecretkey")

# Replace this with your actual Google OAuth 2.0 Client ID
CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "755429138864-ko8hlpa2gju85jeaal3u2senfoo62qcc.apps.googleusercontent.com"
)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/api/verify_token", methods=["POST"])
def verify_token():
    data = request.get_json()
    token = data.get("id_token")

    if not token:
        return jsonify({"error": "Missing ID token"}), 400

    try:
        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)

        user_email = idinfo.get("email")
        user_name = idinfo.get("name")

        # Save user info in session for persistence
        session["user"] = {
            "email": user_email,
            "name": user_name
        }

        return jsonify({
            "status": "success",
            "email": user_email,
            "name": user_name
        })

    except ValueError:
        return jsonify({"error": "Invalid ID token"}), 401

@app.route("/dashboard")
@login_required
def dashboard():
    user = session["user"]
    return jsonify({
        "message": f"Welcome {user['name']} to your dashboard!",
        "email": user["email"]
    })

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

if __name__ == "__main__":
    app.run(debug=True)
