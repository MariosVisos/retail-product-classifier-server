from werkzeug.security import safe_str_cmp
from user import User


# In memory table of registered users
users = [
    User(1, 'user1', '12345'),
    User(2, 'user2', '12345'),
]

# set comprehension
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
