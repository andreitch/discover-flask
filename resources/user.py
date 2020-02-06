from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db


class UserRegister(Resource):
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
    