from models import usuarios # call model file
import os
from werkzeug.security import generate_password_hash

_usuarios = usuarios.Usuario()

# TODO: Create admin user

def create_starting():
    _results = _usuarios.check_admin('admin')
    if _results:
        for _result in _results:
            _id = _result['_id']
            _usuarios.delete(_id)
        _usuarios.create_starting({
            "username": os.environ.get('ADMIN_USERNAME', 'admin'),
            "email": os.environ.get('ADMIN_EMAIL', 'admin@waiwai.com') ,
            "password": generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123')),
            "permission": 3,
        })
    else:
        _usuarios.create_starting({
            "username": os.environ.get('ADMIN_USERNAME', 'admin'),
            "email": os.environ.get('ADMIN_EMAIL', 'admin@waiwai.com') ,
            "password": generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin123')),
            "permission": 3,
        })