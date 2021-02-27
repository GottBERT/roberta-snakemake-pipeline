# GottBERT

GottBERT is a model architecture based on RoBERTa. It uses tokenizer from huggingface in order to compute a language specific GPT-2 BPE. This repository offers a snakemake workflow to pre-process data for a training with [fairseq](https://github.com/pytorch/fairseq).

## Requirements
- [anaconda](https://www.anaconda.com/products/individual#Downloads) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)

## Pre-Training
For pre-training instructions, i.e. data preparaion, read [here](docs/pre-training.md).
