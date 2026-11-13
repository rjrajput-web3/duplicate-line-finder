# duplicate-line-finder

Find duplicate lines in text files and report how often each one repeats.
Stdlib-only Python — no dependencies, no install step.

## What it does

Scans one or more text files (or standard input) and lists every line that
appears at least `--min` times (default 2), with its count. Useful for
spotting repeated entries in logs, lists, CSV exports, and notes.

## How to run

```bash
python dup_lines.py notes.txt
python dup_lines.py a.txt b.txt --min 3 --sort count
python dup_lines.py data.log --ignore-case --trim --json
cat file.txt | python dup_lines.py --stdin
```

## Options

| Flag | What it does |
| --- | --- |
| `--min N` | Minimum occurrences to report (default: 2, minimum: 2) |
| `--ignore-case` | Treat lines differing only by case as the same line |
| `--trim` | Ignore leading/trailing whitespace when comparing |
| `--sort count` | Order by count, highest first (default) |
| `--sort first` | Order by first appearance in the input |
| `--json` | Print results as JSON instead of a table |
| `--stdin` | Also read lines from standard input |

## Example output

Input file:

```text
apple
banana
apple
Cherry
banana
apple
```

```bash
$ python dup_lines.py fruit.txt
    3  apple
    2  banana
2 duplicate line(s) (5 occurrences total)
```

```bash
$ python dup_lines.py fruit.txt --json
[
  {
    "line": "apple",
    "count": 3
  },
  {
    "line": "banana",
    "count": 2
  }
]
```

```bash
$ python dup_lines.py fruit.txt --min 3
    3  apple
1 duplicate line(s) (3 occurrences total)
```

## Exit codes

- `0` — duplicates found
- `1` — no duplicates found
- `2` — usage error or unreadable file

## Requirements

Python 3.8 or newer. No third-party packages.
