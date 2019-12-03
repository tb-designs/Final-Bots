from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Character(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64), index=True, unique=True)
  desc = db.Column(db.String(240))
  name = db.Column(db.String(64))
  health = db.Column(db.Integer)
  pwr = db.Column(db.Integer)
  spd = db.Column(db.Integer)
  intel = db.Column(db.Integer)
  appearance = db.Column(db.String(240))

  def __repr__(self):
    return '<Character {}>'.format(self.title)

class Actions(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  p_action = db.Column(db.String(64), index=True)
  b_action = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<Action {}>'.format(self.p_action)