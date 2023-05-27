# Convert fairseq to huggingface

This snakemake pipeline just consists of a script which converts a fairseq computed GottBERT checkpoint, including all BPE files, into a huggingface compatible file format.

Just setup the `config.yaml` and run snakemake 
```bash
snakemake -c $(nproc --a) --use-conda
```
or directly pass the parameters to the snakemake command
```bash
CHECKPOINT=../../files/checkpoints/checkpoint.pt
DUMP_NAME=holyBERT

snakemake -c $(nproc --a) --use-conda --config file_checkpoint=$CHECKPOINT pytorch_dump_folder_path=$DUMP_NAME
```

## MaskedLM
In case of the GottBERT_base model the result for the masked LM task should be as follows:
```python
from transformers import pipeline

mask_filler = pipeline("fill-mask", "./output/holyBERT")
masked_line = 'Gott ist <mask> ! :)'

mask_filler(masked_line, top_k=3)
# [('Gott ist gut ! :)',        0.3642110526561737,   ' gut'),
#  ('Gott ist überall ! :)',    0.06009674072265625,  ' überall'),
#  ('Gott ist großartig ! :)',  0.0370681993663311,   ' großartig')]
```