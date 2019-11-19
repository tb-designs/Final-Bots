import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
  # create and configure the web application
  app = Flask(__name__, instance_relative_config=True)

  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # load instance config if not testing
    app.config.from_object(Config)
  else:
    #load the test config if passed in
    app.config.from_mapping(test_config)

  db = SQLAlchemy(app)
  from . import routes, models

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  #import authorization blueprint
  from . import start_page
  app.register_blueprint(start_page.bp)

  from . import db
  db.init_app(app)

  @app.teardown_appcontext
  def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

  return app