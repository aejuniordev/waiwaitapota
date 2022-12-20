from factory.validation import Validator
from factory.database import Database


class Palavra(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'palavras'  # collection name

        self.fields = {
            "wordPort": "string",
            "translationWaiwai": "string",
            "category": "string",
            "meaningPort": "string",
            "meaningWaiwai": "string",
            "synonymPort": "string",
            "synonymWaiwai": "string",
            "approved": "boolean"
        }

        self.create_required_fields = [
            "wordPort",
            "translationWaiwai",
        ]

        # Fields optional for CREATE
        self.create_optional_fields = [
            "category",
            "meaningPort",
            "meaningWaiwai",
            "synonymPort",
            "synonymWaiwai",
            "approved"
        ]

        # Fields required for UPDATE
        self.update_required_fields = [
            "wordPort",
            "translationWaiwai",]

        # Fields optional for UPDATE
        self.update_optional_fields = [
            "category",
            "meaningPort",
            "meaningWaiwai",
            "synonymPort",
            "synonymWaiwai",
            "approved"
        ]

    def create(self, word):
        # Validator will throw error if invalid
        word["approved"] = False
        self.validator.validate(word, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(word, self.collection_name)
        return dict(_id=res)

    def find(self, word, *args):  # find all
        if args:
            category= args[0].get("filters[category]")
            if category:
                word["category"]=category
        
        return self.db.find(word, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, word):
        self.validator.validate(word, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, word,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)