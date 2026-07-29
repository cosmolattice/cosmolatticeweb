#!/usr/bin/env python3
"""Tests for the shared helpers in clpubs.py.

Runnable directly (``python3 documentation/scripts/test_clpubs.py``) or via
pytest. Offline: every test feeds a hand-built INSPIRE payload to a pure
function. Nothing on disk is touched and no request is made.

The institution-name tests pin down a bug that cost a third of the institution
table its name: INSPIRE marks a superseded record with the literal ICN
'obsolete' and keeps the real name in legacy_ICN, and

    name = ((md.get("ICN") or [""])[0] or md.get("legacy_ICN") or "")
    name = "" if name.lower() == "obsolete" else name

never reaches the fallback, because 'obsolete' is truthy and short-circuits the
or-chain. The sentinel has to be cleared first. See refresh_institutions.py.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import clpubs  # noqa: E402  (after sys.path tweak)


# ------------------------------------------------------- institution_name ----
def test_prefers_the_current_name():
    assert clpubs.institution_name({"ICN": ["CAS, ITP, Beijing"],
                                    "legacy_ICN": "Beijing, Inst. Theor. Phys."}) \
        == "CAS, ITP, Beijing"


def test_obsolete_falls_back_to_legacy():
    """The regression: 'obsolete' is truthy and used to swallow the fallback."""
    assert clpubs.institution_name({"ICN": ["obsolete"],
                                    "legacy_ICN": "ICTP-AP, Beijing"}) == "ICTP-AP, Beijing"


def test_obsolete_is_case_insensitive():
    assert clpubs.institution_name({"ICN": ["Obsolete"], "legacy_ICN": "Oxford U."}) == "Oxford U."


def test_obsolete_with_no_legacy_is_nameless():
    assert clpubs.institution_name({"ICN": ["obsolete"]}) is None
    assert clpubs.institution_name({"ICN": ["obsolete"], "legacy_ICN": ""}) is None


def test_missing_or_empty_icn_uses_legacy():
    assert clpubs.institution_name({"legacy_ICN": "SUNY, Stony Brook"}) == "SUNY, Stony Brook"
    assert clpubs.institution_name({"ICN": [], "legacy_ICN": "Moscow, INR"}) == "Moscow, INR"
    assert clpubs.institution_name({"ICN": [""], "legacy_ICN": "DESY, Zeuthen"}) == "DESY, Zeuthen"


def test_no_name_at_all_is_none():
    assert clpubs.institution_name({}) is None


def test_whitespace_is_trimmed():
    assert clpubs.institution_name({"ICN": ["  Oxford U.  "]}) == "Oxford U."
    assert clpubs.institution_name({"ICN": ["obsolete"], "legacy_ICN": " Mainz U. "}) == "Mainz U."


# --------------------------------------------------- normalize_institution ----
def _record(**over):
    base = {"ICN": ["obsolete"], "legacy_ICN": "ICTP-AP, Beijing",
            "addresses": [{"cities": ["Beijing"], "country_code": "CN",
                           "latitude": 39.99, "longitude": 116.31}]}
    base.update(over)
    return base


def test_normalize_shapes_the_yaml_row():
    assert clpubs.normalize_institution(_record()) == {
        "name": "ICTP-AP, Beijing", "city": "Beijing", "country": "CN",
        "lat": 39.99, "lon": 116.31}


def test_normalize_applies_the_city_alias():
    r = _record(addresses=[{"cities": ["Burjassot"], "country_code": "ES"}])
    assert clpubs.normalize_institution(r)["city"] == "Valencia"


def test_normalize_tolerates_a_bare_record():
    assert clpubs.normalize_institution({}) == {
        "name": None, "city": None, "country": None, "lat": None, "lon": None}


def test_normalize_leaves_absent_coordinates_null():
    r = _record(addresses=[{"cities": ["Beijing"], "country_code": "CN"}])
    got = clpubs.normalize_institution(r)
    assert got["lat"] is None and got["lon"] is None


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok  %s" % fn.__name__)
    print("\nall %d clpubs-helper tests passed" % len(fns))


if __name__ == "__main__":
    _run()
