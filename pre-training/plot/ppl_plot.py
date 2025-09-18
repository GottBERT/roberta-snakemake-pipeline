#!/usr/bin/env python

import pandas as pd
import sys

from io import StringIO   
import pandas as pd
import csv
import matplotlib.pyplot as plt
import re
import fire
import os

dir = "/mnt/d/GottBERT/"
log_interval = 25

names = {
    "filtered,large":"clean/large/fairseq/training-2023-06-12_11-54-06.log",
    "filtered,base":"clean/base/fairseq/training-2023-06-08_09-04-32.log",
    "large":"dirty/large/fairseq/training-2023-06-18_21-49-22.log",
    "base":"dirty/base/fairseq/training-2020-07-23_11-19-57.log"
}


def get_content(logfile):
  # Open a file: file
  file = open(logfile, mode='r')

  # read all lines at once
  content = file.read()

  # close the file
  file.close()

  return content;


def parse_content(content, type, model, col_suffix='', dir_tmp="/tmp"):
  p = re.compile("(.*\{\"epoch\".*)\n")
  result = p.findall(content)

  log=StringIO('\n'.join(result))

  # load file
  df_logs = pd.read_csv(log, delimiter='|', header=None, skipinitialspace=True)
  df_logs_json = df_logs[df_logs[2] == type][3]
  df_logs_json.to_csv(f"{dir_tmp}/tmp.json", sep=";", index=False, quoting=csv.QUOTE_NONE, header=False)
  
  df_stats = pd.read_json(f"{dir_tmp}/tmp.json", lines=True)
  df_stats['num_updates'] = df_stats[f"{col_suffix}num_updates"]
  df_stats['model'] = model
  df_stats["ppl"] = df_stats[f"{col_suffix}ppl"]

  return df_stats


ax=[]
i=0
for item in names.items():
    model = item[0]
    logfile=os.path.join(dir,item[1])

    content = get_content(logfile)

    # df_tmp = parse_content(content, 'train_inner ', model)
    df_tmp = parse_content(content, 'valid ', model, 'valid_')

    df_stats = pd.DataFrame()
    df_stats[model] = df_tmp["ppl"]
    # if "num_updates" not in df_stats.columns:
    df_stats["num_updates"] = df_tmp["num_updates"]

    #   pd.concat(df_stats, df_tmp)
    if i == 0:
        ax.append(df_stats.plot(xlabel='step', ylabel="perplexity", x="num_updates", logy=True))
    else:
        ax.append(df_stats.plot(xlabel='step', ylabel="perplexity", x="num_updates", logy=True, ax=ax[i-1]))
    
    i=i+1
  

# plt.show()

# save file
plt.savefig(f"perplexity-plot.png")