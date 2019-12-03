from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Datarequired
from wtforms import RadioField
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# Class for simple radio button form
class SimpleForm(Form):
  example = RadioField('Label', choices=[('value', 'description'),('value_two', 'whatever')])

  @app.route('/', methods=['post', 'get'])
  def hello():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
      name=requesr.form['name']
      print name
    
  return render_template('actions.html', form = form)


