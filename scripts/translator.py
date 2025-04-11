"""
translator.py

Houses the core logic for translating English paragraphs to Chinese using the OpenAI API.
"""

import re
from openai import OpenAI
from scripts.text_utils import split_paragraphs

# Create or configure your OpenAI client.
# In reality, you'd do something like:
# client = OpenAI(api_key="YOUR_API_KEY")
client = OpenAI()

def translate_paragraph(paragraph: str) -> str:
    """
    Translate a single English paragraph into Chinese, preserving literary style.
    Returns the translated string.
    """
    if not paragraph.strip():
        return ""

    prompt = (
        "You are a professional literary translator. "
        "Translate the following text from English to Chinese, "
        "preserving its style, tone, nuance, and voice:\n\n"
        f"\"\"\"{paragraph}\"\"\""
    )

    response = client.responses.create(
        model="gpt-4o-mini",  # or whichever model you're using
        input=prompt
    )
    return response.output_text.strip()

def translate_paragraphs(eng_paragraphs: list[str], debug_chi_path: str) -> list[str]:
    """
    Translate a list of English paragraphs into Chinese paragraphs.
    Write the Chinese paragraphs to 'debug_chi_path' (for debugging).
    Print paragraph number before each translation.

    Returns a list of Chinese paragraphs aligned 1:1 with the English paragraphs.
    """
    chi_paragraphs = []
    with open(debug_chi_path, "w", encoding="utf-8") as out_f:
        for i, paragraph in enumerate(eng_paragraphs, start=1):
            print(f"Translating paragraph {i}...")
            chi_para = translate_paragraph(paragraph)
            chi_paragraphs.append(chi_para)
            out_f.write(chi_para + "\n\n")

    return chi_paragraphs