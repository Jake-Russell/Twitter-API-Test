from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import tweepy
import requests
import configparser

# Read Configs
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
number_of_results = 10
# query = 'from:jake_russell123'

tweets = client.search_recent_tweets(query=query,
                                     tweet_fields=['author_id', 'created_at', 'geo'],
                                     expansions=['geo.place_id', 'author_id'],
                                     place_fields=['contained_within', 'country', 'country_code', 'full_name',
                                                   'id', 'name', 'place_type'],
                                     max_results=number_of_results)


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []

    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


# Save data as a dictionary
tweets_dict = tweets.json()
processed_tweets = []
for tweet in tweets_dict['data']:
    processed_tweets.append(preprocess(tweet['text']))

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = TFAutoModelForSequenceClassification.from_pretrained(roberta)

tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']


def sentiment_analysis(text):
    # Sentiment Analysis
    encoded_tweet = tokenizer(text, return_tensors='tf')
    output = model(encoded_tweet)
    scores = output[0][0].numpy()
    scores = softmax(scores)

    # Sort Rankings
    ranking = np.argsort(scores)
    # Reverse Sort Order
    ranking = ranking[::-1]
    rankings = []
    for i in range(len(scores)):
        label = labels[ranking[i]]
        score = scores[ranking[i]]
        rankings.append([label, score])
    return rankings


positivity = []
for processed_tweet in processed_tweets:
    print(processed_tweet)

    rankings = sentiment_analysis(processed_tweet)
    for i in range(len(rankings)):
        print(f"{i+1}) {rankings[i][0]} {np.round(float(rankings[i][1]), 4)}")
        if rankings[i][0] == 'Positive':
            positivity.append(rankings[i][1])
    print("\n")

print(f"The average positivity for '{user_query}' is {np.round(float(np.mean(positivity)), 4)}")
