import pandas as pd
import numpy as np
import nltk
import csv


nltk.download("stopwords")

in_file = "output/filtered.txt"
out_file = "output/filtered_final.txt"
language = "German"
threshold_token = 0.4
threshold_stopword = 0.9
threshold_punctuation = 0.4
threshold_upper = 1.0
min_tokens = 40


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
                                  "upper_ratio"])
word_tokenizer = nltk.RegexpTokenizer(r"\w+")
stop_words = set(nltk.corpus.stopwords.words(language.lower()))

with open(in_file, mode="r", encoding="utf-8") as f_in:
  for document in f_in:
  
    # print(f"{document}\n\n")
    
    word_tokens = nltk.tokenize.word_tokenize(document)
    
    if len(word_tokens) > min_tokens:
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        
        stopword_ratio = len(filtered_sentence)/len(word_tokens)
        
        num_unique_tokens_filtered = len(set(filtered_sentence))
        num_tokens_original = len(word_tokens)
        
        words = word_tokenizer.tokenize(document)
        punctuation = [w for w in word_tokens if not w in words]
        
        upper = [w for w in word_tokens if w[0].isupper()]
    
      
        num_punctuation = len(punctuation)
        
        punctuation_ratio = num_punctuation/num_tokens_original
      
        token_ratio = num_unique_tokens_filtered/num_tokens_original
        
        if num_punctuation > 0:
          num_upper = len(upper)
          upper_ratio = num_upper/num_punctuation
        else:
          upper_ratio = 0
      
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
              "upper_ratio": upper_ratio
            }, ignore_index=True)


    
# df_sorted = df_result.sort_values(by='ratio')

# save it
df_filtered = df_result[
    (df_result['token_ratio'].astype('float') > threshold_token) &
    (df_result['stopword_ratio'].astype('float') < threshold_stopword) &
    (df_result['punctuation_ratio'].astype('float') < threshold_punctuation) & 
    (df_result['upper_ratio'].astype('float') >= threshold_upper)
]['original_text']
#df_filtered.to_csv(out_file, quoting=csv.QUOTE_NONE, sep=' ', index=False, header=False)

np.savetxt(out_file, df_filtered.values, fmt='%s', delimiter='', encoding='utf-8')




#stanza.download('de')
#nlp = stanza.Pipeline('de',use_gpu=False)
#doc = nlp(text)
#doc.sentences[0].print_dependencies()
