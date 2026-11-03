# Exoplanet cleaning

Cleans NASA Exoplanet Archive `pscomppars` for the Observable Plot notebook (no charts here).

## Rerun everything
```
uv run clean_exoplanets.py && uv run pytest -v
```
Requires [uv](https://docs.astral.sh/uv/) and Python 3.10+. `uv run` creates `.venv` and installs the locked
dependencies from `pyproject.toml` / `uv.lock` automatically (`uv sync` does it explicitly).
Add packages with `uv add <pkg>` (or `uv add --dev <pkg>`). `requirements.txt` is kept for pip users:
`pip install -r requirements.txt`, then `python clean_exoplanets.py && python -m pytest tests -v`.

- Uses the newest `data/raw/pscomppars_*.csv`; if none exists it downloads from the archive TAP service
  and saves an untouched copy as `data/raw/pscomppars_<date>.csv` (plus a `.source.json` with the URL).
  To refresh, delete the raw files and rerun.
- Outputs in `data/clean/`: `exoplanets_clean.csv`, `data_dictionary.md`, `cleaning_report.md`.
- Settings (top of `clean_exoplanets.py`): `TOP_N_METHODS = 5`.
- Missing values stay blank; no rows are dropped; duplicates and log-scale problems are reported only.
