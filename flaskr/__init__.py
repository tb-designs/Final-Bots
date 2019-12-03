import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import db as finalbots_db


#Create Flask App
def create_app(test_config=None):
  # create and configure the web application
  app = Flask(__name__, instance_relative_config=True)

  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
  )
  #Grab config from config.py
  if test_config is None:
    # load instance config if not testing
    app.config.from_object(Config)
  else:
    #load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  #import authorization blueprint
  from . import final_bots
  app.register_blueprint(final_bots.bp)

  # Init the db, remove any previous table entries
  finalbots_db.init_app(app)
  with app.app_context():
    finalbots_db.create_all()

  return app