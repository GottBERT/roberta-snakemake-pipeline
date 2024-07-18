#!/usr/bin/env python3

import sys
import argparse
import os


parser = argparse.ArgumentParser("test_ml")

parser.add_argument("--cp", dest="cp", help="checkpoint file name", type=str, default="checkpoint_best.pt")
parser.add_argument("--dir", dest="dir", help="dir of checkpoints", type=str, default="~/checkpoints")
parser.add_argument("--ms", dest="ms", help="masked sentence", type=str, default="In der Stadt traf ich einen <mask> Mann.")
parser.add_argument("--k", dest="k", help="number of predictions", type=int, default=5)

args = parser.parse_args()

print(args)

from fairseq.models.roberta import GottbertModel
gottbert = GottbertModel.from_pretrained(os.path.normpath(args.dir), checkpoint_file=args.cp)
gottbert.eval()  # disable dropout (or leave in train mode to finetune)

filled = gottbert.fill_mask(args.ms, topk=args.k)

fairseq_predictions = list(map(lambda x: x[2], filled))

print(fairseq_predictions)
