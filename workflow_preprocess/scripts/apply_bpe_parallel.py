#!/usr/bin/env python3

import argparse
import fileinput
import multiprocessing
from functools import partial
import uuid

import os
from os import path
import glob

from tokenizers import ByteLevelBPETokenizer

def encode(file, result_file_pattern, tmp_file_pattern, dir_bpe):
    tok = ByteLevelBPETokenizer(
        path.join(dir_bpe,'vocab.json'),
        path.join(dir_bpe,'merges.txt'),
        add_prefix_space=False,
    )

    num_skipped = 0
    out_file = result_file_pattern + file.replace(tmp_file_pattern, "")
    print(out_file)

    out_h = open(out_file, 'w')
    itr = fileinput.input(file, openhook=fileinput.hook_compressed)
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

    out_h.close()

    return num_skipped

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--bpe', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--dir_tmp', help='tmp folder', default=f'/tmp', required=False)
    parser.add_argument('--cores', help='how many cores/threads available', default=multiprocessing.cpu_count(), required=False)
    parser.add_argument('file', help='input file')
    args = parser.parse_args()

    with open(args.file, 'r') as fp:
        for count, line in enumerate(fp):
            pass

    print('Total Lines', count)
    lines_per_file = int((count + int(args.cores)) / int(args.cores))

    print('Lines per file', lines_per_file)
    dir_tmp = path.join(args.dir_tmp, str(uuid.uuid4()))
    dir_tmp_splits = path.join(dir_tmp, 'splits')
    dir_tmp_results = path.join(dir_tmp, 'results')

    # if count/args.cores
    tmp_file_pattern = os.path.join(dir_tmp_splits, 'raw_')
    result_file_pattern = os.path.join(dir_tmp_results, 'bpe_')

    # create tmp folders
    os.system(f"mkdir -p \"{dir_tmp_splits}\"")
    os.system(f"mkdir -p \"{dir_tmp_results}\"")

    # remove existing split files
    os.system(f"rm -f \"{tmp_file_pattern}*\"")

    # do split
    print('do split')
    os.system(f"""
        split \
        -d \
        --additional-suffix=".txt" \
        --lines={lines_per_file} "{args.file}" "{tmp_file_pattern}"
    """)
    print('split done')

    # parallel execute
    files = glob.glob(f"{tmp_file_pattern}*")
    pool = multiprocessing.Pool(int(args.cores))

    skipped = pool.map(
                    partial(encode,
                                dir_bpe=args.bpe,
                                result_file_pattern=result_file_pattern,
                                tmp_file_pattern=tmp_file_pattern),
                    files)
    print('skipped {} examples'.format(sum(skipped)))

    # remove tmp split files
    os.system(f"rm -rf \"{dir_tmp}*\"")
    
    # merge results
    str_result_files = " ".join(glob.glob(f"{result_file_pattern}*"))
    os.system(f"cat {str_result_files} > {args.out}")

if __name__ == '__main__':
    main()