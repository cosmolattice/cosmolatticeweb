#!/usr/bin/env python3
"""Tests for refresh_citations.py.

Runnable directly (``python3 documentation/scripts/test_refresh_citations.py``)
or via pytest. Offline: the merge logic is pure, so every test feeds it a
hand-built "what INSPIRE now says" dict. Nothing on disk is touched and no
request is made.

They pin down the promise the refresher makes — a hand edit is never lost:

1. A null affiliation is filled in once INSPIRE curates it.
2. A non-null one is kept even when INSPIRE disagrees, and the clash is reported.
3. Resolved "author N affiliation" flags leave needs_review; other flags stay.
4. An author list that no longer corresponds is refused rather than merged.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import refresh_citations as ref  # noqa: E402  (after sys.path tweak)


def _entry(**over):
    """A preprint as add_new_citation.py leaves it when INSPIRE is still a stub."""
    base = {
        "arxiv": "2607.25073", "inspire": 3183955, "title": "Fixing the IR tail",
        "authors": [{"name": "Ivan Dankovsky", "id": 2801981, "inst": None},
                    {"name": "Dmitry Gorbunov", "id": 1007949, "inst": None}],
        "journal": None, "doi": None, "date": "2026-07-27",
        "needs_review": ["author 1 affiliation", "author 2 affiliation"],
    }
    base.update(over)
    return base


def _curated(**over):
    """The same paper after INSPIRE's curation pass."""
    base = {
        "arxiv": "2607.25073", "inspire": 3183955, "title": "Fixing the IR tail",
        "authors": [{"name": "Ivan Dankovsky", "id": 2801981, "inst": 914910},
                    {"name": "Dmitry Gorbunov", "id": 1007949, "inst": 906878}],
        "journal": "Phys. Rev. D 114 (2026) 043512", "doi": "10.1103/xyz",
        "date": "2026-07-27", "needs_review": [],
    }
    base.update(over)
    return base


def test_fills_in_curated_affiliations():
    e = _entry()
    changes, conflicts = ref.merge(e, _curated())
    assert [a["inst"] for a in e["authors"]] == [914910, 906878]
    assert e["journal"] == "Phys. Rev. D 114 (2026) 043512"
    assert e["doi"] == "10.1103/xyz"
    assert not conflicts
    assert changes, "filling two affiliations, a journal and a doi is a change"


def test_hand_set_values_survive_disagreement():
    e = _entry(authors=[{"name": "Ivan Dankovsky", "id": 2801981, "inst": 908795},
                        {"name": "Dmitry Gorbunov", "id": 1007949, "inst": None}],
               journal="Hand-entered journal ref")
    _changes, conflicts = ref.merge(e, _curated())
    assert e["authors"][0]["inst"] == 908795, "hand-set affiliation was overwritten"
    assert e["journal"] == "Hand-entered journal ref", "hand-set journal was overwritten"
    assert e["authors"][1]["inst"] == 906878, "the null one should still get filled"
    assert len(conflicts) == 2, "both disagreements should be reported"


def test_title_and_date_are_never_touched():
    e = _entry(title="Hand-cleaned title", date="2026-07-27")
    ref.merge(e, _curated(title="Raw $title$ with markup", date="2026-07-28"))
    assert e["title"] == "Hand-cleaned title"
    assert e["date"] == "2026-07-27"


def test_author_names_are_never_touched():
    e = _entry(authors=[{"name": "I. Dankovsky", "id": 2801981, "inst": None},
                        {"name": "D. Gorbunov", "id": 1007949, "inst": None}])
    ref.merge(e, _curated())
    assert [a["name"] for a in e["authors"]] == ["I. Dankovsky", "D. Gorbunov"]


def test_resolved_review_flags_are_dropped_others_kept():
    e = _entry(needs_review=["author 1 affiliation", "author 2 affiliation", "title"])
    ref.merge(e, _curated())
    assert e["needs_review"] == ["title"]


def test_unresolved_review_flags_stay():
    partly = _curated(authors=[{"name": "Ivan Dankovsky", "id": 2801981, "inst": 914910},
                               {"name": "Dmitry Gorbunov", "id": 1007949, "inst": None}])
    e = _entry()
    ref.merge(e, partly)
    assert e["needs_review"] == ["author 2 affiliation"]


def test_no_news_is_no_change():
    e = _entry()
    changes, conflicts = ref.merge(e, _entry())   # INSPIRE still a stub
    assert changes == [] and conflicts == []
    assert e == _entry(), "a fruitless refresh must leave the entry byte-identical"


def test_author_count_change_is_refused():
    e = _entry()
    grown = _curated(authors=_curated()["authors"] + [{"name": "New Person", "id": 1, "inst": 2}])
    try:
        ref.merge(e, grown)
    except ValueError:
        return
    raise AssertionError("a changed author list must be refused, not merged")


def test_author_identity_change_is_refused():
    e = _entry()
    swapped = _curated()
    swapped["authors"][0]["id"] = 9999999
    try:
        ref.merge(e, swapped)
    except ValueError:
        return
    raise AssertionError("a different author id must be refused, not merged")


def test_candidate_selection():
    complete = _curated()
    assert ref.is_candidate(_entry(), include_journals=False)
    assert not ref.is_candidate(complete, include_journals=False)
    preprint = _curated(journal=None)
    assert not ref.is_candidate(preprint, include_journals=False)
    assert ref.is_candidate(preprint, include_journals=True)


def test_missing_affiliations_positions_are_one_based():
    e = _entry(authors=[{"name": "A", "id": 1, "inst": 5},
                        {"name": "B", "id": 2, "inst": None}])
    assert ref.missing_affiliations(e) == [2]


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print("ok  %s" % fn.__name__)
    print("\nall %d citation-refresher tests passed" % len(fns))


if __name__ == "__main__":
    _run()
