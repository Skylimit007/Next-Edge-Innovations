from flask import Flask, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

app = Flask(__name__)

# Replace this with your actual Google OAuth 2.0 Client ID
CLIENT_ID = "755429138864-ko8hlpa2gju85jeaal3u2senfoo62qcc.apps.googleusercontent.com"

@app.route("/api/verify_token", methods=["POST"])
def verify_token():
    data = request.get_json()
    token = data.get("id_token")

    if not token:
        return jsonify({"error": "Missing ID token"}), 400

    try:
        # Verify the token with Google's OAuth2 service
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)

        # Token is valid, you can extract user info from idinfo
        user_email = idinfo.get("email")
        user_name = idinfo.get("name")

        return jsonify({
            "status": "success",
            "email": user_email,
            "name": user_name
        })

    except ValueError:
        # Token is invalid
        return jsonify({"error": "Invalid ID token"}), 401

if __name__ == "__main__":
    app.run(debug=True)
