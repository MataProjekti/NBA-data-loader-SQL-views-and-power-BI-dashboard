import json

import requests

URL = "https://sportscore.com/api/widget/standings/"

for slug in ["national-basketball-association", "nba"]:
    r = requests.get(
        URL,
        params={"sport": "basketball", "slug": slug, "src": "basketball-data-platform"},
        timeout=30,
    )
    print(slug, "->", r.status_code)
    if r.ok:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:2500])
        break