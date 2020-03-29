from language_data import Language
from training_tweets import input_parser
from tweet import Tweet


vocab = 2
smoothing = 0.5
size = 3

eu, ca, gl, es, pt, en = input_parser(vocab, smoothing, size)
language_eu = Language('eu',eu,smoothing)
language_ca = Language('ca',ca,smoothing)
language_gl = Language('gl',gl,smoothing)
language_es = Language('es',eu,smoothing)
language_pt = Language('pt',pt,smoothing)
language_en = Language('en',en,smoothing)

right = 0
wrong = 0

input_file = open("./OriginalDataSet/test-tweets-given.txt", "r")
for test in input_file:
    try:
        [tweet_id,user_name ,language, text] = test.split('\t')
        test_tweet = Tweet(tweet_id,user_name ,language, text.strip('\n'))

        if vocab == 0:
            test_tweet.lower_case()
        elif vocab == 1:
            test_tweet.case_sensitive()
        elif vocab == 2:
            test_tweet.is_alpha()
        test_tweet.counter(size)

        score = {}

        score['eu'] = language_eu.score(test_tweet.count)
        score['es'] = language_es.score(test_tweet.count)
        score['ca'] = language_ca.score(test_tweet.count)
        score['gl'] = language_gl.score(test_tweet.count)
        score['pt'] = language_pt.score(test_tweet.count)
        score['en'] = language_en.score(test_tweet.count)

        estimate_l = max(score, key=score.get)

        if estimate_l == language:
            right += 1
        else:
            wrong += 1
    except:
        print("error reading line")

print(wrong)
print(right)