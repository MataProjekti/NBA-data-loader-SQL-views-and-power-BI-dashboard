import json
from datetime import datetime
from pathlib import Path

import requests

URL = "https://sportscore.com/api/widget/matches/"
params = {"sport": "basketball", "limit": 50, "src": "basketball-data-platform"}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()
data = response.json()

Path("data").mkdir(exist_ok=True)
out = Path("data") / f"matches_{datetime.now():%Y%m%d_%H%M%S}.json"
out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print("Snimljeno u:", out)
print("Kljucevi u odgovoru:", list(data.keys()))
matches = data.get("matches", [])
print("Broj utakmica:", len(matches))
if matches:
    print(json.dumps(matches[0], indent=2, ensure_ascii=False))