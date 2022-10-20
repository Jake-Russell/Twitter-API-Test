import twint
import csv
from tweet import Tweet
from sentiment_analysis_results import SentimentAnalysisResults

from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np


def reset_csv(filename, header):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)


output_file_name = "twint_csv_output.csv"
csv_header = ['date', 'time', 'username', 'tweet', 'place', 'geo']
reset_csv(output_file_name, csv_header)

required_query_parameters = "lang:en"
user_query = input("Enter the query: ")
print("Now searching Twitter for Tweets with the following query: " + user_query)

c = twint.Config()
# c.Username = "JakeSnaps"
c.Search = [f"{required_query_parameters} {user_query}"]
c.Retweets = False
# c.Location = True
# c.Near = "Swindon"
# c.Geo = '52.77129,-1.21470,10000km'
c.Limit = 49                           # Number of Tweets to scrape
c.Store_csv = True                       # Store tweets in a csv file
c.Custom["tweet"] = ["date", "time", "username", "tweet", "place", "geo"]
c.Output = output_file_name   # Path to csv file
c.Hide_output = True
twint.run.Search(c)

Tweet.instantiate_from_csv(output_file_name)

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = TFAutoModelForSequenceClassification.from_pretrained(roberta)

tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']


def sentiment_analysis(tweet: Tweet):
    # Sentiment Analysis
    encoded_tweet = tokenizer(tweet.text, return_tensors='tf')
    output = model(encoded_tweet)
    scores = output[0][0].numpy()
    scores = softmax(scores)

    tweet.results = SentimentAnalysisResults(positive=np.round(float(scores[2]), 4),
                                             neutral=np.round(float(scores[1]), 4),
                                             negative=np.round(float(scores[0]), 4))


most_negative = 0
most_negative_tweet: Tweet
most_positive = 0
most_positive_tweet: Tweet

negative_count = 0
neutral_count = 0
positive_count = 0

tweet_count = 1

print(f"\nNumber of Tweets = {len(Tweet.allTweets)}")
for tweet in Tweet.allTweets:
    sentiment_analysis(tweet)
    print(f"Tweet number - {tweet_count}")
    tweet_count += 1

    if tweet.results.negative > most_negative:
        most_negative = tweet.results.negative
        most_negative_tweet = tweet

    if tweet.results.positive > most_positive:
        most_positive = tweet.results.positive
        most_positive_tweet = tweet

    if tweet.results.majority == "Negative":
        negative_count += 1
    elif tweet.results.majority == "Neutral":
        neutral_count += 1
    else:
        positive_count += 1

print("\n-----------------------------------------------------------------------------------"
      "-----------------------------------------------------------------------------------"
      "-----------------------------------------------------------------------------------")
print(f"😃 Total Number of Positive Tweets - {positive_count} "
      f"({np.round((positive_count/len(Tweet.allTweets))*100, 2)}%)")
print(f"😐 Total Number of Neutral Tweets - {neutral_count} "
      f"({np.round((neutral_count/len(Tweet.allTweets))*100, 2)}%)")
print(f"☹️ Total Number of Negative Tweets - {negative_count} "
      f"({np.round((negative_count/len(Tweet.allTweets))*100, 2)}%)")
print("-----------------------------------------------------------------------------------"
      "-----------------------------------------------------------------------------------"
      "-----------------------------------------------------------------------------------")

print(f"""😃 The most positive Tweet is: '{most_positive_tweet.text}' 
   By: @{most_positive_tweet.username}
   Positivity: {most_positive}""")

print(f"""
☹️ The most negative Tweet is: '{most_negative_tweet.text}' 
   By: @{most_negative_tweet.username}
   Negativity: {most_negative}""")


# positivity = []
# for processed_tweet in processed_tweets:
#     print(processed_tweet)
#
#     rankings = sentiment_analysis(processed_tweet)
#     for i in range(len(rankings)):
#         print(f"{i+1}) {rankings[i][0]} {np.round(float(rankings[i][1]), 4)}")
#         if rankings[i][0] == 'Positive':
#             positivity.append(rankings[i][1])
#     print("\n")
#
# print(f"The average positivity for '{user_query}' is {np.round(float(np.mean(positivity)), 4)}")