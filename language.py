from math import log10

class Language:
    def __init__(self, iso, uni, bi, tri):
        self.iso = iso
        self.uni = uni
        self.bi = bi
        self.tri = tri
        self.conditional_probabilities = {}


    def cal_conditional_probabilities(self, size, smoothing):
        if size == 1:
            N = 0
            for k in self.uni:
                N += self.uni[k]
            den = N + (len(self.uni) * smoothing)

            for k in self.uni:
                f = (self.uni[k]+smoothing)/den
                self.conditional_probabilities[k] = log10(f)

        elif size == 2:
            N = 0
            for k in self.bi:
                N += self.bi[k]
            den = N + (len(self.bi) * smoothing)

            for k in self.bi:
                f = (self.bi[k]+smoothing)/den
                self.conditional_probabilities[k] = log10(f)

        elif size == 3:
            N = 0
            for k in self.tri:
                N += self.tri[k]
            den = N + (len(self.tri) * smoothing)

            for k in self.tri:
                f = (self.tri[k]+smoothing)/den
                self.conditional_probabilities[k] = log10(f)

    def score(self, tweet_data):
        score = 0
        for k in tweet_data:
            if k in self.conditional_probabilities:
                for i in range(tweet_data[k]):
                    score += self.conditional_probabilities[k]

        return score

