from db import db


class ItemModel(db.Model):
  __tablename__ = 'items'

  name = db.Column(db.String(80), primary_key = True)
  price = db.Column(db.Float(precision=2))
  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
  store = db.relationship('StoreModel')

  def __init__(self, name, price, store_id):
    self.name = name
    self.price = price
    self.store_id = store_id

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  def json(self):
    return {'name': self.name, 'price': self.price}

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def remove_from_db(self):
    db.session.delete(self)
    db.session.commit()
