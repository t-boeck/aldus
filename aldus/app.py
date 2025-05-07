from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, send_from_directory, abort
)
import concurrent.futures as cf
import uuid, time, os
from pathlib import Path

# ────────────────────────── app setup ──────────────────────────
app = Flask(__name__)
OUT = Path(app.root_path) / "output"
OUT.mkdir(exist_ok=True)

executor = cf.ThreadPoolExecutor(max_workers=2)       # background pool
jobs: dict[str, dict] = {}                            # in-memory job store

# ─────────────────────── heavy-work function ───────────────────
def run_translation(jid: str, eng_text: str, model: str, test: bool):
    from scripts.text_utils  import split_paragraphs
    from scripts.translator  import translate_paragraph
    from scripts.latex_utils import make_bilingual_latex

    start_ts = time.time()
    eng_pars  = split_paragraphs(eng_text)
    if test:
        eng_pars = eng_pars[:5]

    total     = len(eng_pars)
    chi_pars  = []
    jobs[jid] = {"status": "running", "start": start_ts, "total": total}

    dbg_path  = OUT / f"{jid}_chi.txt"
    tex_path  = OUT / f"{jid}.tex"

    with dbg_path.open("w", encoding="utf-8") as dbg:
        for i, p in enumerate(eng_pars, 1):
            chi = translate_paragraph(p, model)
            chi_pars.append(chi)
            dbg.write(chi + "\n\n")

            jobs[jid].update(
                done=i,
                msg=f"Paragraph {i}/{total}",
                latest_src=p,
                latest_tgt=chi,
            )

    tex_code = make_bilingual_latex(eng_pars, chi_pars)
    tex_path.write_text(tex_code, encoding="utf-8")

    jobs[jid] = {
        "status": "done",
        "start": start_ts,
        "total": total,
        "done": total,
        "files": {"chi": dbg_path.name, "tex": tex_path.name},
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
    eng_text = f.read().decode("utf-8", errors="replace")
    model    = request.form.get("model", "deepseek-chat")
    test     = request.form.get("test_mode") == "yes"

    jid = uuid.uuid4().hex
    executor.submit(run_translation, jid, eng_text, model, test)
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

@app.get("/download/<path:fname>")
def download(fname):
    return send_from_directory(OUT, fname, as_attachment=True)

# ────────────────────────── entrypoint ─────────────────────────
if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run("0.0.0.0", port, debug)