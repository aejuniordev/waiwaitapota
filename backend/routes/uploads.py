from flask import Flask, request, jsonify, Blueprint, redirect, url_for
from factory.database import Database

uploads = Blueprint('uploads', __name__)
gridfs = Database()

@uploads.route('/', methods=['POST'])
def create_upload():
    if request.method == "POST":
        file = request.files["file"]
        _oid = gridfs.save_file(file.filename, file)
        return dict(filename=str(_oid) ), 201
        # return redirect(url_for("uploads.get_upload", filename=str(_oid))), 201

@uploads.route('/<path:filename>', methods=['GET'])
def get_upload(filename=None):
    if request.method == "GET":
        return gridfs.send_file(filename)