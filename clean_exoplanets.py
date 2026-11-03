#!/usr/bin/env python3
"""Clean the NASA Exoplanet Archive PSCompPars table for the Observable Plot notebook.

Run:  python clean_exoplanets.py
- Uses the newest data/raw/pscomppars_*.csv if present; otherwise downloads from the TAP service.
- Writes data/clean/exoplanets_clean.csv, data_dictionary.md and cleaning_report.md.
Missing values are never filled, estimated or dropped; no planet rows are removed.
"""
import csv
import io
import json
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

# ---------------- settings ----------------
TOP_N_METHODS = 5            # number of named method groups; the rest become "Other"
OTHER_LABEL = "Other"
ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"
TAP_BASE = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
TAP_QUERY = "select * from pscomppars"
DOCS_URL = "https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html"

# raw column -> (clean name, kind, type N/O/Q, unit, meaning)
COLUMNS = {
    "pl_name": ("planet", "text", "N", "", "Planet name most commonly used in the literature"),
    "hostname": ("host", "text", "N", "", "Host star name most commonly used in the literature"),
    "discoverymethod": ("method", "text", "N", "", "Method by which the planet was first identified"),
    "disc_year": ("year", "int", "O", "year", "Year the planet was discovered"),
    "disc_facility": ("facility", "text", "N", "", "Facility that made the discovery observations"),
    "pl_orbper": ("orbital_period_days", "num", "Q", "days", "Time to complete one orbit"),
    "pl_rade": ("radius_earth", "num", "Q", "Earth radii", "Planet radius"),
    "pl_bmasse": ("mass_earth", "num", "Q", "Earth masses",
                  "Best available mass (true mass, else M*sin(i)/sin(i), else M*sin(i)); see mass_source"),
    "pl_bmassprov": ("mass_source", "text", "N", "", "Provenance of the best mass (Mass, Msini, Msini/sini)"),
    "pl_eqt": ("equilibrium_temp_k", "num", "Q", "K", "Equilibrium temperature (black-body, heated by host star only)"),
    "sy_dist": ("distance_pc", "num", "Q", "parsecs", "Distance to the planetary system"),
}
NUMERIC = [v[0] for v in COLUMNS.values() if v[1] == "num"]
# mass_source values documented as a minimum mass (lower limit): counted as "estimated".
ESTIMATED_MASS_VALUES = {"Msini"}
# documented as true/derived masses: counted as not estimated.
NOT_ESTIMATED_MASS_VALUES = {"Mass", "Msin(i)/sin(i)", "Msini/sini"}
# any other value (e.g. "M-R relationship") is undocumented -> mass_is_estimated left blank pending a decision.
DERIVED = {
    "method_group": ("N", "", "method", f"Top {TOP_N_METHODS} discovery methods by planet count; all others labelled '{OTHER_LABEL}'"),
    "has_scatter_values": ("N", "", "orbital_period_days, radius_earth", "true only if orbital period AND radius are both > 0 (usable on a log-log scatterplot)"),
    "mass_is_estimated": ("N", "", "mass_source", "true if mass_source is 'Msini' (minimum mass only, not a true mass); false for 'Mass' and 'Msin(i)/sin(i)'; blank for undocumented values such as 'M-R relationship'"),
}
SPOT_CHECK_NAMES = ["51 Peg b", "Kepler-22 b", "TRAPPIST-1 e", "Proxima Cen b"]


# ---------------- raw data ----------------
def find_raw():
    files = sorted(RAW_DIR.glob("pscomppars_*.csv")) if RAW_DIR.exists() else []
    return files[-1] if files else None


def download_raw():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    url = TAP_BASE + "?" + urllib.parse.urlencode({"query": TAP_QUERY, "format": "csv"})
    req = urllib.request.Request(url, headers={"User-Agent": "exoplanet-cleaning-script"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    today = date.today().isoformat()
    path = RAW_DIR / f"pscomppars_{today}.csv"
    path.write_bytes(data)  # untouched bytes
    (RAW_DIR / f"pscomppars_{today}.source.json").write_text(
        json.dumps({"download_date": today, "source_url": url, "table": "pscomppars"}, indent=2), encoding="utf-8")
    return path


def raw_source_info(path):
    side = path.with_suffix(".source.json")
    if side.exists():
        return json.loads(side.read_text(encoding="utf-8"))
    return {"download_date": "unknown (no sidecar file)", "source_url": "unknown"}


def read_raw(path):
    """All cells as strings; blanks stay blank (no NA coercion)."""
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_filter=False, comment=None)


def check_columns(raw):
    missing = [c for c in COLUMNS if c not in raw.columns]
    if missing:
        sys.exit(f"STOP: expected columns missing from raw file: {missing}. Check {DOCS_URL}")


# ---------------- cleaning ----------------
def clean(raw):
    check_columns(raw)
    out = pd.DataFrame(index=raw.index)
    problems = {}  # column -> list of non-blank values that failed to parse
    for rc, (nc, kind, *_rest) in COLUMNS.items():
        s = raw[rc].str.strip().str.replace(r"\s+", " ", regex=True)
        if kind == "text":
            out[nc] = s
        else:
            num = pd.to_numeric(s.replace("", pd.NA), errors="coerce")
            bad = s[(s != "") & num.isna()]
            if len(bad):
                problems[nc] = bad.tolist()
            if kind == "int":
                nonint = num.notna() & (num != num.round())
                if nonint.any():
                    problems[nc] = problems.get(nc, []) + s[nonint].tolist()
                num = num.round().astype("Int64")
            out[nc] = num
    # method_group
    counts = out["method"][out["method"] != ""].value_counts()
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    top = [m for m, _ in ranked[:TOP_N_METHODS]]
    out["method_group"] = out["method"].map(lambda m: "" if m == "" else (m if m in top else OTHER_LABEL))
    # scatter flag
    out["has_scatter_values"] = (out["orbital_period_days"] > 0) & (out["radius_earth"] > 0)
    # mass_is_estimated: blank when mass_source is blank
    out["mass_is_estimated"] = out["mass_source"].map(
        lambda v: "true" if v in ESTIMATED_MASS_VALUES else ("false" if v in NOT_ESTIMATED_MASS_VALUES else ""))
    out["has_scatter_values"] = out["has_scatter_values"].map({True: "true", False: "false"})
    return out, top, problems


def write_clean(out):
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    path = CLEAN_DIR / "exoplanets_clean.csv"
    out.to_csv(path, index=False, na_rep="", lineterminator="\n", encoding="utf-8")
    return path


def data_dictionary():
    rows = ["# Data dictionary", "",
            "Type: N = nominal, O = ordinal, Q = quantitative. Source: NASA Exoplanet Archive `pscomppars` "
            f"([column docs]({DOCS_URL})). Blank cell = missing in the archive (never filled).", "",
            "| Column | Meaning | Unit | Type | Source column |", "|---|---|---|---|---|"]
    for rc, (nc, _k, t, u, m) in COLUMNS.items():
        rows.append(f"| {nc} | {m} | {u or '-'} | {t} | `{rc}` |")
    for nc, (t, u, src, m) in DERIVED.items():
        rows.append(f"| {nc} | {m} | {u or '-'} | {t} | derived from `{src}` |")
    rows += ["", "Notes: `year` is typed O (ordered, discrete); treat as Q if you want a continuous axis. "
             "Booleans are written as `true`/`false`."]
    return "\n".join(rows) + "\n"


# ---------------- report ----------------
def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def spot_checks(raw, out):
    names = [n for n in SPOT_CHECK_NAMES if n in set(raw["pl_name"].str.strip())][:4]
    mcols = [c for c in COLUMNS if c != "pl_name"]
    miss = out.index[(out[[COLUMNS[c][0] for c in ("pl_rade", "pl_bmasse", "pl_eqt")]].isna().any(axis=1))]
    pick = [raw.index[raw["pl_name"].str.strip() == n][0] for n in names]
    for i in miss:
        if i not in pick:
            pick.append(i)
            break
    pick = pick[:5]
    while len(pick) < 5:
        pick.append(next(i for i in raw.index if i not in pick))
    lines = []
    for i in pick:
        lines.append(f"**{raw.at[i, 'pl_name']}**")
        lines.append("")
        lines.append("| clean column | raw value | clean value | match |")
        lines.append("|---|---|---|---|")
        for rc in mcols:
            nc = COLUMNS[rc][0]
            rv, cv = raw.at[i, rc], out.at[i, nc]
            cv_s = "" if pd.isna(cv) else (str(int(cv)) if COLUMNS[rc][1] == "int" else str(cv))
            if COLUMNS[rc][1] in ("num", "int") and rv.strip() != "":
                ok = float(rv) == float(cv_s)
            else:
                ok = rv.strip() == cv_s
            lines.append(f"| {nc} | {rv if rv else '(blank)'} | {cv_s if cv_s else '(blank)'} | {'yes' if ok else 'NO'} |")
        lines.append("")
    return "\n".join(lines)


def build_report(raw_path, info, raw, out, top, problems):
    L = []
    a = L.append
    a("# Cleaning report\n")
    a("## Source and row counts")
    a(f"- Raw file used: `{raw_path.relative_to(ROOT)}`")
    a(f"- Download date: {info['download_date']}")
    a(f"- Source URL: {info['source_url']}")
    a(f"- Column documentation checked: {DOCS_URL} (all 11 source columns documented for `pscomppars`)")
    a(f"- Raw rows: {len(raw)}; clean rows: {len(out)} (no planets dropped)")
    a(f"- Report generated: {date.today().isoformat()}; TOP_N_METHODS = {TOP_N_METHODS}\n")

    a("## Missing values per column (blank in the clean file)")
    miss = pd.DataFrame({"column": out.columns})
    cnt = []
    for c in out.columns:
        cnt.append(int(out[c].isna().sum()) if c in NUMERIC + ["year"] else int((out[c] == "").sum()))
    miss["missing"] = cnt
    miss["percent"] = [f"{100 * n / len(out):.2f}%" for n in cnt]
    a(md_table(miss) + "\n")

    a("## Numeric summary (non-missing values)")
    rows = []
    for c in ["year"] + NUMERIC:
        s = out[c].dropna().astype(float)
        rows.append({"column": c, "n": len(s), "min": f"{s.min():.6g}", "median": f"{s.median():.6g}", "max": f"{s.max():.6g}"})
    a(md_table(pd.DataFrame(rows)) + "\n")

    a("## Planets per method")
    a(md_table(out["method"].value_counts().rename_axis("method").reset_index(name="planets")) + "\n")
    a(f"## Planets per method_group (named groups: {', '.join(top)})")
    a(md_table(out["method_group"].value_counts().rename_axis("method_group").reset_index(name="planets")) + "\n")

    y = out["year"].dropna()
    a("## Discovery year range")
    a(f"{int(y.min())} to {int(y.max())}\n")

    a("## Scatterplot (orbital period vs radius)")
    p, r = out["orbital_period_days"], out["radius_earth"]
    ok = out["has_scatter_values"] == "true"
    a(f"- Can appear (has_scatter_values = true): **{int(ok.sum())}**")
    a(f"- Omitted: **{int((~ok).sum())}**")
    reasons = [
        ("missing period only", p.isna() & r.notna() & ~(r <= 0)),
        ("missing radius only", r.isna() & p.notna() & ~(p <= 0)),
        ("missing both", p.isna() & r.isna()),
        ("period <= 0 (any radius)", p <= 0),
        ("radius <= 0 (any period)", r <= 0),
    ]
    for label, m in reasons:
        a(f"  - {label}: {int(m.sum())}")
    a("  (categories 4 and 5 may overlap with each other; 1-3 are exclusive of them.)\n")

    a("## Log-scale problems (flagged, not changed)")
    any_bad = False
    for c in NUMERIC:
        bad = out[out[c] <= 0]
        if len(bad):
            any_bad = True
            a(f"- {c}: {len(bad)} value(s) <= 0 — " + "; ".join(f"{n} = {v}" for n, v in zip(bad["planet"], bad[c])))
    if not any_bad:
        a("- None: no zero or negative values in any numeric column.")
    a("")

    a("## Duplicate planet names (reported, NOT removed)")
    names = out["planet"]
    exact = names[names.duplicated(keep=False) & (names != "")]
    folded = names.str.casefold()[names.str.casefold().duplicated(keep=False) & (names != "")]
    if exact.empty and folded.empty:
        a("- None found (exact or case-insensitive).")
    else:
        a(f"- Exact duplicates: {sorted(set(exact))}")
        a(f"- Case-insensitive duplicates: {sorted(set(names[folded.index]))}")
    a(f"- Blank planet names: {int((names == '').sum())}\n")

    a("## mass_is_estimated")
    a("Docs (pl_bmassprov): `Mass` = measured mass; `Msini/sini` = true mass computed from a minimum mass plus inclination; "
      "`Msini` = minimum mass from radial velocity, no inclination correction.")
    a(f"- Counted as estimated (true): {sorted(ESTIMATED_MASS_VALUES)} — a lower limit, not a true mass.")
    a(f"- Counted as not estimated (false): {sorted(NOT_ESTIMATED_MASS_VALUES)}")
    a("- Left BLANK: any other value, e.g. `M-R relationship` (present in the data but NOT in the docs page checked; "
      "it is probably a mass modelled from radius, but I did not assume that). **Decision needed.**")
    a(md_table(out["mass_source"].replace("", "(blank)").value_counts().rename_axis("mass_source").reset_index(name="planets")))
    a(f"\nmass_is_estimated: true={int((out['mass_is_estimated']=='true').sum())}, "
      f"false={int((out['mass_is_estimated']=='false').sum())}, blank={int((out['mass_is_estimated']=='').sum())}\n")

    a("## Spot checks (raw vs clean)")
    a(spot_checks(raw, out))

    a("## Anything unusual / uncertain")
    a("- OPEN QUESTION: `mass_source = 'M-R relationship'` is undocumented on the column page, so mass_is_estimated is blank for those planets.")
    mx = out["orbital_period_days"].max()
    a(f"- Max orbital_period_days = {mx:.4g} ({out.loc[out['orbital_period_days'].idxmax(), 'planet']}); extreme but positive, left as is.")
    a("- Judgement call: `Msini/sini` is treated as NOT estimated (it is a derived true mass). Say if you'd rather count it.")
    a("- Judgement call: `mass_earth` mixes true masses and minimum masses; use mass_is_estimated/mass_source before comparing.")
    a("- Judgement call: `year` typed O in the dictionary; method_group is blank where method is blank.")
    if problems:
        for c, v in problems.items():
            a(f"- Unparseable/non-integer values in {c}: {v[:10]} (set blank)")
    else:
        a("- All non-blank numeric cells parsed cleanly.")
    other_files = [f.name for f in ROOT.glob("PSCompPars_*.csv")]
    if other_files:
        a(f"- A separate manual download exists at the project root ({', '.join(other_files)}); it was NOT used because "
          "it is not in data/raw/.")
    a("")
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    raw_path = find_raw()
    if raw_path is None:
        print("No raw file in data/raw/; downloading from TAP...")
        raw_path = download_raw()
    print(f"Using raw file: {raw_path}")
    info = raw_source_info(raw_path)
    raw = read_raw(raw_path)
    out, top, problems = clean(raw)
    assert len(raw) == len(out)
    write_clean(out)
    (CLEAN_DIR / "data_dictionary.md").write_text(data_dictionary(), encoding="utf-8", newline="\n")
    report = build_report(raw_path, info, raw, out, top, problems)
    (CLEAN_DIR / "cleaning_report.md").write_text(report, encoding="utf-8", newline="\n")
    print(report)


if __name__ == "__main__":
    main()
