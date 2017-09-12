# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.params import TRAINING_DATA_RATIO
from ppg.learn import split_data_set
from ppg.utils import exist, load_json, dump_json


def split():
    extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')
    splited_data_dir = os.path.join(BASE_DIR, 'data', 'splited')

    if exist(pathname=extracted_data_dir):
        for filename_with_ext in fnmatch.filter(os.listdir(extracted_data_dir), '*.json'):
            pathname = os.path.join(extracted_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                output_data = {
                    'train': {},
                    'test': {},
                }
                for label in json_data:
                    ppg45_train, ppg45_test = split_data_set(data=json_data[label]['ppg45'], ratio=TRAINING_DATA_RATIO)
                    svri_train, svri_test = split_data_set(data=json_data[label]['svri'], ratio=TRAINING_DATA_RATIO)
                    output_data['train'][label] = {
                        'ppg45': ppg45_train,
                        'svri': svri_train,
                    }
                    output_data['test'][label] = {
                        'ppg45': ppg45_test,
                        'svri': svri_test,
                    }
                dump_json(data=output_data, pathname=os.path.join(splited_data_dir, filename_with_ext), overwrite=True)


if __name__ == '__main__':
    split()