import tweepy
import json
import re
from classes import Character, Player, Boss

# array of bots to gather tweets from
# in order of [NAME, COLOUR, FLAVOUR, APPEARANCE, EXTRA1, EXTRA2]
BOT_ARRAY = [
  "@kaikkisanat",
  "@color_parrot",
  "@lovecraftmix",
  "@theasciiartbot",
  "@bot_teleport",
  "@carlomarxbot",
  ]

#Get Twitter credentials
with open("twitter_credentials.json", "r") as read_credentials:
  credentials = json.load(read_credentials)

###########################################################################
# get_tweets                                                              #
#                                                                         #
# params:                                                                 #
#   username         == twitter user whos tweets we want                  #
#   number_of_tweets == how many of the most recent tweets to retrieve    #
#                                                                         #
###########################################################################
def get_tweets(username, number_of_tweets):
  # Authorizing consumer key and consumer secret
  auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
  # Access users access key and access secret
  auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
  # Call API
  api = tweepy.API(auth)
  # Extract tweets
  tweets = api.user_timeline(screen_name = username, count=number_of_tweets)
  # Empty Array
  tmp = []
  # Create array of tweet information:
  # [username, tweetID, date/time, text]
  tweets_for_csv = [tweet.text for tweet in tweets] #create CSV file with the text only
  for j in tweets_for_csv:
    # Appending tweets to empty array
    tmp.append(j)
  #return the array of text
  return tmp
# end get_tweets

###########################################################################
# build_a_boss()
# 
# Returns  Boss objects to be used in the final game
# 
###########################################################################
def build_a_boss():
  #create a new Boss object
  new_boss = Boss
  # array will be in order of [NAME, COLOUR, FLAVOUR, APPEARANCE, EXTRA1, EXTRA2]
  attributes_array = []

  # get all needed info from Twitter
  try:
    for bot_name in BOT_ARRAY:
      attributes_array.append(get_tweets(bot_name, 1))

    print("Boss info aquired from twitter")
  except:
    print("Could not access Twitter, loading default boss setup")
    attributes_array.append("","","","")

  # parse array elements to get just the Tweet text
  name       = re.search(r'\[\'(.*)\'\]', str(attributes_array[0]), re.M|re.I )
  colour     = re.search(r'#(\D+)\s+#',   str(attributes_array[1]), re.M|re.I )
  flavour    = re.search(r'\[(.*)\]',     str(attributes_array[2]), re.M|re.I )
  appearance = re.search(r'\[\'(.*)\'\]', str(attributes_array[3]), re.M|re.I )

  #Add break tags in the appearance for insertion into html template
  #appearance = appearance.group(1).replace('\\n','<br>')
  #print(appearance)


  # using the gathered data, create the boss
  new_boss.name       = name.group(1)
  new_boss.colour     = colour.group(1)
  new_boss.flavour    = flavour.group(1)
  new_boss.appearance = appearance.group(1)

  print("Appearance:\n", new_boss.appearance)

  return new_boss


###########################################################################
#TESTING
###########################################################################
if __name__ == "__main__":

  #test the get_tweets function here
  Boss = build_a_boss()
  bs = [Boss.name, Boss.colour, Boss.flavour, Boss.appearance]
  look = Boss.appearance.split('\\n')

  for line in look:
    print (line)