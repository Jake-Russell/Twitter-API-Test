import csv
from datetime import datetime
from sentiment_analysis_results import SentimentAnalysisResults


class Tweet:
    allTweets = []

    def __init__(self, date_time: datetime, username: str, text: str, location: str,
                 results: SentimentAnalysisResults = None):
        self.date_time = date_time
        self.username = username
        self.text = text
        self.location = location
        self.results = results

        Tweet.allTweets.append(self)

    def __repr__(self):
        return f"{self.date_time}, {self.username}, {self.text}, {self.location}"

    @classmethod
    def instantiate_from_csv(cls, file: str):
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            tweets = list(reader)

        for tweet in tweets:
            date_time = datetime.fromisoformat(f"{tweet.get('date')} {(tweet.get('time'))}")

            Tweet(
                date_time=date_time,
                username=tweet.get('username'),
                text=cls.__preprocess(tweet.get('tweet')),
                location=tweet.get('place')
            )

    @staticmethod
    def __preprocess(text):
        new_text = []

        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)
