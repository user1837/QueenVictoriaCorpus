import letter
import re

class Corpus:

    """This class stores all of the data for the corpus of Queen Victoria's correspondence"""

    def __init__(self, letters):
        # A list of Letter objects
        self.letters = letters
        # Total number of words in the corpus
        self.total_word_count = 0
        # A set of the writers in the corpus
        self.writers = set()
        # A set of the recipients in the corpus
        self.addressees = set()
        # A list of the years in the corpus
        self.years = set()

    def add_letter(self, l):
        self.letters.append(l)

    def compute_total_word_count(self):
        """
        Computes the total number of words in the corpus. Only call if self.letters is fully filled
        :return: the number of words in the corpus
        """
        assert len(self.letters) > 0
        self.total_word_count = sum([l.get_total_word_count() for l in self.letters])

    def set_writers(self):
        """
        Creates a set of the names of all the writers in the corpus. Only call if self.letters is fully filled
        :return: None
        """
        assert len(self.letters) > 0
        self.writers = set([i.get_writer() for i in self.letters])

    def add_writer(self, writer):
        self.writers.add(writer)

    def set_addressees(self):
        """
        Creates a set of the names of all the recipients in the corpus. Only call if self.letters is fully filled
        :return: None
        """
        assert len(self.letters) > 0
        self.addressees = set([i.get_addressee() for i in self.letters])

    def add_addressee(self, addressee):
        self.addressees.add(addressee)

    def set_years(self):
        """
        Creates a set of all the years in the corpus. Only call if self.letters is fuly filled.
        :return: None
        """
        assert len(self.letters) > 0
        self.years = set([i.get_year() for i in self.letters])

    def sort_years(self):
        """
        Converts the set of years to a list and sorts it in ascending order
        :return: None
        """
        self.years = list(self.years)
        self.years.sort()

    def add_year(self, year):
        self.years.add(year)

    def filter_letters(self, language='(en)|(fr)', writer='.*', addressee='.*', year='.*'):
        """
        Filters the corpus based on language, writer, addressee, and year
        :param language: a regular expression specifying the language of the letter
        :param writer: a regular expression specifying the writer(s) of the letter
        :param addressee: a regular expression specifying the addressee(s) of the letter
        :param year: a regular expression specifying the year(s) of the letter
        :return: a list of Letter objects that have the required language, writers, addressees, and years
        """
        return [i for i in self.letters if re.search(language, i.get_language(), re.I) and re.search(writer, i.get_writer(), re.I) and re.search(addressee, i.get_addressee(), re.I) and re.search(year, i.get_year(), re.I)]

    def create_subcorpus(self, language='(en)|(fr)', writer='.*', addressee='.*', year='.*'):
        """
        Create a new Corpus with a subset of the Letters from the original corpus
        :param language: a regular expression specifying the language of the letters
        :param writer: a regular expression specifying the writer(s) of the letters
        :param addressee: a regular expression specifying the addressee(s) of the letters
        :param year: a regular expression specifying the year(s) of the letters
        :return: a new Corpus object
        """
        filtered_letters = self.filter_letters(language, writer, addressee, year)
        if len(filtered_letters) == 0:
            raise Exception('No letters found for {0}, {1}, {2}, and {3}. Please enter different specifications.'.format(language, writer, addressee, year))
        subcorp = Corpus(filtered_letters)
        subcorp.compute_total_word_count()
        return subcorp

    def get_total_raw_count(self, search_term, case_sensitive):
        """
        Counts the number of times a word or phrase occurs in the corpus
        :param search_term: a word, phrase, or regular expression to search
        :param case_sensitive: a Boolean indicating whether to do case sensitive or insensitive search
        :return: the raw count of occurrences
        """
        return sum([l.get_raw_count(search_term, case_sensitive) for l in self.letters])

    def get_normalized_count(self, raw_count):
        """
        Computes the normalized count per 1000 words
        :param raw_count: the total number of occurrences of a word or phrase in the corpus
        :return: the normalized count
        """
        raw = raw_count / self.total_word_count * 1000
        return round(raw, 2)

    def name_to_regex(self, name):
        """
        Converts a name to a regular expression by replacing whitespace with '\s'
        :param name: string containing a name
        :return: string containing a regular expression
        """
        return re.sub('\s+', '\s+', name)

    def get_counts_by_category(self, search_term, case_sensitive, category, output_type):
        """
        Compute word or phrase frequency by category
        :param search_term: a word, phrase, or regular expression to search
        :param case_sensitive: a Boolean indicating whether to do case sensitive or insensitive search
        :param category: the category to search by (writer, addressee, or year)
        :param output_type: type of frequency to calculate (raw or normalized)
        :return: a sorted list of tuples, with the first element being a label within the category (name of the writer or recipient or the year) and the second being the frequency
        """
        counts_by_category = {}
        if category == 'writer':
            for w in self.writers:
                w_regex = self.name_to_regex(w)
                new_corp = self.create_subcorpus(writer=w_regex)
                raw = new_corp.get_total_raw_count(search_term, case_sensitive)
                counts_by_category[w] = raw if output_type == 'raw' else new_corp.get_normalized_count(raw)
        elif category == 'addressee':
            for a in self.addressees:
                a_regex = self.name_to_regex(a)
                new_corp = self.create_subcorpus(addressee=a_regex)
                raw = new_corp.get_total_raw_count(search_term, case_sensitive)
                counts_by_category[a] = raw if output_type == 'raw' else new_corp.get_normalized_count(raw)
        else:
            for y in self.years:
                new_corp = self.create_subcorpus(year=y)
                raw = new_corp.get_total_raw_count(search_term, case_sensitive)
                counts_by_category[y] = raw if output_type == 'raw' else new_corp.get_normalized_count(raw)

        return sorted([i for i in counts_by_category.items()], key=lambda x:x[0])

    def get_concordances(self, search_term, case_sensitive, context_len):
        """
        Finds a word or phrase and n context words before and after it
        :param search_term: a word, phrase, or regular expression to search
        :param case_sensitive: a Boolean indicating whether to do case sensitive or insensitive search
        :param context_len: the number of context words to get before and after the word/phrase
        :return: a list of concordance lines, each line containing n context words before the word/phrase, the word/phrase, and n context words after the word/phrase
        """
        concordance_lines = []
        for l in self.letters:
            if case_sensitive:
                results = re.finditer(search_term, l.get_text())
            else:
                results = re.finditer(search_term, l.get_text(), re.I)

            for i in results:
                pre_context = l.get_text()[0:i.start()]  # Gets a substring from the beginning of the file to the current
                # match's index
                prev_words = pre_context.split()
                prev_x_words = prev_words[-context_len:] if len(prev_words) >= context_len else prev_words
                pre = ' '.join(prev_x_words)
                post_context = l.get_text()[i.end():]  # Gets a substring from the first index after the current match to
                # the end of the file
                next_words = post_context.split()
                next_x_words = next_words[:context_len] if len(next_words) >= context_len else next_words
                post = ' '.join(next_x_words)
                concordance = '({0} to {1}, {2})\t{3}\t{4}\t{5}\n'.format(l.get_writer(), l.get_addressee(), l.get_year(), pre, i.group(0).upper(), post)
                concordance_lines.append(concordance)

        return concordance_lines