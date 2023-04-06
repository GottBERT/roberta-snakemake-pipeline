#!/usr/bin/env python3

from sklearn import svm, model_selection
import pandas as pd
import numpy as np

# https://scikit-learn.org/stable/model_persistence.html
# Joblib offers alternative pickle load and dump functions
# which is more efficient for sklearn models
from joblib import load, dump
import argparse
import json

from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report, 
    matthews_corrcoef
)

parser = argparse.ArgumentParser(prog='compute_ratios')
parser.add_argument('--train', dest="in_train", help='input train parquet file', required=True)
parser.add_argument('--test', dest="in_test", help='input test parquet file', required=True)
parser.add_argument('--gt', dest="in_groundtruth", help='path to ground truth json (label studio minimal format)', required=True)
parser.add_argument('--out', dest="out_model", help='output joblib file',required=False, default='oneclasssvm.joblib')
parser.add_argument('--metrics', dest="out_metrics", help='output metrics file',required=False, default='metrics.json')
parser.add_argument('--log', dest="out_log", help='output training log file',required=False, default='training_log.csv')
parser.add_argument('--tol', dest="tol", help='tolerance for stopping criterion',required=False, default=0.003)
parser.add_argument('--cache_size', dest="cache_size", help='cache size in MB for SVM',required=False, default=200)
parser.add_argument('--gamma', dest="gamma", help='Kernel coefficient.',required=False, default='scale')

# list for nu can be created by e.g. print(','.join(str(x.round(3)) for x in np.arange(0.01,0.1, 0.005)))
parser.add_argument('--nu',  dest='nu', required=True, help='multiple values possible als comma separated list')
parser.add_argument('--language', required=False, default='German')
args = parser.parse_args()

# load labelled data
pd_label_studio = pd.read_json(args.in_groundtruth)

# Select a subset of ratios as model features
cols = ["stopword_ratio", "punctuation_ratio", "token_ratio", "upper_ratio", "upper_to_punct_ratio"]
df_train = pd.read_parquet(args.in_train)[cols].astype(float)
df_test = pd.read_parquet(args.in_test)[cols].astype(float)

# 
X_test = df_test.to_numpy()
idx_test = df_test.reset_index()['index'].to_numpy()

X_train = df_train.to_numpy()
idx_train = df_train.reset_index()['index'].to_numpy()

df_eval = pd.DataFrame(columns=['nu', 'tol', 'gamma', 'accuracy', 'precision', 'recall', 'weighted_f1_score', 'mcc', 'report', 'model'])

# estimate best SVM given nu
for nu in list(map(lambda e: float(e), args.nu.split(","))):
    for tol in list(map(lambda e: float(e), args.tol.split(","))):
        for gamma in list(args.gamma.split(",")):
            try:
                # create and train model
                model = svm.OneClassSVM(nu=nu, tol=tol, gamma=gamma, cache_size=int(args.cache_size))
                model.fit(X_train)

                y_pred_test = model.predict(X_test)

                labels = pd.DataFrame(list(zip(idx_test, y_pred_test)), columns=["index", "class"])
                labels.set_index('index', inplace=True)

                d = pd.read_parquet(args.in_test)["original_text"].iloc[idx_test]
                pred = pd.concat([d, labels], axis=1)

                # model evaluation
                # merge with groundtruth data
                df_merge = pd.merge(pd_label_studio.reset_index()[['index','sentiment']], pred.reset_index(), on='index')
                df_merge['sentiment'] = df_merge['sentiment'].replace('mixed', -1).replace('spam', -1).replace('clean', 1)

                # in case some NaN values are in the annotation, find out which by uncommenting this line
                # print(df_merge[df_merge.isna().any(axis=1)])

                y_test = df_merge['sentiment']
                y_test_predictions = df_merge['class']

                # confusion matrix
                conf_matrix = confusion_matrix(y_test, y_test_predictions)

                # compute some metrics
                accuracy = accuracy_score(y_test, y_test_predictions)
                precision = precision_score(y_test, y_test_predictions)
                recall = recall_score(y_test, y_test_predictions)
                f1score = f1_score(y_test, y_test_predictions, average='weighted')

                # https://biodatamining.biomedcentral.com/articles/10.1186/s13040-023-00322-4
                # https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-019-6413-7
                mcc = matthews_corrcoef(y_test, y_test_predictions)

                # append data to pandas dataframe
                report = classification_report(y_test, y_test_predictions, target_names=['dirty', 'clean'], output_dict=True)
            except:
                accuracy=np.nan
                precision=np.nan
                recall=np.nan
                f1score=np.nan
                mcc=abs(np.nan)
                report=None
                model=None

            list_row = [nu, tol, gamma, accuracy, precision, recall, f1score, abs(mcc), report, model]
            df_eval.loc[len(df_eval)] = list_row


            # print(f"Accuracy = {accuracy.round(4)}")
            # print(f"Precision = {precision.round(4)}")
            # print(f"Recall = {recall.round(4)}")
            # print(f"F1 Score = {f1score.round(4)}")
            # print(f"MCC = {mcc.round(4)}")

            # print(classification_report(y_test, y_test_predictions, target_names=['dirty', 'clean']))
    

# estimate best model
o_best_model = df_eval.iloc[df_eval['mcc'].idxmax()]

# save best model
best_model = o_best_model.pop('model')
metrics = o_best_model

# print(metrics)

# save data
dump(best_model, args.out_model)
metrics.to_json(args.out_metrics, orient='index', indent=2)

df_eval[metrics.keys()].to_csv(args.out_log, index=False)
