# GottBERT

GottBERT is a model architecture based on RoBERTa. It uses tokenizer from huggingface in order to compute a language specific GPT-2 BPE. This repository offers a snakemake workflow to pre-process data for a subsequent training with [fairseq](https://github.com/pytorch/fairseq).

## Requirements
- [anaconda](https://www.anaconda.com/products/individual#Downloads) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)

The current software is tested with anaconda using a python 3.11 version and Snakemake 7.25.0.

## Data Preparation
For preprocessing of data continue reading [here](workflow_preprocess/README.md).

## Pre-Training
For pre-training instructions, i.e. computation of the GottBERT model, read [here](pre-training/README.md).

## Working with the resulting model
After successfully pre-training a GottBERT model one can try it out with fairseq as described in [their documentation](https://github.com/pytorch/fairseq/blob/master/examples/gottbert/README.md).
Another possibility is to convert the resulting model to transformer huggingface. 

## License
GottBERT is AGPL-v3 licensed.

## Citation
If you are using this code or our model, please cite as:

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