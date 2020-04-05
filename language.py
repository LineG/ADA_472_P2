from math import log10
import json


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
                f = (self.uni[k] + smoothing) / den
                self.conditional_probabilities[k] = log10(f)

        elif size == 2:
            N = 0
            for k in self.bi:
                N += self.bi[k]
            den = N + (len(self.bi) * smoothing)

            for k in self.bi:
                f = (self.bi[k] + smoothing) / den
                self.conditional_probabilities[k] = log10(f)

        elif size == 3:
            N = 0
            for k in self.tri:
                N += self.tri[k]
            den = N + (len(self.tri) * smoothing)

            for k in self.tri:
                f = (self.tri[k] + smoothing) / den
                self.conditional_probabilities[k] = log10(f)

    def score(self, tweet_data, language_count):
        score = log10(language_count[self.iso] / sum(language_count.values()))
        for k in tweet_data:
            if k in self.conditional_probabilities:
                for i in range(tweet_data[k]):
                    score += self.conditional_probabilities[k]

        return score

    # dump conditional probabilities to JSON
    def export_model(self, vocab, size, smoothing):
        with open(f'models/model_{vocab}_{size}_{smoothing}_{self.iso}.txt', 'w') as model_file:
            for n_gram in self.conditional_probabilities.keys():
                model_file.write(f'"{n_gram}":  {self.conditional_probabilities[n_gram]}')


class ByomLanguage(Language):

    def __init__(self, iso, uni, bi, tri, adjustment):
        super().__init__(iso, uni, bi, tri)
        self.adjustment = adjustment

    def score(self, tweet_data, language_count, tweet):
        return super().score(tweet_data, language_count) + self.adjust_score(tweet)

    def adjust_score(self, tweet):
        return 0
        pass
