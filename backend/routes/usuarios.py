from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import palavras, upload, usuarios # call model file
from werkzeug.security import generate_password_hash

usuario = Blueprint('usuarios', __name__)

_palavras = palavras.Palavra()
_uploads = upload.Upload()
_usuarios = usuarios.Usuario()

@usuario.route('/', methods=['GET'])
@usuario.route('/<string:_oid>', methods=['GET'])
@jwt_required()
def list_usuarios(_oid=None):
    identity = get_jwt_identity()
    args = request.args
    _check_permission = _usuarios.find_by_username(identity)
    if _check_permission['permission'] != 3:
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
                return dict(data=_result, total=_total), 200
            else: return "", 400

@usuario.route('/<string:_oid>', methods=['PUT'])
@jwt_required()
def update_usuario(_oid):
    identity = get_jwt_identity()
    _check_permission = _usuarios.find_by_username(identity)
    _role = _check_permission.get('permission')
    if _check_permission['permission'] != 3:
        return "", 401
    if request.method == "PUT":
        _check = _usuarios.find_by_id(_oid)
        if not _check:
            return dict(error="ID inexistente"), 404
        else:
            if(_check['username'] == identity or _role == 3):
                del _check['_id']
                for key in _usuarios.fields.keys():
                    if key in request.json:
                        if key == "password":
                            _check[key] = generate_password_hash(request.json[key])
                        if key == "permission" and _role == 3:
                            _check[key] = int(request.json[key])
                response = _usuarios.update(_oid, _check)
                return response, 204
            else:
                return dict(error="Palavra não pertence ao usuário"), 401

@usuario.route('/<string:_oid>', methods=['DELETE'])
@jwt_required()
def delete_usuario(_oid):
    identity = get_jwt_identity()
    if request.method == "DELETE":
        _check = _usuarios.find_by_id(_oid)
        if not _check:
            return dict(error="ID inexistente"), 404
        else:
            _profile = _usuarios.find_by_username(identity)
            if(_profile.get('permission') == 3): 
                _usuarios.delete(_oid)
                return dict(message="Deletado", _id=_oid), 204
            else:
                return dict(error="Usuário sem permissão"), 401
