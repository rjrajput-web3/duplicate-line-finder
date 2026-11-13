#!/usr/bin/env python3
"""Find duplicate lines in text files and report how often each repeats.

Usage:
    python dup_lines.py notes.txt
    python dup_lines.py a.txt b.txt --min 3 --sort count
    python dup_lines.py data.log --ignore-case --trim --json
    cat file.txt | python dup_lines.py --stdin

A line counts as a duplicate when it appears at least --min times
(default 2). Exit code 0 when duplicates are found, 1 when none are,
2 on a usage or file error.
"""

import argparse
import json
import sys
from collections import Counter


def normalise(line, ignore_case, trim):
    if trim:
        line = line.strip()
    if ignore_case:
        line = line.lower()
    return line


def collect(paths, use_stdin, ignore_case, trim):
    counts = Counter()
    first_seen = {}
    order = 0
    sources = []
    if use_stdin:
        sources.append(sys.stdin)
    for path in paths:
        try:
            sources.append(open(path, encoding="utf-8", errors="replace"))
        except OSError as exc:
            print(f"dup_lines: cannot open {path}: {exc}", file=sys.stderr)
            return None
    try:
        for source in sources:
            for raw in source:
                line = raw.rstrip("\n")
                key = normalise(line, ignore_case, trim)
                if key not in first_seen:
                    first_seen[key] = (line, order)
                    order += 1
                counts[key] += 1
    finally:
        for source in sources:
            if source is not sys.stdin:
                source.close()
    return counts, first_seen


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Find duplicate lines in text files.")
    parser.add_argument("files", nargs="*", help="text files to scan")
    parser.add_argument("--stdin", action="store_true",
                        help="also read lines from standard input")
    parser.add_argument("--min", type=int, default=2,
                        help="minimum occurrences to report (default: 2)")
    parser.add_argument("--ignore-case", action="store_true",
                        help="treat lines differing only by case as equal")
    parser.add_argument("--trim", action="store_true",
                        help="ignore leading/trailing whitespace")
    parser.add_argument("--sort", choices=["count", "first"],
                        default="count",
                        help="order results by count (default) or first appearance")
    parser.add_argument("--json", action="store_true",
                        help="print results as JSON instead of a table")
    args = parser.parse_args(argv)

    if args.min < 2:
        parser.error("--min must be at least 2")
    if not args.files and not args.stdin:
        parser.error("give at least one file or --stdin")

    collected = collect(args.files, args.stdin,
                        args.ignore_case, args.trim)
    if collected is None:
        return 2
    counts, first_seen = collected

    dups = [(key, counts[key]) for key in counts if counts[key] >= args.min]
    if args.sort == "count":
        dups.sort(key=lambda item: (-item[1], first_seen[item[0]][1]))
    else:
        dups.sort(key=lambda item: first_seen[item[0]][1])

    if args.json:
        print(json.dumps(
            [{"line": first_seen[key][0], "count": n} for key, n in dups],
            indent=2))
    else:
        for key, n in dups:
            print(f"{n:5d}  {first_seen[key][0]}")
        print(f"{len(dups)} duplicate line(s) "
              f"({sum(n for _, n in dups)} occurrences total)")

    return 0 if dups else 1


if __name__ == "__main__":
    sys.exit(main())
