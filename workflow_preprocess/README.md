
# Pre-processing Workflow

This workflow provides a Snakemake pipeline for preparing large-scale text corpora for pre-training language models (e.g., RoBERTa/GottBERT). It includes optional document splitting, shuffling, BPE learning/applying, and binarization for fairseq training.

The original RoBERTa used GPT2's BPE to encode data. According to [their docs](https://github.com/pytorch/fairseq/blob/master/examples/roberta/README.pretraining.md), data should be formatted with one empty line between distinct documents (useful for `--sample-break-mode complete_doc`). Our pipeline expects one document per line as input.


## Preparation
Prepare your data as follows:
- Create a file containing all your data, one document per line.
- [Optional] If you want to use a pre-existing GPT2-BPE, place `dict.txt`, `merges.txt`, and `vocab.json` into `output/bpe_enc/`.


## Usage
1. Adjust `config.yaml` to your needs. For GottBERT, we used 12,000 documents for the validation and test sets (3-5 MB each is usually sufficient).
2. To enable optional document splitting (e.g., for long documents), set `split_documents: true` and specify `split_documents_max_tokens` in `config.yaml`.
3. Run the pipeline:
	```bash
	snakemake --use-conda -j$(nproc --all)
	```

If you want to rerun the pipeline, remove the `output` folder. If you already have a BPE, include the files `dict.txt`, `merges.txt`, and `vocab.json` in `output/bpe_enc`.



## Workflow Graph

You can visualize the workflow with:
```bash
snakemake --use-conda -j$(nproc --all) --rulegraph | dot -Tpdf > graph.pdf
```


## Example
A small extract of the German OSCAR corpus is provided at `../files/example/de_dedup.txt`. You can use this file for a quick test run:

```bash
snakemake --use-conda --config in_file=../files/example/de_dedup.txt num_docs_valid_test_set=100 size_bpe_train_file=700 vocab_size=64 -j$(nproc --all)
```

For further instructions about config parameters, see `config.yaml`. All parameters can be set there or via the command line.

The pipeline processes the following steps:

![Image of snakemake workflow](visualization.png)

## Requirements
See the main project [README](../README.md) for requirements. All other dependencies are managed automatically via the provided Conda environments.
