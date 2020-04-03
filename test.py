from tweet import Tweet
from n_gram import N_Gram
from language import Language
from collections import Counter

size = 3
vocab = 1
smoothing = 0.1

in_file1 = "./OriginalDataSet/training-tweets.txt"
n_gram = N_Gram(in_file1, size, vocab, smoothing)
[uni, bi, tri] = n_gram.count()
language_count = n_gram.language_count

tweets = []

eu = Language('eu', uni['eu'], bi['eu'], tri['eu'])
es = Language('es', uni['es'], bi['es'], tri['es'])
pt = Language('pt', uni['pt'], bi['pt'], tri['pt'])
en = Language('en', uni['en'], bi['en'], tri['en'])
ca = Language('ca', uni['ca'], bi['ca'], tri['ca'])
gl = Language('gl', uni['gl'], bi['gl'], tri['gl'])


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
        [tweet_id, user_name, language, text] = line.split('\t')
        tweets.append(Tweet(tweet_id, user_name, language, text.strip('\n')))
    except:
        print('ERROR reading file')
input_file.close()


overall_result = Counter()
language_result = {'eu': Counter(), 'ca': Counter(), 'gl': Counter(), 'es': Counter(), 'en': Counter(), 'pt': Counter()}
debug = 0

with open(f'ModifiedDataSet/trace_{vocab}_{size}_{smoothing}.txt','w') as csvfile:
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

            score['eu'] = eu.score(count, language_count)
            score['es'] = es.score(count, language_count)
            score['ca'] = ca.score(count, language_count)
            score['gl'] = gl.score(count, language_count)
            score['pt'] = pt.score(count, language_count)
            score['en'] = en.score(count, language_count)

            estimate_l = max(score, key=score.get)
            estimate_s = max(score, key = lambda s: score[s])
            if debug < 0:
                print(tweet.tweet_id)
                print(score)
                print(estimate_l, tweet.language)

            if estimate_l == tweet.language:
                overall_result['right'] += 1
                language_result[tweet.language]['right'] += 1
            else:
                overall_result['wrong'] += 1
                language_result[tweet.language]['wrong'] += 1

                correct_wrong = 'correct' if estimate_l == tweet.language else 'wrong'
                csvfile.write(f'{tweet.tweet_id}  {estimate_l}  {score[estimate_s]}  {tweet.language}  {correct_wrong}\n')

            debug += 1
        except:
            print('ERROR calculating score')

# print(language_result)
print('right: ', (overall_result['right']/sum(overall_result.values()))*100, '%')
print('wrong: ', (overall_result['wrong']/sum(overall_result.values()))*100, '%')
