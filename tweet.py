import re

class Tweet:
    def __init__(self, tweet_id, user_name ,language, text):
        self.tweet_id = tweet_id
        self.user_name = user_name
        self.language = language
        self.strip_text = ''
        self.text = text
        #dividing the sentence into  1, 2 or 3 character string
        self.uni = {}
        self.bi = {}
        self.tri = {}

    # V = 0
    def lower_case(self):
        self.strip_text = re.sub(r'[^A-Za-z]', '*', self.text)
        self.strip_text = self.strip_text.lower()

    # V = 1
    def case_sensitive(self):
        self.strip_text = re.sub(r'[^A-Za-z]', '*', self.text)

    # V = 2
    def is_alpha(self):
        self.strip_text = ''
        for char in self.text:
            if char.isalpha():
                self.strip_text += char
            else:
                self.strip_text += '*'

    #helper function
    def add_key(self, k, count):
        if k in count:
            count[k] += 1
        else:
            count[k] = 1

    def counter(self):
        l  = len(self.strip_text)
        s = self.strip_text

        a = self.strip_text.replace('*','')
        for k in a:
            self.add_key(k, self.uni)

        for n in range(l-1):
            k = s[n]+s[n+1]
            if not '*' in k:
                self.add_key(k, self.bi)

        for n in range(l-2):
            k = s[n]+s[n+1]+s[n+2]
            if not '*' in k:
                self.add_key(k, self.tri)