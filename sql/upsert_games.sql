INSERT INTO core.games (
    match_url, game_date, home_team, away_team, home_score, away_score,
    status, competition, home_logo, away_logo, competition_logo
)
SELECT DISTINCT ON (m->>'url', ((m->>'time')::timestamptz AT TIME ZONE 'UTC')::date)
    m->>'url',
    ((m->>'time')::timestamptz AT TIME ZONE 'UTC')::date,
    m->>'home',
    m->>'away',
    CASE WHEN m->>'home_score' ~ '^\d+$' THEN (m->>'home_score')::int END,
    CASE WHEN m->>'away_score' ~ '^\d+$' THEN (m->>'away_score')::int END,
    m->>'status',
    m->>'competition',
    m->>'home_logo',
    m->>'away_logo',
    m->>'competition_logo'
FROM raw.api_responses r
CROSS JOIN LATERAL jsonb_array_elements(r.payload->'matches') AS m
ORDER BY
    m->>'url',
    ((m->>'time')::timestamptz AT TIME ZONE 'UTC')::date,
    r.fetched_at DESC
ON CONFLICT (match_url, game_date) DO UPDATE SET
    home_score      = EXCLUDED.home_score,
    away_score      = EXCLUDED.away_score,
    status          = EXCLUDED.status,
    last_updated_at = now();