from flask import Flask, request, jsonify, Blueprint
from models import usuarios  # call model file

usuario = Blueprint('usuarios', __name__)

_usuarios = usuarios.Usuario()

# todo routes
@usuario.route('/', methods=['GET'])
def list_usuarios():
    return {"OK": "usuarios"}, 200
    # return jsonify(todo.find({})), 200


# @usuario.route('/todos/<string:todo_id>/', methods=['GET'])
# def get_task(todo_id):
#     return todo.find_by_id(todo_id), 200


# @usuario.route('/todos/', methods=['POST'])
# def add_tasks():
#     if request.method == "POST":
#         title = request.form['title']
#         body = request.form['body']
#         response = todo.create({'title': title, 'body': body})
#         return response, 201


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

