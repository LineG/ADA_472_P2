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

    def export_model(self, vocab, size, smoothing):
        with open(f'models/model_{vocab}_{size}_{smoothing}_{self.iso}.txt', 'w', encoding='utf8') as model_file:
            for n_gram in self.conditional_probabilities:
                model_file.write(n_gram + ' : ' + str(self.conditional_probabilities[n_gram]) + '\n')


class ByomLanguage(Language):

    def __init__(self, iso, uni, bi, tri, adjustment):
        super().__init__(iso, uni, bi, tri)
        self.adjustment = adjustment

    def score(self, tweet_data, language_count, tweet):
        return super().score(tweet_data, language_count) + self.adjustment * self.adjust_score(tweet)

    def adjust_score(self, tweet):
        bonus = 0
        for word in tweet.strip_text.replace('*', ' ').replace("  ", " ").split():
            bonus += self.check_characters_and_words(word.lower())
        return bonus
        pass

    def check_characters_and_words(self, word):
        bonus = 0
        if self.iso == 'eu':
            for syllable in ['tx', 'tz']:
                if syllable in word:
                    bonus += 10
            for letter in word:
                if letter in {'c', 'q', 'v', 'w'}:
                    bonus -= 5
            pass


        if self.iso == 'ca':
            if word in {'això', 'amb', 'mateix', 'tots'}:
                bonus += 100
            for letter in word:
                if letter in {'k', 'w'}:
                    bonus -= 10
            for ending in ['o', 'a', 'es', 'ció', 'tat']:
                if word[-len(ending):] == ending:
                    bonus += 10
            for syllable in ['tg', 'tx', 'aig', 'eig', 'oig', 'uig', 'aix', 'eix', 'oix', 'uix', 'l·l']:
                if syllable in word:
                    bonus += 10
            pass

        if self.iso == 'gl':
            if word in {'unha', 'o', 'os', 'a', 'as'}:
                bonus += 100
            if 'nh' in word or word[:-4] == 'ción':
                bonus += 10
            for letter in word:
                if letter in {'k', 'w', 'y'}:
                    bonus -= 10
            pass

        if self.iso == 'es':
            for letter in word:
                if letter in {'á', 'é', 'í', 'ó', 'ú', 'ñ'}:
                    bonus += 10
                if letter in {'ã', 'õ', 'â', 'ê', 'ô', 'à', 'ç'}:
                    bonus -= 10
            if "'" in word or "üg" in word:
                bonus -= 5
            if "gü" in word or\
                    word in {'el', 'del', 'los', 'la', 'las', 'uno', 'unos', 'una', 'unas', 'y'} or\
                        word[0:2] == 'll':
                bonus += 100
            for ending in [ 'o', 'a', 'ción', 'miento', 'dad']:
                if word[-len(ending):] == ending:
                    bonus += 10
            pass

        if self.iso == 'en':
            if word in {'a', 'an', 'and', 'in', 'of', 'on', 'the', 'that', 'to', 'is', 'I'}:
                bonus += 100
            for syllable in ['th', 'ch', 'sh', 'ough', 'augh']:
                if syllable in word:
                    bonus += 10
            for ending in ['ing', 'tion', 'ed', 'age', 's', '\'s', '\'ve', 'n\'t', '\'d']:
                if word[-len(ending):] == ending:
                    bonus += 10
            for letter in word:
                if letter in {'á', 'é', 'í', 'ó', 'ú', 'ñ', 'ã', 'õ', 'â', 'ê', 'ô', 'à', 'ç'}:
                    bonus -= 10
            pass

        if self.iso == 'pt':
            for letter in word:
                if letter in {'ã', 'õ', 'â', 'ê', 'ô', 'á', 'é', 'í', 'ó', 'ú', 'à', 'ç'}:
                    bonus += 10
                if letter in {'k', 'w', 'y'}:
                    bonus -= 5
            if word in {'a', 'à', 'e', 'é', 'o',
                        'ao', 'as', 'às', 'da', 'de', 'do', 'em', 'os', 'ou', 'um',
                        'aos', 'com', 'das', 'dos', 'ele', 'ela', 'mas', 'não', 'por', 'que', 'são', 'uma'}:
                bonus += 100
            for ending in ['ção', 'dade', 'ismo', 'mente']:
                if word[-len(ending):] == ending:
                    bonus += 10
            for syllable in ['ch', 'nh', 'lh']:
                if syllable in word:
                    bonus += 10
            pass
        return bonus
        pass

    def export_model(self, vocab, size, smoothing):
        with open(f'models/model_myModel_{self.iso}.txt', 'w', encoding='utf8') as model_file:
            for n_gram in self.conditional_probabilities:
                model_file.write(n_gram + ' : ' + str(self.conditional_probabilities[n_gram]) + '\n')
