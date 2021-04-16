#!/usr/bin/env python3

import argparse
import fileinput
import json
import pandas as pd

from shutil import copyfile

from os import path


def main():
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--dir', required=True)
  parser.add_argument('--vocab_json', required=True)
  args = parser.parse_args()

  # create backup if not exists
  if not path.isfile(path.join(args.dir, 'dict.txt.bu')):
    print('create backup of dict.txt')
    copyfile(path.join(args.dir, 'dict.txt'), path.join(args.dir, 'dict.txt.bu'))

  # read dict.txt
  dictionary = pd.read_csv(path.join(args.dir, 'dict.txt'), delimiter=" ", header=None, names=['entry', 'count'])

  with open(args.vocab_json) as json_file:
    data = json.load(json_file)

  inverted_data = {value: key for key, value in data.items()}
  keys = list(inverted_data.keys())
  
  # remove madup words
  dictionary = dictionary[
    ~dictionary['entry'].astype("str").str.startswith("madeupword")
  ].astype('int')
  
  print(len(dictionary))
  dict_list = list(dictionary['entry'])

  # add missing ones skipping special tokens (first 4 ones)
  for key in keys[4:]:
    if int(key) not in dict_list:
      dictionary = dictionary.append({'entry': key, 'count': 0}, ignore_index=True)


  # add madeupwords
  n=0
  while (len(dictionary) + 4) % 8 != 0:
    dictionary = dictionary.append({'entry': f'madeupword{n:04}', 'count': 0}, ignore_index=True)
    n=n+1

  print(len(dictionary))

  dictionary.to_csv(path.join(args.dir, 'dict.txt'), index=False, header=False, sep=" ")

if __name__ == '__main__':
  main()