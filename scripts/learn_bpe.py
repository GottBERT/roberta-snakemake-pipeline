#!/usr/bin/env python3

from tokenizers import ByteLevelBPETokenizer
import argparse

def main():
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--input')
  parser.add_argument('--bpe_size', type=int)
  parser.add_argument('--out')
  
  args = parser.parse_args()

  # Initialize a tokenizer
  tokenizer = ByteLevelBPETokenizer(add_prefix_space=False)

  # special tokens
  special_tokens = ["<s>", "<pad>", "</s>", "<unk>"]
  vocab_size = int(args.bpe_size) + len(special_tokens)

  # Customize training
  tokenizer.train(
    files=[args.input], 
    vocab_size=vocab_size, 
    min_frequency=2, 
    special_tokens=special_tokens
  )

  # Save files to disk
  tokenizer.save_model(args.out)

if __name__ == '__main__':
    main()