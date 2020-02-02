from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'secret'
jwt = JWT(app, authenticate, identity)
api = Api(app)

items = [
  {
    "name": "Chear",
    "price": 19.99
  }
]


class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price', type=float, required=True, help="Can't be blank")

  @jwt_required()
  def get(self, name):
    item = next(filter(lambda x: x['name'] == name, items), None)
    return {"item": item}

  def post(self, name):
    data = self.parser.parse_args()
    item = next(filter(lambda x: x['name'] == name, items), None)
    if not item:
      item = {
        "name": name,
        "price": data['price']
      }
      items.append(item)
      return item, 201
    return {"message": "Item with same name already exists"}, 400

  def delete(self, name):
    global items
    items = next(filter(lambda x: x['name'] != name, items))
    return {"message": "Item deleted"}

  def put(self, name):
    data = self.parser.parse_args()
    item = next(filter(lambda x: x['name'] == name, items), None)
    if not item:
      item = {
        "name": name,
        "price": data['price']
      }
      items.append(item)
      return item, 201
    item.update(data)
    return item


class ItemList(Resource):
  def get(self):
    return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
