from tweet import Tweet
import json
from language_data import Language

def vocabulary_initial(V):
    vocab = []
    if V == 0:
        vocab = [chr(n) for n in range(97,123)]

    elif V == 1:
        vocab = [chr(n) for n in range(65,123) if chr(n).isalpha()]

    elif V == 2:
        vocab = [chr(n) for n in range(65,383) if chr(n).isalpha()]

    return vocab

def n_gram_initial(vocab, smoothing, size):
    n_gram = {}

    if size == 1:
        for n in range(len(vocab)):
            n_gram[vocab[n]] = smoothing

    elif size == 2:
        for n1 in range(len(vocab)):
            for n2 in range(len(vocab)):
                s = vocab[n1]+vocab[n2]
                n_gram[s] = smoothing

    elif size == 3:
        for n1 in range(len(vocab)):
            for n2 in range(len(vocab)):
                for n3 in range(len(vocab)):
                    s = vocab[n1]+vocab[n2]+vocab[n3]
                    n_gram[s] = smoothing

    return n_gram

def merge_dict(d1, d2):
    merged = {}
    for k in d2:
        if k in d1:
            merged[k] = d1[k]+d2[k]
        else:
            merged[k] = d2[k]
    return merged

def n_gram(language, vocab, size):
    t = {}
    for i in range(len(language)):
        if vocab == 0:
            language[i].is_alpha()
        elif vocab == 1:
            language[i].case_sensitive()
        elif vocab == 2:
            language[i].lower_case()
        language[i].counter(size)
        t = merge_dict(t, language[i].count)
    return t

def input_parser(vocab, smoothing, size):
    count = 0

    eu_list = []
    ca_list = []
    gl_list = []
    es_list = []
    en_list = []
    pt_list = []

    input_file = open("./OriginalDataSet/training-tweets.txt", "r")

    for line in input_file:
        count += 1

        [tweet_id,user_name ,language, text] = line.split('\t')
        tweet = Tweet(tweet_id,user_name ,language, text.strip('\n'))
        if language == 'eu':
            eu_list.append(tweet)
        elif language == 'ca':
            ca_list.append(tweet)
        elif language == 'gl':
            gl_list.append(tweet)
        elif language == 'es':
            es_list.append(tweet)
        elif language == 'pt':
            pt_list.append(tweet)
        elif language == 'en':
            en_list.append(tweet)

    eu = n_gram(eu_list, vocab, size)
    ca = n_gram(ca_list, vocab, size)
    gl = n_gram(gl_list, vocab, size)
    es = n_gram(es_list, vocab, size)
    pt = n_gram(pt_list, vocab, size)
    en = n_gram(en_list, vocab, size)

    vocabulary = vocabulary_initial(vocab)
    n_gram_init = n_gram_initial(vocabulary, smoothing, size)

    eu = merge_dict(n_gram_init, eu)
    ca = merge_dict(n_gram_init, ca)
    gl = merge_dict(n_gram_init, gl)
    es = merge_dict(n_gram_init, es)
    pt = merge_dict(n_gram_init, pt)
    en = merge_dict(n_gram_init, en)

    return eu, ca, gl, es, pt, en


vocab = 1
smoothing = 0.3
size = 2

eu, ca, gl, es, pt, en = input_parser(vocab, smoothing, size)

language_eu = Language('eu',eu, smoothing)
language_es = Language('es',es, smoothing)

test = "442920689906221056	Malik_Dominguez	es	Llevo preparada desde las ocho de la mañana... ¿Que me ha pasado? Nunca me pasa esto..."
[tweet_id,user_name ,language, text] = test.split('\t')
test_tweet = Tweet(tweet_id,user_name ,language, text.strip('\n'))
test_tweet.case_sensitive()
test_tweet.counter(size)

print(language_eu.score(test_tweet.count))
print(language_es.score(test_tweet.count))

