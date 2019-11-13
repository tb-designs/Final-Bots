import tweepy
import json


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

  print(tmp)
# end get_tweets







###########################################################################
#TESTING

if __name__ == "__main__":

  #Import Twitter credentials from .json file
  with open("twitter_credentials.json", "r") as read_credentials:
    credentials = json.load(read_credentials)

  #test the get_tweets function here

  print("\nColor Parrot!\n")
  get_tweets("@color_parrot", 2)
  print("Genrenator!\n")
  get_tweets("@genrenator", 2)