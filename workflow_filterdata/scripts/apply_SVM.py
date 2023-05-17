#!/usr/bin/env python3

import polars as pl
import joblib
import argparse

parser = argparse.ArgumentParser(prog='apply_SVM')
parser.add_argument('--model', dest="in_model", help='input model joblib file path', required=True)
parser.add_argument('--ratio', dest="in_ratio", help='input ratio parquet file path', required=True)
parser.add_argument('--out', dest="out_clean", help='output resulting text file', required=True)
parser.add_argument('--dirt', dest="out_dirt", help='output text file with the dirt', required=True)
args = parser.parse_args()

# Load model, ratios
clf = joblib.load(args.in_model)
df = pl.read_parquet(args.in_ratio)

# Select subset of ratios as model features
X = df.select(["stopword_ratio", "punctuation_ratio",
        "token_ratio", "upper_ratio"]).to_numpy()

predictions = clf.predict(X)
df = df.with_columns(pl.Series(name="prediction", values=predictions))

# Generate output textfile
df_clean = df.filter(pl.col('prediction') == 1)
df_dirty = df.filter(pl.col('prediction') == -1)

df_clean.select(["original_text"]).write_csv(args.out_clean, separator='\n', has_header=False)
df_dirty.select(["original_text"]).write_csv(args.out_dirt, separator='\n', has_header=False)
