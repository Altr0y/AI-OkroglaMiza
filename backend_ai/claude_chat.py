import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

# Load .env from parent directory
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Missing ANTHROPIC_API_KEY in .env")
    sys.exit(1)

client = Anthropic(api_key=api_key)

print("💬 Claude Chat (Ctrl+C to exit)\n")

while True:
    try:
        user_input = input("You: ")
        if not user_input.strip():
            continue

        response = client.messages.create(
            model="claude-3-haiku-20240307",  # cheapest Claude model
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        print("\nClaude:", response.content[0].text, "\n")

    except KeyboardInterrupt:
        print("\n👋 Exiting chat.")
        break
    except Exception as e:
        print("❌ Error:", e)
