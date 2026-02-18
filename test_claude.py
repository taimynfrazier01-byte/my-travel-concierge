import os
from dotenv import load_dotenv
from anthropic import Anthropic

# 1. Load the API key from your .env file
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. Initialize the Claude Client
client = Anthropic(api_key=api_key)

try:
    # 3. Send a small test message (using the budget-friendly Haiku model)
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'Connection Successful!' if you can read this."}
        ]
    )
    # 4. Print the result
    print("-" * 30)
    print(f"CLAUDE SAYS: {message.content[0].text}")
    print("-" * 30)

except Exception as e:
    print(f"Error: {e}")