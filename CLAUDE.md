# Bracket Project

World Cup 32-team bracket system for a friendly pool among friends.

## Stack
- Python 3.11 via uv
- `svgwrite` for bracket SVG generation
- `cairosvg` for SVG → PDF conversion
- Flask (future) for web form and public results

## Project Goals
1. **Bracket generator** — programmatic SVG/PDF bracket creation with tunable layout
2. **Fillable PDF** — friends pick winners in each round
3. **Web form** — online bracket entry
4. **Scoring engine** — enter results, score all brackets, rank friends
5. **Flask site** — public transparency page showing standings

## Conventions
- Generated files go in `output/`
- Data files (brackets, results) go in `data/`
- Bracket layout config is in `bracket/config.py` so design iteration is fast
