# This file contains necessary class definitions for Final Bots

###########################################################################
# STATS
###########################################################################
class Stats:
  def __init__ (self, power, speed, int):
    self.power = 0
    self.speed = 0
    self.int   = 0
  # end init

  def set_player_stats(self, char_class, equip):
    if char_class not in ["Warrior", "Mage", "Thief"]:
      print("INVLAID CHARACTER CLASS found during stat seting")
      exit
    # Player stat init
    if char_class == "Warrior":
      self.power = 15
      self.speed = 10
      self.int   = 5
    elif char_class == "Mage":
      self.power = 5
      self.speed = 10
      self.int   = 15
    elif char_class == "Thief":
      self.power = 5
      self.speed = 15
      self.int   = 10   
  # end set_player_stats

  def getStat(self, stat_name):
    if stat_name not in ["power", "speed", "int"]:
      print("invalid stat name given when requesting character stats, exiting")
      exit
    else:
      return self.stat_name
  # end getStat
# end Stats

###########################################################################
# CHARACTER
###########################################################################
class Character:
  # Attributes
  previous_action = "none"
  current_action = "none"
  next_action = "none"
  status = 'idle'
  # Methods
  def __init__ (self):
    self.name = 'name'
    self.health = 100
    self.status = 'idle'
  # end init

  def changeStatus(self, newStatus):
    self.status = newStatus
  #end changeStatus
  
  def reduceHealth(self, damageAmount):
    self.health = (self.health - damageAmount)
    if self.health < 0:
      self.health = 0
  #end reduceHealth

###########################################################################
# BOSS
###########################################################################
class Boss(Character):
  # Default Boss Setup, different than Character
  def __init__ (self, name, colour, flavour, appearance):
    self.name = "BIG SCARY DEFAULT THING"
    self.colour = "DEFAULT COLOUR"
    self.flavour = "Here it comes, so default, never ending"
    self.appearance = "\O.o/"
    self.health = 1000

  def set_stats(self, name):
    #Boss stats based on name length
    print("Setting bos Stats")
    name_length = len(name)
    #print("name length:", name_length)
    if name_length <= 10:
      # Balanced Stats
      self.pwr = name_length * 10
      self.int = name_length * 10
      self.spd = name_length * 10
    elif name_length > 10:
      # High Int, Low Everything Else
      self.pwr = name_length * 10
      self.int = name_length
      self.spd = name_length
    else:
      print("Error! Could not set Boss characters stats")

###########################################################################
# CHARACTER
###########################################################################
class Player(Character):
  # Attributes
  char_class = ''
  #equip = ''

  # Methods
  # Default Player Setup, same as Character
  def __init__ (self):
    Character.__init__(self)
  # end init

  def set_stats(self, char_class):
    stat_obj = Stats.set_player_stats(char_class)
    self.pwr = stat_obj.pwr
    self.int = stat_obj.int
    self.spd = stat_obj.spd
  # end set_class

