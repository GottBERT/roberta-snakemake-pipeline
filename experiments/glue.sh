export TASK_NAME=mrpc
export BATCH_SIZE=16
export LR=1e-5
export TOTAL_UPDATES=2296
export WARMUP_UPDATES=137
export OUTPUT_DIR=/tmp/$TASK_NAME/
export MODEL=uklfr/gottbert-base

python run_glue.py \
  --seed 1 \
  --model_name_or_path $MODEL \
  --task_name $TASK_NAME \
  --do_train \
  --do_eval \
  --do_predict \
  --max_seq_length 512 \
  --per_device_train_batch_size $BATCH_SIZE \
  --per_device_eval_batch_size $BATCH_SIZE \
  --learning_rate $LR \
  --max_steps $TOTAL_UPDATES \
  --warmup_steps $WARMUP_UPDATES \
  --fp16 \
  --optim adamw_torch \
  --adam_epsilon 1e-06 \
  --adam_beta1 0.9 \
  --adam_beta2 0.98 \
  --max_grad_norm 0.0 \
  --weight_decay 0.1 \
  --lr_scheduler_type polynomial \
  --save_total_limit 1 \
  --load_best_model_at_end \
  --save_strategy epoch \
  --evaluation_strategy epoch \
  --metric_for_best_model accuracy \
  --overwrite_output_dir \
  --output_dir $OUTPUT_DIR



# --num_train_epochs 10
# maybe use --bf16 instead of --fp16

# for STS-B:
# --metric_for_best_model loss
# --greater_is_better?


 TOTAL_NUM_UPDATES=2036  # 10 epochs through RTE for bsz 16
WARMUP_UPDATES=122      # 6 percent of the number of updates
LR=2e-05                # Peak LR for polynomial LR scheduler.
NUM_CLASSES=2
MAX_SENTENCES=16        # Batch size.
ROBERTA_PATH=/path/to/roberta/model.pt

CUDA_VISIBLE_DEVICES=0 fairseq-train RTE-bin/ \
    #--max-tokens 4400 \
    #--task sentence_prediction \
    #--reset-optimizer --reset-dataloader --reset-meters \
    #--required-batch-size-multiple 1 \
    #--init-token 0 --separator-token 2 \
    #--arch roberta_large \
    #--criterion sentence_prediction \
    #--num-classes $NUM_CLASSES \
    #--dropout 0.1 --attention-dropout 0.1 \ 
    # --fp16-init-scale 4 --threshold-loss-scale 1 --fp16-scale-window 128 \
    #--max-epoch 10 \
    #--find-unused-parameters \
    #--best-checkpoint-metric accuracy --maximize-best-checkpoint-metric;