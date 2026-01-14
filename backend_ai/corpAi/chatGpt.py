import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load .env RELIABLY
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

if not ENV_PATH.exists():
    raise RuntimeError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set or not loaded")

if not API_KEY.startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY format looks invalid")

# 2. Load config.json
CONFIG_PATH = Path(__file__).parent / "config" / "models.json"

if not CONFIG_PATH.exists():
    raise RuntimeError(f"Config file not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

openai_cfg = config["providers"]["openai"]
SYSTEM_PROMPT = config["system_prompts"]["default"]


# 3. OpenAI Client
client = OpenAI(api_key=API_KEY)

# 4. Chat function
def chat(user_input: str) -> str:
    response = client.chat.completions.create(
        model=openai_cfg["model_id"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        max_tokens=openai_cfg["max_tokens"],
        temperature=openai_cfg["temperature"]
    )

    return response.choices[0].message.content.strip()


# 5. CLI entry point
if __name__ == "__main__":
    print("OpenAI backend ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("> ")
        if user_input.lower() in ("exit", "quit"):
            break

        try:
            reply = chat(user_input)
            print("\nAI:", reply, "\n")
        except Exception as e:
            print("Error:", str(e))
