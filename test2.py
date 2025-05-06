import os
key = os.getenv("DEEPSEEK_API_KEY")

if key is None:
    raise RuntimeError("DEEPSEEK_API_KEY is not set in the environment")

print(key)