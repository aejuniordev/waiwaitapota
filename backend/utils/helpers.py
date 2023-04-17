import re

def check_username(username):
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, username))

def check_email(email):
    pattern = r'^\S+@\S+\.\S+$'
    return bool(re.match(pattern, email))