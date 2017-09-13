# -*- coding: utf-8 -*-

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier


def split_data_set(data, ratio):
    return data[:int(len(data) * ratio)], data[int(len(data) * ratio):]


def get_feature_set(data, label_set, feature_type_set):
    def __flatten(stuctured_data, feature_type_set):
        sample_num = len(stuctured_data[feature_type_set[0]])
        flattened_data = [[] for x in range(sample_num)]
        for feature_type in feature_type_set:
            for sample_index in range(sample_num):
                if isinstance(stuctured_data[feature_type], list):
                    if isinstance(stuctured_data[feature_type][0], list):
                        flattened_data[sample_index].extend(stuctured_data[feature_type][sample_index])
                    else:
                        flattened_data[sample_index].append(stuctured_data[feature_type][sample_index])
                else:
                    flattened_data[sample_index].append(stuctured_data[feature_type])
        return flattened_data, sample_num
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    for label in label_set:
        for feature_type in feature_type_set:
            train_flattened_data, train_sample_num = __flatten(stuctured_data=data['train'][label], feature_type_set=feature_type_set)
            train_features.extend(train_flattened_data)
            train_labels.extend([label for x in range(train_sample_num)])
            test_flattened_data, test_sample_num = __flatten(stuctured_data=data['test'][label], feature_type_set=feature_type_set)
            test_features.extend(test_flattened_data)
            test_labels.extend([label for x in range(test_sample_num)])
    return train_features, train_labels, test_features, test_labels


def logistic_regression_classifier(features, labels):
    classifier = LogisticRegression(random_state=1)
    classifier.fit(features, labels)
    return classifier


def support_vector_classifier(features, labels):
    parameters = {
        'C': [1.0, 10.0, 100.0],
        'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
    }
    classifier = GridSearchCV(SVC(random_state=1, probability=True), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def gaussian_naive_bayes_classifier(features, labels):
    classifier = GaussianNB()
    classifier.fit(features, labels)
    return classifier


def decision_tree_classifier(features, labels):
    parameters = {
        'max_depth': [None] + range(1, 11, 1),
    }
    classifier = GridSearchCV(DecisionTreeClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def random_forest_classifier(features, labels):
    parameters = {
        'n_estimators': range(10, 201, 10),
        'max_depth': [None] + range(1, 11, 1),
    }
    classifier = GridSearchCV(RandomForestClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def adaboost_classifier(features, labels):
    parameters = {
        'n_estimators': range(50, 201, 10),
        'learning_rate': [float(x) / 10.0 for x in range(1, 11, 1)],
    }
    classifier = GridSearchCV(AdaBoostClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def gradient_boosting_classifier(features, labels):
    parameters = {
        'learning_rate': [float(x) / 10.0 for x in range(1, 11, 1)],
        'n_estimators': range(50, 201, 10),
        'max_depth': range(1, 11, 1),
    }
    classifier = GridSearchCV(GradientBoostingClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def voting_classifier(estimators, features, labels):
    parameters = {
        'voting': ['soft', 'hard'],
    }
    classifier = GridSearchCV(VotingClassifier(estimators=estimators), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier