import os
import io
import re
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent


def _load_env_file(path):
    env_path = Path(path)
    if not env_path.exists():
        return
    try:
        content = env_path.read_text(encoding="utf-8")
    except OSError:
        return

    normalized = re.sub(r"([\"'])\s*([A-Z][A-Z0-9_]+)=", r"\1\n\2=", content)
    if normalized != content:
        env_path.write_text(normalized, encoding="utf-8")

    load_dotenv(stream=io.StringIO(normalized), override=False)


_load_env_file(PROJECT_ROOT / ".a0proj" / "secrets.env")
_load_env_file(PROJECT_ROOT / ".a0proj" / "variables.env")

if os.environ.get("AIRTABLE_API") and not os.environ.get("AIRTABLE_API_KEY"):
    os.environ["AIRTABLE_API_KEY"] = os.environ["AIRTABLE_API"]

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
