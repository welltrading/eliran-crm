import os, re
from app import app

def _load_env_file(path):
    try:
        with open(path, 'r') as f:
            content = f.read()
            for k, v in re.findall(r'([A-Z_]+)=["\']?([^"\' ]+)["\']?', content):
                os.environ[k] = v
    except: pass

_load_env_file(".a0proj/secrets.env")
_load_env_file(".a0proj/variables.env")

if os.environ.get("AIRTABLE_API") and not os.environ.get("AIRTABLE_API_KEY"):
    os.environ["AIRTABLE_API_KEY"] = os.environ["AIRTABLE_API"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
