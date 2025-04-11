import re
import jieba

def split_paragraphs(text):
    paragraphs = text.strip().split('\n\n')
    return paragraphs

def split_into_sentences(paragraph):
    parts = re.split(r'([.!?。！？])', paragraph)
    sentences = []
    for i in range(0, len(parts), 2):
        chunk = parts[i].strip()
        if i + 1 < len(parts):
            chunk += parts[i+1]
        if chunk:
            sentences.append(chunk.strip())
    return sentences

def latex_escape(s: str) -> str:
    return (s.replace("\\", "\\textbackslash ")
             .replace("&", "\\&")
             .replace("%", "\\%")
             .replace("$", "\\$")
             .replace("#", "\\#")
             .replace("_", "\\_")
             .replace("{", "\\{")
             .replace("}", "\\}"))

def is_punctuation_or_quotes(tok: str) -> bool:
    return bool(re.fullmatch(r'[\W]+', tok, flags=re.UNICODE))

def bold_first_word(sentence: str) -> str:
    sentence = sentence.strip()
    if not sentence:
        return ""
    tokens = sentence.split()

    for i, token in enumerate(tokens):
        if is_punctuation_or_quotes(token):
            continue

        m = re.match(r'^([\\"\'“”«»]+)(.+)$', token)
        if m:
            leading = m.group(1)
            the_rest = m.group(2)
        else:
            leading = ""
            the_rest = token

        # Decide if it's mostly Chinese
        cjk_count = len(re.findall(r'[\u4e00-\u9fff]', the_rest))
        if cjk_count >= (len(the_rest) / 2):
            # Use jieba for first 'word'
            segments = list(jieba.cut(the_rest, cut_all=False))
            if segments:
                first_seg = segments[0]
                remainder = the_rest[len(first_seg):]
                bolded_token = leading + r"\textbf{" + latex_escape(first_seg) + "}" + latex_escape(remainder)
            else:
                bolded_token = leading + r"\textbf{" + latex_escape(the_rest) + "}"
        else:
            bolded_token = leading + r"\textbf{" + latex_escape(the_rest) + "}"

        tokens[i] = bolded_token
        break

    for j in range(i + 1, len(tokens)):
        tokens[j] = latex_escape(tokens[j])

    return " ".join(tokens)

def process_paragraph(paragraph, line_stretch=1.3):
    sentences = split_into_sentences(paragraph)
    bolded_sentences = [bold_first_word(s) for s in sentences]
    joined = " ".join(bolded_sentences)
    return "{\\setstretch{" + str(line_stretch) + "}\n" + joined + "\n}"