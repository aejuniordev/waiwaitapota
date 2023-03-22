from models import usuarios # call model file
import os

_usuarios = usuarios.Usuario()

# TODO: Create admin user

def create_starting():
    return
    # _result = _usuarios.find_by_username('admin')
    # if _result:
    #     return
    # _usuarios.create_starting({
    #     "username": os.environ.get('ADMIN_USERNAME', 'admin'),
    #     "email": os.environ.get('ADMIN_EMAIL', 'admin@waiwai.com') ,
    #     "password": os.environ.get('ADMIN_PASSWORD', 'admin123'),
    #     "permission": 0,
    # })