from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

# Radio button class

class ActionsForm(FlaskForm):
  """Radio Buttons saying which action to choose"""
  action = RadioField('Action', choices=[('attack', 'tough guy'), ('magic', 'smart guy'), ('dodge', 'sneaky guy')])
  submit = SubmitField('Submit')

class CharacterForm(FlaskForm):
  """Radio Buttons saying which class to choose"""
  character = RadioField('Action', choices=[('warrior', 'tough guy'), ('mage', 'smart guy'), ('thief', 'sneaky guy')])
  submit = SubmitField('Submit')
