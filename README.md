# RoBERTa Snakemake Pipeline

A modular, Snakemake-based framework for preprocessing large-scale text and pretraining RoBERTa models with fairseq, including support for language-specific BPE tokenization.

The pipeline has been used to train several RoBERTa-based language models,
including [GottBERT](https://huggingface.co/GottBERT/),
[GeistBERT](https://huggingface.co/GeistBERT),
[ChristBERT](https://huggingface.co/ChristBERT),
[PortBERT](https://huggingface.co/PortBERT),
[SindBERT](https://huggingface.co/SindBERT),
and [HalleluBERT](https://huggingface.co/HalleluBERT).

This repository focuses on the software infrastructure.
Model-specific details are described in the corresponding publications.
The workflow integrates seamlessly with a custom fairseq fork:
https://github.com/GottBERT/fairseq

## Features
- End-to-end data preprocessing pipeline using Snakemake
- Support for large-scale German text corpora
- Language-specific BPE tokenization workflows
- Easy integration with Hugging Face and our [fairseq fork](https://github.com/GottBERT/fairseq)
- Scripts for model conversion and evaluation


## Requirements
- [Anaconda](https://www.anaconda.com/products/individual#Downloads) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- [Snakemake 9.0.1](https://snakemake.readthedocs.io/en/v9.0.1/getting_started/installation.html)
- [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (see below)

Tested with Python 3.12.9 and Anaconda.
## Submodules

This repository uses git submodules for external dependencies. To clone with submodules, use:

```bash
git clone --recurse-submodules https://github.com/GottBERT/fairseq
```

If you already cloned the repo, initialize submodules with:

```bash
git submodule update --init --recursive
```

### Included submodules
- `external/fairseq`: [GottBERT fairseq fork (legacy version)](https://github.com/GottBERT/fairseq)
      - This fork is used for compatibility with the original GottBERT pre-training scripts and data formats presented in this repo.
      - For new projects, consider using the latest [fairseq](https://github.com/pytorch/fairseq) if possible.


## Quickstart
1. **Clone the repository**
      ```bash
      git clone https://github.com/GottBERT/corpus
      cd corpus
      ```
2. **Set up the environment**
      ```bash
      conda env create -f requirements.txt
      conda activate gottbert
      ```
3. **Preprocess your data**
      See [workflow_preprocess/README.md](workflow_preprocess/README.md) for detailed instructions.
4. **Pre-train the model**
      See [pre-training/README.md](pre-training/README.md) for training steps.
5. **Use or convert the model**  
      For model conversion and usage, see the following:
      - Use with our fairseq fork as described in the [GottBERT example](https://github.com/GottBERT/fairseq/tree/master/examples/gottbert).
      - Convert to Hugging Face Transformers format using provided scripts.

## Pre-Training
For pre-training instructions, including scripts for TPU/GPU training and environment setup, see the [pre-training](pre-training/README.md) folder.

## Model Conversion
To convert a fairseq-trained GottBERT model to Hugging Face Transformers format, see the scripts and instructions in the [pre-training/convert](pre-training/convert/README.md) folder.


## License
This project is licensed under the MIT License.


## Citation
If you use this code or model, please cite:

```bibtex
@inproceedings{scheible-etal-2024-gottbert,
    title = "{G}ott{BERT}: a pure {G}erman Language Model",
    author = "Scheible, Raphael  and
      Frei, Johann  and
      Thomczyk, Fabian  and
      He, Henry  and
      Tippmann, Patric  and
      Knaus, Jochen  and
      Jaravine, Victor  and
      Kramer, Frank  and
      Boeker, Martin",
    editor = "Al-Onaizan, Yaser  and
      Bansal, Mohit  and
      Chen, Yun-Nung",
    booktitle = "Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.emnlp-main.1183/",
    doi = "10.18653/v1/2024.emnlp-main.1183",
    pages = "21237--21250"
}
```
