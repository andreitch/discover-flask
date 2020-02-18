import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import (
  User, 
  UserList,
  UserLogin,
  UserLogout,
  UserRegister,
  RefreshToken
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.secret_key = 'secret'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)
api = Api(app)

blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.before_first_request
def create_tables():
  db.create_all()

@jwt.expired_token_loader
def expired_token_callback():
  return {"description": "The tocken expired",
          "error": "The token expired"}, 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(RefreshToken, '/refresh')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)
