from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price', type=float, required=True, help="Can't be blank")

  @classmethod
  def find_by_name(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    result = cursor.execute("SELECT * FROM items WHERE name=?" \
      , (name,)).fetchone()

    connection.close()
    return result

  @classmethod
  def insert(cls, item):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    query = "INSERT INTO items VALUES(?,?)"
    cursor.execute(query, (item['name'], item['price']))
    connection.commit()
    connection.close()
    return {"message": "Item created"}, 201

  @jwt_required()
  def get(self, name):
    item = Item.find_by_name(name)
    if item:
      return {"item": item}
    return {"message": "Item not found"}, 404

  @jwt_required()
  def post(self, name):
    data = self.parser.parse_args()
    item = self.find_by_name(name)
    if item:
      return {"message": "Duplicate item name"}, 400
    else:
      return Item.insert({"name": name, "price": data['price']})

  @jwt_required()
  def delete(self, name):
    item = Item.find_by_name(name)
    if not item:
      return {"message": "Item not found"}, 404
    
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    query = "DELETE FROM items WHERE name=?"
    cursor.execute(query, (name,))
    connection.commit()
    connection.close()

    return {"message": "Item deleted"}

  @jwt_required()
  def put(self, name):
    data = self.parser.parse_args()
    item = self.find_by_name(name)
    if not item:
      return Item.insert({"name": name, "price": data['price']})

    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    query = "UPDATE items SET price=?"
    cursor.execute(query, (data['price'],))
    connection.commit()
    connection.close()

    return self.get(name)


class ItemList(Resource):
  @jwt_required()
  def get(self):
    items = []
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    query = "SELECT * FROM items"
    for item in cursor.execute(query).fetchall():
      items.append({"name": item[0], 'price': item[1]})
    return {"items": items}