# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.params import PPG_SAMPLE_RATE
from ppg.utils import exist, load_text, dump_json


def segment():
    raw_data_dir = os.path.join(BASE_DIR, 'data', 'raw')
    segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')

    if exist(pathname=raw_data_dir):
        output_data = {}
        for filename_with_ext in fnmatch.filter(os.listdir(raw_data_dir), '*.txt'):
            filename, file_ext = os.path.splitext(filename_with_ext)
            participant, label = filename.split('-')
            if participant not in output_data:
                output_data[participant] = {}
            output_data[participant][label] = {
                'sample_rate': PPG_SAMPLE_RATE,
                'signal': map(float, load_text(pathname=os.path.join(raw_data_dir, filename_with_ext))),
            }

        for participant in output_data:
            output_filename = '%s.json' % participant
            dump_json(data=output_data[participant], pathname=os.path.join(segmented_data_dir, output_filename), overwrite=True)


if __name__ == '__main__':
    segment()