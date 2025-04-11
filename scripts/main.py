import os
import time
import sys
import subprocess
from scripts.text_utils import split_paragraphs
from scripts.latex_utils import make_bilingual_latex, compile_latex
from scripts.translator import translate_paragraphs

def main():

    start_time = time.time()

    # 1. Read the English text file from the data folder.
    eng_file = os.path.join("data", "moby_dick.txt")
    with open(eng_file, "r", encoding="utf-8") as f:
        eng_text = f.read()

    # 2. Split the English text into paragraphs.
    eng_paragraphs = split_paragraphs(eng_text)

    # 3. If the user provided "test" as an argument, limit to first 15 paragraphs.
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        eng_paragraphs = eng_paragraphs[:15]
        print("Test mode enabled: processing only first 15 paragraphs.")
    else:
        print("Processing full text.")

    # 4. Prepare the output folder.
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # 5. Translate paragraphs to Chinese and output the debug Chinese file.
    debug_chi_path = os.path.join(output_folder, "moby_dick_translated.txt")
    chi_paragraphs = translate_paragraphs(eng_paragraphs, debug_chi_path)
    print(f"Chinese debug text written to: {debug_chi_path}")

    # 6. Generate bilingual LaTeX code.
    latex_code = make_bilingual_latex(eng_paragraphs, chi_paragraphs)

    # 7. Write the LaTeX file to the output folder.
    tex_filename = os.path.join(output_folder, "bilingual_moby_dick.tex")
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_code)
    print(f"Bilingual LaTeX file generated: {tex_filename}")

    # 8. Compile the LaTeX file to generate a PDF.
    compile_latex(tex_filename)
    print("PDF compilation complete. Check the output folder for bilingual_moby_dick.pdf.")

    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Total runtime: {total_runtime:.2f} seconds")

if __name__ == "__main__":
    main()