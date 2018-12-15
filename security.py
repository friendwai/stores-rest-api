from werkzeug.security import safe_str_cmp
from models.user import UserModel

# users = [
#     {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# ]
#
# username_mapping = { 'bob': {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf'
#     }
# }
#
# userid_mapping = { 1: {
#         'id': 1,
#         'username': 'bob',
#         'password': 'asdf',
#     }
# }
# by importing user object/class created from user.py, instead of dictionary
# and copying mopping as above


#local variable and mapping method
# users = [
#     User(1, 'bob', 'asdf')
# ]
#
# username_mapping = {u.username: u for u in users}
#
# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    # user = username_mapping.get(username, None) #mapping through local list users
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None) #mapping through local list users
    return UserModel.find_by_id(user_id)
