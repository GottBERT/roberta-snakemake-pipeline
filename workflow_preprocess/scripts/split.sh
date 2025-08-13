#!/bin/bash

set -euo pipefail

# === CONFIGURE THESE ===
INPUT_FILE="/home/data/corpus/final/shuffled_coprus.txt"                         # Input corpus file
OUTPUT_FILE="/home/data/corpus/final/shuffled_coprus_split.txt"                       # Final output
TOKENIZER_DIR="/home/data/corpus/final/output/bpe_enc/"                  # Folder with vocab.json + merges.txt
MAX_TOKENS=500                                 # Token limit per chunk (510 if RoBERTa)
SCRIPT_PATH="./split_documents.py"             # Path to your Python script

# # === CONFIGURE THESE ===
# INPUT_FILE="test/test.txt"                         # Input corpus file
# OUTPUT_FILE="test/test_split.txt"                       # Final output
# TOKENIZER_DIR="/home/data/corpus/final/output/bpe_enc/"                  # Folder with vocab.json + merges.txt
# MAX_TOKENS=512                                 # Token limit per chunk (510 if RoBERTa)
# SCRIPT_PATH="./split_documents.py"             # Path to your Python script

# === AUTO-DETECT CORES ===
NUM_PARALLEL_JOBS=$(nproc)
echo "Detected $NUM_PARALLEL_JOBS CPU cores."

# === COMPUTE LINES PER CHUNK ===
TOTAL_LINES=$(wc -l < "$INPUT_FILE")
CHUNK_LINES=$(( (TOTAL_LINES + NUM_PARALLEL_JOBS - 1) / NUM_PARALLEL_JOBS ))
echo "Input has $TOTAL_LINES lines. Splitting into $NUM_PARALLEL_JOBS chunks of ~$CHUNK_LINES lines each."

# === WORKING DIRS ===
TMP_DIR=$(mktemp -d split_tmp.XXXX)
CHUNKS_DIR="$TMP_DIR/chunks"
OUT_DIR="$TMP_DIR/output"
mkdir -p "$CHUNKS_DIR" "$OUT_DIR"

# === SPLIT FILE ===
split -l "$CHUNK_LINES" "$INPUT_FILE" "$CHUNKS_DIR/chunk_"

# === PARALLEL PROCESSING ===
echo "Processing chunks in parallel..."
ls "$CHUNKS_DIR"/chunk_* | parallel -j "$NUM_PARALLEL_JOBS" '
    chunk={}
    out_file='$OUT_DIR'/$(basename $chunk).out
    '$SCRIPT_PATH' -i $chunk -o $out_file -m '$MAX_TOKENS' -t '$TOKENIZER_DIR'
'

# === MERGE OUTPUT ===
echo "Merging output files..."
cat "$OUT_DIR"/*.out > "$OUTPUT_FILE"

# === CLEANUP ===
rm -rf "$TMP_DIR"

echo "✅ Done! Output saved to: $OUTPUT_FILE"
