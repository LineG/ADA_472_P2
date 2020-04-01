from math import log

class Language:
    def __init__(self, iso, data, smoothing):
        self.smoothing = smoothing
        self.iso = iso
        self.data = data[0]
        self.vocab_len = 0
        self.conditional_probabilities = {}
        self.language_prob = log(data[1])
        self.cal_vocab_len()
        self.cal_conditional_probabilities()

    def cal_vocab_len(self):
        l = len(self.data)
        self.vocab_len = l + (l ** self.smoothing)

    def cal_conditional_probabilities(self):
        for k in self.data:
            f = self.data[k]/self.vocab_len
            self.conditional_probabilities[k] = log(f)

    def score(self, tweet_data):
        score = self.language_prob
        for k in tweet_data:
            if k in self.conditional_probabilities:
                for i in range(tweet_data[k]):
                    score += self.conditional_probabilities[k]
        return score

