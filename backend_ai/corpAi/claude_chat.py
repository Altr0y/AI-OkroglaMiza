# Funkcija chat() vrne odgovor

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic


# 1. Load .env RELIABLY
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

if not ENV_PATH.exists():
    raise RuntimeError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY is not set or not loaded")


# 2. Load models.json
CONFIG_PATH = Path(__file__).parent / "config" / "models.json"

if not CONFIG_PATH.exists():
    raise RuntimeError(f"Config file not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

anthropic_cfg = config["providers"]["anthropic"]
SYSTEM_PROMPT = config["system_prompts"]["default"]


# 3. Anthropic Client
client = Anthropic(api_key=API_KEY)


# 4. Chat function
def chat(user_input: str) -> str:
    response = client.messages.create(
        model=anthropic_cfg["model_id"],
        max_tokens=anthropic_cfg["max_tokens"],
        temperature=anthropic_cfg["temperature"],
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.content[0].text.strip()


# 5. CLI entry point
if __name__ == "__main__":
    print("Anthropic backend ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in ("exit", "quit"):
            break

        try:
            reply = chat(user_input)
            print("\nAI:", reply, "\n")
        except Exception as e:
            print("Error:", str(e))
