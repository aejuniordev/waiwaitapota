from factory.validation import Validator
from factory.database import Database


class Usuario(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'usuarios'  # collection name

        self.fields = {
            "username": "string",
            "email": "string",
            "password": "string",
            "permission": "number"
        }

        self.create_required_fields = [
            "username",
            "email",
            "password"
        ]

        # Fields optional for CREATE
        # 0 - admin
        # 1 - user
        # 2 - guest
        # Only admin can create admin
        self.create_optional_fields = [
            "permission"
        ]

        # Fields required for UPDATE
        self.update_required_fields = [

        ]

        # Fields optional for UPDATE
        self.update_optional_fields = [
            "username",
            "email",
            "password",
            "permission",
            "created",
            "updated",
        ]

    def create(self, user):
        # Validator will throw error if invalid
        self.validator.validate(user, self.fields, self.create_required_fields, self.create_optional_fields)
        # Set default permission to guest
        user['permission'] = 2
        res = self.db.insert(user, self.collection_name)
        return dict(_id=res)
    
    def create_starting(self, user):
        res = self.db.insert(user, self.collection_name)
        return dict(_id=res)
    
    def find(self, user, projection=None, limit=None, page=None):
        return self.db.find(user, self.collection_name, projection=projection, limit=limit, page=(page-1))

    def find_by_id(self, id, projection=None):
        return self.db.find_by_id(id, self.collection_name, projection=projection)
    
    def find_by_username(self, username):
        return self.db.find_by_username(username, self.collection_name)

    def find_by_username_or_email(self, username, email):
        return self.db.find_by_username_or_email(username, email, self.collection_name)

    def find_by_email(self, email):
        return self.db.find_by_email(email, self.collection_name)

    def update(self, id, user):
        print(self.update_required_fields, self.update_optional_fields)
        self.validator.validate(user, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, user,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
    
    def count_documents(self, criteria={}):
        return self.db.count(self.collection_name, criteria)
    
    def check_admin(self, username):
        return self.db.find_starting(username, self.collection_name)