import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from models import db


DATABASE = 'database.db'

#create db
def create_db():
    try:
        db.create_all()
    except:
        print("Could not create db!")
        return False
    return True

#open db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print("Got database!")
    return db

#close db connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# initialize database
def init_db():
    with current_app.app_context():
        db = get_db()
        with current_app.open_resource('database.db', mode='r') as f:
            file = f.read()
            db.cursor().executescript(file)
        db.commit()

# init app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

#create connection
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
    return conn

#create table
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
#class Character(db.Model):
#  id = db.Column(db.Integer, primary_key=True)
#  title = db.Column(db.String(64), index=True, unique=True)
#  health = db.Column(db.Integer)
#  pwr = db.Column(db.Integer)
 # spd = db.Column(db.Integer)
  #intel = db.Column(db.Integer)

  #def __repr__(self):
   # return '<Character {}>'.format(self.title)

#class Actions(db.Model):
 # id = db.Column(db.Integer, primary_key=True)
  #p_action = db.Column(db.String(64), index=True)
  #b_action = db.Column(db.String(64), index=True)
#create character
def create_character(conn, character):
    """
    Create a new character
    :param title:
    :param health:
    :param pwr:
    :param spd:
    :param intel:
    :return:
    """

    sql = ''' INSERT INTO Character(title,health,pwr,spd,intel)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, character)
    return cur.lastrowid

#update record
def update_record(conn, sql):
  c = conn.cursor()
  c.execute(sql)
  conn.commit()

#query db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# create CLI command to init the database
@click.command('init-db')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')
