import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import clean_exoplanets as ce  # noqa: E402

CLEAN = ROOT / "data" / "clean" / "exoplanets_clean.csv"


@pytest.fixture(scope="module")
def raw():
    p = ce.find_raw()
    assert p is not None, "no raw file in data/raw/"
    return ce.read_raw(p)


@pytest.fixture(scope="module")
def clean():
    return pd.read_csv(CLEAN, dtype=str, keep_default_na=False, na_filter=False)


def test_row_counts_match(raw, clean):
    assert len(raw) == len(clean) > 0


def test_required_columns(clean):
    required = [v[0] for v in ce.COLUMNS.values()] + list(ce.DERIVED)
    assert not [c for c in required if c not in clean.columns]
    assert "method" in clean.columns  # original method kept


def test_raw_has_documented_columns(raw):
    assert not [c for c in ce.COLUMNS if c not in raw.columns]


def test_planet_names_present(clean):
    assert (clean["planet"].str.strip() != "").all()


def test_numeric_columns_parse(clean):
    for c in ce.NUMERIC + ["year"]:
        s = clean[c]
        nonblank = s[s != ""]
        pd.to_numeric(nonblank, errors="raise")
    y = clean["year"][clean["year"] != ""]
    assert y.str.fullmatch(r"\d{4}").all()  # integers, no ".0"


def test_no_missing_filled_and_values_preserved(raw, clean):
    for rc, (nc, kind, *_r) in ce.COLUMNS.items():
        r = raw[rc].str.strip()
        c = clean[nc]
        assert ((r == "") == (c == "")).all(), f"{nc}: blank pattern changed"
        if kind in ("num", "int"):
            both = r != ""
            assert (r[both].astype(float) == c[both].astype(float)).all(), nc
        else:
            assert (r.str.replace(r"\s+", " ", regex=True) == c).all(), nc


def test_derived_flags(clean):
    p = pd.to_numeric(clean["orbital_period_days"].replace("", pd.NA))
    r = pd.to_numeric(clean["radius_earth"].replace("", pd.NA))
    expected = ((p > 0) & (r > 0)).map({True: "true", False: "false"})
    assert (clean["has_scatter_values"] == expected).all()
    groups = set(clean["method_group"]) - {"", ce.OTHER_LABEL}
    assert len(groups) <= ce.TOP_N_METHODS


def test_spot_check_five_planets_incl_missing(raw, clean):
    names = [n for n in ce.SPOT_CHECK_NAMES if n in set(raw["pl_name"])][:4]
    idx = [raw.index[raw["pl_name"] == n][0] for n in names]
    miss = raw.index[(raw["pl_rade"].str.strip() == "") | (raw["pl_bmasse"].str.strip() == "")]
    assert len(miss), "no planet with missing value to spot-check"
    idx.append(miss[0])
    for i in idx:
        for rc, (nc, kind, *_r) in ce.COLUMNS.items():
            rv, cv = raw.at[i, rc].strip(), clean.at[i, nc]
            if rv == "":
                assert cv == ""
            elif kind in ("num", "int"):
                assert float(rv) == float(cv)
            else:
                assert rv == cv


def test_mass_type_and_flag(raw, clean):
    allowed = set(ce.MASS_TYPE)
    assert set(raw["pl_bmassprov"].str.strip()) - {""} <= allowed, "new mass_source value: ask before classifying"
    mass_missing = clean["mass_earth"] == ""
    expected = clean["mass_source"].map(ce.MASS_TYPE).where(~mass_missing, "")
    assert (clean["mass_type"] == expected).all()
    assert (clean.loc[mass_missing, ["mass_type", "mass_is_estimated"]] == "").all().all()
    pres = ~mass_missing
    assert ((clean.loc[pres, "mass_is_estimated"] == "true") == (clean.loc[pres, "mass_source"] == "M-R relationship")).all()
    assert set(clean.loc[pres, "mass_is_estimated"]) <= {"true", "false"}
    for src, typ in {"Mass": "measured", "Msin(i)/sin(i)": "derived_from_inclination",
                     "Msini": "minimum_mass", "M-R relationship": "estimated"}.items():
        sel = pres & (clean["mass_source"] == src)
        assert sel.any() and (clean.loc[sel, "mass_type"] == typ).all()


def test_radius_is_estimated(raw, clean):
    rad_missing = clean["radius_earth"] == ""
    assert (clean.loc[rad_missing, ["radius_reference", "radius_is_estimated"]] == "").all().all()
    calc = raw["pl_rade_reflink"].str.contains("CALCULATED_VALUE")
    pres = ~rad_missing
    assert ((clean.loc[pres, "radius_is_estimated"] == "true") == calc[pres]).all()
    assert set(clean.loc[pres, "radius_is_estimated"]) <= {"true", "false"}
    assert not clean["radius_reference"].str.contains("<").any()
    # calculated radii carry no uncertainty in the archive (docs), a consistency check on the identification
    assert (raw.loc[calc & pres, "pl_radeerr1"].str.strip() == "").all()
    # never co-occurs with a mass that was itself computed from radius
    assert not (calc & (raw["pl_bmassprov"] == "M-R relationship")).any()
