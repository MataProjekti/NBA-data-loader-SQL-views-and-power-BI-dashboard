INSERT INTO mart.dim_leagues (competition, competition_logo)
SELECT DISTINCT ON (competition) competition, competition_logo
FROM core.games
ORDER BY competition, last_updated_at DESC
ON CONFLICT (competition) DO UPDATE SET competition_logo = EXCLUDED.competition_logo;

INSERT INTO mart.dim_teams (team_name, logo)
SELECT DISTINCT ON (team_name) team_name, logo
FROM (
    SELECT home_team AS team_name, home_logo AS logo, last_updated_at FROM core.games
    UNION ALL
    SELECT away_team, away_logo, last_updated_at FROM core.games
) t
ORDER BY team_name, last_updated_at DESC
ON CONFLICT (team_name) DO UPDATE SET logo = EXCLUDED.logo;