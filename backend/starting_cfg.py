from models import usuarios # call model file
import os

_usuarios = usuarios.Usuario()

def create_starting():
    _result = _usuarios.find_by_username('admin')
    if _result:
        return
    _usuarios.create_starting({
        "username": os.environ.get('ADMIN_USERNAME', 'admin'),
        "email": os.environ.get('ADMIN_EMAIL', 'admin@waiwai.com') ,
        "password": os.environ.get('ADMIN_PASSWORD', 'admin'),
        "permission": 0,
    })