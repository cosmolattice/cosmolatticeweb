#!/usr/bin/env python3
"""Re-ask INSPIRE about entries that came in incomplete, and fill in what arrived.

    python3 refresh_citations.py               # every entry missing an affiliation
    python3 refresh_citations.py --journals    # ... plus every entry with no journal
    python3 refresh_citations.py 2607.25073    # just these arXiv ids
    python3 refresh_citations.py --dry-run     # report only, write no YAML

Why this exists: INSPIRE creates a record as soon as a paper appears on arXiv, but
the record starts as a stub — authors are matched to their profiles, yet
affiliations (and later the journal reference and DOI) are only added in a curation
pass some days afterwards. add_new_citation.py therefore flags fresh preprints with
``needs_review: [author N affiliation]`` and leaves ``inst: null``. This script
picks those entries back up, drops their cached INSPIRE answer so the fetch really
goes to the network, and merges in whatever has since been curated.

Merge policy — a hand edit always wins:
  * only fields that are currently null are ever filled in;
  * a non-null inst / journal / doi is left exactly as it is, even if INSPIRE now
    disagrees (the disagreement is reported, not applied);
  * title, date and author names are never touched — those get curated by hand
    (markup stripping, initials vs full names) and re-fetching would undo that;
  * ``needs_review`` loses only the "author N affiliation" items that got resolved;
    a "title" flag stays until a human clears it.

Nothing is written when nothing changed, so running this on a quiet week leaves the
working tree clean. Exit status is 0 whenever the run itself worked — "INSPIRE has
not caught up yet" is a normal outcome, not a failure. It returns 1 only for a
genuine problem: the network being unreachable, or an entry whose author list no
longer lines up with ours and so needs a human.
"""
import sys
import urllib.error

import clpubs
import gen_publications
import build_map_data


# ------------------------------------------------------------------ picking ----
def missing_affiliations(entry):
    """1-based positions of the authors on this entry that still have no institution."""
    return [i for i, a in enumerate(entry.get("authors") or [], 1) if not a.get("inst")]


def is_candidate(entry, include_journals):
    if missing_affiliations(entry):
        return True
    return bool(include_journals and not entry.get("journal"))


def describe(entry):
    """One-line summary of what is still missing on an entry."""
    bits = []
    gaps = missing_affiliations(entry)
    if gaps:
        bits.append("%d/%d affiliations" % (len(gaps), len(entry.get("authors") or [])))
    if not entry.get("journal"):
        bits.append("journal")
    if not entry.get("doi"):
        bits.append("doi")
    return ", ".join(bits) or "nothing"


# ------------------------------------------------------------------ merging ----
def merge(entry, fresh):
    """Fill null fields on `entry` from the freshly fetched `fresh`. Mutates `entry`.

    Returns (changes[], conflicts[]) — changes are what was filled in, conflicts are
    places where INSPIRE now says something other than what we already hold. Raises
    ValueError when the author lists no longer correspond, which means the paper was
    revised and a human has to look.
    """
    ours, theirs = entry.get("authors") or [], fresh.get("authors") or []
    if len(ours) != len(theirs):
        raise ValueError("author count changed on INSPIRE: %d here, %d there"
                         % (len(ours), len(theirs)))
    for i, (a, b) in enumerate(zip(ours, theirs), 1):
        if a.get("id") and b.get("id") and a["id"] != b["id"]:
            raise ValueError("author %d is a different person on INSPIRE now "
                             "(id %s here, %s there)" % (i, a["id"], b["id"]))

    changes, conflicts = [], []
    for i, (a, b) in enumerate(zip(ours, theirs), 1):
        for field in ("id", "inst"):
            if a.get(field) is None and b.get(field) is not None:
                a[field] = b[field]
                changes.append("author %d (%s): %s -> %s" % (i, a.get("name"), field, b[field]))
            elif a.get(field) is not None and b.get(field) is not None and a[field] != b[field]:
                conflicts.append("author %d (%s): %s is %s here, %s on INSPIRE — kept ours"
                                 % (i, a.get("name"), field, a[field], b[field]))

    for field in ("journal", "doi", "inspire"):
        if entry.get(field) is None and fresh.get(field) is not None:
            entry[field] = fresh[field]
            changes.append("%s -> %s" % (field, fresh[field]))
        elif entry.get(field) is not None and fresh.get(field) is not None \
                and entry[field] != fresh[field]:
            conflicts.append("%s is %r here, %r on INSPIRE — kept ours"
                             % (field, entry[field], fresh[field]))

    # An "author N affiliation" flag is only meaningful while author N has none.
    still = set("author %d affiliation" % i for i in missing_affiliations(entry))
    kept = [r for r in (entry.get("needs_review") or [])
            if not r.startswith("author ") or not r.endswith(" affiliation") or r in still]
    if kept != (entry.get("needs_review") or []):
        entry["needs_review"] = kept
        changes.append("needs_review -> %s" % (kept or "[]"))

    return changes, conflicts


# --------------------------------------------------------------------- main ----
def main(argv):
    include_journals = "--journals" in argv
    dry_run = "--dry-run" in argv
    wanted = [a.strip().replace("arXiv:", "").replace("arxiv:", "")
              for a in argv if not a.startswith("-")]
    for flag in argv:
        if flag.startswith("-") and flag not in ("--journals", "--dry-run"):
            print("usage: python3 refresh_citations.py [--journals] [--dry-run] [<arxiv-id> ...]",
                  file=sys.stderr)
            return 2

    pubs, insts = clpubs.load()
    by_arxiv = {str(p.get("arxiv")): p for p in pubs}

    if wanted:
        unknown = [a for a in wanted if a not in by_arxiv]
        if unknown:
            print("  ⚠ not in publications.yaml: %s" % ", ".join(unknown), file=sys.stderr)
            return 2
        todo = [by_arxiv[a] for a in wanted]
    else:
        todo = [p for p in pubs if is_candidate(p, include_journals)]

    if not todo:
        print("• nothing incomplete — all %d entries have their affiliations." % len(pubs))
        return 0

    print("• re-asking INSPIRE about %d of %d entries:" % (len(todo), len(pubs)))
    for e in todo:
        print("    %-11s %s  (missing: %s)" % (e["arxiv"], e["date"], describe(e)))
    print()

    touched, still, failed = [], [], []
    for e in todo:
        arxiv = str(e["arxiv"])
        clpubs.forget_literature(arxiv)   # also under --dry-run: a stale cache hit would
                                          # report "no news" without ever asking INSPIRE
        try:
            fresh, _warnings = clpubs.build_entry(arxiv, insts)
        except (urllib.error.URLError, OSError) as exc:
            failed.append((arxiv, "could not reach INSPIRE: %s" % exc))
            continue
        if fresh is None:
            failed.append((arxiv, "no INSPIRE record for this arXiv id"))
            continue

        try:
            changes, conflicts = merge(e, fresh)
        except ValueError as exc:
            failed.append((arxiv, str(exc)))
            continue

        if changes:
            touched.append((arxiv, e, changes, conflicts))
            print("  ✓ %s — %s" % (arxiv, e["title"]))
            for c in changes:
                print("      + " + c)
        else:
            still.append(arxiv)
        for c in conflicts:
            print("      ! %s: %s" % (arxiv, c))

    if touched and not dry_run:
        clpubs.save(pubs, insts)
        gen_publications.main([])
        build_map_data.main()

    print()
    if touched:
        verb = "would update" if dry_run else "updated"
        print("%s %d entr%s:" % (verb.capitalize(), len(touched), "y" if len(touched) == 1 else "ies"))
        for arxiv, e, _c, _x in touched:
            print("  %-11s now missing: %s" % (arxiv, describe(e)))
        if not dry_run:
            print("\nRegenerated Publications.md and researcher-locations.js.")
    if still:
        print("INSPIRE has not caught up yet on %d entr%s: %s"
              % (len(still), "y" if len(still) == 1 else "ies", ", ".join(still)))
    if dry_run and touched:
        print("\n(--dry-run: nothing was written)")

    if failed:
        print("\n%d entr%s need a human:" % (len(failed), "y" if len(failed) == 1 else "ies"),
              file=sys.stderr)
        for arxiv, why in failed:
            print("  ⚠ %s — %s" % (arxiv, why), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
