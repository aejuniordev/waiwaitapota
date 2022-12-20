from flask import Flask, request, jsonify, Blueprint
from models import palavras  # call model file

palavra = Blueprint('palavras', __name__)

_palavras = palavras.Palavra()

@palavra.route('/', methods=['GET'])
@palavra.route('/<string:_oid>', methods=['GET'])
def list_palavras(_oid=None):
    args = request.args
    word_obj = {}
    if _oid:
        word_obj["_id"] =_oid
    return _palavras.find(word_obj, args), 200

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
            return dict(error="Entrada já existe"), 409
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

# @palavra.route('/todos/<string:todo_id>/', methods=['GET'])
# def get_task(todo_id):
#     return todo.find_by_id(todo_id), 200


# @usuario.route('/todos/<string:todo_id>/', methods=['PUT'])
# def update_tasks(todo_id):
#     if request.method == "PUT":
#         title = request.form['title']
#         body = request.form['body']
#         response = todo.update(todo_id, {'title': title, 'body': body})
#         return response, 201


# @usuario.route('/todos/<string:todo_id>/', methods=['DELETE'])
# def delete_tasks(todo_id):
#     if request.method == "DELETE":
#         todo.delete(todo_id)
#         return "Record Deleted"

