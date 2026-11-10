import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"
API_URL = "https://sportscore.com/api/widget/matches/"
SPORT = "basketball"


def extract():
    response = requests.get(
        API_URL,
        params={"sport": SPORT, "limit": 50, "src": "basketball-data-platform"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("matches"):
        raise ValueError("API je vratio prazan odgovor")
    return payload


def load_raw(conn, payload):
    conn.execute(
        text(
            "INSERT INTO raw.api_responses (endpoint, sport, payload) "
            "VALUES (:endpoint, :sport, CAST(:payload AS JSONB))"
        ),
        {"endpoint": "matches", "sport": SPORT, "payload": json.dumps(payload)},
    )


def run_sql_file(conn, name):
    sql = (SQL_DIR / name).read_text(encoding="utf-8")
    conn.exec_driver_sql(sql)


def main():
    payload = extract()
    print("Preuzeto utakmica:", len(payload["matches"]))

    with engine.begin() as conn:
        load_raw(conn, payload)
        run_sql_file(conn, "upsert_games.sql")
        run_sql_file(conn, "refresh_marts.sql")
        games = conn.execute(text("SELECT count(*) FROM core.games")).scalar()
        teams = conn.execute(text("SELECT count(*) FROM mart.dim_teams")).scalar()
        fact = conn.execute(text("SELECT count(*) FROM mart.fact_games")).scalar()

    print("core.games:", games, "| dim_teams:", teams, "| fact_games:", fact)


if __name__ == "__main__":
    main()