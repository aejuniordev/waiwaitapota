from flask import Flask, request, jsonify, Blueprint, redirect, url_for
from factory.database import Database

uploads = Blueprint('uploads', __name__)
gridfs = Database()

@uploads.route('/', methods=['POST'])

# Todo: Verificar token do usuário logado para postar a imagem e anexar email do token
def create_upload():
    if request.method == "POST":
        oidWord = request.form["oidword"]
        if oidWord:
            file = request.files["file"]
            print(file)
            # Todo: Verificar se oidword é válido para criar no BD
            _oid = gridfs.save_file(file.filename, file, oidword=oidWord)
            return dict(filename=str(_oid)), 201
        else:
            return dict(error="Informe o ID da palavra!"), 400

@uploads.route('/<path:filename>', methods=['DELETE'])
# Todo: Verificar token do usuário logado para deletar a imagem/audio, caso pertença a ele o upload
# Todo: Checar se tipo de arquivo já está vinculado ao ID da palavra
def delete_upload(filename=None):
    gridfs.find_by_id(filename, "fs.files")
    gridfs.delete_file(filename)
    return "", 202
    

@uploads.route('/<path:filename>', methods=['GET'])
# Todo: Para consultar imagens necessário autenticação
def get_upload(filename=None):
    if request.method == "GET":
        return gridfs.send_file(filename)