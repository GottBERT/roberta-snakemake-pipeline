#!/usr/bin/env bash

dir_data=${1}
dir_out=${2}

if [[ -f "${dir_data}/dict.txt" ]]; then
  fairseq-preprocess \
    --only-source \
    --cpu \
    --srcdict ${dir_data}/dict.txt \
    --trainpref ${dir_data}/train.bpe \
    --validpref ${dir_data}/valid.bpe \
    --testpref ${dir_data}/test.bpe \
    --bpe hf_byte_bpe \
    --destdir ${dir_out} \
    --workers 60
else 
  fairseq-preprocess \
    --only-source \
    --cpu \
    --trainpref ${dir_data}/train.bpe \
    --validpref ${dir_data}/valid.bpe \
    --testpref ${dir_data}/test.bpe \
    --bpe hf_byte_bpe \
    --destdir ${dir_out} \
    --workers 60
fi