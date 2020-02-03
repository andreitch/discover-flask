import sqlite3
from flask_restful import Resource, reqparse


class User:
  def __init__(self, _id, username, password):
    self.id = _id
    self.username = username
    self.password = password

  @classmethod
  def find_by_username(cls, username):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username=?"
    result = cursor.execute(query, (username,))
    user = result.fetchone()

    connection.close()

    if user:
      return User(*user)

  @classmethod
  def find_by_id(cls, _id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE id=?"
    result = cursor.execute(query, (_id,))
    user = result.fetchone()

    connection.close()

    if user:
      return User(*user)


class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username', required=True, help="User login name")
  parser.add_argument('password', required=True, help="User login password")

  def post(self):
    data = UserRegister.parser.parse_args()

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username=?"
    if cursor.execute(query, (data['username'],)).fetchone():
      return {"message": "User with username '{}' already exists!" \
        .format(data['username'])}, 400

    query = "INSERT INTO users ( username, password ) VALUES (?,?)"
    cursor.execute(query, (data['username'], data['password'],))

    connection.commit()
    connection.close

    return {"message": "User created succesfully"}, 201
    