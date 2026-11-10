import json
import os

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

ENDPOINT = "matches"
SPORT = "basketball"

response = requests.get(
    "https://sportscore.com/api/widget/matches/",
    params={"sport": SPORT, "limit": 50, "src": "basketball-data-platform"},
    timeout=30,
)
response.raise_for_status()
payload = response.json()

with engine.begin() as conn:
    conn.execute(
        text(
            "INSERT INTO raw.api_responses (endpoint, sport, payload) "
            "VALUES (:endpoint, :sport, CAST(:payload AS JSONB))"
        ),
        {"endpoint": ENDPOINT, "sport": SPORT, "payload": json.dumps(payload)},
    )

print("Upisano. Utakmica u odgovoru:", len(payload.get("matches", [])))