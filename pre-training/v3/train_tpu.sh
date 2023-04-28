#!/usr/bin/env bash
export MKL_THREADING_LAYER=GNU
export XLA_EVEN_HEARTBEAT_TIMEOUT=7200
export XLA_UNEVEN_HEARTBEAT_TIMEOUT=7200

SAVE_INTERVAL=2000
TOTAL_UPDATES=100000          # Total number of training steps
WARMUP_UPDATES=10000          # Warmup the learning rate over this many updates
PEAK_LR=0.0004                # Peak learning rate, adjust as needed
TOKENS_PER_SAMPLE=512         # Max sequence length
LOG_INTERVAL=25               # Log interval. Don't do 1, it slows things down
MAX_SENTENCES=16              # Number of sequences per batch (batch size)
UPDATE_FREQ=64                # Increase the batch size 2x

GCLOUD_ZONE="europe-west4-a"

DATASET="clean_test"
DATA_DIR="/home/scheiblr/data/$DATASET"
WORLD_SIZE=8
TPU_NAME=uklfr-bert-tpu-$WORLD_SIZE

export TPU_IP_ADDRESS=$(gcloud compute tpus describe $TPU_NAME --zone $GCLOUD_ZONE | grep "\- ipAddress:" | cut -d" " -f3)
export XRT_TPU_CONFIG="tpu_worker;0;$TPU_IP_ADDRESS:8470"

fairseq-train $DATA_DIR \
  --distributed-world-size $WORLD_SIZE \
  --tpu \
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
  --save-dir checkpoints \
  --warmup-updates $WARMUP_UPDATES \
  --total-num-update $TOTAL_UPDATES \
  --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
  --batch-size $MAX_SENTENCES --update-freq $UPDATE_FREQ \
  --skip-invalid-size-inputs-valid-test \
  --save-interval 3 \
  --save-interval-updates $SAVE_INTERVAL \
  --max-update $TOTAL_UPDATES &> training-$(date +"%Y-%m-%d_%H-%M-%S").log
  # (yes | gcloud compute instance-groups managed delete $GCLOUD_INSTANCE_GROUP --zone $GCLOUD_ZONE) 
  # && (yes | gcloud compute tpus delete $TPU_NAME --zone $GCLOUD_ZONE)
