# 🧹 GlyphSweeper

**GlyphSweeper** provides lightweight, dependency-free command-line tools (available in both **Python** and pure **Bash**) designed to detect, list, and substitute hidden, confusing, or non-standard Unicode characters in your text and code files. 

Invisible zero-width spaces, smart quotes, and similar-looking math operators can cause compiling errors, string matching bugs, and general headaches. `GlyphSweeper` helps you sanitize your files effortlessly.

## ✨ Features

- **🔎 Detect Hidden Characters:** Scans your file and outputs the exact line number, character, and Unicode Code Point of any out-of-range/hidden characters.
- **🔄 Standard Substitution:** Replaces common problem-makers (zero-width characters, smart quotes, en/em dashes) with their safe ASCII equivalents.
- **🚀 Extended Substitution:** Optionally replaces a wide array of math operators, arrows, brackets, and bullet points with standard ASCII representations (e.g., `∑` to `sum`, `→` to `->`).
- **📖 Dictionary Inspection:** Easily print and review all active translation maps straight from the terminal.

## 🚀 Usage

You can use either the robust Python script or the fallback Bash script depending on your environment.

### Using Python
```bash
python check_unicode.py [filename] [options]
```

### Using Bash (no Python required)
Make sure the script is executable first: `chmod +x glyphswep.sh`
```bash
./glyphswep.sh [filename] [options]
```

## 💡 Examples

### Python Examples
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

### Bash Examples
**1. Check a file**
```bash
./glyphswep.sh my_script.py
```

**2. Substitute basic and extended hidden characters**
```bash
./glyphswep.sh my_script.py -s -e
```

## 🛠️ Requirements
- **Python Script:** Python 3.6+ (No external dependencies, uses standard library).
- **Bash Script:** Standard Unix utilities (`bash`, `perl`). Works cross-platform on MacOS and Linux.

## No Warranties
**GlyphSweeper** is provided **AS-IS**, without any warranty or guarantee of fitness for a particular purpose. Use at your own risk. The authors are not responsible for any data loss or issues arising from the use of these tools.
