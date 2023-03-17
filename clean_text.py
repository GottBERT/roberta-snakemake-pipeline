#!/usr/bin/env python3

from cleantext import clean

INFILE = "files/example/de_dedup.txt"
OUTFILE = "de_dedup_cleaned.txt"

with open(INFILE, "r") as r, open(OUTFILE, "w") as w:
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
