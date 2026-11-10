import json

import requests

URL = "https://sportscore.com/api/widget/team/"
params = {
    "sport": "basketball",
    "slug": "atlanta-hawks",
    "limit": 30,
    "src": "basketball-data-platform",
}

response = requests.get(URL, params=params, timeout=30)
print("HTTP status:", response.status_code)
response.raise_for_status()
data = response.json()

print("Kljucevi:", list(data.keys()))
for key, value in data.items():
    if isinstance(value, list):
        print(f"\n'{key}': lista od {len(value)}")
        if value:
            print(json.dumps(value[0], indent=2, ensure_ascii=False))
    else:
        print(f"\n'{key}':", repr(value)[:200])