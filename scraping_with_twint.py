import twint
import pandas as pd

c = twint.Config()

c.search = ['Liz Truss']

c.Search = ['Liz Truss']                # Topic
# c.Pandas = True
# c.Location = True
c.Near = "Loughborough"
# c.Custom_csv = ["id", "user_id", "username", "date", "tweet"]
# c.Location = True
# c.Geo = '52.77129,-1.21470,100km'
c.Limit = 1000                           # Number of Tweets to scrape
c.Store_csv = True                      # Store tweets in a csv file
c.Output = "twint_scraping_tweets.csv"  # Path to csv file

twint.run.Search(c)

# c.Username = "jakesnaps"
# c.Store_csv = True
# c.Output = "test.csv"
#
# twint.run.Lookup(c)