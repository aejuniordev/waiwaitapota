from flask import request, jsonify, Blueprint
from models import usuarios  # call model file
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies

auth = Blueprint('auth', __name__)

_usuarios = usuarios.Usuario()

@auth.route('/register', methods=['POST'])
def create_user():
    if request.method == "POST":
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        _check = _usuarios.find({ "$or": [ {"username": username }, {"email": email} ] })
        if _check:
            return jsonify(error="Email ou usuário em uso"), 400
        else:
            _usuarios.create({
                "username":username,
                "email":email,
                "password":generate_password_hash(password)
            })
            return "", 201

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
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            else:
                return jsonify(error="Senha ou email errados"), 400
        else: 
            return jsonify(error="Conta não encontrada"), 400
    else: 
        return jsonify(error="Necessário informário email e senha"), 401
    

@auth.route("/protected")
@jwt_required(refresh=True)
def protected():
    identity = get_jwt_identity()
    return jsonify(foo="bar")

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/#explicit-refreshing-with-refresh-tokens
# @auth.route("/refresh", methods=["POST"])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#     refresh_token = create_refresh_token(identity=identity)
#     response = jsonify(access_token=access_token, refresh_token=refresh_token)
#     set_access_cookies(response, access_token)
#     set_refresh_cookies(response, refresh_token)
#     return response

@auth.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logout efetuado"})
    unset_jwt_cookies(response)
    return response
