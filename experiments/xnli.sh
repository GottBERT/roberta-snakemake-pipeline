export TASK_NAME=xnli
export MODEL=uklfr/gottbert-base

export BATCH_SIZE=4 # 8 GPUs * 4 = 32
export LR='1e-5'
export TRAIN_EPOCHS=10
export WARMUP_RATIO=0.06   # 6 percent
export OUTPUT_DIR=~/models/$TASK_NAME-$(echo $MODEL | sed "s/\//-/")
export LANG=de

mkdir -p $OUTPUT_DIR

CUDA_VISIBLE_DEVICES="0" python run_xnli.py \
  --seed 1 \
  --model_name_or_path $MODEL \
  --language $LANG \
  --do_train \
  --do_eval \
  --do_predict \
  --warmup_ratio $WARMUP_RATIO \
  --per_device_train_batch_size $BATCH_SIZE \
  --per_device_eval_batch_size $BATCH_SIZE \
  --learning_rate $LR \
  --num_train_epochs $TRAIN_EPOCHS \
  --max_seq_length 512 \
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
  --output_dir $OUTPUT_DIR &> $OUTPUT_DIR/train.log