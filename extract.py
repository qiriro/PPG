# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.utils import exist, load_json, dump_json
from ppg.feature import extract_ppg45, extract_svri


def extract():
    preprocessed_data_dir = os.path.join(BASE_DIR, 'data', 'preprocessed')
    extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')

    if exist(pathname=preprocessed_data_dir):
        for filename_with_ext in fnmatch.filter(os.listdir(preprocessed_data_dir), '*.json'):
            pathname = os.path.join(preprocessed_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for label in json_data:
                    json_data[label]['ppg45'] = [extract_ppg45(single_waveform=single_waveform, sample_rate=json_data[label]['sample_rate']) for single_waveform in json_data[label]['single_waveforms']]
                    json_data[label]['svri'] = [extract_svri(single_waveform=single_waveform) for single_waveform in json_data[label]['single_waveforms']]
                    del json_data[label]['single_waveforms']
                dump_json(data=json_data, pathname=os.path.join(extracted_data_dir, filename_with_ext), overwrite=True)


if __name__ == '__main__':
    extract()