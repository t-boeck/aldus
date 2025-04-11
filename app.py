from flask import Flask, render_template, request
import os
import io
import uuid
from contextlib import redirect_stdout

from scripts.text_utils import split_paragraphs
from scripts.translator import translate_paragraphs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Expect one file input: the English text.
        eng_file = request.files.get('english_file')
        if not eng_file:
            return "Please upload an English text file."

        # Read and decode the uploaded file.
        eng_text = eng_file.read().decode('utf-8', errors='replace')
        eng_paragraphs = split_paragraphs(eng_text)
        
        # Check for test mode via a checkbox named "test_mode".
        test_mode = request.form.get("test_mode")
        if test_mode == "on":
            eng_paragraphs = eng_paragraphs[:15]
            print("Test mode enabled: processing only first 15 paragraphs.")
        
        # Prepare the output folder.
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        
        # Build a unique filename for the Chinese debug file.
        chi_debug_path = os.path.join(output_folder, f"{uuid.uuid4()}_translated.txt")
        
        # Capture log messages during translation.
        log_stream = io.StringIO()
        with redirect_stdout(log_stream):
            chi_paragraphs = translate_paragraphs(eng_paragraphs, chi_debug_path)
        logs = log_stream.getvalue()
        
        # Combine all translated paragraphs.
        chi_text = "\n\n".join(chi_paragraphs)
        
        # Build an HTML response that displays the translation and the logs.
        html_response = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Translation Result</title>
        </head>
        <body>
            <h1>Translation Result</h1>
            <h2>Chinese Translation</h2>
            <pre style="border:1px solid #ddd; padding:10px;">{chi_text}</pre>
            <h2>Translation Logs</h2>
            <pre style="border:1px solid #ddd; padding:10px;">{logs}</pre>
        </body>
        </html>
        """
        return html_response

    # GET: Render the file-upload form.
    return render_template("index.html")

if __name__ == '__main__':
    # Run the Flask app on port 5000; ensure host is 0.0.0.0 for external access if needed.
    app.run(debug=True, host="0.0.0.0", port=5000)