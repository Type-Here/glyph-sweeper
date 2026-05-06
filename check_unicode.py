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
    'U+2190': '<-',   # ←
    'U+2191': '^',    # ↑
    'U+2192': '->',   # →
    'U+2193': 'v',    # ↓
    'U+2194': '<->',  # ↔
    'U+21D0': '<=',   # ⇐
    'U+21D2': '=>',   # ⇒
    'U+21D4': '<=>',  # ⇔
    'U+27F5': '<-',   # ⟵
    'U+27F6': '->',   # ⟶
    'U+27F7': '<->',  # ⟷

    # Operators / relations
    'U+2260': '!=',   # ≠
    'U+2264': '<=',   # ≤
    'U+2265': '>=',   # ≥
    'U+2248': '~',    # ≈
    'U+221E': 'inf',  # ∞
    'U+2211': 'sum',  # ∑
    'U+220F': 'prod', # ∏
    'U+221A': 'sqrt', # √
    'U+221D': 'prop', # ∝
    'U+2212': '-',    # − (minus)

    # Set / logic
    'U+2208': 'in',    # ∈
    'U+2209': 'notin', # ∉
    'U+2200': 'forall',# ∀
    'U+2203': 'exists',# ∃
    'U+00AC': '!',     # ¬
    'U+2227': '&&',    # ∧
    'U+2228': '||',    # ∨
    'U+22C5': '*',     # ⋅

    # Brackets / braces
    'U+27E8': '<',    # ⟨
    'U+27E9': '>',    # ⟩
    'U+3010': '[',    # 【
    'U+3011': ']',    # 】

    # Punctuation / misc
    'U+00B7': '.',    # ·
    'U+00D7': 'x',    # ×
    'U+00F7': '/',    # ÷
    'U+2022': '*',    # •
    'U+25CF': '*',    # ●
    'U+25CB': 'o',    # ○
    'U+25A0': '#',    # ■
    'U+25A1': '#',    # □

    # Quotes / apostrophes
    'U+2010': '-',    # ‐
    'U+2011': '-',    # ‑
    'U+2032': "'",    # ′
    'U+2033': '"',    # ″
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