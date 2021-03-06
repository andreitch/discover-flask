from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_optional, fresh_jwt_required
from models.store import StoreModel



class Store(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('name', type=str, required=True, help="Can't be blank")

  def get(self, name):
    store = StoreModel.find_by_name(name)
    if store:
      return {"store": store.json()}
    return {"message": "Store not found"}, 404

  @jwt_required
  def post(self, name):
    store = StoreModel.find_by_name(name)
    if store:
      return {"message": "Duplicate store name"}, 400
    else:
      store = StoreModel(name=name)
      store.save_to_db()
      return {"store": store.json()}, 201

  @fresh_jwt_required
  def delete(self, name):
    store = StoreModel.find_by_name(name)
    if not store:
      return {"message": "Store not found"}, 404
    
    for item in store.items:
      item.remove_from_db()
    store.remove_from_db()
    return {"message": "Store deleted"}


class StoreList(Resource):
  def get(self):
    stores = []
    for store in StoreModel.query.all():
      stores.append(store.json())
    return {"stores": stores}, 200
