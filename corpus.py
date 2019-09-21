import letter
import re

class Corpus:

    def __init__(self, letters):
        self.letters = letters
        self.total_word_count = 0
        self.writers = set()
        self.addressees = set()
        self.years = set()

    def add_letter(self, l):
        self.letters.append(l)

    def compute_total_word_count(self):
        assert len(self.letters) > 0
        self.total_word_count = sum([l.get_total_word_count() for l in self.letters])

    def set_writers(self):
        assert len(self.letters) > 0
        self.writers = set([i.get_writer() for i in self.letters])

    def add_writer(self, writer):
        self.writers.add(writer)

    def set_addressees(self):
        assert len(self.letters) > 0
        self.addressees = set([i.get_addressee() for i in self.letters])

    def add_addressee(self, addressee):
        self.addressees.add(addressee)

    def set_years(self):
        assert len(self.letters) > 0
        self.years = set([i.get_year() for i in self.letters])

    def add_year(self, year):
        self.years.add(year)

    def filter_letters(self, language='(en)|(fr)', writer='.*', addressee='.*', from_year=1821, to_year=1862):
        return [i for i in self.letters if re.search(language, i.get_language(), re.I) and re.search(writer, i.get_writer(), re.I) and re.search(addressee, i.get_addressee(), re.I) and (i.get_year() >= from_year and i.get_year() <= to_year)]

    def create_subcorpus(self, language='(en)|(fr)', writer='.*', addressee='.*', from_year=1821, to_year=1862):
        filtered_letters = self.filter_letters(language, writer, addressee, from_year, to_year)
        if len(filtered_letters) == 0:
            raise Exception('No letters found for {0}, {1}, {2}, and years {3} to {4}. Please enter different specifications.'.format(language, writer, addressee, from_year, to_year))
        subcorp = Corpus(filtered_letters)
        subcorp.compute_total_word_count()
        # subcorp.set_writers()
        # subcorp.set_addressees()
        # subcorp.set_years()
        return subcorp

    def get_total_raw_count(self, search_term, case_sensitive):
        return sum([l.get_raw_count(search_term, case_sensitive) for l in self.letters])

    def get_normalized_count(self, raw_count):
        raw = raw_count / self.total_word_count * 1000
        return round(raw, 2)

    def name_to_regex(self, name):
        return re.sub('\s+', '\s+', name)

    def get_counts_by_category(self, search_term, case_sensitive, category, output_type):
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
            list_years = list(self.years)
            list_years.sort()
            for y in list_years:
                new_corp = self.create_subcorpus(from_year=y, to_year=y)
                raw = new_corp.get_total_raw_count(search_term, case_sensitive)
                counts_by_category[y] = raw if output_type == 'raw' else new_corp.get_normalized_count(raw)

        return sorted([i for i in counts_by_category.items()], key=lambda x:x[0])

    def get_concordances(self, search_term, case_sensitive, context_len):
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