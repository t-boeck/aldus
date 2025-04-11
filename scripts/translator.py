import re
from openai import OpenAI
from scripts.text_utils import split_paragraphs

# Configure your OpenAI client.
# Ensure your API key is set (e.g., via OPENAI_API_KEY environment variable).
client = OpenAI()

def translate_paragraph(paragraph: str) -> str:
    """
    Translate a single English paragraph into Chinese in a literary style.
    The prompt instructs the model to output ONLY the Chinese translation.
    """
    if not paragraph.strip():
        return ""

    prompt = (
        "You are a highly professional literary translator. "
        "Translate the following text from English to Chinese, preserving its style, tone, nuance, and voice. "
        "Return ONLY the Chinese translation with no additional commentary, greetings, or extraneous text. "
        "Do not include any extra phrases such as 'Sure!' or 'Here’s the translation:'.\n\n"
        f"\"\"\"{paragraph}\"\"\""
    )

    response = client.responses.create(
        model="gpt-4o-mini",  # Replace with your chosen model
        input=prompt
    )
    
    return response.output_text.strip()

def translate_paragraphs(eng_paragraphs: list[str], debug_chi_path: str) -> list[str]:
    """
    Translate a list of English paragraphs into Chinese.
    Write each translated paragraph (with a blank line following) to debug_chi_path.
    Print the paragraph number before processing each paragraph.
    
    Returns a list of Chinese paragraphs.
    """
    chi_paragraphs = []
    with open(debug_chi_path, "w", encoding="utf-8") as out_f:
        for i, paragraph in enumerate(eng_paragraphs, start=1):
            print(f"Translating paragraph {i}...")
            chi_para = translate_paragraph(paragraph)
            chi_paragraphs.append(chi_para)
            out_f.write(chi_para + "\n\n")
    return chi_paragraphs

if __name__ == "__main__":
    # Optional quick test:
    sample = "Call me Ishmael. Some years ago--never mind how long precisely..."
    print(translate_paragraph(sample))