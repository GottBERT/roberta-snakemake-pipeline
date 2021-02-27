#!/usr/bin/env python3

import argparse
import fileinput
import json

from os import path

from tokenizers import ByteLevelBPETokenizer


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--bpe', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('files', nargs='*', help='input files')
    args = parser.parse_args()

    tok = ByteLevelBPETokenizer(
        path.join(args.bpe,'vocab.json'),
        path.join(args.bpe,'merges.txt'),
        add_prefix_space=False,
    )

    out_h = open(args.out, 'w')

    num_skipped = 0
    itr = fileinput.input(args.files, openhook=fileinput.hook_compressed)
    for i, line in enumerate(itr, start=1):
        if i % 100 == 0:
            print('.', end='', flush=True)
        if i % 10000 == 0:
            print()

        # removing new line
        computing_line = line[:-1]

        # BPE encode the line
        if len(computing_line) > 0:
            bpe = ' '.join(map(str, tok.encode(computing_line).ids))


            # output context and target to files
            print(bpe+"\n", file=out_h)

    print('skipped {} examples'.format(num_skipped))

    out_h.close()


if __name__ == '__main__':
    main()