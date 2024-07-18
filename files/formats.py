# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


##% fix new checkpoint
import torch

new_model = torch.load("checkpoints/checkpoint_17_100000.pt")
old_model = torch.load("checkpoints/checkpoint.pt")

new_model['cfg']['include_index'] = False
new_model['cfg']['bpe'] = {'_name': 'hf_byte_bpe',
                           'bpe_merges': 'merges.txt',
                           'bpe_vocab': 'vocab.json',
                           'bpe_add_prefix_space': False}

new_model['bpe'] = {'_name': 'hf_byte_bpe',
                           'bpe_merges': 'merges.txt',
                           'bpe_vocab': 'vocab.json',
                           'bpe_add_prefix_space': False}

torch.save(new_model, 'checkpoints/checkpoint_fixed.pt')

new_model['args'] = new_model['cfg']['model']
del new_model['cfg']

# rename fields: 
# {'encoder.sentence_encoder.layernorm_embedding.weight', 'encoder.sentence_encoder.layernorm_embedding.bias', 'encoder.sentence_encoder.version'}
# to {'encoder.sentence_encoder.emb_layer_norm.weight', 'encoder.sentence_encoder.emb_layer_norm.bias'}
# and delete 'encoder.sentence_encoder.version'

new_model['model']['encoder.sentence_encoder.emb_layer_norm.weight'] = new_model['model']['encoder.sentence_encoder.layernorm_embedding.weight']
del new_model['model']['encoder.sentence_encoder.layernorm_embedding.weight']

new_model['model']['encoder.sentence_encoder.emb_layer_norm.bias'] = new_model['model']['encoder.sentence_encoder.layernorm_embedding.bias']
del new_model['model']['encoder.sentence_encoder.layernorm_embedding.bias']

del new_model['model']['encoder.sentence_encoder.version']

torch.save(new_model, 'checkpoints/checkpoint_fixed_old.pt')



##% load stuff with fairseq
from fairseq.models.roberta import GottbertModel as FairseqRobertaModel
roberta_checkpoint_path="../../files/checkpoints"
robert_checkpoint_file="checkpoint_fixed.pt"
gottbert = FairseqRobertaModel.from_pretrained(roberta_checkpoint_path, checkpoint_file=robert_checkpoint_file)
gottbert.eval()

masked_line = 'Gott ist <mask> ! :)'
gottbert.fill_mask(masked_line, topk=5)


##% load the model with transformers
from transformers import pipeline

mask_filler = pipeline("fill-mask", "./output/convertedBERT")
masked_line = 'Gott ist <mask> ! :)'

mask_filler(masked_line, top_k=5)