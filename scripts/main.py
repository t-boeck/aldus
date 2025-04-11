import os
import subprocess
from scripts.text_utils import split_paragraphs
from scripts.latex_utils import make_bilingual_latex, compile_latex
from scripts.translator import translate_paragraphs

def main():
    # 1. Read the English text file from the data folder.
    eng_file = os.path.join("data", "moby_dick.txt")
    with open(eng_file, "r", encoding="utf-8") as f:
        eng_text = f.read()

    # 2. Split the English text into paragraphs.
    eng_paragraphs = split_paragraphs(eng_text)

    # 3. Prepare the output folder.
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # 4. Translate paragraphs one by one.
    # Write the Chinese text to output/moby_dick_translated.txt for debugging.
    chi_file = os.path.join(output_folder, "moby_dick_translated.txt")
    chi_paragraphs = translate_paragraphs(eng_paragraphs, debug_chi_path=chi_file)
    print(f"Chinese paragraphs written to: {chi_file}")

    # 5. Generate bilingual LaTeX code.
    latex_code = make_bilingual_latex(eng_paragraphs, chi_paragraphs)

    # 6. Write the LaTeX file to the output folder.
    tex_filename = os.path.join(output_folder, "bilingual_moby_dick.tex")
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"Bilingual LaTeX file generated: {tex_filename}")

    # 7. Compile the LaTeX file to generate the PDF.
    compile_latex(tex_filename)
    print("PDF compilation complete. Check the output folder for bilingual_moby_dick.pdf.")

if __name__ == "__main__":
    main()