from nltk.tokenize import word_tokenize
import re

class Letter:
    """
    Class for storing data for a single letter from the Queen Victoria Correspondence Corpus
    """
    def __init__(self, writer, addressee, year, language, text, index):
        # String containing the name of the writer
        self.writer = writer
        # String containing the name of the recipient
        self.addressee = addressee
        # String containing the year the letter was written
        self.year = year
        # String containing the language, 'en' is English and 'fr' is French
        self.language = language
        # String containing the entire text of the letter
        self.text = text
        # Total number of words in the letter
        self.total_word_count = 0
        self.set_total_word_count()
        # Index of the letter in the corpus
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
        """
        Computes the total number of words in the text of the letter. Only call this function after self.text is set
        :return: None
        """
        self.total_word_count = len([word for word in word_tokenize(self.text) if word.isalnum()])

    def get_total_word_count(self):
        return self.total_word_count

    def get_raw_count(self, search_term, case_sensitive):
        """
        Counts the number of times a word or phrase occurs in the text of the letter
        :param search_term: the word, phrase, or regular expression to search for
        :param case_sensitive: a Boolean indicating whether to use case sensitive or insensitive search
        :return: the number of matches
        """
        if case_sensitive:
            return len(re.findall(search_term, self.text))
        else:
            return len(re.findall(search_term, self.text, re.I))