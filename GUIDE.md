# 2026 World Cup Bracket Pool — Guide

A friendly bracket pool for the 2026 FIFA World Cup. Print brackets, collect picks from friends, score them as results come in, and share standings on a public web page.

## What's in the box

| What | Where | Purpose |
|------|-------|---------|
| **Bracket generator** | `bracket/` + `generate.py` | Produces a printable 32-team SVG/PDF bracket matching the official FIFA knockout path |
| **Group stage SVG** | `bracket/draw_groups.py` + `generate_groups.py` | 12-group grid showing all 48 teams |
| **Interactive entry** | `docs/entry.html` | Drag-and-drop bracket filling in the browser |
| **Scoring engine** | `score.py` | Scores every entry against actual results and writes standings |
| **Leaderboard site** | `docs/index.html` | Public standings page |
| **Data files** | `data/` | JSON files for entries, results, and scoring config |
| **Sync script** | `sync_to_parkland.py` | Copies static assets to parkland Flask app |
| **Flask blueprint** | `parklandapp/worldcup/` (in parkland repo) | Serves pages at parkland.dev/worldcup, handles submissions |

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

Friends can also submit brackets online at **parkland.dev/worldcup/entry** (requires a 6-character access code).

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

Brackets submitted online at parkland.dev/worldcup/entry are saved automatically to the Flask server. Each entry gets a unique ID like `Ronaldo-07`.

To add a bracket manually, edit `data/entries.json` and add an object to the `"entries"` array. Each entry needs:

- **id** — unique ID (e.g., `Messi-12`)
- **name** — the friend's real name (private)
- **nickname** — public display name shown on the leaderboard
- **paid** — `true` or `false`
- **submitted** — date submitted (YYYY-MM-DD)
- **picks** — their winner pick for every match, organized by round
- **champion** — their overall champion pick

Match IDs follow FIFA numbering (M73-M88 for R32, M89-M96 for R16, etc.). See the example entry already in the file.

## Admin guide (for your son)

This is the daily routine once the tournament starts.

### After each day's matches

1. Open `data/results.json`
2. Add the winner of each match that was played:

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

The winner is the team name as it appears in everyone's brackets (e.g., `"Mexico"`, `"Brazil"`).

3. Save the file and run:

```
uv run score.py --verbose
```

This prints the leaderboard to the console and writes `docs/standings.json`.

4. Sync and push:

```
uv run sync_to_parkland.py
git add -A
git commit -m "Results for June 28"
git push
```

The public leaderboard updates automatically.

### Marking someone as paid

Open the entries file on the Flask server (`parklandapp/worldcup/data/entries.json` in the parkland repo) and change `"paid": false` to `"paid": true` for the entry.

### Changing the access code

From the bracket project:

```
uv run set_access_code.py NEWCODE
```

The code must be exactly 6 characters. Case-sensitive. Then sync and deploy.

### Match ID reference

| Round | Match IDs |
|-------|-----------|
| Round of 32 | M73 - M88 (16 matches) |
| Round of 16 | M89 - M96 (8 matches) |
| Quarterfinals | M97 - M100 (4 matches) |
| Semifinals | M101 - M102 (2 matches) |
| Final | M103 (1 match) |

### Setting the champion

Once the final is decided, add the winner to `data/results.json`:

```json
{
  "rounds": {
    "Final": { "M103": "Brazil" }
  },
  "champion": "Brazil"
}
```

Then run `uv run score.py` — champion bonus points are applied automatically.

## Bracket slot labels

The bracket uses the official FIFA 2026 knockout path. Slots are labeled by group outcome:

- **1A** = Group A winner
- **2B** = Group B runner-up
- **Blank slots** = third-place qualifiers (unknown until group stage ends)

## Deploying to parkland.dev

Static assets live in `docs/` in this repo (source of truth). To push changes to parkland.dev:

```
uv run sync_to_parkland.py       # copies changed files to parkland app
cd E:\projects\parkland
gcloud app deploy                # deploy to parkland.dev
```

Pages are served at:
- **parkland.dev/worldcup** — public leaderboard
- **parkland.dev/worldcup/entry** — bracket entry (access code required)

## GitHub Pages (backup)

The leaderboard is also available at: **https://pdbartsch.github.io/bracket/**

Served from `docs/`. Pushing to `main` triggers a rebuild automatically.

## Planned

- Admin page for entering results in the browser
- D3.js analysis infographics
- Fillable PDF bracket
