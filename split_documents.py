#!/usr/bin/env python

import argparse
import os
import re
import sys
from tokenizers import ByteLevelBPETokenizer

def split_if_too_long(document, max_tokens, tokenizer):
    encoding = tokenizer.encode(document, add_special_tokens=False)

    if len(encoding.ids) <= max_tokens:
        return [document.strip() + "\n"]

    # Only now: split at sentence boundaries
    sentence_delimiters = r"([.!?;\-])"
    parts = re.split(sentence_delimiters, document)

    if len(parts) < 2:
        sys.stderr.write(f"[warn] No delimiters, doing hard token split: {document[:80]}...\n")
        ids = encoding.ids
        chunks = []
        for i in range(0, len(ids), max_tokens):
            chunk_ids = ids[i:i + max_tokens]
            chunk = tokenizer.decode(chunk_ids).strip() + "\n"
            chunks.append(chunk)
        return chunks

    sentences = ["".join(parts[i:i+2]).strip() for i in range(0, len(parts) - 1, 2)]

    chunks = []
    current_chunk = ""
    current_len = 0

    for sentence in sentences:
        token_len = len(tokenizer.encode(sentence, add_special_tokens=False).ids)

        if current_len + token_len <= max_tokens:
            current_chunk += " " + sentence if current_chunk else sentence
            current_len += token_len
        else:
            if current_chunk:
                chunks.append(current_chunk.strip() + "\n")
            current_chunk = sentence
            current_len = token_len

    if current_chunk:
        chunks.append(current_chunk.strip() + "\n")

    return chunks

def process_corpus(input_file, output_file, max_tokens, tokenizer_path):
    if os.path.isdir(tokenizer_path):
        vocab_path = os.path.join(tokenizer_path, "vocab.json")
        merges_path = os.path.join(tokenizer_path, "merges.txt")
    else:
        raise ValueError("Tokenizer path must be a directory containing vocab.json and merges.txt")

    tokenizer = ByteLevelBPETokenizer(vocab_path, merges_path)

    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            document = line.strip()
            if not document:
                continue

            chunks = split_if_too_long(document, max_tokens, tokenizer)
            outfile.writelines(chunks)

    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split documents only if they exceed max token length.")
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-m", "--max_tokens", type=int, required=True)
    parser.add_argument("-t", "--tokenizer", required=True)

    args = parser.parse_args()
    process_corpus(args.input, args.output, args.max_tokens, args.tokenizer)
