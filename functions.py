# This file contains functions needed for different types of in game calculations

#imports
import classes
import db

###########################################################################
# get_turn_order()
# 
# Returns an array of the turn order based on the 
# current stats of each player and the boss. This is used at the beginning
# of each turn.
#
# NOTE: noSQL approach only being used as a placeholder until the
#       database code is up and running
###########################################################################
def get_turn_order(players, boss):
  p1 = players[0]
  p2 = players[1]

  character_array = [p1, p2, boss]
  turn_order = []
  # Sort based on character speed
  set fastest_spd = 0
  while len(character_array) != 0:
    fastest_spd = 0
    fastest_character = ''
    for character in character_array:
      if character.speed >= fastest_spd:
        fastest_spd = character.speed
        fastest_character = character
    
    turn_order.append(character)

  return turn_order
# end get_turn_order()

###########################################################################
# display_health()
##########################################################################
def display_health(players, boss):
  p1 = players[0]
  p2 = players[1]

  print("P1 Health:", p1.health)
  print("P2 Health:", p2.health)
  print("Boss Health:", boss.health)
#end display_health()

###########################################################################
# health_check()
###########################################################################
def health_check(players, boss):
  p1 = players[0]
  p2 = players[1]

  if boss.health <= 0:
    win_state()
  elif (p1.health and p2.health) <= 0:
    lose_state()
  
###########################################################################
# win_state()
###########################################################################
def win_state(boss):
  win_string1 = "Congrats! You've slain"
  win_string2 = "The people can now rest easy" # TODO use Extra1 bot to give random text here
  print(win_string1, boss.name, win_string2)
  teardown() #TODO define the teardown function once have a better grasp of Flask

###########################################################################
# lose_state()
###########################################################################
def lose_state(boss):
  win_string1 = "YOU DIED,"
  win_string2 = "has slain you. The townsfolk are next!" #TODO use Extra1 bot to give random text here
  print(win_string1, boss.name, win_string2)
  teardown() #TODO define the teardown function once have a better grasp of Flask