from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, send_from_directory, abort
)
import concurrent.futures as cf
import uuid, time, os
from pathlib import Path

from werkzeug.utils import secure_filename

from datetime import datetime

# ────────────────────────── app setup ──────────────────────────
app = Flask(__name__)
OUT = Path(app.root_path) / "output"
OUT.mkdir(exist_ok=True)

executor = cf.ThreadPoolExecutor(max_workers=2)       # background pool
jobs: dict[str, dict] = {}                            # in-memory job store

# ─────────────────────── heavy-work function ───────────────────
def run_translation(jid: str, src_text: str, model: str, test: bool, api_key: str, system_prompt: str, original_filename: str, source_language: str, target_language: str, font_size: int):
    from scripts.text_utils  import split_paragraphs
    from scripts.translator  import translate_paragraph
    from scripts.latex_utils import make_bilingual_latex, compile_latex

    try:
        start_ts = time.time()
        src_pars  = split_paragraphs(src_text)
        if test:
            src_pars = src_pars[:5]

        total     = len(src_pars)
        tgt_pars  = []
        jobs[jid] = {
            "status": "running", 
            "start": start_ts, 
            "total": total, 
            "cancelled": False,
            "done": 0,
            "msg": f"Paragraph 0/{total}"
        }

        # Generate timestamped filename
        base_name = Path(original_filename).stem
        date_str = datetime.fromtimestamp(start_ts).strftime('%Y_%m_%d_%H%M%S')
        out_name = f"{base_name}_{date_str}"

        dbg_path  = OUT / f"{out_name}_target.txt"
        tex_path  = OUT / f"{out_name}.tex"

        with dbg_path.open("w", encoding="utf-8") as dbg:
            for i, p in enumerate(src_pars, 1):
                # Check for cancellation
                if jobs[jid].get("cancelled"):
                    jobs[jid]["status"] = "cancelled"
                    jobs[jid]["msg"] = "Translation cancelled by user."
                    jobs[jid]["files"] = {"chi": dbg_path.name}
                    return

                tgt = translate_paragraph(p, api_key, system_prompt, model)
                tgt_pars.append(tgt)
                dbg.write(tgt + "\n\n")

                jobs[jid].update(
                    done=i,
                    msg=f"Paragraph {i}/{total}",
                    latest_src=p,
                    latest_tgt=tgt,
                )

        tex_code = make_bilingual_latex(src_pars, tgt_pars, source_language, target_language, font_size)
        tex_path.write_text(tex_code, encoding="utf-8")
        
        # Compile PDF
        try:
            compile_latex(str(tex_path))
            # The compile_latex function outputs to the same directory with .pdf extension
            # We need to make sure we capture the correct pdf name
            pdf_name = f"{out_name}.pdf"
        except Exception as e:
            print(f"Compilation failed: {e}")
            pdf_name = None
            compile_error = str(e)
        else:
            compile_error = None

        jobs[jid] = {
            "status": "done",
            "start": start_ts,
            "total": total,
            "done": total,
            "files": {"chi": dbg_path.name, "tex": tex_path.name, "pdf": pdf_name},
            "compile_error": compile_error
        }
    except Exception as e:
        print(f"Job {jid} failed: {e}")
        jobs[jid] = {
            "status": "error",
            "start": start_ts,
            "msg": str(e)
        }

# ─────────────────────────── routes ────────────────────────────
@app.get("/")
def home():
    return render_template("index.html")

@app.post("/start")
def start():
    f = request.files.get("english_file")
    if not f:
        return "No file uploaded", 400
    src_text = f.read().decode("utf-8", errors="replace").replace("\r\n", "\n")
    original_filename = secure_filename(f.filename)
    
    model    = request.form.get("model", "deepseek-chat")
    test     = request.form.get("test_mode") == "yes"
    api_key  = request.form.get("api_key")
    
    source_language = request.form.get("source_language", "english")
    target_language = request.form.get("target_language", "chinese")
    font_size       = int(request.form.get("font_size", 17))
    
    # Get provided system prompt or generate default based on language
    system_prompt = request.form.get("system_prompt")
    if not system_prompt or not system_prompt.strip():
        src_name = source_language.capitalize()
        tgt_name = target_language.capitalize()
        system_prompt = f"You are a professional literary translator, tasked with translating the provided text from {src_name} to {tgt_name}. Preserve the text's style, tone, nuance, and voice. Return ONLY the {tgt_name} translation with no additional commentary, greetings or extraneous text."

    if not api_key:
        return "API Key is required", 400

    jid = uuid.uuid4().hex
    executor.submit(run_translation, jid, src_text, model, test, api_key, system_prompt, original_filename, source_language, target_language, font_size)
    return redirect(url_for("progress", jid=jid))

@app.get("/progress/<jid>")
def progress(jid):
    return render_template("progress.html", jid=jid)

@app.get("/status/<jid>")
def status(jid):
    d = jobs.get(jid)
    if not d:
        # job entry not created yet → tell the client to keep polling
        return jsonify({"status": "pending"}), 200

    elapsed = int(time.time() - d["start"])
    pct     = d.get("done", 0) / max(d.get("total", 1), 1e-9)
    eta_sec = int(elapsed * (1 - pct) / pct) if pct else None

    return jsonify({**d, "elapsed": elapsed, "eta": eta_sec})

@app.post("/stop/<jid>")
def stop_job(jid):
    if jid in jobs:
        jobs[jid]["cancelled"] = True
        return jsonify({"status": "stopping"}), 200
    return jsonify({"error": "Job not found"}), 404

@app.get("/library")
def library():
    files = []
    if OUT.exists():
        for f in OUT.iterdir():
            if f.is_file() and not f.name.startswith('.'):
                stat = f.stat()
                dt = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                size_kb = round(stat.st_size / 1024, 1)
                files.append({
                    "name": f.name,
                    "date": dt,
                    "size": f"{size_kb} KB",
                    "ts": stat.st_mtime
                })
    # Sort by newest first
    files.sort(key=lambda x: x["ts"], reverse=True)
    return render_template("library.html", files=files)

@app.route("/compile", methods=["GET", "POST"])
def compile_tool():
    if request.method == "GET":
        return render_template("compile.html")
    
    f = request.files.get("tex_file")
    if not f:
        return render_template("compile.html", error="No file uploaded")
    
    filename = secure_filename(f.filename)
    if not filename.endswith(".tex"):
        return render_template("compile.html", error="File must be a .tex file")
        
    save_path = OUT / filename
    f.save(save_path)
    
    from scripts.latex_utils import compile_latex
    try:
        compile_latex(str(save_path))
        pdf_name = filename.replace(".tex", ".pdf")
        return redirect(url_for("download", fname=pdf_name))
    except Exception as e:
        return render_template("compile.html", error=f"Compilation failed: {str(e)}")

@app.get("/download/<path:fname>")
def download(fname):
    return send_from_directory(OUT, fname, as_attachment=True)

# ────────────────────────── entrypoint ─────────────────────────
if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run("0.0.0.0", port, debug)