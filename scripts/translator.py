import re
from openai import OpenAI
from scripts.text_utils import split_paragraphs

# Configure your OpenAI client (ensure your API key is set via environment variable or otherwise)
client = OpenAI()

def translate_paragraph(paragraph: str, model: str = "gpt-4o-mini") -> str:
    """
    Translate a single English paragraph into Chinese using the specified model.
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
        model=model,
        input=prompt
    )
    
    return response.output_text.strip()

def translate_paragraphs(eng_paragraphs: list[str], debug_chi_path: str, model: str) -> list[str]:
    """
    Translate a list of English paragraphs into Chinese using the specified model.
    Writes each translated paragraph (with a blank line following) to debug_chi_path.
    Prints the paragraph number along with the model being used.
    
    Returns a list of Chinese paragraphs.
    """
    chi_paragraphs = []
    with open(debug_chi_path, "w", encoding="utf-8") as out_f:
        for i, paragraph in enumerate(eng_paragraphs, start=1):
            print(f"Translating paragraph {i} using model {model}...")
            chi_para = translate_paragraph(paragraph, model)
            chi_paragraphs.append(chi_para)
            out_f.write(chi_para + "\n\n")
    return chi_paragraphs

if __name__ == "__main__":
    sample = "Call me Ishmael. Some years ago--never mind how long precisely..."
    translation = translate_paragraph(sample)
    print("Translation:", translation)