
## Workflow Graph
Below is a visualization of the pre-training workflow (see `media/pretrain/graph.png`):

![Pre-training workflow graph](../media/pretrain/graph.png)

# Pre-training

This directory contains scripts and instructions for pre-training the GottBERT model using fairseq on both TPU and GPU. It covers environment setup, hardware recommendations, and usage tips for large-scale training.

## Requirements

For large datasets, you must install `pyarrow` (required by fairseq for efficient data loading):

```bash
pip install pyarrow
```


## TPU Training

This repo provides scripts for TPUv3 and TPUv4:

1. [v3/train_tpu.sh](./v3/train_tpu.sh) — single TPU
2. [v3/train_tpu_pod.sh](./v3/train_tpu_pod.sh) — TPU Pod
3. [v4/train_tpu.sh](./v4/train_tpu.sh) — single TPU (v4)

For single TPU training, use script 1 or 3. For TPU Pod training, use script 2. Choose a VM type with sufficient memory, as fairseq stores a lot of data in memory. For GottBERT (~60GB binary data), we used `n1-highmem-32` VMs to control a 256-core TPU pod (32 VMs, one per 8 cores). We recommend disabling automatic disk deletion on VMs, as the scripts remove the VMs after training, allowing you to keep your model outputs.

### Batch Size Configuration
Set the following variables in the scripts to control batch size and parallelism:

```bash
MAX_SENTENCES=16    # Number of sequences per batch (batch size)
UPDATE_FREQ=16      # Gradient accumulation steps
WORLD_SIZE=32       # Number of TPU cores
```

According to [this publication](https://www.aclweb.org/anthology/W18-6301.pdf), this results in a total batch size of 16 x 16 x 32 = 8192.

**Example:** GottBERT was pre-trained in ~36 hours with a batch size of 8k for 100k steps on a 256-core TPU pod. Raw data: ~135GB, binarized: ~60GB.



## GPU Training

This repository provides several scripts for GPU-based pre-training, located in `pre-training/gpu/`:

- **train.sh**: Standard masked language model (MLM) pre-training with fairseq.
- **train_WWM.sh**: Pre-training with Whole Word Masking (WWM) enabled, using the `--mask-whole-words` flag and typically a larger model (e.g., `roberta_large`).
- **train_continued_WWM.sh**: Continued pre-training from an existing checkpoint, with WWM and optimizer/dataloader/lr-scheduler reset for further domain adaptation or additional data.

You may need to review and adapt the scripts to your data and hardware setup. See the script headers for environment variables and options.

For custom setups or more details, you can also refer to the [original fairseq documentation](https://github.com/pytorch/fairseq/blob/master/examples/roberta/README.pretraining.md).


## Loading Your Pretrained Model

After training, you can load your model in Python as follows:

```python
from fairseq.models.roberta import GottbertModel
roberta = GottbertModel.from_pretrained('checkpoints', 'checkpoint_best.pt', 'path/to/data')
assert isinstance(roberta.model, torch.nn.Module)
```



## Model Conversion
To convert a fairseq-trained GottBERT model to Hugging Face Transformers format, see the scripts and instructions in the [convert](./convert/) folder.

## Checkpoint Testing
You can use [test.py](./test.py) to quickly check a model checkpoint on any machine (including a TPU node). This script loads a checkpoint and runs a fill-mask prediction for a given sentence. See the script for usage details and command-line options.

## Tips & Troubleshooting
- Always ensure you have enough disk and RAM for large datasets.
- Monitor VM and TPU usage to avoid unexpected costs.
- If you encounter data loading errors, check that `pyarrow` is installed.

