import os
import io
import math
from collections import Counter


class BLEUCalculator():
    """ Calculates BLEU metric for MT """

    def __init__(self):
        self.candidate = None
        self.references = None
        self.N = 4
        self.output_file_name = 'bleu_out.txt'

    def main(self, args):
        self.load_files(args[0], args[1])
        BLEU_score = self.calculate_BLEU_score()
        self.write_file(BLEU_score)

    def load_files(self, candidate_file, reference_path):
        reference_files = []
        if (os.path.isfile(reference_path)):
            reference_files.append(list(io.open(reference_path, encoding='utf-8')))
        else:
            reference_file_dir = reference_path
            for f, file in enumerate(os.listdir(reference_path)):
                reference_filename = reference_path + '/' + file
                reference_files.append(list(io.open(reference_filename, encoding='utf-8')))

        self.references = reference_files
        self.candidate = list(io.open(candidate_file, encoding='utf-8'))

    def calculate_BLEU_score(self):
        BP = self.calculate_brevity_penalty()
        pn_term = self.calculate_weighted_pn_sum()

        BLEU_score = BP * math.exp(pn_term)

        print
        "------------------------"
        print
        "BLEU: " + str(BLEU_score)
        print
        "------------------------"
        return BLEU_score

    def calculate_brevity_penalty(self):
        BP = 0;
        c = 0;
        r = 0;
        for l_no, candidate_line in enumerate(self.candidate):
            candidate_length = len(self.clean_read_words(candidate_line))  # length of candidate sentence

            reference_lengths = []
            for ref_file_no, reference in enumerate(self.references):
                reference_lengths.append(len(self.clean_read_words(reference[l_no])))

            effective_reference_length = min(reference_lengths, key=lambda x: abs(x - candidate_length))
            r += effective_reference_length
            c += candidate_length

        # 	print "(" + str(candidate_length) + ") " + str(reference_lengths) + " --> " + str(effective_reference_length)

        if (c > r):
            BP = 1
        else:
            BP = math.exp(1 - float(r) / float(c))

        # print "r: " + str(r)
        # print "c: " + str(c)
        print("BP: " + str(BP))

        return BP

    def calculate_weighted_pn_sum(self):
        weighted_pn_sum = 0

        wn = 1.0 / float(self.N)
        for n in range(1, self.N + 1):
            pn = self.calculate_modified_pn(n)
            if (pn != 0):
                weighted_pn_sum += (wn * math.log(pn), wn)[pn == 0]

        return weighted_pn_sum

    def calculate_modified_pn(self, n):

        clipped_count_sum = 0
        candidate_n_grams_count_sum = 0

        for l_no, line in enumerate(self.references[0]):
            ref_ngram_counts = self.get_max_ref_count(n, l_no)
            clipped_count, candidate_n_grams_count = self.calculate_clipped_count_sum(l_no, ref_ngram_counts, n)
            clipped_count_sum += clipped_count
            candidate_n_grams_count_sum += candidate_n_grams_count

        modified_pn = float(clipped_count_sum) / float(candidate_n_grams_count_sum)
        print(
        "P(" + str(n) + ") = " + str(clipped_count_sum) + "/" + str(candidate_n_grams_count_sum) + " = " + str(
            modified_pn))
        return modified_pn

    def get_ngrams(self, n, line):
        ngrams = []
        words = self.clean_read_words(line)
        for i in range(0, len(words) - n + 1):
            if (n <= len(words)):
                ngrams.append(' '.join(str(w.encode('utf-8')) for w in words[i:i + n]))
        # print ngrams
        return ngrams

    def calculate_clipped_count_sum(self, l_no, ref_ngram_counts, n):
        clipped_count_sum = 0
        line = self.candidate[l_no]
        words = self.clean_read_words(line)
        max_ngram_count = len(words) - n + 1

        ngram_counts = {}
        ngrams = self.get_ngrams(n, line)
        for g, ngram in enumerate(ngrams):
            ngram_counts[ngram] = ngrams.count(ngram)

        ngram_counts = Counter(ngrams)

        for g, ngram in enumerate(ngram_counts.keys()):
            count = ngram_counts.get(ngram)
            max_ref_count = (ref_ngram_counts.get(ngram), 0)[ref_ngram_counts.get(ngram) == None]
            clipped_count_sum += min(count, max_ref_count)

        return clipped_count_sum, max_ngram_count

    def get_max_ref_count(self, n, l_no):
        ref_ngram_counts = {}
        for ref_file_no, reference in enumerate(self.references):
            line = reference[l_no]
            words = self.clean_read_words(reference[l_no])
            ngrams = self.get_ngrams(n, line)
            for g, ngram in enumerate(ngrams):
                count = ref_ngram_counts.get(ngram)
                if (count == None):
                    count = 1
                ref_ngram_counts[ngram] = max(count, ngrams.count(ngram))
        # print "ref_ngram_counts: " + str(ref_ngram_counts)
        return ref_ngram_counts

    def write_file(self, BLEU_score):
        output_file = open(self.output_file_name, 'w')
        output_file.write(str(BLEU_score))
        output_file.close()

    def clean_read_words(self, line):
        return self.clean_read(line).split()

    def clean_read(self, line):
        return line.lower().strip()
