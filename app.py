import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserResource, UserLogin, RefreshToken
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

jwt = JWTManager(app)
api = Api(app)

@app.before_first_request
def create_tables():
  db.create_all()

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
  if identity == 1:
    return {"is_admin": True}
  return {"is_admin": False}

@jwt.expired_token_loader
def expired_token_callback():
  return {"description": "The tocken expired",
          "error": "The token expired"}, 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserLogin, '/auth')
api.add_resource(RefreshToken, '/refresh')


if __name__ == '__main__':
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)
