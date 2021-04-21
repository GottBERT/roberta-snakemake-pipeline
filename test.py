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
min_tokens = 40


df_result = pd.DataFrame(columns=["filtered_tokens", 
                                  "original_tokens",
                                  "original_text",
                                  "stopword_ratio",
                                  "#tokens_original", 
                                  "#tokens_filtered", 
                                  "token_ratio",
                                  ""])

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
      
        token_ratio = num_unique_tokens_filtered/num_tokens_original
        
        if num_tokens_original > 0:
          df_result = df_result.append({
              "filtered_tokens": " ".join(filtered_sentence),
              "original_tokens": " ".join(word_tokens),
              "original_text": document.rstrip('\n'),
              "stopword_ratio": stopword_ratio,
              "#tokens_original": num_tokens_original,
              "#tokens_filtered": num_unique_tokens_filtered,
              "token_ratio": token_ratio
            }, ignore_index=True)


    
# df_sorted = df_result.sort_values(by='ratio')

# save it
df_filtered = df_result[
    (df_result['token_ratio'].astype('float') > threshold_token) &
    (df_result['stopword_ratio'].astype('float') < threshold_stopword)
]['original_text']
#df_filtered.to_csv(out_file, quoting=csv.QUOTE_NONE, sep=' ', index=False, header=False)

np.savetxt(out_file, df_filtered.values, fmt='%s', delimiter='', encoding='utf-8')




#stanza.download('de')
#nlp = stanza.Pipeline('de',use_gpu=False)
#doc = nlp(text)
#doc.sentences[0].print_dependencies()
