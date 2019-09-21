from nltk.tokenize import word_tokenize
import re

class Letter:
    def __init__(self, writer, addressee, year, language, text, index):
        self.writer = writer
        self.addressee = addressee
        self.year = year # this is an int
        self.language = language
        self.text = text
        self.total_word_count = 0
        self.set_total_word_count()
        self.index = index

    def get_writer(self):
        return self.writer

    def get_addressee(self):
        return self.addressee

    def get_year(self):
        return self.year

    def get_language(self):
        return self.language

    def get_text(self):
        return self.text

    def set_total_word_count(self):
        self.total_word_count = len([word for word in word_tokenize(self.text) if word.isalnum()])

    def get_total_word_count(self):
        return self.total_word_count

    def get_raw_count(self, search_term, case_sensitive):
        if case_sensitive:
            return len(re.findall(search_term, self.text))
        else:
            return len(re.findall(search_term, self.text, re.I))