import os
from .text_utils import split_paragraphs
from .latex_utils import make_bilingual_latex, compile_latex

def main():
    # 1. Read English text
    with open("data/moby_dick.txt", "r", encoding="utf-8") as f:
        eng_text = f.read()

    # 2. (Optional) Either read Chinese text or translate from the English
    with open("data/moby_dick_chinese.txt", "r", encoding="utf-8") as f:
        chi_text = f.read()

    # 3. Split into paragraphs
    eng_paragraphs = split_paragraphs(eng_text)
    chi_paragraphs = split_paragraphs(chi_text)

    # 4. Build LaTeX code
    latex_code = make_bilingual_latex(eng_paragraphs, chi_paragraphs)

    # 5. Save to output folder
    output_tex = "output/bilingual_moby_dick.tex"
    with open(output_tex, "w", encoding="utf-8") as f:
        f.write(latex_code)

    # 6. Compile
    compile_latex(output_tex)

if __name__ == "__main__":
    main()