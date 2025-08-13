#!/usr/bin/env bash
export MKL_THREADING_LAYER=GNU
export XLA_EVEN_HEARTBEAT_TIMEOUT=7200
export XLA_UNEVEN_HEARTBEAT_TIMEOUT=7200

TOTAL_UPDATES=100000          # Total number of training steps
SAVE_INTERVAL_UPDATES=100000  # Save intervals (should be multiple of total updates)
WARMUP_UPDATES=10000          # Warmup the learning rate over this many updates
PEAK_LR=0.0007                # Peak learning rate, adjust as needed
TOKENS_PER_SAMPLE=512         # Max sequence length
LOG_INTERVAL=25               # Log interval. Don't do 1, it slows things down
MAX_SENTENCES=32              # Number of sequences per batch (batch size)
UPDATE_FREQ=32                # Increase the batch size 2x


DIR_OUTPUT="/data/geistbert/model/"

DATA_DIR="/data/geistbert/output/bin"
BPE=hf_byte_bpe

RESTORE_CHECKPOINT=/data/geistbert/fairseq_checkpoints/large_clean/checkpoint_best.pt

SAVE_DIR="$DIR_OUTPUT/checkpoints"
LOG_DIR="$DIR_OUTPUT/logs"

export BPE_VOCAB="$DATA_DIR/vocab.json"
export BPE_MERGES="$DATA_DIR/merges.txt"

WORLD_SIZE=8

fairseq-train $DATA_DIR \
  --restore-file $RESTORE_CHECKPOINT \
  --distributed-world-size $WORLD_SIZE \
  --log-format json \
  --log-interval $LOG_INTERVAL \
  --task masked_lm \
  --criterion masked_lm \
  --optimizer adam \
  --adam-betas '(0.9,0.98)' \
  --adam-eps 1e-6 \
  --bpe $BPE \
  --clip-norm 0.0 \
  --arch roberta_large \
  --sample-break-mode complete \
  --tokens-per-sample $TOKENS_PER_SAMPLE \
  --lr-scheduler polynomial_decay \
  --lr $PEAK_LR \
  --fp16 \
  --mask-whole-words \
  --save-dir $SAVE_DIR \
  --warmup-updates $WARMUP_UPDATES \
  --total-num-update $TOTAL_UPDATES \
  --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
  --batch-size $MAX_SENTENCES --update-freq $UPDATE_FREQ \
  --skip-invalid-size-inputs-valid-test \
  --save-interval-updates $SAVE_INTERVAL_UPDATES \
  --tensorboard-logdir $LOG_DIR \
  --restore-file $RESTORE_CHECKPOINT \
  --reset-optimizer --reset-dataloader --reset-meters --reset-lr-scheduler \
  --max-update $TOTAL_UPDATES &> "$DIR_OUTPUT/training-$(date +"%Y-%m-%d_%H-%M-%S").log"
#   --num-workers 4 \
