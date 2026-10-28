import os
from dotenv import load_dotenv
from google import genai

# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

# Create a Gemini client
client = genai.Client(api_key=api_key)

# Send a simple request to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="In one sentence, explain what AI lead classification means."
)

print("Gemini connection successful!")
print("Gemini response:")
print(response.text)