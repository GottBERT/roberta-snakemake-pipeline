# raw files

- test.raw: test file for RoBERTa training
- valid.raw: validation file, which is used to validate the model's perplexity after each x steps
- label_studio.raw: test.raw without line breaks in order to be loaded into label_studio to distinguish between spam and not spam

## label_studio
- create `label_studio.raw`: 
```
jq -r '.[].text' files/SVM/label_studio-min.json > label_studio.raw
```

## properties of labelled data
- overall: 1800, 100,0%
- clean:   1466,  81,5%
- other:    334,  15,5%
    - mixed: 90
    - spam: 244
