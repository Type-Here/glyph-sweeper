#!/bin/bash

# Default settings
SUBSTITUTE=0
EXTENDED=0
PRINT_SUB=0
FILE=""

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -s|--substitute) SUBSTITUTE=1 ;;
        -e|--extended) EXTENDED=1 ;;
        -p|--print-substitutions) PRINT_SUB=1 ;;
        -h|--help)
            echo "Usage: $0 [filename] [-s] [-e] [-p]"
            echo "Options:"
            echo "  -s, --substitute           Substitute hidden unicode characters"
            echo "  -e, --extended             Use extended substitution list"
            echo "  -p, --print-substitutions  Print the substitution list"
            exit 0
            ;;
        *) FILE="$1" ;;
    esac
    shift
done

# Base and Extended Substitution Dictionaries in Perl Format (s/FIND/REPLACE/g)
# We use Unicode code points \x{XXXX}
DICT_STD="s/\x{200B}//g; s/\x{200C}//g; s/\x{200D}//g; s/\x{FEFF}//g; s/\x{2013}/-/g; s/\x{2014}/-/g; s/\x{2018}/'/g; s/\x{2019}/'/g; s/\x{201C}/\"/g; s/\x{201D}/\"/g; s/\x{2026}/.../g; s/\x{0131}/i/g;"

DICT_EXT="s/\x{2190}/<-/g; s/\x{2191}/^/g; s/\x{2192}/->/g; s/\x{2193}/v/g; s/\x{2194}/<->/g; s/\x{21D0}/<=/g; s/\x{21D2}/=>/g; s/\x{21D4}/<=>/g; s/\x{27F5}/<-/g; s/\x{27F6}/->/g; s/\x{27F7}/<->/g; s/\x{2260}/!=/g; s/\x{2264}/<=/g; s/\x{2265}/>=/g; s/\x{2248}/~/g; s/\x{221E}/inf/g; s/\x{2211}/sum/g; s/\x{220F}/prod/g; s/\x{221A}/sqrt/g; s/\x{221D}/prop/g; s/\x{2212}/-/g; s/\x{2208}/in/g; s/\x{2209}/notin/g; s/\x{2200}/forall/g; s/\x{2203}/exists/g; s/\x{00AC}/!/g; s/\x{2227}/&&/g; s/\x{2228}/||/g; s/\x{22C5}/*/g; s/\x{27E8}/</g; s/\x{27E9}/>/g; s/\x{3010}/[/g; s/\x{3011}/]/g; s/\x{00B7}/./g; s/\x{00D7}/x/g; s/\x{00F7}/\//g; s/\x{2022}/*/g; s/\x{25CF}/*/g; s/\x{25CB}/o/g; s/\x{25A0}/#/g; s/\x{25A1}/#/g; s/\x{2010}/-/g; s/\x{2011}/-/g; s/\x{2032}/'/g; s/\x{2033}/\"/g;"

# Print substitution lists if requested
if [ "$PRINT_SUB" -eq 1 ]; then
    echo "Printing substitution list..."
    echo "Standard: $DICT_STD"
    if [ "$EXTENDED" -eq 1 ]; then echo "Extended: $DICT_EXT"; fi
    exit 0
fi

# Validate file input
if [ -z "$FILE" ]; then
    echo "Error: Please provide a filename."
    exit 1
elif [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

echo "Checking file: $FILE for hidden/extended unicode characters..."

# Use perl to find all lines containing non-ASCII characters
perl -CSD -ne 'print "Line $.: $_" if /[^\x00-\x7F]/' "$FILE"

if [ "$SUBSTITUTE" -eq 1 ]; then
    echo "Substituting hidden unicode characters..."
    
    # Prepare the final perl command
    REPLACEMENT_CMD="$DICT_STD"
    if [ "$EXTENDED" -eq 1 ]; then
        REPLACEMENT_CMD="$DICT_STD $DICT_EXT"
    fi

    # Perl command to substitute characters in-place (cross-platform)
    perl -CSD -i -pe "$REPLACEMENT_CMD" "$FILE"
    
    echo "Substitution complete in '$FILE'."
fi
