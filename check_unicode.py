# Check file for hidden unicode characters
# Usage: python check_unicode.py <filename>
# Prints any lines containing hidden unicode characters, 
# line number, and the character(s) found
import sys
import re
import argparse

substitution_dict = {
    'U+200B': '', #'Zero Width Space'
    'U+200C': '', #'Zero Width Non-Joiner'
    'U+200D': '', #'Zero Width Joiner'
    'U+FEFF': '', #'Zero Width No-Break Space'
    'U+2013': '-', #'En Dash'
    'U+2014': '-', #'Em Dash'
    'U+2018': "'", #'Left Single Quotation Mark'
    'U+2019': "'", #'Right Single Quotation Mark'
    'U+201C': '"', #'Left Double Quotation Mark'
    'U+201D': '"', #'Right Double Quotation Mark'
    'U+2026': '...', #'Horizontal Ellipsis'
    'U+0131': 'i', # 'Latin Small Letter Dotless I'
}

substitution_extended = {
    # Arrows (cardinal + common)
    'U+2190': '<-',   # Leftwards Arrow
    'U+2191': '^',    # Upwards Arrow
    'U+2192': '->',   # Rightwards Arrow
    'U+2193': 'v',    # Downwards Arrow
    'U+2194': '<->',  # Left Right Arrow
    'U+21D0': '<=',   # Leftwards Double Arrow
    'U+21D2': '=>',   # Rightwards Double Arrow
    'U+21D4': '<=>',  # Left Right Double Arrow
    'U+27F5': '<-',   # Long Leftwards Arrow
    'U+27F6': '->',   # Long Rightwards Arrow
    'U+27F7': '<->',  # Long Left Right Arrow

    # Operators / relations
    'U+2260': '!=',   # Not Equal To
    'U+2264': '<=',   # Less-Than Or Equal To
    'U+2265': '>=',   # Greater-Than Or Equal To
    'U+2248': '~',    # Almost Equal To
    'U+221E': 'inf',  # Infinity
    'U+2211': 'sum',  # N-Ary Summation
    'U+220F': 'prod', # N-Ary Product
    'U+221A': 'sqrt', # Square Root
    'U+221D': 'prop', # Proportional To
    'U+2212': '-',    # Minus Sign

    # Set / logic
    'U+2208': 'in',    # Element Of
    'U+2209': 'notin', # Not An Element Of
    'U+2200': 'forall',# For All
    'U+2203': 'exists',# There Exists
    'U+00AC': '!',     # Not Sign
    'U+2227': '&&',    # Logical And
    'U+2228': '||',    # Logical Or
    'U+22C5': '*',     # Dot Operator

    # Brackets / braces
    'U+27E8': '<',    # Mathematical Left Angle Bracket
    'U+27E9': '>',    # Mathematical Right Angle Bracket
    'U+3010': '[',    # Left Black Lenticular Bracket
    'U+3011': ']',    # Right Black Lenticular Bracket

    # Punctuation / misc
    'U+00B7': '.',    # Middle Dot
    'U+00D7': 'x',    # Multiplication Sign
    'U+00F7': '/',    # Division Sign
    'U+2022': '*',    # Bullet
    'U+25CF': '*',    # Black Circle
    'U+25CB': 'o',    # White Circle
    'U+25A0': '#',    # Black Square
    'U+25A1': '#',    # White Square

    # Quotes / apostrophes
    'U+2010': '-',    # Hyphen
    'U+2011': '-',    # Non-Breaking Hyphen
    'U+2032': "'",    # Prime
    'U+2033': '"',    # Double Prime
}


def find_hidden_unicode_from_content(content):
    hidden_unicode_pattern = re.compile(r'[^\x00-\x7F]+')
    matches = hidden_unicode_pattern.findall(content)
    if matches:
        lines = content.splitlines()
        for i, line in enumerate(lines, start=1):
            if hidden_unicode_pattern.search(line):
                print(f"Line {i}: {line.strip()}")
                line_matches = hidden_unicode_pattern.findall(line)
                print(f"Hidden Unicode Characters: {', '.join(line_matches)}\n")
                code_points = [f"U+{ord(ch):04X}" for m in line_matches for ch in m]
                print(f"Unicode Code Points: {', '.join(code_points)}\n")

def substitute_hidden_unicode_from_content(content, substitutions):
    hidden_unicode_pattern = re.compile(r'[^\x00-\x7F]')
    changed = False

    def _repl(match):
        nonlocal changed
        ch = match.group(0)
        code_point = f"U+{ord(ch):04X}"
        substitute = substitutions.get(code_point, ch)
        if substitute != ch:
            changed = True
        return substitute

    new_content = hidden_unicode_pattern.sub(_repl, content)
    return new_content, changed

def print_substitutions_nice(substitutions):
    print("=" * 45)
    print(f"{'Code Point':<12} | {'Char':<4} | {'Replacement'}")
    print("=" * 45)
    for code_point in sorted(substitutions.keys()):
        # Check if the code point is in the format 'U+XXXX'
        char = chr(int(code_point[2:], 16))
        substitute = substitutions[code_point]
        
        # Format the empty string case for better display
        if substitute == '':
            substitute_display = '<empty>'
        else:
            substitute_display = f"'{substitute}'"
            
        print(f"{code_point:<12} | {char:<4} | {substitute_display}")
    print("=" * 45)
    print(f"Total mappings: {len(substitutions)}\n")


if __name__ == "__main__":
    # Add arg parser for better command line handling
    parse = argparse.ArgumentParser(description='Check a file for hidden unicode characters.')
    parse.add_argument('filename', help='The file to check for hidden unicode characters', type=str, nargs='?')
    parse.add_argument('-s', '--substitute', help='Substitute hidden unicode characters with a predefined list', action='store_true')
    parse.add_argument('-e', '--extended', help='Use extended substitution list', action='store_true')
    parse.add_argument('-p', '--print-substitutions', help='Print the substitution dictionary', action='store_true')

    args = parse.parse_args()

    substitutions = {**substitution_dict, **(substitution_extended if args.extended else {})}

    if args.print_substitutions:
        print_substitutions_nice(substitutions)
        exit(0)

    if not args.filename:
        print("Error: Please provide a filename to check for hidden unicode characters.\n")
        parse.print_help() # Stampa l'help automaticamente se manca il file
        sys.exit(1)

    print(f"Checking file: {args.filename} for hidden unicode characters...\n")

    with open(args.filename, 'r', encoding='utf-8') as file:
        content = file.read()

    find_hidden_unicode_from_content(content)

    if args.substitute:
        print("Substituting hidden unicode characters with replacements...")
        new_content, changed = substitute_hidden_unicode_from_content(content, substitutions)
        if changed:
            with open(args.filename, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Substituted hidden unicode characters in {args.filename}.")