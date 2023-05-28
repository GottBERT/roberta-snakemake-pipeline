# Experiments

We use [Farm](https://github.com/deepset-ai/FARM) as the framerwork for experiments, as they have a amazing infrastrucure for testing.

Following experiments are setup:
- NER
  - CoNLL 2003 DE
  - germEval 14
- QA
  - [SQuAD2.0](https://rajpurkar.github.io/SQuAD-explorer/)
- Text Classification
  - germEval 18 Coarse
  - germEval 18 Fine
  - [10kGNAD](https://tblock.github.io/10kGNAD/)


see [here](https://hpi.de/naumann/sites/krestel/?Publications___Workshop_Papers) for bibtex.


## MLflow

Install it
```
pip install mlflow
```

and run it:
```
mlflow ui
```

Now browse it under [localhost](http://localhost:5000).