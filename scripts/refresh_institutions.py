#!/usr/bin/env python3
"""Re-ask INSPIRE about institutions with gaps in institutions.yaml, and fill them.

    python3 refresh_institutions.py            # every institution with a null field
    python3 refresh_institutions.py --dry-run  # report only, write no YAML
    python3 refresh_institutions.py 903237     # just these INSPIRE institution ids

The sibling of refresh_citations.py, one level down: that one chases papers, this
one chases the institutions they point at. Two reasons a row here has holes.

First, a long-standing bug (fixed in clpubs.institution_name): INSPIRE marks a
superseded record with the literal ICN 'obsolete' and keeps the real name in
legacy_ICN, but the old expression stopped at the truthy sentinel and never
consulted the fallback, so a third of the table was stored with name: null. The
map skips nameless institutions when it builds each city's popup list, which is
why cities like Lausanne and Oxford listed no institution at all. The fix only
affects institutions fetched from now on — ensure_institution() returns early for
ids already in the YAML — so this script exists to repair the rows already there.

Second, INSPIRE genuinely improves records over time: coordinates in particular
get added to institutions that had none, and those are worth picking up (an
institution without coordinates is placed at its city centre on the map).

Merge policy is the same as the citation refresher's — a hand edit always wins.
Only fields that are currently null are ever filled; anything you have already set
is kept even when INSPIRE now disagrees, and the disagreement is reported rather
than applied. The 'note' fields marking hand-added coordinates are preserved.

Nothing is written when nothing changed. Exit status is 0 whenever the run worked;
1 only if INSPIRE could not be reached.
"""
import sys
import urllib.error

import clpubs
import build_map_data

FIELDS = ("name", "city", "country", "lat", "lon")


def gaps(record):
    """Which of the fields we care about are still null on this row."""
    return [f for f in FIELDS if record.get(f) is None]


def merge(record, fresh):
    """Fill null fields on `record` from `fresh`. Mutates. Returns (changes[], conflicts[])."""
    changes, conflicts = [], []
    for f in FIELDS:
        old, new = record.get(f), fresh.get(f)
        if new is None:
            continue
        if old is None:
            record[f] = new
            changes.append("%s -> %r" % (f, new))
        elif old != new:
            conflicts.append("%s is %r here, %r on INSPIRE — kept ours" % (f, old, new))
    return changes, conflicts


def main(argv):
    dry_run = "--dry-run" in argv
    wanted = [a for a in argv if not a.startswith("-")]
    for flag in argv:
        if flag.startswith("-") and flag != "--dry-run":
            print("usage: python3 refresh_institutions.py [--dry-run] [<inspire-id> ...]",
                  file=sys.stderr)
            return 2

    pubs, insts = clpubs.load()
    insts = {int(k): v for k, v in insts.items()}

    if wanted:
        try:
            ids = [int(a) for a in wanted]
        except ValueError:
            print("  ⚠ institution ids must be integers: %s" % ", ".join(wanted), file=sys.stderr)
            return 2
        unknown = [i for i in ids if i not in insts]
        if unknown:
            print("  ⚠ not in institutions.yaml: %s" % ", ".join(map(str, unknown)), file=sys.stderr)
            return 2
        todo = ids
    else:
        todo = sorted(i for i, rec in insts.items() if gaps(rec))

    if not todo:
        print("• nothing to fill — all %d institutions are complete." % len(insts))
        return 0

    print("• re-asking INSPIRE about %d of %d institutions" % (len(todo), len(insts)))
    print("  (gaps: %s)\n" % ", ".join(
        "%s×%d" % (f, sum(1 for i in todo if insts[i].get(f) is None)) for f in FIELDS
        if any(insts[i].get(f) is None for i in todo)))

    filled, quiet, failed = [], [], []
    for iid in todo:
        clpubs.forget_institution(iid)
        try:
            md = clpubs.fetch_institution(iid)
        except (urllib.error.URLError, OSError) as exc:
            failed.append((iid, "could not reach INSPIRE: %s" % exc))
            continue
        if not md:
            failed.append((iid, "no INSPIRE record for this institution id"))
            continue

        rec = insts[iid]
        changes, conflicts = merge(rec, clpubs.normalize_institution(md))
        if changes:
            filled.append((iid, rec, changes))
            print("  ✓ %-8d %s" % (iid, rec.get("name") or "(still unnamed)"))
            for c in changes:
                print("      + " + c)
        else:
            quiet.append(iid)
        for c in conflicts:
            print("      ! %d: %s" % (iid, c))

    if filled and not dry_run:
        clpubs.save(pubs, insts)
        build_map_data.main()

    print()
    if filled:
        named = sum(1 for _i, _r, ch in filled if any(c.startswith("name ->") for c in ch))
        coord = sum(1 for _i, _r, ch in filled if any(c.startswith("lat ->") for c in ch))
        verb = "Would fill" if dry_run else "Filled"
        print("%s %d institution(s): %d gained a name, %d gained coordinates."
              % (verb, len(filled), named, coord))
        if not dry_run:
            print("Regenerated researcher-locations.js.")
    if quiet:
        print("INSPIRE has nothing to add for %d institution(s): %s"
              % (len(quiet), ", ".join(map(str, quiet))))
    if dry_run and filled:
        print("\n(--dry-run: nothing was written)")

    if failed:
        print("\n%d institution(s) need a human:" % len(failed), file=sys.stderr)
        for iid, why in failed:
            print("  ⚠ %d — %s" % (iid, why), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
