import pandas as pd
import joblib


model_path = 'oneclasssvm.joblib'
ratio_path = 'ratios.pkl'
output_textfile = 'de_dedup_filtered.txt'

# Load model, ratios
clf = joblib.load(model_path)
df = pd.read_pickle(ratio_path)

# Select subset of ratios as model features
X = df[["stopword_ratio", "punctuation_ratio",
        "token_ratio", "upper_ratio", "upper_to_punct_ratio"]]
X = X.astype(float).to_numpy()
y = clf.predict(X)
df["outlier"] = y

# Generate output textfile
df = df[df["outlier"] == 1]
df["original_text"].to_csv(output_textfile, sep='\n',
                           index=False, header=False)
