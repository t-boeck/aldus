# from openai import OpenAI

# client = OpenAI(api_key="sk-0ffd5e488d9541b2b2023f937b7a6345", base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)


import requests, json

HOST = "http://localhost:11434"
# PROMPT = """
# You are a highly professional literary translator, tasked with translating this sample from Herman Melville's novel Moby Dick, published in 1851. Translate the following text from English to Chinese, preserving its style, tone, nuance, and voice. Return ONLY the Chinese translation with no additional commentary, greetings, or extraneous text. Do not include any extra phrases such as 'Sure!' or 'Here’s the translation':

# What of it, if some old hunks of a sea-captain orders me to get a broom
# and sweep down the decks? What does that indignity amount to, weighed,
# I mean, in the scales of the New Testament? Do you think the archangel
# Gabriel thinks anything the less of me, because I promptly and
# respectfully obey that old hunks in that particular instance? Who ain’t
# a slave? Tell me that. Well, then, however the old sea-captains may
# order me about—however they may thump and punch me about, I have the
# satisfaction of knowing that it is all right; that everybody else is
# one way or other served in much the same way—either in a physical or
# metaphysical point of view, that is; and so the universal thump is
# passed round, and all hands should rub each other’s shoulder-blades,
# and be content.
# """

PROMPT = """### system
You are an elite bilingual literary translator. Your job is to render 19th-century English prose into elegant Chinese (simplified, not traditional characters) that preserves the author’s cadence, irony, and seafaring flavour. Retain line breaks, punctuation (including em-dashes), and rhetorical questions. Do not add explanations, footnotes, or framing phrases.

### user
Translate the following passage from Herman Melville’s *Moby-Dick* (1851) into Simplified Chinese.  
Output **only** the Simplified Chinese text, keeping the same line structure.

What of it, if some old hunks of a sea-captain orders me to get a broom
and sweep down the decks? What does that indignity amount to, weighed,
I mean, in the scales of the New Testament? Do you think the archangel
Gabriel thinks anything the less of me, because I promptly and
respectfully obey that old hunks in that particular instance? Who ain’t
a slave? Tell me that. Well, then, however the old sea-captains may
order me about—however they may thump and punch me about, I have the
satisfaction of knowing that it is all right; that everybody else is
one way or other served in much the same way—either in a physical or
metaphysical point of view, that is; and so the universal thump is
passed round, and all hands should rub each other’s shoulder-blades,
and be content."""

resp = requests.post(
    f"{HOST}/api/generate",
    json={
        "model": 'yi:34b-chat', #"deepseek-llm:7b-chat-q4_0",
        "prompt": PROMPT,
        "stream": False,   # easier first-time; set True for token stream
        "options": {
            "temperature": 0.15,
            "top_p": 0.95,
            "repeat_penalty": 1.1,
            "num_predict": -1,
            "num_ctx": 4096,
            "seed": 42
        }
    },
    timeout=120,
)
print(resp.json()["response"])