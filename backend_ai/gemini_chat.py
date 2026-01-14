# Funkcija chat() vrne odgovor

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai


# 1. Load .env RELIABLY
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

if not ENV_PATH.exists():
    raise RuntimeError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set or not loaded")


# 2. Load models.json
CONFIG_PATH = Path(__file__).parent / "config" / "models.json"

if not CONFIG_PATH.exists():
    raise RuntimeError(f"Config file not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

gemini_cfg = config["providers"]["gemini"]
SYSTEM_PROMPT = config["system_prompts"]["default"]


# 3. Gemini Client
client = genai.Client(api_key=API_KEY)


# 4. Chat function
def chat(user_input: str) -> str:
    response = client.models.generate_content(
        model=gemini_cfg["model_id"],
        contents=[
            SYSTEM_PROMPT,
            user_input
        ]
    )

    return response.text.strip()


# 5. CLI entry point
if __name__ == "__main__":
    print("Gemini backend ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in ("exit", "quit"):
            break

        try:
            reply = chat(user_input)
            print("\nAI:", reply, "\n")
        except Exception as e:
            print("Error:", str(e))
