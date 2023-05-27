#!/usr/bin/env python3

import argparse
import json
import pandas as pd

from shutil import copyfile

from os import path


def main():
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--indir', required=True)
  parser.add_argument('--outdir', required=True)
  parser.add_argument('--add-specials', action='store_true',
                      help='add <s>, <pad>, </s> and <unk>')
  args = parser.parse_args()

  with open(path.join(args.indir, 'vocab.json')) as json_file:
    data = json.load(json_file)

  inverted_data = {value: key for key, value in data.items()}

  dictionary = pd.read_csv(path.join(args.indir, 'dict.txt'), delimiter=" ", header=None, names=['index', 'count'])

  if getattr(args, 'add_specials', False):
    json_result_inverted = {0:"<s>", 1:"<pad>", 2: "</s>", 3: "<unk>"}
    k=4
  else:
    json_result_inverted = {}
    k=0


  for key in dictionary['index']:
    if not str(key).startswith('madeupword'):
      json_result_inverted[k] = inverted_data[int(key)]
    else:
      json_result_inverted[k] = key
    
    k=k+1

  # add <mask> as last thing
  json_result_inverted[k] = "<mask>"
  
  # sort
  json_result_inverted_sorted = {}
  for key in sorted(json_result_inverted.keys()):
    json_result_inverted_sorted[key] = json_result_inverted[key]

  json_result = {value: int(key) for key, value in json_result_inverted_sorted.items()}

  with open(path.join(args.outdir, 'vocab.json'), 'w') as outfile:
    json.dump(json_result, outfile, ensure_ascii=False)

  copyfile(path.join(args.indir, 'merges.txt'), path.join(args.outdir, 'merges.txt'))

if __name__ == '__main__':
  main()