from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np

tweet = "@JakeSnaps Today is cold @ home ☹️ https://jakerussell.photography"
# tweet = 'Great content! Subscribed! 😜'


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []

    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


tweet_processed = preprocess(tweet)
print(tweet_processed)

# Load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"
model = TFAutoModelForSequenceClassification.from_pretrained(roberta)

tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

# Sentiment Analysis
encoded_tweet = tokenizer(tweet_processed, return_tensors='tf')
output = model(encoded_tweet)
scores = output[0][0].numpy()
scores = softmax(scores)

# Sort Rankings
ranking = np.argsort(scores)
# Reverse Sort Order
ranking = ranking[::-1]
for i in range(len(scores)):
    label = labels[ranking[i]]
    score = scores[ranking[i]]
    print(f"{i+1}) {label} {np.round(float(score), 4)}")