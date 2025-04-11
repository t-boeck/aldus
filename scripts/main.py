"""
main.py

Reads English text, uses translator.py to get Chinese paragraphs,
generates a bilingual LaTeX file, compiles to PDF.
"""

import os
import subprocess
from scripts.text_utils import split_paragraphs
from scripts.latex_utils import make_bilingual_latex, compile_latex
from scripts.translator import translate_paragraphs

def main():
    # 1. Read the English text file
    eng_file = "data/moby_dick.txt"
    with open(eng_file, "r", encoding="utf-8") as f:
        eng_text = f.read()

    # 2. Split into paragraphs
    eng_paragraphs = split_paragraphs(eng_text)

    # 3. Translate English paragraphs -> Chinese paragraphs
    chi_file = "moby_dick_translated.txt"  # debug output
    chi_paragraphs = translate_paragraphs(eng_paragraphs, debug_chi_path=chi_file)

    print(f"Chinese paragraphs written to: {chi_file}")

    # 4. Generate the bilingual LaTeX
    latex_code = make_bilingual_latex(eng_paragraphs, chi_paragraphs)

    # 5. Write out the bilingual LaTeX file
    tex_filename = "bilingual_moby_dick.tex"
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_code)

    print(f"Bilingual LaTeX file generated: {tex_filename}")

    # 6. Compile to PDF (using xelatex)
    compile_latex(tex_filename)

    print("PDF compilation complete. Check bilingual_moby_dick.pdf.")

if __name__ == "__main__":
    main()