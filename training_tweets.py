from tweet import Tweet
import json
from language_data import Language
import copy


def vocabulary_initial(vocab, size, smothing):
    input_file = open("./OriginalDataSet/training-tweets.txt", "r")
    list_all = []
    for line in input_file:
        [tweet_id,user_name ,language, text] = line.split('\t')
        tweet = Tweet(tweet_id,user_name ,language, text.strip('\n'))
        list_all.append(tweet)
    n_gram_all = n_gram(list_all, vocab, size)
    for k in n_gram_all:
        n_gram_all[k] = smothing

    return n_gram_all


def merge_dict(d1, d2):
    merged = copy.copy(d1)
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
            language[i].lower_case()
        elif vocab == 1:
            language[i].case_sensitive()
        elif vocab == 2:
            language[i].is_alpha()
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

    c_eu = 0
    c_ca = 0
    c_gl = 0
    c_es = 0
    c_pt = 0
    c_en = 0

    input_file = open("./OriginalDataSet/training-tweets.txt", "r")

    for line in input_file:
        count += 1

        [tweet_id,user_name ,language, text] = line.split('\t')
        tweet = Tweet(tweet_id,user_name ,language, text.strip('\n'))
        if language == 'eu':
            c_eu += 1
            eu_list.append(tweet)
        elif language == 'ca':
            c_ca += 1
            ca_list.append(tweet)
        elif language == 'gl':
            c_gl += 1
            gl_list.append(tweet)
        elif language == 'es':
            c_es += 1
            es_list.append(tweet)
        elif language == 'pt':
            c_pt += 1
            pt_list.append(tweet)
        elif language == 'en':
            c_en += 1
            en_list.append(tweet)

    eu = n_gram(eu_list, vocab, size)
    ca = n_gram(ca_list, vocab, size)
    gl = n_gram(gl_list, vocab, size)
    es = n_gram(es_list, vocab, size)
    pt = n_gram(pt_list, vocab, size)
    en = n_gram(en_list, vocab, size)

    n_gram_init = vocabulary_initial(vocab, size,smoothing)

    eu_t = merge_dict(n_gram_init, eu)
    ca_t = merge_dict(n_gram_init, ca)
    gl_t = merge_dict(n_gram_init, gl)
    es_t = merge_dict(n_gram_init, es)
    pt_t = merge_dict(n_gram_init, pt)
    en_t = merge_dict(n_gram_init, en)

    print(count, 'eu',c_eu,'ca' ,c_ca, 'gl',c_gl, 'pt',c_pt,'es', c_es,'en', c_en)
    eu_p  = c_eu/count
    ca_p  = c_ca/count
    gl_p  = c_gl/count
    pt_p  = c_pt/count
    es_p  = c_es/count
    en_p  = c_en/count

    input_file.close()
    return [eu_t, eu_p], [ca_t, ca_p], [gl_t,gl_p], [es_t,es_p], [pt_t,pt_p], [en_t,en_p]
