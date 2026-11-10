CREATE OR REPLACE VIEW mart.fact_games AS
SELECT
    g.game_id,
    g.game_date,
    l.league_id,
    ht.team_id AS home_team_id,
    awt.team_id AS away_team_id,
    g.home_score,
    g.away_score,
    g.home_score + g.away_score AS total_points,
    CASE
        WHEN g.status <> 'finished' THEN NULL
        WHEN g.home_score > g.away_score THEN ht.team_id
        WHEN g.away_score > g.home_score THEN awt.team_id
    END AS winner_team_id,
    g.status
FROM core.games g
JOIN mart.dim_leagues l  ON l.competition = g.competition
JOIN mart.dim_teams  ht  ON ht.team_name  = g.home_team
JOIN mart.dim_teams  awt ON awt.team_name = g.away_team;

CREATE OR REPLACE VIEW mart.v_team_record AS
WITH results AS (
    SELECT competition, home_team AS team,
           (home_score > away_score)::int AS win,
           home_score AS pts_for, away_score AS pts_against
    FROM core.games WHERE status = 'finished'
    UNION ALL
    SELECT competition, away_team,
           (away_score > home_score)::int,
           away_score, home_score
    FROM core.games WHERE status = 'finished'
)
SELECT
    competition,
    team,
    count(*)                               AS games,
    sum(win)                               AS wins,
    count(*) - sum(win)                    AS losses,
    round(sum(win)::numeric / count(*), 3) AS win_pct,
    round(avg(pts_for), 1)                 AS avg_pts_for,
    round(avg(pts_against), 1)             AS avg_pts_against
FROM results
GROUP BY competition, team;

CREATE OR REPLACE VIEW mart.v_team_games AS
SELECT game_id, game_date, competition,
       home_team AS team, away_team AS opponent, TRUE AS is_home,
       home_score AS pts_for, away_score AS pts_against,
       (home_score > away_score) AS won
FROM core.games
WHERE status = 'finished'
UNION ALL
SELECT game_id, game_date, competition,
       away_team, home_team, FALSE,
       away_score, home_score,
       (away_score > home_score)
FROM core.games
WHERE status = 'finished';

CREATE OR REPLACE VIEW mart.v_nba_standings AS
SELECT
    rank() OVER (ORDER BY win_pct DESC, wins DESC) AS rank,
    team,
    games,
    wins,
    losses,
    win_pct,
    avg_pts_for,
    avg_pts_against,
    round(avg_pts_for - avg_pts_against, 1) AS avg_margin
FROM mart.v_team_record
WHERE competition = 'National Basketball Association';

CREATE OR REPLACE VIEW mart.v_team_form AS
WITH ranked AS (
    SELECT *,
           row_number() OVER (
               PARTITION BY competition, team
               ORDER BY game_date DESC, game_id DESC
           ) AS rn
    FROM mart.v_team_games
)
SELECT
    competition,
    team,
    count(*)                 AS games_in_form,
    sum(won::int)            AS wins,
    count(*) - sum(won::int) AS losses,
    string_agg(CASE WHEN won THEN 'W' ELSE 'L' END, ''
               ORDER BY game_date DESC, game_id DESC) AS form
FROM ranked
WHERE rn <= 5
GROUP BY competition, team;