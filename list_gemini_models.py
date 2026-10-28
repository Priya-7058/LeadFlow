import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Locate the .env file beside this Python script.
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        f"GEMINI_API_KEY not found. Check this file: {env_path}"
    )

client = genai.Client(api_key=api_key)

print("Checking available Gemini models...\n")

for model in client.models.list():
    if "generateContent" in (model.supported_actions or []):
        print(model.name)