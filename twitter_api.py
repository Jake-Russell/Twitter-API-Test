import tweepy
import requests
import configparser
import pandas as pd

# Read Configs
from tweet import Tweet

config = configparser.ConfigParser()
config.read('config.ini')

bearer_token = config['twitter']['bearer_token']

client = tweepy.Client(bearer_token=bearer_token,
                       return_type=requests.Response,
                       wait_on_rate_limit=True)

required_query_parameters = "lang:en -is:retweet"

user_query = input("Enter the query: ")
print("Now searching Twitter for Tweets with the following query: " + user_query)

query = user_query + " " + required_query_parameters
number_of_results = 100
# query = 'from:jake_russell123'

tweets = client.search_recent_tweets(query=query,
                                     tweet_fields=['author_id', 'created_at', 'geo'],
                                     expansions=['geo.place_id', 'author_id'],
                                     place_fields=['contained_within', 'country', 'country_code', 'full_name',
                                                   'id', 'name', 'place_type'],
                                     user_fields=['location', 'description'],
                                     max_results=number_of_results)

# Save data as a dictionary
tweets_dict = tweets.json()

for data in tweets_dict['data']:
    author_id = data['author_id']
    try:
        place_id = data['geo']['place_id']
    except KeyError:
        place_id = "n/a"
    username = ""
    location = ""

    # Extract Author Username
    for user in tweets_dict['includes']['users']:
        if user['id'] == author_id:
            username = user['username']

    # Extract Geolocation
    if place_id != "n/a":
        for place in tweets_dict['includes']['places']:
            if place['id'] == place_id:
                location = place['full_name']
                print("\n\nTHIS ONE HAS LOCATION!")
                print(f"{data['text']} - {location}\n\n")
    else:
        print("This Tweet has no geolocation data")
        location = place_id

    Tweet(data['text'], username, location)

for tweet in Tweet.allTweets:
    print(tweet)





# # Extract "data" value from dictionary
# has_tweet_data = True
# has_tweet_users = True
# has_tweet_places = True
#
# try:
#     tweets_data = tweets_dict['data']
# except KeyError:
#     print("No tweets matching: " + query)
#     has_tweet_data = False
#
# try:
#     tweets_users = tweets_dict['includes']['users']
# except KeyError:
#     print("No user data available for any of the returned tweets")
#     has_tweet_users = False
#
# try:
#     tweets_places = tweets_dict['includes']['places']
# except KeyError:
#     print("No location data available for any of the returned tweets")
#     has_tweet_places = False
#
# if has_tweet_data:
#     for data in tweets_dict['data']:
#         data_author_id = data['author_id']
#         if has_tweet_users:
#             for user in tweets_dict['includes']['users']:
#                 if user['id'] == data['author_id']:
#                     data['author_username'] = user['username']
#         if has_tweet_places:
#             try:
#                 for place in tweets_dict['includes']['places']:
#                     if place['id'] == data['geo']['place_id']:
#                         data['geo_name'] = place['full_name']
#             except KeyError:
#                 print("This tweet has no location data")
#                 data['geo_name'] = ''
#
#
#     # Transform to pandas Dataframe
#     df = pd.json_normalize(tweets_dict['data'])
#
#     df.to_csv("tweets.csv")
