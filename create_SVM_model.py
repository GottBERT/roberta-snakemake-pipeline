#!/usr/bin/env python3

from sklearn import svm, model_selection
import pandas as pd
import numpy as np
# https://scikit-learn.org/stable/model_persistence.html
# Joblib offers alternative pickle load and dump functions
# which is more efficient for sklearn models
from joblib import load, dump
import argparse

parser = argparse.ArgumentParser(prog='compute_ratios')
parser.add_argument('--train', dest="in_train", help='input train file', required=True)
parser.add_argument('--test', dest="in_test", help='input test file', required=True)
parser.add_argument('--in', dest="in_pickle", help='input pickle file', required=True)
parser.add_argument('--out', dest="out_model", help='output joblib file',required=False, default='oneclasssvm.joblib')
parser.add_argument('--nu',  help='nu', required=True)
parser.add_argument('--language', required=False, default='German')
args = parser.parse_args()

# Select a subset of ratios as model features
df = pd.read_pickle(args.out_pickle)
df = df[["stopword_ratio", "punctuation_ratio", "token_ratio", "upper_ratio", "upper_to_punct_ratio"]]
df = df.astype(float)

# 
X = df.to_numpy()
idx = range(len(X))
X_train, X_test, idx_train, idx_test = model_selection.train_test_split(X, idx, test_size=0.2)
clf = svm.OneClassSVM(nu=nu)
clf.fit(X_train)

y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)

labels = pd.DataFrame(list(zip(idx_test, y_pred_test)), columns=["index", "class"])
labels.set_index('index', inplace=True)

d = pd.read_pickle("ratios.pkl")["original_text"].iloc[idx_test]
pred = pd.concat([d, labels], axis=1)

# pred[pred['class'] == -1].to_csv('pred.csv')

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# load labelled data
pd_label_studio = pd.read_json('label_studio-min.json')


# model evaluation
# merge with groundtruth data
df_merge = pd.merge(pd_label_studio.reset_index()[['index','sentiment']], pred.reset_index(), on='index')
df_merge['sentiment'] = df_merge['sentiment'].replace('mixed', -1).replace('spam', -1).replace('clean', 1)

y_test = df_merge['sentiment']
y_test_predictions = df_merge['class']

conf_matrix = confusion_matrix(y_test, y_test_predictions)


# Metrics
from sklearn.metrics import classification_report

accuracy = accuracy_score(y_test, y_test_predictions)
precision = precision_score(y_test, y_test_predictions)
recall = recall_score(y_test, y_test_predictions)
f1score = f1_score(y_test, y_test_predictions)

print(f"Accuracy = {accuracy.round(4)}")
print(f"Precision = {precision.round(4)}")
print(f"Recall = {recall.round(4)}")
print(f"F1 Score = {f1score.round(4)}")

print(classification_report(y_test, y_test_predictions, target_names=['dirty', 'clean']))

# save model
dump(clf, out_model)
