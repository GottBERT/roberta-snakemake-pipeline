#!/usr/bin/env python3

import nltk
import fire

nltk.download("stopwords")

# in_file = "output/filtered.txt"
# out_file = "output/filtered_final.txt"
# language = "German"
# threshold_token = 0.4
# threshold_stopword = 0.9
# min_tokens = 40


def filter(in_file, out_file, language, threshold_token, threshold_stopword, min_tokens):
  # get stopwords
  stop_words = set(nltk.corpus.stopwords.words(language.lower()))
  with open(out_file, mode='w', encoding="utf-8") as f_out:
    with open(in_file, mode="r", encoding="utf-8") as f_in:
      for document in f_in:
      
        # print(f"{document}\n\n")
        
        word_tokens = nltk.tokenize.word_tokenize(document)
        
        if len(word_tokens) > min_tokens:
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            
            stopword_ratio = len(filtered_sentence)/len(word_tokens)
            
            num_unique_tokens_filtered = len(set(filtered_sentence))
            num_tokens_original = len(word_tokens)
          
            token_ratio = num_unique_tokens_filtered/num_tokens_original
            
            if (num_tokens_original > 0 
              and token_ratio > threshold_token 
              and stopword_ratio < threshold_stopword):
                f_out.write("%s\n" % document.rstrip('\n'))


if __name__ == '__main__':
  fire.Fire(filter)
