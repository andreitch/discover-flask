
from werkzeug.security import safe_str_cmp
from user import User

users = [
  User(1, "bob", "abc")
]

username_mapping = {
  "bob": User(1, "bob", "abc")
}

userid_mapping = {
  1: User(1, "bob", "abc")
}

def authenticate(username, password):
  user = username_mapping.get(username, None)
  if user and safe_str_cmp(user.password, password):
    return user

def identity(payload):
  userid = payload["identity"]
  return userid_mapping[userid]