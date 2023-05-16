#!/usr/bin/env python3

import sys

from io import StringIO   
import pandas as pd
import csv
import matplotlib.pyplot as plt
import re
import fire

def generate_plot(logfile, dir_target, log_interval):

  # Open a file: file
  file = open(logfile, mode='r')

  # read all lines at once
  content = file.read()

  # close the file
  file.close()

  p = re.compile("(.*\{\"epoch\".*)\n")
  result = p.findall(content)

  log=StringIO('\n'.join(result))

  # load file
  df_logs = pd.read_csv(log, delimiter='|', header=None, skipinitialspace=True)
  df_logs_json = df_logs[df_logs[2] == 'train_inner '][3]
  df_logs_json.to_csv(f"{dir_target}/tmp.json", sep=";", index=False, quoting=csv.QUOTE_NONE, header=False)

  df_stats = pd.read_json(f"{dir_target}/tmp.json", lines=True)

  # correct wps according to log_interval
  # https://github.com/pytorch/fairseq/issues/1045#issuecomment-628048646
  df_stats['wps'] = df_stats['wps'] * int(log_interval)

  df_stats.index=df_stats['num_updates']
  plot = df_stats['loss'].plot()
  fig = plot.get_figure()

  # save file
  fig.savefig(f"{dir_target}/plot.pdf")

if __name__ == '__main__':
  fire.Fire(generate_plot)
