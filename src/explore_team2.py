from collections import Counter

import requests

URL = "https://sportscore.com/api/widget/team/"
params = {
    "sport": "basketball",
    "slug": "atlanta-hawks",
    "limit": 30,
    "src": "basketball-data-platform",
}

data = requests.get(URL, params=params, timeout=30).json()
matches = data["matches"]

print("Statusi:", dict(Counter(m["status"] for m in matches)))
dates = sorted(m["time"] for m in matches)
print("Od:", dates[0][:10], " Do:", dates[-1][:10])
print()
for m in matches:
    score = f"{m['home_score']}-{m['away_score']}" if m["home_score"] else "-"
    print(f"{m['time'][:10]}  {m['status']:10} {m['home']:25} vs {m['away']:25} {score}")