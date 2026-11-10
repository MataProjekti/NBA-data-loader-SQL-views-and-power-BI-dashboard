CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS raw.api_responses (
    id          BIGSERIAL PRIMARY KEY,
    fetched_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    endpoint    TEXT NOT NULL,
    sport       TEXT NOT NULL,
    payload     JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS core.games (
    game_id          BIGSERIAL PRIMARY KEY,
    match_url        TEXT NOT NULL,
    game_date        DATE NOT NULL,
    home_team        TEXT NOT NULL,
    away_team        TEXT NOT NULL,
    home_score       INT,
    away_score       INT,
    status           TEXT NOT NULL,
    competition      TEXT NOT NULL,
    home_logo        TEXT,
    away_logo        TEXT,
    competition_logo TEXT,
    first_seen_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (match_url, game_date)
);

CREATE TABLE IF NOT EXISTS mart.dim_leagues (
    league_id        SERIAL PRIMARY KEY,
    competition      TEXT NOT NULL UNIQUE,
    competition_logo TEXT
);

CREATE TABLE IF NOT EXISTS mart.dim_teams (
    team_id   SERIAL PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    logo      TEXT
);

CREATE TABLE IF NOT EXISTS mart.dim_dates (
    date_id     DATE PRIMARY KEY,
    year        INT NOT NULL,
    month       INT NOT NULL,
    month_name  TEXT NOT NULL,
    day         INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name    TEXT NOT NULL,
    is_weekend  BOOLEAN NOT NULL
);

INSERT INTO mart.dim_dates
SELECT
    d::date,
    EXTRACT(year FROM d)::int,
    EXTRACT(month FROM d)::int,
    to_char(d, 'FMMonth'),
    EXTRACT(day FROM d)::int,
    EXTRACT(isodow FROM d)::int,
    to_char(d, 'FMDay'),
    EXTRACT(isodow FROM d) >= 6
FROM generate_series('2026-01-01'::date, '2027-12-31'::date, interval '1 day') AS d
ON CONFLICT (date_id) DO NOTHING;