import twint
import csv
from tweet import Tweet


def reset_csv(filename, header):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)


output_file_name = "twint_csv_output.csv"
csv_header = ['date', 'time', 'username', 'tweet', 'place', 'geo']
reset_csv(output_file_name, csv_header)

c = twint.Config()

# c.Username = "JakeSnaps"
c.Search = ['lang:en Liz Truss']
c.Retweets = False
# c.Location = True
# c.Near = "Swindon"
# c.Geo = '52.77129,-1.21470,10000km'
c.Limit = 20                           # Number of Tweets to scrape
c.Store_csv = True                       # Store tweets in a csv file
c.Custom["tweet"] = ["date", "time", "username", "tweet", "place", "geo"]
c.Output = output_file_name   # Path to csv file
c.Hide_output = True
twint.run.Search(c)

Tweet.instantiate_from_csv(output_file_name)

print(f"\nNumber of Tweets = {len(Tweet.allTweets)}")
for tweet in Tweet.allTweets:
    print(tweet)
