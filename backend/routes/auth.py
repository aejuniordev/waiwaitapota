from flask import Flask, request, jsonify, Blueprint
from models import usuarios  # call model file
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token, get_jwt_identity ,jwt_required, create_refresh_token, set_access_cookies, unset_jwt_cookies

auth = Blueprint('auth', __name__)

_usuarios = usuarios.Usuario()

# todo routes
@auth.route('/register', methods=['POST'])
def create_user():
    if request.method == "POST":
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        # print(username, email, generate_password_hash(password))
        _check = _usuarios.find({ "$or": [ {"username": username }, {"email": email} ] })
        if _check:
            return "", 400
        else:
            _usuarios.create({
                "username":username,
                "email":email,
                "password":generate_password_hash(password)
            })
            return "", 200
    # return jsonify(todo.find({})), 200

@auth.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if password and email:
        _check = _usuarios.find( {"email": email})
        if _check:
            if check_password_hash(_check[0]['password'], password):
                access_token = create_access_token(identity=_check[0]['username'], fresh=True)
                refresh_token = create_refresh_token(identity=_check[0]['username'])
                response = jsonify(access_token=access_token, refresh_token=refresh_token)
                set_access_cookies(response, access_token, refresh_token)
                return response
            else: 
                return jsonify(error="Necessário informário email e senha"), 401
    else: 
        return jsonify(error="Necessário informário email e senha"), 401
    

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logout efetuado"})
    unset_jwt_cookies(response)
    return response
