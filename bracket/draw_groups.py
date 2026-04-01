"""Generate a group stage SVG showing all 12 groups in a grid."""

from __future__ import annotations

import svgwrite

from bracket.groups import GROUPS


# --- Layout config ---
PAGE_WIDTH = 1200
PAGE_HEIGHT = 900
MARGIN_TOP = 60
MARGIN_LEFT = 30
MARGIN_RIGHT = 30

COLS = 4                     # 4 groups per row
ROWS = 3                     # 3 rows = 12 groups

GROUP_PADDING = 12           # internal padding
TEAM_ROW_HEIGHT = 28
HEADER_HEIGHT = 32

FONT_FAMILY = "Arial, Helvetica, sans-serif"
BACKGROUND = "#f9f9f9"

# Colors
HEADER_FILL = "#1a5f2a"
HEADER_TEXT = "#ffffff"
ROW_FILL_EVEN = "#ffffff"
ROW_FILL_ODD = "#f4f4f0"
BORDER_COLOR = "#cccccc"
TEXT_COLOR = "#222222"
RANK_COLOR = "#999999"

TITLE_TEXT = "2026 FIFA World Cup — Group Stage"
TITLE_FONT_SIZE = 22
TITLE_COLOR = "#111111"

# Result columns
COL_HEADERS = ["", "Team", "W", "D", "L", "GF", "GA", "GD", "Pts"]
COL_WIDTHS = [24, 120, 28, 28, 28, 28, 28, 28, 32]  # relative widths


def draw_groups(filename: str = "groups.svg") -> str:
    """Render all 12 groups to an SVG file."""
    col_total = sum(COL_WIDTHS)

    # Calculate group box dimensions
    avail_w = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    avail_h = PAGE_HEIGHT - MARGIN_TOP - 20
    gap_x = 20
    gap_y = 20

    group_w = (avail_w - (COLS - 1) * gap_x) / COLS
    group_h = HEADER_HEIGHT + 4 * TEAM_ROW_HEIGHT + GROUP_PADDING

    # Scale col widths to fit group_w
    scale = (group_w - GROUP_PADDING * 2) / col_total

    page_h = max(PAGE_HEIGHT, MARGIN_TOP + 20 + ROWS * (group_h + gap_y))

    dwg = svgwrite.Drawing(filename, size=(PAGE_WIDTH, page_h))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(PAGE_WIDTH, page_h), fill=BACKGROUND))

    # Title
    dwg.add(dwg.text(
        TITLE_TEXT,
        insert=(PAGE_WIDTH / 2, 38),
        text_anchor="middle",
        font_size=TITLE_FONT_SIZE,
        font_family=FONT_FAMILY,
        fill=TITLE_COLOR,
        font_weight="bold",
    ))

    group_keys = list(GROUPS.keys())

    for idx, key in enumerate(group_keys):
        teams = GROUPS[key]
        row = idx // COLS
        col = idx % COLS

        gx = MARGIN_LEFT + col * (group_w + gap_x)
        gy = MARGIN_TOP + row * (group_h + gap_y)

        _draw_group_table(dwg, gx, gy, group_w, key, teams, scale)

    dwg.save()
    return filename


def _draw_group_table(
    dwg: svgwrite.Drawing,
    x: float, y: float, width: float,
    group_letter: str,
    teams: list[str],
    scale: float,
):
    """Draw one group table."""
    # Outer border
    table_h = HEADER_HEIGHT + 4 * TEAM_ROW_HEIGHT
    dwg.add(dwg.rect(
        insert=(x, y),
        size=(width, table_h),
        fill="none",
        stroke=BORDER_COLOR,
        stroke_width=1,
        rx=4, ry=4,
    ))

    # Header row
    dwg.add(dwg.rect(
        insert=(x, y),
        size=(width, HEADER_HEIGHT),
        fill=HEADER_FILL,
        rx=4, ry=4,
    ))
    # Square off the bottom corners of the header
    dwg.add(dwg.rect(
        insert=(x, y + HEADER_HEIGHT - 4),
        size=(width, 4),
        fill=HEADER_FILL,
    ))

    dwg.add(dwg.text(
        f"Group {group_letter}",
        insert=(x + 10, y + HEADER_HEIGHT / 2 + 5),
        font_size=13,
        font_family=FONT_FAMILY,
        fill=HEADER_TEXT,
        font_weight="bold",
    ))

    # Column headers (right side of header)
    cx = x + GROUP_PADDING + (COL_WIDTHS[0] + COL_WIDTHS[1]) * scale
    for i in range(2, len(COL_HEADERS)):
        cw = COL_WIDTHS[i] * scale
        dwg.add(dwg.text(
            COL_HEADERS[i],
            insert=(cx + cw / 2, y + HEADER_HEIGHT / 2 + 4),
            text_anchor="middle",
            font_size=9,
            font_family=FONT_FAMILY,
            fill=HEADER_TEXT,
            font_weight="bold",
        ))
        cx += cw

    # Team rows
    for t_idx, team in enumerate(teams):
        ry = y + HEADER_HEIGHT + t_idx * TEAM_ROW_HEIGHT
        fill = ROW_FILL_EVEN if t_idx % 2 == 0 else ROW_FILL_ODD

        # Row background
        if t_idx == 3:
            dwg.add(dwg.rect(
                insert=(x + 1, ry), size=(width - 2, TEAM_ROW_HEIGHT),
                fill=fill, rx=0, ry=0,
            ))
        else:
            dwg.add(dwg.rect(
                insert=(x + 1, ry), size=(width - 2, TEAM_ROW_HEIGHT),
                fill=fill,
            ))

        # Rank number
        dwg.add(dwg.text(
            str(t_idx + 1),
            insert=(x + GROUP_PADDING + 8, ry + TEAM_ROW_HEIGHT / 2 + 4),
            text_anchor="middle",
            font_size=10,
            font_family=FONT_FAMILY,
            fill=RANK_COLOR,
        ))

        # Team name
        dwg.add(dwg.text(
            team,
            insert=(x + GROUP_PADDING + COL_WIDTHS[0] * scale + 4, ry + TEAM_ROW_HEIGHT / 2 + 4),
            font_size=11,
            font_family=FONT_FAMILY,
            fill=TEXT_COLOR,
        ))

        # Stat cells (empty — to be filled in)
        cx = x + GROUP_PADDING + (COL_WIDTHS[0] + COL_WIDTHS[1]) * scale
        for i in range(2, len(COL_HEADERS)):
            cw = COL_WIDTHS[i] * scale
            # Subtle cell divider
            dwg.add(dwg.line(
                start=(cx, ry + 4), end=(cx, ry + TEAM_ROW_HEIGHT - 4),
                stroke="#e0e0e0", stroke_width=0.5,
            ))
            cx += cw

        # Horizontal divider between rows
        if t_idx < 3:
            dwg.add(dwg.line(
                start=(x + 4, ry + TEAM_ROW_HEIGHT),
                end=(x + width - 4, ry + TEAM_ROW_HEIGHT),
                stroke="#e8e8e8", stroke_width=0.5,
            ))

        # Qualifier indicator: top 2 get a subtle green left border
        # (visual hint that top 2 advance automatically)
        if t_idx < 2:
            dwg.add(dwg.line(
                start=(x + 1, ry + 2), end=(x + 1, ry + TEAM_ROW_HEIGHT - 2),
                stroke="#2d8f4e", stroke_width=3,
            ))
