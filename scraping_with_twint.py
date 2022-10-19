import twint

c = twint.Config()

# c.Username = "JakeSnaps"
c.Search = ['Liz Truss']
# c.Location = True
c.Near = "Swindon"
# c.Geo = '52.77129,-1.21470,10000km'
c.Limit = 1000                           # Number of Tweets to scrape
c.Store_csv = True                       # Store tweets in a csv file
c.Output = "twint_scraping_tweets.csv"   # Path to csv file

twint.run.Search(c)
