import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'user_key1'
  
  SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False