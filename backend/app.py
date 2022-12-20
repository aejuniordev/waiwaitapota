import os

from flask import Flask, request, jsonify
from flask_cors import CORS  # to avoid cors error in different frontend like react js or any other

from flask_jwt_extended import get_jwt_identity, create_access_token, set_access_cookies, get_jwt, JWTManager

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from routes.palavras import palavra
from routes.usuarios import usuario 
from routes.auth import auth 
from routes.uploads import uploads


from config import config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Setup the Flask-JWT-Extended extension

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

app.config["JWT_SECRET_KEY"] = config["SECRET_KEY"]  # Change this!

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=config["ACCESS_TOKEN_EXPIRES"])
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=config["REFRESH_TOKEN_EXPIRES"])

jwt = JWTManager(app)

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@app.route('/', methods=['GET'])
def hello():
    return {"hello": "world"}, 200

@app.errorhandler(404)
def not_found(error=None):
    return jsonify(error="Not found"), 404

app.register_blueprint(palavra, url_prefix='/palavras')
app.register_blueprint(usuario, url_prefix='/usuarios')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(uploads, url_prefix='/uploads')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=True )