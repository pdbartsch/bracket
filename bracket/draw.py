"""Generate a 32-team symmetrical single-elimination bracket as SVG.

Left 16 teams flow right, right 16 teams flow left, final in the center.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import svgwrite

from bracket import config as C


@dataclass
class Team:
    name: str = ""


@dataclass
class Match:
    """A single match -- two slots, one winner advances."""
    round: int = 0
    position: int = 0
    team_top: Team = field(default_factory=Team)
    team_bot: Team = field(default_factory=Team)
    winner: Team | None = None


def default_teams(n: int = 32) -> list[Team]:
    """Return placeholder teams seeded 1..n."""
    return [Team(seed=i + 1, name=f"Team {i + 1}") for i in range(n)]


def build_half_bracket(teams: list[Team]) -> list[list[Match]]:
    """Build round-by-round match structure for one half (16 teams -> 4 rounds)."""
    n = len(teams)
    num_rounds = int(math.log2(n))
    rounds: list[list[Match]] = []

    # Round 0: seed matchups
    r0 = []
    for i in range(0, n, 2):
        r0.append(Match(round=0, position=i // 2, team_top=teams[i], team_bot=teams[i + 1]))
    rounds.append(r0)

    # Subsequent rounds: empty slots
    for r in range(1, num_rounds):
        num_matches = n // (2 ** (r + 1))
        rounds.append([Match(round=r, position=p) for p in range(num_matches)])

    return rounds


def _slot_label(team: Team) -> str:
    return team.name


def draw_bracket(
    teams: list[Team],
    filename: str = "bracket.svg",
) -> str:
    """Render a symmetrical 32-team bracket to SVG."""
    n = len(teams)
    half = n // 2

    left_teams = teams[:half]
    right_teams = teams[half:]

    left_rounds = build_half_bracket(left_teams)
    right_rounds = build_half_bracket(right_teams)

    num_half_rounds = len(left_rounds)  # 4 for 16 teams
    col_width = C.SLOT_WIDTH + C.ROUND_GAP

    # Vertical layout driven by round-0 (8 matches per side)
    r0_count = len(left_rounds[0])
    matchup_height = C.SLOT_HEIGHT * 2 + C.SLOT_GAP
    vert_pitch_r0 = max(
        matchup_height + 8,
        (C.PAGE_HEIGHT - C.MARGIN_TOP - 40) / r0_count,
    )

    page_h = max(C.PAGE_HEIGHT, C.MARGIN_TOP + 40 + r0_count * vert_pitch_r0)
    # Left columns + center champion + right columns (mirrored)
    content_w = num_half_rounds * col_width * 2 + C.SLOT_WIDTH + C.ROUND_GAP * 2
    page_w = max(C.PAGE_WIDTH, C.MARGIN_LEFT + C.MARGIN_RIGHT + content_w)

    center_x = page_w / 2

    dwg = svgwrite.Drawing(filename, size=(page_w, page_h))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(page_w, page_h), fill=C.BACKGROUND))

    # Title
    dwg.add(dwg.text(
        C.TITLE_TEXT,
        insert=(center_x, 35),
        text_anchor="middle",
        font_size=C.TITLE_FONT_SIZE,
        font_family=C.TITLE_FONT_FAMILY,
        fill=C.TITLE_COLOR,
        font_weight="bold",
    ))

    # --- Compute positions for each half ---

    def compute_positions(num_rounds: int, r0_matches: int, base_x: float, direction: int):
        """Compute (x, y_center) for each matchup.
        direction: +1 for left side (slots flow right), -1 for right side (slots flow left).
        """
        positions: list[list[tuple[float, float]]] = []
        for r in range(num_rounds):
            if direction == 1:
                col_x = base_x + r * col_width
            else:
                col_x = base_x - r * col_width - C.SLOT_WIDTH

            match_count = r0_matches // (2 ** r)
            vert_pitch = vert_pitch_r0 * (2 ** r)
            total_h = (match_count - 1) * vert_pitch
            start_y = C.MARGIN_TOP + 30 + (page_h - C.MARGIN_TOP - 40 - total_h) / 2

            round_positions = []
            for m in range(match_count):
                y_center = start_y + m * vert_pitch
                round_positions.append((col_x, y_center))
            positions.append(round_positions)
        return positions

    left_base_x = C.MARGIN_LEFT
    right_base_x = page_w - C.MARGIN_RIGHT

    left_pos = compute_positions(num_half_rounds, r0_count, left_base_x, +1)
    right_pos = compute_positions(num_half_rounds, r0_count, right_base_x, -1)

    # --- Draw round labels (mirrored) ---
    for r in range(num_half_rounds):
        label = C.ROUND_LABELS[r] if r < len(C.ROUND_LABELS) else f"Round {r + 1}"

        # Left label
        lx = left_pos[r][0][0] + C.SLOT_WIDTH / 2
        dwg.add(dwg.text(
            label, insert=(lx, C.MARGIN_TOP + 15), text_anchor="middle",
            font_size=C.ROUND_LABEL_FONT_SIZE, font_family=C.SLOT_FONT_FAMILY,
            fill=C.ROUND_LABEL_COLOR, font_weight="bold",
        ))

        # Right label
        rx = right_pos[r][0][0] + C.SLOT_WIDTH / 2
        dwg.add(dwg.text(
            label, insert=(rx, C.MARGIN_TOP + 15), text_anchor="middle",
            font_size=C.ROUND_LABEL_FONT_SIZE, font_family=C.SLOT_FONT_FAMILY,
            fill=C.ROUND_LABEL_COLOR, font_weight="bold",
        ))

    # Final label in center
    final_label = C.ROUND_LABELS[num_half_rounds] if num_half_rounds < len(C.ROUND_LABELS) else "Final"
    dwg.add(dwg.text(
        final_label, insert=(center_x, C.MARGIN_TOP + 15), text_anchor="middle",
        font_size=C.ROUND_LABEL_FONT_SIZE, font_family=C.SLOT_FONT_FAMILY,
        fill=C.ROUND_LABEL_COLOR, font_weight="bold",
    ))

    # --- Draw one side ---
    def _draw_matchup_connector(x, yc, direction):
        """Draw the internal connector for a single matchup (stubs + vertical).
        Returns (mid_x, merge_y) -- the point where the winner line exits.
        """
        y_top = yc - C.SLOT_GAP / 2 - C.SLOT_HEIGHT
        y_bot = yc + C.SLOT_GAP / 2

        if direction == 1:
            stub_x = x + C.SLOT_WIDTH
            mid_x = stub_x + C.ROUND_GAP / 2
        else:
            stub_x = x
            mid_x = stub_x - C.ROUND_GAP / 2

        top_mid_y = y_top + C.SLOT_HEIGHT / 2
        bot_mid_y = y_bot + C.SLOT_HEIGHT / 2

        # Horizontal stubs from each slot
        dwg.add(dwg.line(
            start=(stub_x, top_mid_y), end=(mid_x, top_mid_y),
            stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
        ))
        dwg.add(dwg.line(
            start=(stub_x, bot_mid_y), end=(mid_x, bot_mid_y),
            stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
        ))

        # Vertical connector between the two stubs
        dwg.add(dwg.line(
            start=(mid_x, top_mid_y), end=(mid_x, bot_mid_y),
            stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
        ))

        merge_y = (top_mid_y + bot_mid_y) / 2
        return mid_x, merge_y

    def draw_half(rounds, positions, direction):
        """direction: +1 = connectors go right, -1 = connectors go left."""
        num_r = len(rounds)
        for r, round_matches in enumerate(rounds):
            for m, match in enumerate(round_matches):
                x, yc = positions[r][m]

                y_top = yc - C.SLOT_GAP / 2 - C.SLOT_HEIGHT
                y_bot = yc + C.SLOT_GAP / 2

                _draw_slot(dwg, x, y_top, match.team_top)
                _draw_slot(dwg, x, y_bot, match.team_bot)

            # Draw connectors for this round
            if r < num_r - 1:
                # Process in pairs -- each pair of matchups feeds one next-round slot
                for p in range(0, len(round_matches), 2):
                    x0, yc0 = positions[r][p]
                    x1, yc1 = positions[r][p + 1]

                    # Internal connectors for each matchup
                    mid_x0, merge_y0 = _draw_matchup_connector(x0, yc0, direction)
                    mid_x1, merge_y1 = _draw_matchup_connector(x1, yc1, direction)

                    # Next round slot position
                    next_m = p // 2
                    next_x, next_yc = positions[r + 1][next_m]

                    if direction == 1:
                        join_x = next_x
                    else:
                        join_x = next_x + C.SLOT_WIDTH

                    # Horizontal lines from each matchup midpoint to join_x
                    dwg.add(dwg.line(
                        start=(mid_x0, merge_y0), end=(join_x, merge_y0),
                        stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
                    ))
                    dwg.add(dwg.line(
                        start=(mid_x1, merge_y1), end=(join_x, merge_y1),
                        stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
                    ))

                    # Vertical line connecting the pair at the next round's edge
                    dwg.add(dwg.line(
                        start=(join_x, merge_y0), end=(join_x, merge_y1),
                        stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
                    ))

        # Last round: draw internal connector but don't draw line to center yet.
        # Return the merge_y so we can position finalist slots on it.
        semi_merge_y = None
        if num_r > 0:
            last_x, last_yc = positions[-1][0]
            mid_x, merge_y = _draw_matchup_connector(last_x, last_yc, direction)
            semi_merge_y = merge_y
            semi_exit_x = mid_x
        return semi_merge_y, semi_exit_x

    left_merge_y, left_exit_x = draw_half(left_rounds, left_pos, +1)
    right_merge_y, right_exit_x = draw_half(right_rounds, right_pos, -1)

    # --- Finalist slots centered on the semi connector lines ---
    final_x = center_x - C.SLOT_WIDTH / 2

    # Left finalist: centered vertically on the left semi merge line
    left_final_y = left_merge_y - C.SLOT_HEIGHT / 2
    _draw_slot(dwg, final_x, left_final_y, Team())

    # Right finalist: centered vertically on the right semi merge line
    right_final_y = right_merge_y - C.SLOT_HEIGHT / 2
    _draw_slot(dwg, final_x, right_final_y, Team())

    # Connector lines from semi exits to finalist slots
    dwg.add(dwg.line(
        start=(left_exit_x, left_merge_y), end=(final_x, left_merge_y),
        stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
    ))
    dwg.add(dwg.line(
        start=(right_exit_x, right_merge_y),
        end=(final_x + C.SLOT_WIDTH, right_merge_y),
        stroke=C.LINE_COLOR, stroke_width=C.LINE_WIDTH,
    ))

    # --- Champion box between the two finalist slots ---
    champ_w = C.SLOT_WIDTH + 40
    champ_h = 110
    champ_x = center_x - champ_w / 2
    champ_y = (left_merge_y + right_merge_y) / 2 - champ_h / 2
    pad = 12

    # Crown above the champion box
    crown_color = "#e8d49a"
    crown_dash = "5,4"
    crown_sw = 1.5

    # Crown dimensions
    crown_h = 110       # total height of crown above the box
    crown_base_y = champ_y  # bottom of crown = top of box
    crown_top_y = crown_base_y - crown_h
    crown_left = champ_x + 10
    crown_right = champ_x + champ_w - 10
    crown_w = crown_right - crown_left

    # 5 points across the top: left, left-center, center, right-center, right
    # Zigzag: base-left -> peak1 -> valley1 -> peak2 -> valley2 -> peak3 -> base-right
    p_bl = (crown_left, crown_base_y)
    p_br = (crown_right, crown_base_y)

    peak1_x = crown_left + crown_w * 0.1
    valley1_x = crown_left + crown_w * 0.28
    peak2_x = crown_left + crown_w * 0.5
    valley2_x = crown_left + crown_w * 0.72
    peak3_x = crown_left + crown_w * 0.9

    peak_y = crown_top_y + 8
    valley_y = crown_base_y - 15

    # Main crown outline as a path
    crown_path = dwg.path(
        d=(
            f"M {p_bl[0]},{p_bl[1]} "
            f"L {peak1_x},{peak_y} "
            f"L {valley1_x},{valley_y} "
            f"L {peak2_x},{peak_y} "
            f"L {valley2_x},{valley_y} "
            f"L {peak3_x},{peak_y} "
            f"L {p_br[0]},{p_br[1]}"
        ),
        fill="none",
        stroke=crown_color,
        stroke_width=crown_sw,
        stroke_dasharray=crown_dash,
        stroke_linejoin="round",
    )
    dwg.add(crown_path)

    # Small diamonds/jewels at the three peaks
    jewel_size = 12
    for px in (peak1_x, peak2_x, peak3_x):
        jewel = dwg.polygon(
            points=[
                (px, peak_y - jewel_size),
                (px + jewel_size, peak_y),
                (px, peak_y + jewel_size),
                (px - jewel_size, peak_y),
            ],
            fill=crown_color,
            stroke=crown_color,
            stroke_width=crown_sw,
        )
        dwg.add(jewel)

    # Outer champion box
    dwg.add(dwg.rect(
        insert=(champ_x, champ_y),
        size=(champ_w, champ_h),
        fill=C.CHAMPION_FILL,
        stroke=C.CHAMPION_STROKE,
        stroke_width=2,
        rx=6, ry=6,
    ))

    # "CHAMPION" title
    dwg.add(dwg.text(
        "CHAMPION",
        insert=(center_x, champ_y + 18),
        text_anchor="middle",
        font_size=C.SLOT_FONT_SIZE + 2,
        font_family=C.SLOT_FONT_FAMILY,
        fill="#666",
        font_weight="bold",
    ))

    # Two write-in lines for the finalist teams
    line1_y = champ_y + 38
    line2_y = champ_y + 58
    for ly in (line1_y, line2_y):
        dwg.add(dwg.line(
            start=(champ_x + pad, ly),
            end=(champ_x + champ_w - pad, ly),
            stroke="#aaa", stroke_width=0.8,
        ))

    # Thick dotted box for the user's champion pick
    pick_y = champ_y + 68
    pick_h = 30
    dwg.add(dwg.rect(
        insert=(champ_x + pad, pick_y),
        size=(champ_w - pad * 2, pick_h),
        fill="none",
        stroke=C.CHAMPION_STROKE,
        stroke_width=2.5,
        stroke_dasharray="6,4",
        rx=4, ry=4,
    ))

    dwg.save()
    return filename


def _draw_slot(dwg: svgwrite.Drawing, x: float, y: float, team: Team, is_final: bool = False):
    """Draw a single team slot (rectangle + text)."""
    fill = C.SLOT_FILL
    stroke = C.SLOT_STROKE

    dwg.add(dwg.rect(
        insert=(x, y),
        size=(C.SLOT_WIDTH, C.SLOT_HEIGHT),
        fill=fill,
        stroke=stroke,
        stroke_width=C.SLOT_STROKE_WIDTH,
        rx=2, ry=2,
    ))

    label = _slot_label(team)
    if label:
        dwg.add(dwg.text(
            label,
            insert=(x + 6, y + C.SLOT_HEIGHT / 2 + 4),
            font_size=C.SLOT_FONT_SIZE,
            font_family=C.SLOT_FONT_FAMILY,
            fill=C.SLOT_TEXT_COLOR,
        ))
