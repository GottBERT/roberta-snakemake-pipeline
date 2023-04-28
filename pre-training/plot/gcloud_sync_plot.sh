#!/usr/bin/env bash

export vm_name=$1
export log_file=$2
export output=${3:-plot/}
export log_interval=${4:-25}

function sync() {
  gcloud compute scp "$vm_name":"~/$log_file" .
  $(dirname $0)/create_plot.py $log_file $output $log_interval
}

sync