# 2026 World Cup Bracket Pool — Guide

A friendly bracket pool for the 2026 FIFA World Cup. Print brackets, collect picks from friends, score them as results come in, and share standings on a public web page.

## What's in the box

| What | Where | Purpose |
|------|-------|---------|
| **Bracket generator** | `bracket/` + `generate.py` | Produces a printable 32-team SVG/PDF bracket matching the official FIFA knockout path |
| **Scoring engine** | `score.py` | Scores every entry against actual results and writes standings |
| **Leaderboard site** | `docs/index.html` | Single-page GitHub Pages site showing live standings |
| **Data files** | `data/` | JSON files for entries, results, and scoring config |

## Setup

Requires Python 3.11 and [uv](https://docs.astral.sh/uv/).

```
cd E:\projects\bracket
uv sync
```

That's it. No activation needed — use `uv run` for everything.

## Generate a print bracket

```
uv run generate.py              # SVG only  → output/bracket.svg
uv run generate.py --pdf        # SVG + PDF → output/bracket.pdf
uv run generate.py --open       # SVG + open in browser
```

Tweak colors, fonts, spacing, and sizes in `bracket/config.py` and re-run.

## How the pool works

1. **Print brackets** and hand them out (or share the PDF)
2. Each friend fills in their picks for every round through the champion
3. **You enter their picks** into `data/entries.json` (see format below)
4. As matches are played, **update results** in `data/results.json`
5. Run `uv run score.py` to regenerate standings
6. Push to GitHub — the leaderboard updates automatically

A web form for friends to submit picks online is planned for later.

## Scoring

Points escalate by round:

| Round | Points per correct pick |
|-------|------------------------|
| Round of 32 | 1 |
| Round of 16 | 2 |
| Quarterfinals | 4 |
| Semifinals | 8 |
| Final | 16 |
| Champion bonus | +10 |

**Payout**: 1st place 60%, 2nd place 25%, 3rd place 15% of the pot.

### Changing the scoring

Edit `data/scoring.json`. All scoring values live there:

```json
{
  "points_per_round": {
    "R32": 1,
    "R16": 2,
    "QF": 4,
    "SF": 8,
    "Final": 16
  },
  "champion_bonus": 10,
  "payout": {
    "1st": "60%",
    "2nd": "25%",
    "3rd": "15%"
  }
}
```

Change any value, re-run `uv run score.py`, and push. The leaderboard site reads these values directly so it always reflects the current config.

## Adding a friend's bracket

Edit `data/entries.json` and add an object to the `"entries"` array. Each entry needs:

- **name** — the friend's display name
- **submitted** — date submitted (YYYY-MM-DD)
- **picks** — their winner pick for every match, organized by round
- **champion** — their overall champion pick

Match IDs follow FIFA numbering (M73–M88 for R32, M89–M96 for R16, etc.). See the example entry already in the file.

## Entering results

As matches finish, add the winner to the appropriate round in `data/results.json`:

```json
{
  "last_updated": "2026-06-28",
  "rounds": {
    "R32": {
      "M73": "2A",
      "M74": "1E"
    }
  },
  "champion": ""
}
```

Then run:

```
uv run score.py --verbose      # scores + prints leaderboard to console
git add docs/standings.json data/results.json
git commit -m "Update results"
git push
```

## Bracket slot labels

The bracket uses the official FIFA 2026 knockout path. Slots are labeled by group outcome:

- **1A** = Group A winner
- **2B** = Group B runner-up
- **Blank slots** = third-place qualifiers (unknown until group stage ends)

## GitHub Pages

The leaderboard is live at: **https://pdbartsch.github.io/bracket/**

It's a static page served from `docs/`. Pushing to `main` triggers a rebuild automatically.

## Planned

- Web form for friends to submit brackets online
- Fillable PDF bracket
