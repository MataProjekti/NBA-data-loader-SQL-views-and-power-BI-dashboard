from sqlalchemy import text


def count(conn, where):
    query = f"SELECT count(*) FROM core.games WHERE {where}"
    return conn.execute(text(query)).scalar()


def test_table_is_not_empty(conn):
    assert count(conn, "TRUE") > 0


def test_no_duplicate_games(conn):
    rows = conn.execute(
        text(
            "SELECT match_url, game_date FROM core.games "
            "GROUP BY match_url, game_date HAVING count(*) > 1"
        )
    ).fetchall()
    assert rows == []


def test_finished_games_have_scores(conn):
    assert count(
        conn, "status = 'finished' AND (home_score IS NULL OR away_score IS NULL)"
    ) == 0


def test_scores_are_not_negative(conn):
    assert count(conn, "home_score < 0 OR away_score < 0") == 0


def test_no_ties_in_finished_games(conn):
    # u kosarci nema nereseno (produzeci), pa jednak rezultat znaci gresku u podacima
    assert count(conn, "status = 'finished' AND home_score = away_score") == 0


def test_teams_are_different(conn):
    assert count(conn, "home_team = away_team") == 0


def test_required_text_fields_not_empty(conn):
    assert count(
        conn,
        "trim(home_team) = '' OR trim(away_team) = '' OR trim(competition) = ''",
    ) == 0


def test_fact_games_matches_core_games(conn):
    core = conn.execute(text("SELECT count(*) FROM core.games")).scalar()
    fact = conn.execute(text("SELECT count(*) FROM mart.fact_games")).scalar()
    assert core == fact


def test_no_orphan_teams_in_fact(conn):
    n = conn.execute(
        text(
            "SELECT count(*) FROM mart.fact_games "
            "WHERE home_team_id IS NULL OR away_team_id IS NULL"
        )
    ).scalar()
    assert n == 0