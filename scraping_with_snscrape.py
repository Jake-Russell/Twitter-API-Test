from time import time

import snscrape.modules.twitter as sntwitter
import pandas as pd
import twint

# loc = '34.052235, -118.243683, 10km'
# query = 'Rishi Sunak lang:en geocode:51.600882,-1.661890,25km'
#
# tweets = []
# limit = 50
# count = 0
#
# for tweet in sntwitter.TwitterSearchScraper(query).get_items():
#     count += 1
#     if len(tweets) == limit:
#         break
#     else:
#         tweets.append([tweet.date, tweet.user.username, tweet.rawContent, tweet.coordinates, tweet.user.location])
#         print("Tweet " + str(count))
#
# df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Coordinates', 'Location'])
# print(df)
# df.to_csv('snscrape_csv_output.csv', sep='\t')

# snscrape
snscrape_start_time = time()

tweets = []
query = 'Apple lang:en near:Loughborough within:50km'
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == 500:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.rawContent, tweet.coordinates, tweet.user.location])

pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Coordinates', 'Location']).to_csv('snscrape_csv_output.csv', sep='\t')

snscrape_end_time = time()
snscrape_total_time = snscrape_end_time - snscrape_start_time
print("Total time = " + str(snscrape_total_time))

# Twint
twint_start_time = time()

c = twint.Config()
c.Search = "Apple lang:en near:Loughborough within:50km"
c.Retweets = False
# c.Near = "Loughborough"
c.Limit = 500
c.Store_csv = True
c.Custom["tweet"] = ["date", "username", "tweet", "near"]
c.Output = "twint_output.csv"
c.Hide_output = True
twint.run.Search(c)

twint_end_time = time()
twint_total_time = twint_end_time - twint_start_time
print("Total time = " + str(twint_total_time))
