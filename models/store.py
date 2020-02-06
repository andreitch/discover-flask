from db import db
from models.item import ItemModel


class StoreModel(db.Model):
  __tablename__ = 'stores'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True)
  items = db.relationship('ItemModel')

  def json(self):
    return {'id': self.id, 'name': self.name, 'items': [
      {'name': item.name, 'price': item.price} for item in self.items
    ]}

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.get(_id)

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def remove_from_db(self):
    db.session.delete(self)
    db.session.commit()