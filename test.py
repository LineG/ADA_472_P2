from tweet import Tweet
from n_gram import N_Gram
from language import Language

size = 2
vocab = 2
smoothing = 0.3

in_file1 = "./OriginalDataSet/training-tweets.txt"
n_gram = N_Gram(in_file1, size, vocab, smoothing)
[uni, bi, tri] = n_gram.count()

tweets = []

right = 0
wrong = 0

eu = Language('eu',uni['eu'],bi['eu'],tri['eu'])
es = Language('es',uni['es'],bi['es'],tri['es'])
pt = Language('pt',uni['pt'],bi['pt'],tri['pt'])
en = Language('en',uni['en'],bi['en'],tri['en'])
ca = Language('ca',uni['ca'],bi['ca'],tri['ca'])
gl = Language('gl',uni['gl'],bi['gl'],tri['gl'])


eu.cal_conditional_probabilities(size, smoothing)
es.cal_conditional_probabilities(size, smoothing)
pt.cal_conditional_probabilities(size, smoothing)
en.cal_conditional_probabilities(size, smoothing)
ca.cal_conditional_probabilities(size, smoothing)
gl.cal_conditional_probabilities(size, smoothing)

in_file2 = "./OriginalDataSet/test-tweets-given.txt"
input_file = open(in_file2, "r")

for line in input_file:
    try:
        [tweet_id,user_name ,language, text] = line.split('\t')
        tweets.append(Tweet(tweet_id,user_name ,language, text.strip('\n')))
    except:
        print('ERROR reading file')
input_file.close()

debug = 0
for tweet in tweets:
    try:
        if vocab == 0:
            tweet.lower_case()
        elif vocab == 1:
            tweet.case_sensitive()
        elif vocab == 2:
            tweet.is_alpha()
        tweet.counter()

        count = {}
        if size == 1:
            count = tweet.uni
        elif size == 2:
            count = tweet.bi
        elif size == 3:
            count = tweet.tri

        score = {}

        score['eu'] = eu.score(count)
        score['es'] = es.score(count)
        score['ca'] = ca.score(count)
        score['gl'] = gl.score(count)
        score['pt'] = pt.score(count)
        score['en'] = en.score(count)

        estimate_l = max(score, key=score.get)

        if debug < 0:
            print(tweet.tweet_id)
            print(score)
            print(estimate_l, tweet.language)

        if estimate_l == tweet.language:
            right += 1
        else:
            wrong += 1

        debug+=1
    except:
        print('ERROR calculating score')


print('right: ',(right/(right+wrong))*100,'%')
print('wrong: ',(wrong/(right+wrong))*100,'%')