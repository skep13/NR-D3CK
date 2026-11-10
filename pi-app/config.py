# settings for app

from pathlib import Path

HERE = Path(__file__).parent

#brain

BRAIN_URL = "http://192.168.1.15:8080/v1/chat/completions"
MODEL = "marina"
MAX_TOKENS = 150
MAX_HISTORY = 10
TIMEOUT = 60 #seconds

PROMPT_PATH = HERE.parent /"berri" / "systemprompt.txt"

SECRETS_PATH = HERE / "secrets.env"

def _read_key() -> str:
    if not SECRETS_PATH.exists():
        print(f"[NR config] missing {SECRETS_PATH}")
        return ""

    for line in SECRETS_PATH.read_text().splitlines():
        if line.startswith("BERRI_API_KEY="):
            return line.split("=", 1)[1].strip()
    print("[NR config] BERRI_API_KEY not found in secrets")
    return ""

API_KEY = _read_key()