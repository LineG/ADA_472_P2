from tweet import Tweet
from n_gram import N_Gram
from language import Language
from collections import Counter
import os

size = 3
vocab = 2
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

eu.export_model(vocab, size, smoothing)
es.export_model(vocab, size, smoothing)
pt.export_model(vocab, size, smoothing)
en.export_model(vocab, size, smoothing)
ca.export_model(vocab, size, smoothing)
gl.export_model(vocab, size, smoothing)

in_file2 = "./OriginalDataSet/test-tweets-given.txt"
input_file = open(in_file2, "r", encoding="utf8")

for line in input_file:
    try:
        [tweet_id, user_name, language, text] = line.split('\t')
        tweets.append(Tweet(tweet_id, user_name, language, text.strip('\n')))
    except:
        print('ERROR reading file')
input_file.close()

overall_result = Counter()
language_result = {'eu': Counter(), 'ca': Counter(), 'gl': Counter(), 'es': Counter(), 'en': Counter(), 'pt': Counter()}
language_predictions = Counter()
debug = 0

if os.path.exists(f'ModifiedDataSet/trace_{vocab}_{size}_{smoothing}.txt'):
    os.remove(f'ModifiedDataSet/trace_{vocab}_{size}_{smoothing}.txt')
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
        estimate_s = score[estimate_l]

        if debug < 0:
            print(tweet.tweet_id)
            print(score)
            print(estimate_l, tweet.language)

        language_predictions[estimate_l] += 1
        if estimate_l == tweet.language:
            overall_result['right'] += 1
            language_result[tweet.language]['right'] += 1
        else:
            overall_result['wrong'] += 1
            language_result[tweet.language]['wrong'] += 1

        # Trace Output File
        with open(f'ModifiedDataSet/trace_{vocab}_{size}_{smoothing}.txt', 'a') as trace_file:
            correct_wrong = 'correct' if estimate_l == tweet.language else 'wrong'
            trace_file.write(f'{tweet.tweet_id}  {estimate_l}  {estimate_s:.2E}  {tweet.language}  {correct_wrong}\n')

        debug += 1
    except Exception as error_msg:
        print(f'ERROR calculating score: {error_msg}')

# Eval Output File
with open(f'ModifiedDataSet/eval_{vocab}_{size}_{smoothing}.txt', 'w') as eval_file:
    accuracy = round(overall_result['right'] / sum(overall_result.values()), 4)
    per_class_precision = []
    per_class_recall = []
    for language in language_result:
        per_class_precision.append(round(language_result[language]['right'] / language_predictions[language], 4)) if language_predictions[language] > 0 else per_class_precision.append(0)
        per_class_recall.append(round(language_result[language]['right'] / sum(language_result[language].values()), 4))
    per_class_f1 = [round((x * y) / (x + y), 2) if x > 0 or y > 0 else 0.0 for x, y in
                    zip(per_class_precision, per_class_recall)]
    macro_f1 = round(sum(per_class_f1) / len(per_class_f1), 4)

    weighted_f1 = 0
    for index, language in enumerate(language_result):
        weighted_f1 += sum(language_result[language].values()) * per_class_f1[index]
    weighted_f1 = round(weighted_f1 / sum(overall_result.values()), 4)

    eval_file.write(f'{accuracy}\n')
    eval_file.writelines(f'{c}  ' for c in per_class_precision)
    eval_file.write('\n')
    eval_file.writelines(f'{c}  ' for c in per_class_recall)
    eval_file.write('\n')
    eval_file.writelines(f'{c}  ' for c in per_class_f1)
    eval_file.write('\n')
    eval_file.write(f'{macro_f1}  {weighted_f1}')

print('right: ', (overall_result['right'] / sum(overall_result.values())) * 100, '%')
print('wrong: ', (overall_result['wrong'] / sum(overall_result.values())) * 100, '%')
