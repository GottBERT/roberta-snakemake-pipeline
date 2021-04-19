# Pre-processing
The original RoBERTa used GPT2's BPE in order to encode data. Further, according to [their docs](https://github.com/pytorch/fairseq/blob/master/examples/roberta/README.pretraining.md) data should be formatted with one empty line between distinct documents. This is only useful when using `--sample-break-mode complete_doc` in the training step. Additionally, in order to use our pre-processing pipeline, we expect one document per line.

## Preparation
In order to let this script run properly, you need to prepare you data as follows:
- Create a file containing all of you data, per line one document.
- [optional] if you don't want to compute a new GPT2-BPE but rely on a pre-existing one, place `dict.txt`, `merges.txt` and `vocab.json` into `output/bpe_enc/`.

## Usage
According to our experience a test and valid set file of about 3-5 MB should be sufficient. In case of GottBERT we used 12000 documents.

## Example
In `../files/example/de_dedup.txt` lies a file which is a small extract of the German OSCAR corpus. We can use it for a small test computation.
In order to run the entire pipeline just run the following lines **while located in the root folder of the project**:

```bash
snakemake --use-conda --config in_file=files/example/de_dedup.txt nun_docs_valid_test_set=100 size_bpe_train_file=700 vocab_size=64 -j$(nproc --all)
```

For furhter insrucitons about the config parameters, which we pass in the example per command line, read `GIT_ROOT/config/preprocess.yaml`. It's also possible to define all parameters there.

The pipeline processes the depicted steps:

![Image of snakemake workflow](visualization.png)
