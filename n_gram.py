from tweet import Tweet
from language import Language
from copy import copy
import json

class N_Gram:
    def __init__(self,in_file, size, vocab, smoothing):
        self.in_file = in_file
        self.size = size
        self.vocab = vocab
        self.smoothing = smoothing
        self.tweets = []
        self.char_set = []
        self.uni_gram = {}
        self.bi_gram = {}
        self.tri_gram = {}

    def parse_input(self):
        input_file = open(self.in_file, "r")

        for i in range(97,123):
            if chr(i) not in self.char_set:
                self.char_set.append(chr(i))

        if self.vocab > 0:
            for i in range(65,91):
                if chr(i) not in self.char_set:
                    self.char_set.append(chr(i))

        for line in input_file:
            [tweet_id,user_name ,language, text] = line.split('\t')
            self.tweets.append(Tweet(tweet_id,user_name ,language, text.strip('\n')))
            if self.vocab > 1:
                for char in text:
                    if char not in self.char_set:
                        if char.isalpha():
                            self.char_set.append(char)
        input_file.close()

    def build_n_gram(self):
        s = len(self.char_set)
        c = self.char_set

        g = {}
        for i in range(s):
            g[c[i]] = 0
        self.uni_gram = g

        g = {}
        for i1 in range(s):
            for i2 in range(s):
                i = c[i1]+c[i2]
                g[i] = 0
        self.bi_gram = g

        g = {}
        for i1 in range(s):
            for i2 in range(s):
                for i3 in range(s):
                    i = c[i1]+c[i2]+c[i3]
                    g[i] = 0
        self.tri_gram = g

    def count(self):
        self.parse_input()
        self.build_n_gram()

        language_uni_gram = {'eu':copy(self.uni_gram), 'pt':copy(self.uni_gram), 'gl':copy(self.uni_gram), 'en':copy(self.uni_gram), 'es':copy(self.uni_gram), 'ca':copy(self.uni_gram)}
        language_bi_gram = {'eu':copy(self.bi_gram), 'pt':copy(self.bi_gram), 'gl':copy(self.bi_gram), 'en':copy(self.bi_gram), 'es':copy(self.bi_gram), 'ca':copy(self.bi_gram)}
        language_tri_gram = {'eu':copy(self.tri_gram), 'pt':copy(self.tri_gram), 'gl':copy(self.tri_gram), 'en':copy(self.tri_gram), 'es':copy(self.tri_gram), 'ca':copy(self.tri_gram)}


        for tweet in self.tweets:
            if self.vocab == 0:
                tweet.lower_case()
            elif self.vocab == 1:
                tweet.case_sensitive()
            elif self.vocab == 2:
                tweet.is_alpha()
            tweet.counter()

            for k in tweet.uni:
                l = language_uni_gram[tweet.language]
                l[k] += tweet.uni[k]

            for k in tweet.bi:
                l = language_bi_gram[tweet.language]
                l[k] += tweet.bi[k]

            for k in tweet.tri:
                l = language_tri_gram[tweet.language]
                l[k] += tweet.tri[k]

        return language_uni_gram, language_bi_gram, language_tri_gram



# in_file = "./OriginalDataSet/training-tweets.txt"

# n_gram = N_Gram(in_file, 2, 1, 0.1)
# [uni, bi, tri] = n_gram.count()

# with open("n_gram.json", 'w') as f:
#     json.dump(bi['eu'], f)

# line = '439379404574453760	aritzabrodes	es	@AnderDelPozo @PesqueWhite hahaha yo tambien me he quedao pillao ahahha'
# [tweet_id,user_name ,language, text] = line.split('\t')
# t = Tweet(tweet_id,user_name ,language, text.strip('\n'))
# t.case_sensitive()
# t.counter()
# d = t.bi

# es = Language('es',uni['es'],bi['es'],tri['es'])
# es.cal_conditional_probabilities(2, 0.1)
# print(es.score(d))

# ca = Language('ca',uni['ca'],bi['ca'],tri['ca'])
# ca.cal_conditional_probabilities(2, 0.1)
# print(ca.score(d))
