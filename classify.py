# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.utils import exist, load_json, dump_json, load_model, dump_model, export_csv
from ppg.learn import get_feature_set
from ppg.learn import logistic_regression_classifier
# from ppg.learn import support_vector_classifier
from ppg.learn import gaussian_naive_bayes_classifier
from ppg.learn import decision_tree_classifier
from ppg.learn import random_forest_classifier, adaboost_classifier, gradient_boosting_classifier
from ppg.learn import voting_classifier


def classify():
    splited_data_dir = os.path.join(BASE_DIR, 'data', 'splited')
    model_dir = os.path.join(BASE_DIR, 'models')
    result_dir = os.path.join(BASE_DIR, 'results')


    label_sets = [
        ['pre', 'in'],
    ]
    feature_type_sets = [
        ['ppg45', 'svri'],
        ['ppg45'],
        ['svri'],
    ]
    classifiers = [
        ('logistic_regression', logistic_regression_classifier, ),
        # ('support_vector', support_vector_classifier, ),
        ('gaussian_naive_bayes', gaussian_naive_bayes_classifier, ),
        ('decision_tree', decision_tree_classifier, ),
        ('random_forest', random_forest_classifier, ),
        ('adaboost', adaboost_classifier, ),
        ('gradient_boosting', gradient_boosting_classifier, ),
        ('voting', voting_classifier, ), # voting classifier has to be the LAST item in the list
    ]


    if exist(pathname=splited_data_dir):
        result_data = {}
        for filename_with_ext in fnmatch.filter(os.listdir(splited_data_dir), '*.json'):
            participant = os.path.splitext(filename_with_ext)[0]
            pathname = os.path.join(splited_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for label_set in label_sets:
                    label_set_name = '-'.join(label_set)
                    if label_set_name not in result_data:
                        result_data[label_set_name] = {}
                    for feature_type_set in feature_type_sets:
                        feature_type_set_name = '-'.join(feature_type_set)
                        if feature_type_set_name not in result_data[label_set_name]:
                            result_data[label_set_name][feature_type_set_name] = {}
                        train_features, train_labels, test_features, test_labels = get_feature_set(data=json_data, label_set=label_set, feature_type_set=feature_type_set)
                        estimators = []
                        for classifier_name, classifier_object in classifiers:
                            if classifier_name not in result_data[label_set_name][feature_type_set_name]:
                                result_data[label_set_name][feature_type_set_name][classifier_name] = {}
                            model_pathname = os.path.join(model_dir, label_set_name, feature_type_set_name, classifier_name, '%s.model' % participant)
                            classifier = load_model(pathname=model_pathname)
                            if classifier is None:
                                if classifier_name == 'voting':
                                    classifier = classifier_object(estimators=estimators, features=train_features, labels=train_labels)
                                else:
                                    classifier = classifier_object(features=train_features, labels=train_labels)
                                dump_model(model=classifier, pathname=model_pathname)
                            score = classifier.score(test_features, test_labels)
                            print participant, score, label_set_name, feature_type_set_name, classifier_name
                            result_data[label_set_name][feature_type_set_name][classifier_name][participant] = score

                            # prepare estimators for the training of voting classifier
                            if classifier_name != 'voting':
                                if hasattr(classifier, 'best_estimator_'):
                                    estimators.append((classifier_name, classifier.best_estimator_, ))
                                else:
                                    estimators.append((classifier_name, classifier, ))

        for label_set_name in result_data:
            dump_json(data=result_data[label_set_name], pathname=os.path.join(result_dir, '%s.json' % label_set_name), overwrite=True)
            csv_data = []
            for feature_type_set in feature_type_sets:
                feature_type_set_name = '-'.join(feature_type_set)
                csv_row = {
                    'feature_set': feature_type_set_name,
                }
                for classifier_name in result_data[label_set_name][feature_type_set_name]:
                    csv_row[classifier_name] = sum(result_data[label_set_name][feature_type_set_name][classifier_name].values()) / len(result_data[label_set_name][feature_type_set_name][classifier_name])
                csv_data.append(csv_row)
            fieldnames = ['feature_set'] + [val[0] for val in classifiers]
            export_csv(data=csv_data, fieldnames=fieldnames, pathname=os.path.join(result_dir, '%s.csv' % label_set_name), overwrite=True)


if __name__ == '__main__':
    classify()