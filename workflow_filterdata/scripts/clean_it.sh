#!/usr/bin/env bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# for regex information see https://www.regular-expressions.info/unicode.html
${DIR}/clean_text.py -p ${1} \
    | grep -P -v '^\s*$' \
    | grep -P -v '\\{2,}' \
    | grep -P -v '(\/ ){3,}|(\/){3,}' \
    | grep -P -v '[A-Za-z0-9]{25,}' \
    | perl -CSD -Mutf8 -pe \
        's/\p{Modifier_Symbol}+|\p{Other_Symbol}+|\p{Unassigned}+|\p{Private_Use}+|\p{Surrogate}+|\p{Mark}+|\p{Other_Letter}+//g'

    # | grep -P -v '\\{2,}' \
    # | grep -P -v '(?:([-[\](){}><]+ *\w* *[-[\](){}><]+) *\w* *){5,}' \
    # | grep -P -o '(^\p{Lu}|(?<=[.!?]\s))\p{Lu}.{50,}(\w\.|\s\!|\s\?)+' | grep -P -v '\d+ Fax|Tel \(' \
    # | grep -P -v '[eE]mail|[fF]ax|[tT]elefon|[tT]el|[kK]ontact|[i|I]nfo *[@:]+' \
    # | grep -P -v '^:' \
    # | grep -P -v '(\/ ){3,}|(\/){3,}' \
    # | grep -P -v '[A-Za-z0-9]{25,}' \
    # | grep -P -v '(\w{4,}\d{2,})|(\d{2,}\w{4,})' \
    # | grep -P '^(?!.*(.)\1{5,})' \
    # | grep -P '^(?!.*(..)\1{5,})' \


    # | grep -P -v '\\{2,}' \
    # | grep -P -v '\(weiter lesen\)' \
    # | grep -P -v '\(Weiter\)' \
    # | grep -P -v '\(mehr Text anzeigen\)' \
    # | grep -P -v '(?:([-[\](){}><]+ *\w* *[-[\](){}><]+) *\w* *){5,}' \
    # | grep -P -o '(^\p{Lu}|(?<=[.!?]\s))\p{Lu}.{50,}(\w\.|\s\!|\s\?)+' | grep -P -v '\d+ Fax|Tel \(' \
    # | grep -P -v '[eE]mail|[fF]ax|[tT]elefon|[tT]el|[kK]ontact|[i|I]nfo *[@:]+' \
    # | grep -P -v '^:' \
    # | grep -P -v '(\/ ){3,}|(\/){3,}' \
    # | grep -P -v '[A-Za-z0-9]{25,}' \
    # | grep -P -v '(\w{4,}\d{2,})|(\d{2,}\w{4,})' \
    # | grep -P '^(?!.*(.)\1{5,})' \
    # | grep -P '^(?!.*(..)\1{5,})' \