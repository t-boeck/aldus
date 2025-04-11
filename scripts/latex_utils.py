import subprocess
from .text_utils import process_paragraph

def make_bilingual_latex(eng_paragraphs, chi_paragraphs):
    lines = []
    # Preamble
    lines.append(r"\documentclass[12pt]{article}")
    lines.append(r"\usepackage[UTF8]{ctex}")
    lines.append(r"\usepackage[margin=0.5in]{geometry}")
    lines.append(r"\usepackage{paracol}")
    lines.append(r"\usepackage{setspace}")
    lines.append("")
    lines.append(r"\columnratio{0.6}")
    lines.append(r"\setlength{\parindent}{0pt}")
    lines.append(r"\setlength{\parskip}{1em}")
    lines.append(r"\begin{document}")
    lines.append(r"\begin{paracol}{2}")
    lines.append(r"\sloppy")
    lines.append("")

    # Body
    length = min(len(eng_paragraphs), len(chi_paragraphs))
    for i in range(length):
        epara = eng_paragraphs[i]
        cpara = chi_paragraphs[i]
        e_latex = process_paragraph(epara, line_stretch=1.3)
        c_latex = process_paragraph(cpara, line_stretch=1.0)
        lines.append(e_latex)
        lines.append(r"\switchcolumn")
        lines.append(c_latex)
        lines.append(r"\switchcolumn*")
        lines.append("")

    lines.append(r"\end{paracol}")
    lines.append(r"\end{document}")
    return "\n".join(lines)

def compile_latex(tex_file: str):
    """
    Runs xelatex on the given .tex file in a subprocess.
    """
    subprocess.run(["xelatex", "-output-directory=output", tex_file])