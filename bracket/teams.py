"""Team data for the 2026 FIFA World Cup knockout stage.

Labels match the official FIFA bracket path (matches 73-88).
Group winners = "1X", runners-up = "2X", third-place qualifiers = blank (write-in).
"""

from bracket.draw import Team

# Left half: Semifinal 101 path
# Right half: Semifinal 102 path
# Order: top-to-bottom within each half

WORLD_CUP_TEAMS = [
    # --- LEFT HALF (16 teams) ---
    # M74: 1E vs 3rd
    Team(name="1E"),
    Team(),             # 3rd place (A/B/C/D/F)
    # M77: 1I vs 3rd
    Team(name="1I"),
    Team(),             # 3rd place (C/D/F/G/H)
    # M73: 2A vs 2B
    Team(name="2A"),
    Team(name="2B"),
    # M75: 1F vs 2C
    Team(name="1F"),
    Team(name="2C"),
    # M83: 2K vs 2L
    Team(name="2K"),
    Team(name="2L"),
    # M84: 1H vs 2J
    Team(name="1H"),
    Team(name="2J"),
    # M81: 1D vs 3rd
    Team(name="1D"),
    Team(),             # 3rd place (B/E/F/I/J)
    # M82: 1G vs 3rd
    Team(name="1G"),
    Team(),             # 3rd place (A/E/H/I/J)

    # --- RIGHT HALF (16 teams) ---
    # M76: 1C vs 2F
    Team(name="1C"),
    Team(name="2F"),
    # M78: 2E vs 2I
    Team(name="2E"),
    Team(name="2I"),
    # M79: 1A vs 3rd
    Team(name="1A"),
    Team(),             # 3rd place (C/E/F/H/I)
    # M80: 1L vs 3rd
    Team(name="1L"),
    Team(),             # 3rd place (E/H/I/J/K)
    # M86: 1J vs 2H
    Team(name="1J"),
    Team(name="2H"),
    # M88: 2D vs 2G
    Team(name="2D"),
    Team(name="2G"),
    # M85: 1B vs 3rd
    Team(name="1B"),
    Team(),             # 3rd place (E/F/G/I/J)
    # M87: 1K vs 3rd
    Team(name="1K"),
    Team(),             # 3rd place (D/E/I/J/L)
]
