export MKL_THREADING_LAYER=GNU
export XLA_EVEN_HEARTBEAT_TIMEOUT=7200
export XLA_UNEVEN_HEARTBEAT_TIMEOUT=7200

TOTAL_UPDATES=100000          # Total number of training steps
SAVE_INTERVAL_UPDATES=100000  # Save intervals (should be multiple of total updates)
WARMUP_UPDATES=10000          # Warmup the learning rate over this many updates
PEAK_LR=0.00015               # Peak learning rate, adjust as needed
TOKENS_PER_SAMPLE=512         # Max sequence length
LOG_INTERVAL=25               # Log interval. Don't do 1, it slows things down
MAX_SENTENCES=32              # Number of sequences per batch (batch size)
UPDATE_FREQ=4                 # Increase the batch size 2x

DIR_OUTPUT="/home/scheible/mnt"

DATA_DIR="/home/scheible/data_pt/norberto"
SAVE_DIR="$DIR_OUTPUT/checkpoints"
LOG_DIR="$DIR_OUTPUT/logs"
BPE_MERGES=$DATA_DIR/merges.txt
BPE_VOCAB=$DATA_DIR/vocab.json

WORLD_SIZE=128
TPU_NAME=tum-bert-tpu-$WORLD_SIZE
TPU_NUM_DEVICES=$((WORLD_SIZE/2))

# training command
python3 -m torch_xla.distributed.xla_dist \
  --tpu=$TPU_NAME \
  --restart-tpuvm-pod-server \
  --env=MKL_THREADING_LAYER=GNU \
  --env=TPUv4=True \
  -- \
  /home/scheible/.local/bin/fairseq-train $DATA_DIR \
  --distributed-world-size $TPU_NUM_DEVICES \
  --no-epoch-checkpoints \
  --tpu \
  --log-format json \
  --log-interval $LOG_INTERVAL \
  --task masked_lm \
  --criterion masked_lm \
  --optimizer adam \
  --adam-betas '(0.9,0.98)' \
  --adam-eps 1e-6 \
  --clip-norm 0.0 \
  --arch roberta_large \
  --save-dir $SAVE_DIR \
  --sample-break-mode none \
  --tokens-per-sample $TOKENS_PER_SAMPLE \
  --lr-scheduler polynomial_decay \
  --lr $PEAK_LR \
  --total-num-update $TOTAL_UPDATES \
  --warmup-updates $WARMUP_UPDATES \
  --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
  --batch-size $MAX_SENTENCES --update-freq $UPDATE_FREQ \
  --skip-invalid-size-inputs-valid-test \
  --save-interval-updates $SAVE_INTERVAL_UPDATES \
  --tensorboard-logdir $LOG_DIR \
  --max-update $TOTAL_UPDATES &> "$DIR_OUTPUT/training-$(date +"%Y-%m-%d_%H-%M-%S").log" 
