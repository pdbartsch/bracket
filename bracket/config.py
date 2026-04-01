"""Bracket layout configuration — tweak these values to iterate on the design."""

# --- Page ---
PAGE_WIDTH = 1400
PAGE_HEIGHT = 900
MARGIN_TOP = 60
MARGIN_LEFT = 40
MARGIN_RIGHT = 40

# --- Slots (team name boxes) ---
SLOT_WIDTH = 150
SLOT_HEIGHT = 28
SLOT_GAP = 4          # vertical gap between two teams in a matchup
SLOT_FONT_SIZE = 11
SLOT_FONT_FAMILY = "Arial, Helvetica, sans-serif"
SLOT_FILL = "#ffffff"
SLOT_STROKE = "#333333"
SLOT_STROKE_WIDTH = 1
SLOT_TEXT_COLOR = "#111111"
SLOT_SEED_COLOR = "#888888"

# --- Connector lines ---
LINE_COLOR = "#333333"
LINE_WIDTH = 1.2

# --- Round spacing ---
ROUND_GAP = 40        # horizontal gap between round columns

# --- Title ---
TITLE_TEXT = "2026 FIFA World Cup Bracket"
TITLE_FONT_SIZE = 22
TITLE_FONT_FAMILY = "Arial, Helvetica, sans-serif"
TITLE_COLOR = "#111111"

# --- Colors / theming ---
BACKGROUND = "#f9f9f9"
CHAMPION_FILL = "#fff8dc"
CHAMPION_STROKE = "#d4a937"

# --- Round labels ---
ROUND_LABELS = [
    "Round of 32",
    "Round of 16",
    "Quarterfinals",
    "Semifinals",
    "Final",
]
ROUND_LABEL_FONT_SIZE = 13
ROUND_LABEL_COLOR = "#555555"
