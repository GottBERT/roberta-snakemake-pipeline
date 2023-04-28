#!/usr/bin/env bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# fix encodings, remove bad encodings and remove special symbols
${DIR}/clean_text.py -p ${1} \
    | grep -axv '.*' \
    | grep -va '�' \
    | perl -CSD -Mutf8 -pe \
        's/\p{Modifier_Symbol}+|\p{Other_Symbol}+|\p{Unassigned}+|\p{Private_Use}+|\p{Surrogate}+|\p{Mark}+|\p{Other_Letter}+//g' 
