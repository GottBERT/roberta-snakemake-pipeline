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
  args = parser.parse_args()

  # create backup if not exists
  # if not path.isfile(path.join(args.indir, 'vocab.json.bu')):
  #   print('create backup of vocab.json')
  #   copyfile(path.join(args.indir, 'vocab.json'), path.join(args.indir, 'vocab.json.bu'))

  #   json_file = 'vocab.json'
  # else:
  #   json_file = 'vocab.json.bu'

  json_file = 'vocab.json'

  # read dict.txt
  dictionary = pd.read_csv(path.join(args.indir, 'dict.txt'), delimiter=" ", header=None, names=['entry', 'count'])

  with open(path.join(args.indir, json_file)) as f_json_file:
    data = json.load(f_json_file)

  last_index=data[list(data)[-1]]

  # get madeup words
  madeupwords = dictionary[
    dictionary['entry'].astype("str").str.startswith("madeupword")
  ]

  for madeupword in list(madeupwords['entry']):
    last_index = last_index+1

    data[madeupword] = last_index
    
  data['<mask>'] = last_index+1

  # save hf converted vocab
  with open(path.join(args.outdir, 'vocab.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f)

  copyfile(path.join(args.indir, 'merges.txt'), path.join(args.outdir, 'merges.txt'))

if __name__ == '__main__':
  main()