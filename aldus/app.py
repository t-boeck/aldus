from flask import Flask, render_template, request, Response, send_from_directory
import os
import io
import uuid
from contextlib import redirect_stdout

from scripts.text_utils import split_paragraphs
from scripts.translator import translate_paragraph, translate_paragraphs
from scripts.latex_utils import make_bilingual_latex, compile_latex

app = Flask(__name__)

def generate_translation(eng_paragraphs, model):
    yield "<html><head><meta charset='utf-8'><title>Translation Progress</title>"
    yield """<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { background-color: #f8f9fa; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
      .container { max-width: 800px; margin: 2% auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
      pre { background: #eee; padding: 10px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; }
    </style>"""
    yield "</head><body><div class='container'>"
    yield "<h1>Translation in Progress</h1>"
    
    # Prepare output folder and unique debug filename.
    OUTPUT_DIR = os.path.join(app.root_path, "output")  # <— absolute path
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    chi_debug_filename = "moby_dick_translated.txt"
    chi_debug_path = os.path.join(OUTPUT_DIR, chi_debug_filename)
    
    chi_paragraphs = []
    for i, paragraph in enumerate(eng_paragraphs, start=1):
        yield f"<p><strong>Paragraph {i}:</strong></p>"
        yield f"<p><strong>Input:</strong><br><pre>{paragraph}</pre></p>"
        yield f"<p>Translating paragraph <strong>{i}</strong> using model <code>{model}</code>...</p>"
        translation = translate_paragraph(paragraph, model)
        chi_paragraphs.append(translation)
        yield f"<p><strong>Output:</strong><br><pre>{translation}</pre></p>"
        yield "<hr/>"
    
    # Write Chinese debug file.
    with open(chi_debug_path, "w", encoding="utf-8") as f:
        for para in chi_paragraphs:
            f.write(para + "\n\n")
    yield f"<p>Chinese debug file written: <code>{chi_debug_filename}</code></p>"
    
    # Generate bilingual LaTeX.
    latex_code = make_bilingual_latex(eng_paragraphs, chi_paragraphs)
    tex_filename = "bilingual_moby_dick.tex"
    tex_path = os.path.join(OUTPUT_DIR, tex_filename)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(latex_code)
    yield f"<p>Bilingual LaTeX file generated: <code>{tex_filename}</code></p>"
    
    # Compile to PDF.
    # compile_latex(tex_path)
    # pdf_filename = "bilingual_moby_dick.pdf"
    # yield f"<p>PDF compilation complete: <code>{pdf_filename}</code></p>"
    
    # Provide download links.
    yield f'<p><a href="/download?file={chi_debug_filename}" class="btn btn-primary">Download Chinese Translation .txt</a></p>'
    yield f'<p><a href="/download?file={tex_filename}" class="btn btn-primary">Download Uncompiled Latex</a></p>'
    # yield f'<p><a href="/download?file={pdf_filename}" class="btn btn-primary">Download PDF</a></p>'
    yield "</div></body></html>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        eng_file = request.files.get('english_file')
        if not eng_file:
            return "Please upload an English text file."
        eng_text = eng_file.read().decode('utf-8', errors='replace')
        eng_paragraphs = split_paragraphs(eng_text)
        
        # Test mode: limit to first 5 paragraphs.
        test_mode = request.form.get("test_mode")
        if test_mode == "on":
            eng_paragraphs = eng_paragraphs[:5]
            print("Test mode enabled: processing only first 5 paragraphs.")
        else:
            print("Processing full text.")
        
        # Get model selection from the form, default to "gpt-4o-mini"
        model_selected = request.form.get("model", "gpt-4o-mini")
        print(f"Using model: {model_selected}")
        
        return Response(generate_translation(eng_paragraphs, model_selected), mimetype='text/html')
    
    return render_template("index.html")

@app.route('/download')
def download():
    filename = request.args.get("file")
    OUTPUT_DIR = os.path.join(app.root_path, "output")
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)