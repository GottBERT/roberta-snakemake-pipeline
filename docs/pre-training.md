# Pre-training

Most importantly, as this is easily overlooked at fairseq's documentation, for large datasets install pyarrow:
```bash
pip install pyarrow

```

## TPU
This repo provides two shell scripts for TPU computation:
1. [train_tpu.sh](../train_tpu.sh)
2. [train_tpu_pod.sh](../train_tpu_pod.sh)

1 is intended for single TPU training, whereas 2 is intended for a TPU Pod computation. Depending on data size, a decent vm should be chosen, a a s fairseq stores a lot of data memory. For GottBERT which result in a ~60GB binary blob, we used n1-highmem-32 machines to steer a 256 core TPU pod. It is required to take 1 vm per 8 cores, which makes 32 machines for a 256 core TPU pod. We recommend to setup the VMs without the feature of automatically removing the discs, as the scripts remove the VMs in the end. Like that, after training you can remove the expensive VMs without losing your resulting model.

Further, the batch size has to be chosen. Therefore, we have three Variables to setup in both script:
```bash
MAX_SENTENCES=16              # Number of sequences per batch (batch size)
UPDATE_FREQ=16                # Increase the batch size 16x
WORLD_SIZE=32                 # number of cores
```
According to [this publication](https://www.aclweb.org/anthology/W18-6301.pdf), in which `UPDATE_FREQ` is named cumul, the example above results in a batch size of 8k: 16x16x32 = 8096.

As an estimate: GottBERT was pre-computed within ~36 hours using a batch size of 8k for 100k steps on a 256 core TPU pod. The raw data size was ~135GB and resulted in a ~60GB data after binarization.


## GPU

Just stick do the [original fairseq documentation](https://github.com/pytorch/fairseq/blob/master/examples/roberta/README.pretraining.md) if you are using GPUs.

## Load your pretrained model
```python
from fairseq.models.roberta import GottbertModel
roberta = GottbertModel.from_pretrained('checkpoints', 'checkpoint_best.pt', 'path/to/data')
assert isinstance(roberta.model, torch.nn.Module)
```
