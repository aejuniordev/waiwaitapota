from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import palavras, upload # call model file

# todo: refatorar essa parte
from factory.database import Database

db = Database()

palavra = Blueprint('palavras', __name__)

_palavras = palavras.Palavra()
_uploads = upload.Upload()


@palavra.route('/', methods=['GET'])
@palavra.route('/<string:_oid>', methods=['GET'])
def list_palavras(_oid=None):
    print("sem autenticação")
    args = request.args
    if _oid:
        attach_image = _uploads.find(_oid, 'image')
        attach_audio = _uploads.find(_oid, 'audio')
        _result = _palavras.find_by_id(_oid)
        _result.update({'audio': None,'image': None})
        if len(attach_image):
            _id = attach_image[0]['_id']
            _result.update({'image': _id})
        if len(attach_audio):
            _id = attach_audio[0]['_id']
            _result.update({'audio': _id})
        return _result, 200
    else:
        return _palavras.find({}, args), 200


@palavra.route('/me', methods=['GET'])
@jwt_required()
def get_by_user():
    identity = get_jwt_identity()
    return _palavras.find_by_username(identity), 200
    

@palavra.route('/', methods=['POST'])
@jwt_required()
def create_palavra():    
    if request.method == "POST":
        identity = get_jwt_identity()
        wordPort = request.json["wordPort"] 
        translationWaiwai = request.json["translationWaiwai"]
        category = request.json["category"]
        meaningPort = request.json["meaningPort"]
        meaningWaiwai = request.json["meaningWaiwai"]
        synonymPort = request.json["synonymPort"]
        synonymWaiwai = request.json["synonymWaiwai"]
        _check = _palavras.find(word={"wordPort":wordPort})
        if _check:
            return dict(error="Palavra já existe"), 409
        else:
            response = _palavras.create({
                "wordPort": wordPort, 
                "translationWaiwai": translationWaiwai, 
                "category": category, 
                "meaningPort": meaningPort, 
                "meaningWaiwai": meaningWaiwai, 
                "synonymPort": synonymPort, 
                "synonymWaiwai": synonymWaiwai,
                "user": identity
            })
            return response, 201

@palavra.route('/<string:_oid>', methods=['PUT'])
def update_palavra(_oid):
    if request.method == "PUT":
        _check = _palavras.find_by_id(_oid)
        if not _check:
            return dict(error="ID inexistente"), 404
        else:
            del _check['_id']
            for key in _palavras.fields.keys():
                if key in request.json:
                    _check[key] = request.json[key]
            response = _palavras.update(_oid, _check)
            return response, 204 

@palavra.route('/<string:_oid>', methods=['DELETE'])
def delete_palavra(_oid):
    if request.method == "DELETE":
         _palavras.delete(_oid)
         return dict(message="Deleted", _id=_oid), 204
         