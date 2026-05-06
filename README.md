# 🧹 GlyphSweeper

**GlyphSweeper** is a lightweight, zero-dependency Python command-line tool designed to detect, list, and substitute hidden, confusing, or non-standard Unicode characters in your text and code files. 

Invisible zero-width spaces, smart quotes, and similar-looking math operators can cause compiling errors, string matching bugs, and general headaches. `GlyphSweeper` helps you sanitize your files effortlessly.

## ✨ Features

- **🔎 Detect Hidden Characters:** Scans your file and outputs the exact line number, character, and Unicode Code Point of any out-of-range/hidden characters.
- **🔄 Standard Substitution:** Replaces common problem-makers (zero-width characters, smart quotes, en/em dashes) with their safe ASCII equivalents.
- **🚀 Extended Substitution:** Optionally replaces a wide array of math operators, arrows, brackets, and bullet points with standard ASCII representations (e.g., `∑` to `sum`, `→` to `->`).
- **📖 Dictionary Inspection:** Easily print and review all active translation maps straight from the terminal.

## 🚀 Usage

Run the script from the command line using Python 3:

```bash
python check_unicode.py [filename] [options]
```

### Positional Arguments
- `filename`: The file you want to check or sanitize.

### Options
- `-h`, `--help` : Show the help message and exit.
- `-s`, `--substitute` : Modify the file in-place, replacing detected Unicode characters using the defined dictionary.
- `-e`, `--extended` : Include the extended dictionary (arrows, logic operators, etc.) in your substitutions.
- `-p`, `--print-substitutions` : Print a nicely formatted table of the current substitution rules and exit.

## 💡 Examples

**1. Check a file for hidden characters (Read-only)**
```bash
python check_unicode.py my_script.py
```

**2. Substitute basic hidden characters in-place**
```bash
python check_unicode.py my_script.py -s
```

**3. Substitute using the extended mapping (math, arrows, etc.)**
```bash
python check_unicode.py my_script.py -s -e
```

**4. View the extended substitution dictionary**
```bash
python check_unicode.py -e -p
```

## 🛠️ Requirements
- Python 3.6+
- No external dependencies (uses standard library `sys`, `re`, `argparse`).
