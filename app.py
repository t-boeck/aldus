from flask import Flask, render_template, request, send_file
import os
import uuid
import subprocess

# Import your existing code
# from scripts.main import run_bilingual_generation
# or from scripts.text_utils, scripts.latex_utils, etc.
from scripts.text_utils import split_paragraphs, process_paragraph
from scripts.latex_utils import make_bilingual_latex, compile_latex

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1) Grab the uploaded files from the form
        eng_file = request.files['english_file']
        chi_file = request.files['chinese_file']

        if not eng_file or not chi_file:
            return "Please upload both English and Chinese text files"

        # 2) Read them as strings
        eng_text = eng_file.read().decode('utf-8', errors='replace')
        chi_text = chi_file.read().decode('utf-8', errors='replace')

        # 3) Process text -> paragraphs
        eng_paragraphs = split_paragraphs(eng_text)
        chi_paragraphs = split_paragraphs(chi_text)

        # 4) Convert to LaTeX
        latex_code = make_bilingual_latex(eng_paragraphs, chi_paragraphs)

        # 5) Write latex file to a temp location
        tex_filename = f"{uuid.uuid4()}.tex"  # unique name
        pdf_filename = tex_filename.replace(".tex", ".pdf")

        # Save in some temp folder, e.g. "output" or "tmp"
        tex_path = os.path.join("output", tex_filename)
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # 6) Compile using xelatex
        compile_latex(tex_path)  # your latex_utils function

        # PDF should now exist at output/<uuid>.pdf
        pdf_path = os.path.join("output", pdf_filename)

        # 7) Send file back as download
        return send_file(pdf_path, as_attachment=True, download_name="bilingual.pdf")

    # If GET request: show upload form
    return render_template("index.html")

if __name__ == '__main__':
    # create output folder if doesn't exist
    os.makedirs("output", exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)