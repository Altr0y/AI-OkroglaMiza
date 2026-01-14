from google import genai
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


#############################
# Preden zaženeš moreš v .env nastavit api key
# pri spremenljivki OPENAI_API_KEY=[tvoj api ključ]
# Namig: gemini ima free tier
#############################

# Load .env from parent directory
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ Missing GEMINI_API_KEY in .env")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# Test za en prompt
"""response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What is the capital city of the Paris"
)
print(response.text)"""



def chat_with_gemini():
    print("💬 Gemini Chat (type 'exit' to quit):")

    while True:
        try:
            user_msg = input("You: ").strip()
            if user_msg.lower() == "exit":
                break

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=user_msg,
            )

            print("\nGemini:", response.text, "\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting chat.")
            break
        except Exception as e:
            print("❌ Error:", e)

"""
if __name__ == "__main__":
    chat_with_gemini()
"""

chat_with_gemini()

