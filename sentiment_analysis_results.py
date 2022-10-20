class SentimentAnalysisResults:
    def __init__(self, positive: float, neutral: float, negative: float):
        self.positive = positive
        self.neutral = neutral
        self.negative = negative
        self.majority = self.__calculate_majority()

    def __repr__(self):
        return f"MAJORITY = {self.majority} (Positive: {self.positive}, Neutral: {self.neutral}, " \
               f"Negative: {self.negative})"

    def __calculate_majority(self):
        if (self.positive >= self.neutral) and (self.positive >= self.negative):
            return "Positive"
        elif (self.neutral >= self.positive) and (self.neutral >= self.negative):
            return "Neutral"
        else:
            return "Negative"
