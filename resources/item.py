from flask_restful import Resource, reqparse
from flask_jwt_extended import (
  jwt_required, 
  get_jwt_claims, 
  jwt_optional, 
  get_jwt_identity, 
  fresh_jwt_required
)
from models.item import ItemModel



class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price', type=float, required=True, help="Can't be blank")
  parser.add_argument('store_id', type=int, required=True, help="Can't be blank")

  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return {"item": item.json()}, 200
    return {"message": "Item not found"}, 404

  @jwt_required
  def post(self, name):
    data = self.parser.parse_args()
    item = ItemModel.find_by_name(name)
    if item:
      return {"message": "Duplicate item name"}, 400
    else:
      item = ItemModel(name=name, price=data['price'], store_id=data['store_id'])
      item.save_to_db()
      return {"item": item.json()}, 201

  @classmethod
  @fresh_jwt_required
  def delete(cls, name):
    item = ItemModel.find_by_name(name)
    if not item:
      return {"message": "Item not found"}, 404
    item.remove_from_db()
    return {"message": "Item deleted"}, 200

  @jwt_required
  def put(self, name):
    data = self.parser.parse_args()
    item = ItemModel.find_by_name(name)
    if not item:
      item = ItemModel(name=name, 
        price=data['price'], store_id=data['store_id'])
    else:
      item.price = data['price']
      item.store_id = data['store_id']
    item.save_to_db()
    return {'item': item.json()}, 200


class ItemList(Resource):
  """Public item listing"""
  def get(self):
    items = []
    for item in ItemModel.query.all():
      items.append(item.json())
    return {'items': items}, 200