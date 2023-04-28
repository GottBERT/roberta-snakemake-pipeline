#!/usr/bin/env python3

# https://pypi.org/project/clean-text/
from cleantext import clean
import argparse

parser = argparse.ArgumentParser(
                    prog='clean_text',
                    description='cleans a text file')
parser.add_argument('-i', '--in_file')
parser.add_argument('-o', '--out_file')
args = parser.parse_args()

with open(args.in_file, "r") as r, open(args.out_file, "w") as w:
    for line in r:
        text = clean(line,
                     lower=False,
                     fix_unicode=True,
                     no_urls=True,
                     no_emails=True,
                     no_phone_numbers=True,
                     no_emoji=True,
                     replace_with_url="",
                     replace_with_email="",
                     replace_with_phone_number="",
                     lang="de")
        w.write(text + "\n")
