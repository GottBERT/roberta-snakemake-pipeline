#!/usr/bin/env bash
export MKL_THREADING_LAYER=GNU
export XLA_EVEN_HEARTBEAT_TIMEOUT=7200
export XLA_UNEVEN_HEARTBEAT_TIMEOUT=7200

TOTAL_UPDATES=100000          # Total number of training steps
WARMUP_UPDATES=10000          # Warmup the learning rate over this many updates
PEAK_LR=0.0004                # Peak learning rate, adjust as needed
TOKENS_PER_SAMPLE=512         # Max sequence length
LOG_INTERVAL=25               # Log interval. Don't do 1, it slows things down
MAX_SENTENCES=8              # Number of sequences per batch (batch size)
UPDATE_FREQ=8                 # Increase the batch size 2x


DATASET="clean-small"
DATA_DIR="./$DATASET"
SAVE_DIR="./checkpoints"
WORLD_SIZE=1

fairseq-train $DATA_DIR \
  --distributed-world-size $WORLD_SIZE \
  --log-format json \
  --log-interval $LOG_INTERVAL \
  --task masked_lm \
  --criterion masked_lm \
  --optimizer adam \
  --num-workers 4 \
  --adam-betas '(0.9,0.98)' \
  --adam-eps 1e-6 \
  --clip-norm 0.0 \
  --arch roberta_base \
  --sample-break-mode none \
  --tokens-per-sample $TOKENS_PER_SAMPLE \
  --lr-scheduler polynomial_decay \
  --lr $PEAK_LR \
  --save-dir $SAVE_DIR \
  --warmup-updates $WARMUP_UPDATES \
  --total-num-update $TOTAL_UPDATES \
  --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
  --batch-size $MAX_SENTENCES --update-freq $UPDATE_FREQ \
  --skip-invalid-size-inputs-valid-test \
  --save-interval-updates 25 \
  --bpe hf_byte_bpe \
  --max-update $TOTAL_UPDATES &> training-$(date +"%Y-%m-%d_%H-%M-%S").log
