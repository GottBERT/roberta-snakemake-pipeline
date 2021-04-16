import pandas as pd
import nltk

nltk.download("stopwords")

filename = "/home/scheiblr/git/github/scheiblr/GottBERT/files/example/de_dedup.txt"

df_result = pd.DataFrame(columns=["filtered_tokens", 
                                  "original_tokens", 
                                  "#tokens_original", 
                                  "#tokens_filtered", 
                                  "ratio"])

stop_words = set(nltk.corpus.stopwords.words('german')) 

with open(filename) as f:
  for document in f:
  
    # print(f"{document}\n\n")
    
    word_tokens = nltk.tokenize.word_tokenize(document)
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    
    num_unique_tokens_filtered = len(set(filtered_sentence))
    num_tokens_original = len(word_tokens)
  
    df_result = df_result.append({
        "filtered_tokens": " ".join(filtered_sentence),
        "original_tokens": " ".join(word_tokens),
        "#tokens_original": num_tokens_original,
        "#tokens_filtered": num_unique_tokens_filtered,
        "ratio": num_unique_tokens_filtered/num_tokens_original
      }, ignore_index=True)

    
    
df_sorted = df_result.sort_values(by='ratio')

df_sorted[df_sorted['ratio']<=0.4].size()

#stanza.download('de')
#nlp = stanza.Pipeline('de',use_gpu=False)
#doc = nlp(text)
#doc.sentences[0].print_dependencies()
