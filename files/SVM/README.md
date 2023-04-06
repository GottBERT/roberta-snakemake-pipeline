# raw files

- test.raw: test file for RoBERTa training
- valid.raw: validation file, which is used to validate the model's perplexity after each x steps
- label_studio.txt: test.raw without line breaks in order to be loaded into label_studio to distinguish between spam and not spam

## label_studio
- create `label_studio.raw`: 
```
jq -r '.[].text' files/SVM/label_studio-min.json > label_studio.raw
```
