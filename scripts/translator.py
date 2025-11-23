import re
import os
from openai import OpenAI
from scripts.text_utils import split_paragraphs

# Configure your OpenAI client (ensure your API key is set via environment variable or otherwise)
def translate_paragraph(paragraph: str, api_key: str, system_prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Translate a single English paragraph into Chinese using the specified model.
    The prompt instructs the model to output ONLY the Chinese translation.
    """
    if not paragraph.strip():
        return ""

    # client = OpenAI() #uses open ai env api key
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    user_prompt = f"""
        Please translate the following paragraph:
        
        {paragraph}
    """

    # response = client.responses.create(
    #     model=model,
    #     input=prompt
    # )
    
    # return response.output_text.strip()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"},
        ],
        stream=False
    )

    return response.choices[0].message.content.strip()

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