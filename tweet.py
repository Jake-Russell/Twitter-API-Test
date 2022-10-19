class Tweet:
    allTweets = []

    def __init__(self, text: str, username: str, location: str):
        self.text = text
        self.username = username
        self.location = location

        Tweet.allTweets.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.text}', {self.username}, {self.location})"
