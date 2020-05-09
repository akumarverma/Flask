from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1,'amit','admin123')
]

user_name_mapping = {u.user_name: u for u in users}

user_id_mapping = {u.id: u for u in users}


def authenticate(username,password):
    user = user_name_mapping.get(username,None)

    if user is not None and safe_str_cmp(password,user.password):
        return user
    else:
        return None


def identity(payload):
    user_id = payload['identity']
    return user_id_mapping.get(user_id,None)