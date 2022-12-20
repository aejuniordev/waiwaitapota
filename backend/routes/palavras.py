from flask import Flask, request, jsonify, Blueprint
from models import palavras  # call model file

palavra = Blueprint('palavras', __name__)

_palavras = palavras.Palavra()

@palavra.route('/', methods=['GET'])
@palavra.route('/<string:_oid>', methods=['GET'])
def list_palavras(_oid=None):
    args = request.args
    if _oid:
        return _palavras.find_by_id(_oid), 200
    else:
        return _palavras.find({}, args), 200

@palavra.route('/', methods=['POST'])
def create_palavra():
    if request.method == "POST":
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
                "synonymWaiwai": synonymWaiwai
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
            print(response)
            return response, 204 

@palavra.route('/<string:_oid>', methods=['DELETE'])
def delete_palavra(_oid):
    if request.method == "DELETE":
         _palavras.delete(_oid)
         return dict(message="Deleted", _id=_oid), 204
         