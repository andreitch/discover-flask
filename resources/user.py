from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from models.user import UserModel
from flask_jwt_extended import (
  create_access_token, 
  create_refresh_token, 
  jwt_refresh_token_required,
  fresh_jwt_required,
  get_jwt_identity,
  jwt_required,
  get_raw_jwt
)
from db import db

class User(Resource):
  """Represents User endpoints"""
  @classmethod
  def get(cls, user_id):
    user = UserModel.find_by_id(user_id)
    if user:
      return user.json(), 200
    return {"message": "User not found"}, 404

  @classmethod
  @fresh_jwt_required
  def delete(cls, user_id):
    user = UserModel.find_by_id(user_id)
    if user:
      user.remove_from_db()
      return {"message": "User removed successfully"}, 200
    return {"message": "User not found"}, 404


class UserList(Resource):
  def get(self):
    users = []
    for user in UserModel.query.all():
      users.append(user.json())
    return {"users": users}, 200


class UserLogin(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username', required=True, help="User login username")
  parser.add_argument('password', required=True, help="User login password")

  def post(self):
    data = self.parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    print(user)
    if user and safe_str_cmp(user.password, data['password']):
      access_token = create_access_token(identity=user.id, fresh=True)
      refresh_token = create_refresh_token(user.id)
      return {"access_token": access_token,
              "refresh_token": refresh_token}, 200
    return {"message": "User with such username or password not found"}, 404


class UserLogout(Resource):
  """Blacklist access_token to sign out"""
  @jwt_required
  def get(self):
    from app import blacklist
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return {"message": "Successfully logged out"}, 200


class UserRegister(Resource):
  """New user registration"""
  parser = reqparse.RequestParser()
  parser.add_argument('username', required=True, help="User login username")
  parser.add_argument('password', required=True, help="User login password")
  
  def post(self):
    data = UserRegister.parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return {"message": "User with username '{}' already exists!" \
        .format(data['username'])}, 400
    user = UserModel(username=data['username'], password=data['password'])
    user.save_to_db()
    return {"message": "User created succesfully"}, 201


class RefreshToken(Resource):
  """Create new token for security cause"""
  @jwt_refresh_token_required
  def post(self):
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=True)
    return {"access_token": new_token}, 200
    