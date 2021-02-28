# GottBERT

GottBERT is a model architecture based on RoBERTa. It uses tokenizer from huggingface in order to compute a language specific GPT-2 BPE. This repository offers a snakemake workflow to pre-process data for a training with [fairseq](https://github.com/pytorch/fairseq).

## Requirements
- [anaconda](https://www.anaconda.com/products/individual#Downloads) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)

## Data Preparation
For preprocessing of data continue reading [here](docs/preprocessing.md).

## Pre-Training
For pre-training instructions, i.e. computation of the GottBERT model, read [here](docs/pre-training.md).


## License
GottBERT is AGPL-v3 licensed.

## Citation
Please cite as:

```
@misc{scheible2020gottbert,
      title={GottBERT: a pure German Language Model},
      author={Raphael Scheible and Fabian Thomczyk and Patric Tippmann and Victor Jaravine and Martin Boeker},
      year={2020},
      eprint={2012.02110},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```