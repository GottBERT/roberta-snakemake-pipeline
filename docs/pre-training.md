# Pre-training

## TPU


## GPU

Just stick do the [original fairseq documentation](https://github.com/pytorch/fairseq/blob/master/examples/roberta/README.pretraining.md) if you are using GPUs.

## Load your pretrained model
```python
from fairseq.models.roberta import GottbertModel
roberta = GottbertModel.from_pretrained('checkpoints', 'checkpoint_best.pt', 'path/to/data')
assert isinstance(roberta.model, torch.nn.Module)
```