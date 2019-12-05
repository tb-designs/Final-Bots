from flaskr.db_utils import create_db, get_db, create_character, init_db, create_connection
from forms import ActionsForm, CharacterForm
from flask_sqlalchemy import SQLAlchemy
from models import db as finalbots_db
from models import Character, Actions

import math
import random


######################################################################
# Function Name: random_boss_action()
#
# Purpose: Choose an action for the boss to perform this term.
#
# Parameters: N/A
#
# Returns: One of "attack", "block", or "ignore" strings
#
#

def random_boss_action():
  #List of possible boss actions
  actions = ["attack", "block", "ignore"]
  weighting = [0.4, 0.2, 0.4]
  boss_action =  random.choices(population=actions, weights=weighting, k=1)
  print("Boss has taken action:", boss_action[0])
  return boss_action[0]


######################################################################
# Function Name: get_turn_order()
#
# Purpose:  Establishes the damage calculation order based on the SPD
#           of each character.
#
# Parameters: N/A
#
# Returns: List of character titles from fastest to slowest
#
#

def get_turn_order():
  #Query the SQL database and return sorted list from fastest to slowest
  boss = Character.query.filter_by(title='boss').first()
  p1 = Character.query.filter_by(title='player1').first()

  turn_order = []
  print("Boss Speed:", boss.spd, "Player Speed:", p1.spd)
  if (boss.spd/10) > p1.spd:
    turn_order.append(boss.title)
    turn_order.append(p1.title)
  else:
    turn_order.append(p1.title)
    turn_order.append(boss.title)  

  turn_order.sort() #Sort lowest to highest
  new_order = [turn_order[1], turn_order[0]] #reverse
  print("The turn order is:", new_order)
  return new_order


######################################################################
# Function Name: update_health()
#
# Purpose: Updates the given characters health in its table entry. Also
#          checks if the characters health is now at or below 0.
#
# Parameters: char_name ------> Name of character whos health we want
#                               to update
#             health_reoved --> Integer amount of health to remove
#
# Returns: Boolean T/F value, False if new_health <= 0, True otherwise
#
#
def update_health(char_name, health_removed):
  #Get desired character from database
  character = Character.query.filter_by(title=char_name).first()
  #update that characters health and return true, false if health<0
  new_health = character.health - health_removed
  character.health = new_health
  finalbots_db.session.add(character)
  finalbots_db.session.commit()

  if(new_health <= 0):
    return False
  else:
    return True


######################################################################
# Function Name: player_dodge_check()
#
# Purpose: Decides if players Dodge succeeds or fails. Is weighted by
#          that players speed stat.
#
# Parameters: player_spd --> dictates the likelihood of a succesful dodge.
#
# Returns: Boolean T/F value, True if dodge is succesful, False otherwise.
#
#
# take player speed and normalize and randomly choose if dodged or not
# dodge chance is 50, 55, or 60% chance depending on character speed stat
def player_dodge_check(player_spd):
  dodge_chance = (player_spd/100) + 0.45
  hit_chance = 1-dodge_chance
  succesful_dodge =  random.choices(population=[True, False], weights=[dodge_chance, hit_chance], k=1)
  return succesful_dodge


######################################################################
# Function Name: boss_attack()
#
# Purpose: Modifier dictating the strength of the Boss' attack
#
# Parameters: boss_pwr_stat --> The PWR stat of the Boss. Decided
#                               during game initialization.
#
# Returns: New integer boss damage value.
#
#
def boss_attack(boss_pwr_stat):
  #reduces the boss's attack so player doesn't get one shot
  return int((boss_pwr_stat/100) + 10)


######################################################################
# Function Name: player_attack()
#
# Purpose: Modifier dictating the strength of the players attack
#
# Parameters: p1_pwr --------> The players PWR stat. Dictated by the chosen class.
#             boss_blocked --> Boolean T/F value True if Boss is currently blocking,
#                              False if boss is not blocking.
#
# Returns: New integer player damage amount.
#
#
def player_attack(p1_pwr, boss_blocked):
  if boss_blocked:
    p1_damage = 3
  else:
    p1_damage = p1_pwr
  return int(p1_damage)

######################################################################
# Function Name: turn_result()
#
# Purpose: Calculates the overall turn result based on the current table
#          information and the character turn order.
#
# Parameters: turn_list ----> List of character titles from fastest to slowest
#
# Returns: turn_status -----> Dictionary where the key = character title and
#                             the value = True/False if character is alive/dead
#
#          return_dialogue -> List of strings to display on the webpage that give
#                             what happened during the turn. 
#
#
def turn_result(turn_list):
  #get the boss and player tables
  boss = Character.query.filter_by(title='boss').first()
  p1 = Character.query.filter_by(title='player1').first()

  #get most recent actions from action table
  actions = Actions.query.order_by(Actions.id.desc()).first()

  print("Obtained most recent actions: Boss ->", actions.b_action, "Player ->", actions.p_action)

  #Array of dialogue to return
  return_dialogue = []
  #Assume no damage dealt this turn to begin
  boss_damage = 0
  player_damage = 0

  ##########################################################################
  # Basic Game Logic
  ##########################################################################

  # BOSS ATTACK
  if actions.b_action == 'attack':
    # PLAYER BLOCK
    if actions.p_action == 'block':
      return_dialogue.append("You courageously block the beasts advance! You took no damage this turn.")
    # PLAYER DODGE
    elif actions.p_action == 'dodge':
      #SUCCEFUL DODGE
      if(player_dodge_check(p1.spd)):
        return_dialogue.append("At the very last moment you jump out of the beasts way. You took no damage this turn.")
      # FAILED DODGE
      else:
        #Calculate damage dealt to player
        player_damage += boss_attack(boss.pwr)
        return_dialogue.append("You trip over your own feet attempting to dodge out of the way. The boss deals you ")
        return_dialogue.append(player_damage)
        return_dialogue.append("points of damage.")
    # PLAYER ATTACK
    elif actions.p_action == 'attack':
      #Calculate damage dealt to player and to boss
      boss_damage += player_attack(p1.pwr, False)
      player_damage += boss_attack(boss.pwr)          
      return_dialogue.append("You and the boss trade blows. You take ")
      return_dialogue.append(player_damage)
      return_dialogue.append("points of damage. The Boss takes ")
      return_dialogue.append(boss_damage)
      return_dialogue.append("points of damage.")

  # BOSS BLOCK
  elif actions.b_action == 'block':
    # PLAYER BLOCK
    if actions.p_action == 'block':
      return_dialogue.append("You and the boss circle each other with your guard up. No damage dealt this turn.")
    # PLAYER DODGE
    elif actions.p_action == 'dodge':
      return_dialogue.append("You dodge out of the way but the boss isn't even looking at you. No damage dealt this turn.")
    # PLAYER ATTACK
    elif actions.p_action == 'attack':
      boss_damage += player_attack(p1.pwr, True)
      return_dialogue.append("You charge furiously but the boss anticipates and blocks your attack! The boss takes 3 damage.")

  # BOSS IGNORE
  elif actions.b_action == 'ignore':
    # PLAYER BLOCK
    if actions.p_action == 'block':
      return_dialogue.append("You circle the boss. They don't seem to notice or care. No damage dealt this turn.")
    # PLAYER DODGE
    elif actions.p_action == 'dodge':
      return_dialogue.append("You dodge out of the way but the boss isn't even looking at you. No damage dealt this turn.")
    # PLAYER ATTACK
    elif actions.p_action == 'attack':
      boss_damage += player_attack(p1.pwr, False)
      return_dialogue.append("You charge furiously and take the boss by surprise! The boss takes")
      return_dialogue.append(boss_damage)
      return_dialogue.append("points of damage.")

  # Depending on fastest character, update health
  # updateHealth returns a bool
  PlayerIsAlive = update_health('player1', player_damage)
  BossIsAlive = update_health('boss', boss_damage)
  char_status_list = []

  # Create the results dictionary
  for character in turn_list:
    if character == 'boss':
      char_status_list.append(BossIsAlive)
    elif character == 'player1':
      char_status_list.append(PlayerIsAlive)

  turn_status = dict(zip(turn_list, char_status_list))

  #return dict displaying if characters are alive or not
  return turn_status, return_dialogue

