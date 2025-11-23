import os
import subprocess
from .text_utils import process_paragraph

def make_bilingual_latex(src_paragraphs, tgt_paragraphs, source_lang="english", target_lang="chinese", font_size=17):
    lines = []
    # Preamble
    lines.append(f"\\documentclass[{font_size}pt]{{extarticle}}")
    
    # Load necessary language packages
    langs = {source_lang.lower(), target_lang.lower()}
    
    if "chinese" in langs:
        lines.append(r"\usepackage[UTF8]{ctex}")
    
    # Load babel for other languages if needed
    babel_langs = []
    if "spanish" in langs:
        babel_langs.append("spanish")
    if "french" in langs:
        babel_langs.append("french")
    
    if babel_langs:
        lines.append(f"\\usepackage[{','.join(babel_langs)}]{{babel}}")
        
    lines.append(r"\usepackage[margin=0.5in]{geometry}")
    lines.append(r"\usepackage{paracol}")
    lines.append(r"\usepackage{setspace}")
    lines.append("")
    
    # Determine column ratio
    # Chinese is compact. 
    # If Left (Source) is Spacious (Non-Chinese) and Right (Target) is Compact (Chinese) -> 0.6
    # If Left (Source) is Compact (Chinese) and Right (Target) is Spacious (Non-Chinese) -> 0.4
    # Otherwise -> 0.5
    
    is_src_compact = (source_lang.lower() == "chinese")
    is_tgt_compact = (target_lang.lower() == "chinese")
    
    if not is_src_compact and is_tgt_compact:
        ratio = 0.6
    elif is_src_compact and not is_tgt_compact:
        ratio = 0.4
    else:
        ratio = 0.5
        
    lines.append(f"\\columnratio{{{ratio}}}")
    lines.append(r"\setlength{\parindent}{0pt}")
    lines.append(r"\setlength{\parskip}{1em}")
    lines.append(r"\begin{document}")
    lines.append(r"\begin{paracol}{2}")
    lines.append(r"\sloppy")
    lines.append("")

    # Body
    length = min(len(src_paragraphs), len(tgt_paragraphs))
    for i in range(length):
        spara = src_paragraphs[i]
        tpara = tgt_paragraphs[i]
        
        s_latex = process_paragraph(spara, language=source_lang, line_stretch=1.3)
        t_latex = process_paragraph(tpara, language=target_lang, line_stretch=1.3 if not is_tgt_compact else 1.0)
        
        lines.append(s_latex)
        lines.append(r"\switchcolumn")
        lines.append(t_latex)
        lines.append(r"\switchcolumn*")
        lines.append("")

    lines.append(r"\end{paracol}")
    lines.append(r"\end{document}")
    return "\n".join(lines)

def compile_latex(tex_file: str):
    """
    Runs xelatex on the given .tex file in a subprocess.
    """
    output_dir = os.path.dirname(tex_file)
    cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={output_dir}",
        tex_file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        # If there is an error, print the captured output
        print("LaTeX compilation failed:")
        print(result.stdout)
        print(result.stderr)
        # Raise exception with the last 500 chars of stdout to help debug
        raise Exception(f"LaTeX compilation failed. Log: {result.stdout[-500:]}")