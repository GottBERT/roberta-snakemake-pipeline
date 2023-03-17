#!/usr/bin/env python3

import pandas as pd
import numpy as np
import nltk
import csv
import pickle

nltk.download("stopwords")

in_file = "files/example/de_dedup.txt"
out_file = "output/filtered_final.txt"
pickle_out = "ratios.pkl"
language = "German"


df_result = pd.DataFrame(columns=["filtered_tokens", 
                                  "original_tokens",
                                  "original_text",
                                  "stopword_ratio",
                                  "punctuation_ratio",
                                  "#tokens_original", 
                                  "#tokens_filtered",
                                  "#tokens_puctuation",
                                  "token_ratio",
                                  "#token_upper",
                                  "upper_ratio",
                                  "upper_to_punct_ratio"])
word_tokenizer = nltk.RegexpTokenizer(r"\w+")
stop_words = set(nltk.corpus.stopwords.words(language.lower()))

with open(in_file, mode="r", encoding="utf-8") as f_in:
  for document in f_in:
  
    word_tokens = nltk.tokenize.word_tokenize(document)
    
    # tokens without stopwords
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    
    # compute stopword ratio, i.e. 1-|tokens without stop words|/|tokens of document|
    if len(word_tokens) > 0:
        stopword_ratio = 1-len(filtered_sentence)/len(word_tokens)
    else:
        stopword_ratio = 0
    
    # number of unique tokens
    num_unique_tokens_filtered = len(set(filtered_sentence))
    
    # number of tokens of the original document
    num_tokens_original = len(word_tokens)
    
    # apply word tokenizer to get words
    words = word_tokenizer.tokenize(document)
    
    # compute puntuation, i.e. difference of word tokens and original tokens
    punctuation = [w for w in word_tokens if not w in words]
    
    # get tokens starting with upper case character
    upper = [w for w in word_tokens if w[0].isupper()]

    
    # compute how many puncuations occur in document
    num_punctuation = len(punctuation)
    
    # compute puntuation ratio, i.e. |puncuation tokens|/|tokens of document|
    if num_tokens_original > 0:
        punctuation_ratio = num_punctuation/num_tokens_original
    else:
        punctuation_ratio = 0
  
    # compute token ratio, which describes the occurence of repeating words
    if num_tokens_original > 0:
        token_ratio = num_unique_tokens_filtered/num_tokens_original
    else:
        token_ratio = 0

    # number of tokens which start with a upper case character
    num_upper = len(upper)
    
    # after puctuation, in German, one continues to write in capital
    if num_punctuation > 0 and num_upper > 0:
      upper_to_punct_ratio = (num_upper/num_punctuation) / num_upper
    else:
      upper_ratio = 0
  
    # ratio between upper word tokens and tokens in general, i.e. |upper case tokens|/|tokens of document|
    if num_tokens_original > 0:
        upper_ratio = num_upper/num_tokens_original
    else:
        num_tokens_original = 0
  
    if num_tokens_original > 0:
      df_result = df_result.append({
          "filtered_tokens": " ".join(filtered_sentence),
          "original_tokens": " ".join(word_tokens),
          "original_text": document.rstrip('\n'),
          "stopword_ratio": stopword_ratio,
          "punctuation_ratio": punctuation_ratio,
          "#tokens_original": num_tokens_original,
          "#tokens_filtered": num_unique_tokens_filtered,
          "#tokens_puctuation": num_punctuation,
          "token_ratio": token_ratio,
          "#token_upper": num_upper,
          "upper_ratio": upper_ratio,
          "upper_to_punct_ratio": upper_to_punct_ratio
        }, ignore_index=True)

# pickle dump
with open(pickle_out,'wb') as f_pickle:
  pickle.dump(df_result,f_pickle)
