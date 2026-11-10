# Basketball Data Platform

End-to-end data engineering projekat: preuzima košarkaške rezultate iz javnog API-ja, čuva ih u PostgreSQL bazi, transformiše SQL-om, proverava kvalitet podataka testovima i priprema model za Power BI dashboard.

Powered by [SportScore](https://sportscore.com/)

## Tok podataka

```
SportScore API  →  raw.api_responses  →  core.games  →  mart (dim + fact + pogledi)  →  Power BI
   (JSON)            (sirovi JSONB)       (očišćeno)       (model za analitiku)
```

| Sloj | Šema | Opis |
|---|---|---|
| Raw | `raw` | Ceo API odgovor sačuvan kao JSONB, ništa se ne gubi |
| Core | `core` | Očišćene utakmice, jedan red po utakmici (upsert bez dupliranja) |
| Mart | `mart` | Dimenzije, činjenice i pogledi spremni za Power BI |

### Mart objekti

- `dim_teams`, `dim_leagues`, `dim_dates`: dimenzije
- `fact_games`: činjenice o utakmicama
- `v_team_record`: pobede, porazi, prosek poena po timu
- `v_nba_standings`: NBA poredak
- `v_team_form`: forma poslednjih 5 utakmica
- `v_team_games`: jedan red po timu po utakmici

## Tehnologije

Python 3.13, PostgreSQL, SQLAlchemy, psycopg2, requests, pytest, Power BI

## Pokretanje

1. Kloniraj repozitorijum i napravi virtuelno okruženje:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Napravi PostgreSQL bazu `basketball_db` i šeme `raw`, `core`, `mart` (SQL skripte su u folderu `sql/`).
3. Napravi fajl `.env` u korenu projekta:
   ```
   DB_USER=postgres
   DB_PASSWORD=tvoja_lozinka
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=basketball_db
   ```
4. Pokreni pipeline:
   ```powershell
   python src/pipeline.py
   ```
5. Pokreni testove kvaliteta podataka:
   ```powershell
   pytest -v
   ```

## Kvalitet podataka

Automatski testovi (`tests/test_data_quality.py`) proveravaju:

- tabela nije prazna i nema duplih utakmica
- završene utakmice imaju rezultat, rezultati nisu negativni
- nema nerešenih završenih utakmica (u košarci ne postoji nerešeno)
- domaćin i gost su različiti timovi, obavezna polja nisu prazna
- `fact_games` ima isti broj utakmica kao `core.games` (nijedna ne ispada iz JOIN-a)

## Ograničenja

- API je „widget“ tipa i vraća samo **poslednjih 50 utakmica** svih liga, bez parametra za datum. Istorija se zato gradi **dnevnim punjenjem** (pipeline se pokreće više puta dnevno), pa dashboard u početku ima malo podataka.
- API ne daje ID-jeve utakmica i timova. Utakmica se identifikuje kombinacijom `url + datum`, a tim po imenu.
- Odgovor meša više liga (NBA, NCAA, ženske i južnoameričke lige), pa se analitika filtrira po ligi.

## Plan razvoja

- [ ] Automatsko pokretanje (Windows Task Scheduler, zatim Airflow)
- [ ] Power BI dashboard
- [ ] Docker
- [ ] dbt transformacije

## Izvor podataka

Podaci dolaze sa [SportScore](https://sportscore.com/) widget API-ja (besplatan, bez ključa). Prema uslovima korišćenja obavezan je vidljiv link „Powered by SportScore“, koji se nalazi na vrhu ovog fajla.