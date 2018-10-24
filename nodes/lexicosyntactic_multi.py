import subprocess
import collections
import csv
import os
import re
import logging

from nodes.helper import FileOutputNode
from utils import file_utils
import config


SENTENCE_TOKENS = '.。!?！？'

POS_TAGS = [
    "AD","AS","BA","CC","CD","CS","DEC","DEG","DER","DEV","DT","ETC","FW","IJ",
    "JJ","LB","LC","M","MSP","NN","NR","NT","OD","ON","P","PN","PU","SB","SP",
    "VA","VC","VE","VV","X"
]


class MultilangTranscript(object):
    def __init__(self, filepath, out_file, output_parse_dir):
        self.filepath = filepath
        self.out_file = out_file
        self.output_parse_dir = output_parse_dir

        self.features = collections.OrderedDict()
        self.pos_tags = []


    def _run_chinese_corenlp(self, filepath):
        self.corenlp_out_file = os.path.join(self.output_parse_dir, os.path.basename(filepath) + '.out')

        if os.path.isfile(self.corenlp_out_file):
            print('Already parsed:', self.corenlp_out_file)
        else:
            # lexparser_chinese.sh [output_dir] [transcript_file]
            subprocess.call([
                os.path.join(config.path_to_stanford_cp, 'lexparser_chinese.sh'),
                self.output_parse_dir,
                filepath
            ])

    def _parse_corenlp_output(self):
        with open(self.corenlp_out_file) as f:
            for line in f.readlines():
                line = line[:-1]

                match = re.search(r'PartOfSpeech=([A-Z]+)\]', line)
                if match:
                    tag = match.group(1)
                    assert(tag in POS_TAGS)
                    self.pos_tags.append(tag)

        # Count POS tag features
        for pos_tag in POS_TAGS:
            count = 0
            for tag in self.pos_tags:
                if tag == pos_tag:
                    count += 1
            self.features[pos_tag] = count
            self.features['ratio_' + pos_tag] = count / len(self.pos_tags)

        # A few special ones
        self.features['ratio_pronoun_noun'] = self.features['PN'] / (self.features['PN'] + self.features['NN'])
        self.features['ratio_noun_verb'] = self.features['NN'] / (self.features['NN'] + self.features['VV'])


    def _write_features(self, out_file):
        with open(out_file, 'w') as f:
            csvw = csv.writer(f)
            csvw.writerow(list(self.features.keys()))
            csvw.writerow(list(self.features.values()))

    def _calc_ttr(self, text):
        """TTR = unique words / all words"""
        N = len(text)
        V = len(set(text))
        return V / N


    def compute_basic_word_stats(self):
        num_sentences = len([x for x in self.tokens if x in SENTENCE_TOKENS])
        num_words = len(self.tokens) - num_sentences
        ttr = self._calc_ttr([x for x in self.tokens if x not in SENTENCE_TOKENS])
        word_lengths = [len(x) for x in self.tokens if x not in SENTENCE_TOKENS]

        self.features['num_sentences'] = num_sentences
        self.features['mean_words_per_sentence'] = num_words / num_sentences
        self.features['ttr'] = ttr

    def run(self):
        if file_utils.should_run(self.filepath, self.out_file):
            self.features['FileID'] = self.filepath

            with open(self.filepath) as f:
                self.tokens = f.read()

            self.compute_basic_word_stats()

            self._run_chinese_corenlp(self.filepath)
            self._parse_corenlp_output()
            #self._write_features(out_file)


class MultilingualLex(FileOutputNode):
    def setup(self):
        self.output_parse_dir = os.path.join(self.out_dir, "stanford_parses")

    def run(self, filepath):
        self.log(logging.INFO, "Starting %s" % (filepath))
        out_file = self.derive_new_file_path(filepath, ".csv")

        transcript = MultilangTranscript(filepath, out_file, self.output_parse_dir)
        transcript.run()

        self.emit(out_file)
