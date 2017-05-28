from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

#MONGO_HOST = 'mongodb://localhost/twitterdb'  # assuming you have mongoDB installed locally
#MONGO_HOST = 'mongodb://52.14.253.82/twitterdb'  # assuming you have mongoDB installed locally
#MONGO_HOST = 'mongodb://52.15.217.66/twitterdb'  # assuming you have mongoDB installed locally
MONGO_HOST = 'mongodb://52.15.122.180/twitterMessagesDocker'  # assuming you have mongoDB installed locally



WORDS = ['Docker']

CONSUMER_KEY = "ZQgLcreyMzsX1HwrvieDTm0vL"
CONSUMER_SECRET = "RxwTndNp83ouLalJEeoDcqjOcISTC2Di9xjnRrBlM00Fe4c8VC"
ACCESS_TOKEN = "867459469881602048-JK0kdrdhwh2BQoxMDk2MjYQt5QagFOI"
ACCESS_TOKEN_SECRET = "IjSQx2RH5r6HsbT5eArJqs9cSlffAvYT27nYLv7BCT6fx"

class StreamListener(tweepy.StreamListener):
    # This is a class provided by tweepy to access the Twitter Streaming API.

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False

    def on_data(self, data):
        # connects to mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)

            # Use twitterMessagesDocker database. If it doesn't exist, it will be created.
            db = client.twitterMessagesDocker

            # Decode the JSON from Twitter
            datajson = json.loads(data)

            # grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))

            # insert the data into the mongoDB into a collection called twitterMessagesDocker
            # if twitterMessagesDocker doesn't exist, it will be created.
            #b.create_collection('twitterMessagesDocker', capped=True, size=5242880, max=20)

            db.twitterMessagesDocker.insert(datajson)
            
        except Exception as e:
            print(e)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
