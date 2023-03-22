from flask import Blueprint
from models import usuarios  # call model file

usuario = Blueprint('usuarios', __name__)

_usuarios = usuarios.Usuario()

# Todo: Operations with users
@usuario.route('/', methods=['GET'])
def list_usuarios():
    return {"OK": "usuarios"}, 200
 