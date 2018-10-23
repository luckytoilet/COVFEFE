import subprocess
import collections
import csv
import os
import logging

from nodes.helper import FileOutputNode
from utils import file_utils
import config


class MultilingualLex(FileOutputNode):
    def setup(self):
        self.output_parse_dir = os.path.join(self.out_dir, "stanford_parses")
        self.features = collections.OrderedDict()
        
    def _run_chinese_corenlp(self, filepath):
        # lexparser_chinese.sh [output_dir] [transcript_file]
        subprocess.call([
            os.path.join(config.path_to_stanford_cp, 'lexparser_chinese.sh'),
            self.output_parse_dir,
            filepath
        ])

    def _write_features(self, out_file):
        with open(out_file, 'w') as f:
            csvw = csv.writer(f)
            csvw.writerow(list(self.features.keys()))
            csvw.writerow(list(self.features.values()))

    def run(self, filepath):
        self.log(logging.INFO, "Starting %s" % (filepath))
        out_file = self.derive_new_file_path(filepath, ".csv")

        if file_utils.should_run(filepath, out_file):
            self.features['FileID'] = filepath
            self._run_chinese_corenlp(filepath)
            self._write_features(out_file)

        self.emit(out_file)
