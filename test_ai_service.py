from app.ai_service import classify_lead


# Sample customer enquiry
enquiry = """
We are looking for an AI automation solution for our company.
We want to implement it this month. Please contact us with pricing.
"""


try:
    result = classify_lead(enquiry)

    print("\nAI Lead Classification Successful!")
    print("-" * 40)
    print(f"Classification: {result['classification']}")
    print(f"Reason: {result['reason']}")
    print(f"Suggested Action: {result['suggested_action']}")
    print("-" * 40)

except Exception as error:
    print("\nAI Classification Failed!")
    print(f"Error: {error}")