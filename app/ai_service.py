import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load the .env file from the LeadFlow project folder
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


# Get the Gemini API key securely from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )


# Create the Gemini client
client = genai.Client(api_key=api_key)

# Use the Gemini model that worked in our connection test
MODEL_NAME = "gemini-3.5-flash-lite"


def classify_lead(enquiry: str) -> dict:
    """
    Analyze a lead's enquiry and classify its potential.
    """

    prompt = f"""
    You are an AI sales assistant.

    Analyze the following customer enquiry and classify the lead.

    Customer enquiry:
    {enquiry}

    Choose exactly one classification:
    - High: The customer shows strong buying intent or is ready to purchase.
    - Medium: The customer shows interest but needs more information or time.
    - Low: The customer shows little buying intent or is only casually exploring.

    Return your answer as valid JSON with these three fields:
    {{
        "classification": "High, Medium, or Low",
        "reason": "A short explanation for your classification",
        "suggested_action": "The next action the sales team should take"
    }}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    # Convert Gemini's JSON response into a Python dictionary
    result = json.loads(response.text)

    # Check that the expected fields are present
    required_fields = {
        "classification",
        "reason",
        "suggested_action"
    }

    if not required_fields.issubset(result.keys()):
        raise ValueError("Gemini returned an incomplete classification.")

    # Make sure the classification is valid
    if result["classification"] not in ["High", "Medium", "Low"]:
        raise ValueError("Gemini returned an invalid classification.")

    return result