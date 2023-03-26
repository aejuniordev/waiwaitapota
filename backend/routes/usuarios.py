from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import palavras, upload, usuarios # call model file
from werkzeug.security import generate_password_hash

usuario = Blueprint('usuarios', __name__)

_palavras = palavras.Palavra()
_uploads = upload.Upload()
_usuarios = usuarios.Usuario()

# TODO: Refatorar para middleware de permissão

@usuario.route('/', methods=['GET'])
@usuario.route('/<string:_oid>', methods=['GET'])
@jwt_required()
#Busca a palavras pelo ID
def list_usuarios(_oid=None):
    identity = get_jwt_identity()
    args = request.args
    _check_permission = _usuarios.find_by_username(identity)
    if _check_permission['permission'] != 0:
        return "", 401
    else:
        if _oid:
            _result = _usuarios.find_by_id(_oid, {"created": 1,
                    "email": 1,
                    "permission": 1,
                    "updated": 1,
                    "username": 1})
            return _result, 200
        else:
            limit = args.get('limit', default=10, type=int)
            page = args.get('page', default=1, type=int)
            if page > 0 and limit > 0 and limit <= 1000:
                _total = _usuarios.count_documents()
                _result = _usuarios.find({"username": { "$not": {"$eq": identity} }}, {"created": 1,
                    "email": 1,
                    "permission": 1,
                    "updated": 1,
                    "username": 1}, 
                    limit=limit,
                    page=page
                    )
                response = jsonify(_result)
                response.headers.set('Total-Documents ', _total)
                return response, 200
            else: return "", 400

# TODO: Check if username or email exists before create
@usuario.route('/<string:_oid>', methods=['PUT'])
@jwt_required()
def update_usuario(_oid):
    identity = get_jwt_identity()
    _check_permission = _usuarios.find_by_username(identity)
    _role = _check_permission.get('permission')
    if _check_permission['permission'] != 0:
        return "", 401
    if request.method == "PUT":
        _check = _usuarios.find_by_id(_oid)
        if not _check:
            return dict(error="ID inexistente"), 404
        else:
            if(_check['username'] == identity or _role == 0):
                del _check['_id']
                for key in _usuarios.fields.keys():
                    if key in request.json:
                        if key == "password":
                            _check[key] = generate_password_hash(request.json[key])
                        if key == "permission":
                            if _role == 0:
                                _check[key] = request.json[key]
                        if key == "username" or key == "email":
                            if _check[key] != request.json[key]:
                                _check = _usuarios.find_by_username_or_email(request.json[key], request.json[key])
                                if _check:
                                    return jsonify(error="Email ou usuário em uso"), 409
                        else: 
                            _check[key] = request.json[key]
                print(_check)                        
                response = _usuarios.update(_oid, _check)
                return response, 204
            else:
                return dict(error="Palavra não pertence ao usuário"), 401
