# Advent of Code 2025

My solutions for [Advent of Code 2025](https://adventofcode.com/2025).

## Setup

1. Install the project:
```bash
uv pip install -e .
```

2. Create a `.env` file with your Advent of Code session cookie:
```
AOC_SESSION_COOKIE=YOUR_SESSION_ID
```

To find your session ID:
1. Sign in on [Advent of Code](https://adventofcode.com)
2. Open browser DevTools (Chromium: `Ctrl+Shift+C`)
3. Go to Network tab and reload the page
4. Click the first request
5. In Request Headers, find `Cookie: session=YOUR_SESSION_ID` (exclude the semicolon)

## Running Solutions

Run solutions with:

```bash
aoc-25 run <day>
```

For example:
```bash
aoc-25 run 1
```

## Structure

Each day's solution is organized in its own directory under `src/`:

- `src/day-XX/solution.py` - Solution implementation
- `src/day-XX/input.txt` - Puzzle input
- `src/day-XX/README.md` - Problem description and notes

## Note

Only this README was generated with AI assistance. All solutions are written manually.
