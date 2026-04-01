"""Export bracket structure and group data to JSON for the interactive web app.

Usage:
    uv run export_data.py           # writes to docs/data/
"""

import json
import os

from bracket.groups import GROUPS


# --- Match topology: the FIFA 2026 knockout bracket path ---
# R32 matches (M73-M88), each with top/bottom slot labels and which R16 they feed
MATCHES = {
    # LEFT HALF — Semifinal 101 path
    "M74": {"round": "R32", "top": "1E",  "bot": "",   "feeds": "M89", "side": "left"},
    "M77": {"round": "R32", "top": "1I",  "bot": "",   "feeds": "M89", "side": "left"},
    "M73": {"round": "R32", "top": "2A",  "bot": "2B", "feeds": "M90", "side": "left"},
    "M75": {"round": "R32", "top": "1F",  "bot": "2C", "feeds": "M90", "side": "left"},
    "M83": {"round": "R32", "top": "2K",  "bot": "2L", "feeds": "M93", "side": "left"},
    "M84": {"round": "R32", "top": "1H",  "bot": "2J", "feeds": "M93", "side": "left"},
    "M81": {"round": "R32", "top": "1D",  "bot": "",   "feeds": "M94", "side": "left"},
    "M82": {"round": "R32", "top": "1G",  "bot": "",   "feeds": "M94", "side": "left"},
    # RIGHT HALF — Semifinal 102 path
    "M76": {"round": "R32", "top": "1C",  "bot": "2F", "feeds": "M91", "side": "right"},
    "M78": {"round": "R32", "top": "2E",  "bot": "2I", "feeds": "M91", "side": "right"},
    "M79": {"round": "R32", "top": "1A",  "bot": "",   "feeds": "M92", "side": "right"},
    "M80": {"round": "R32", "top": "1L",  "bot": "",   "feeds": "M92", "side": "right"},
    "M86": {"round": "R32", "top": "1J",  "bot": "2H", "feeds": "M95", "side": "right"},
    "M88": {"round": "R32", "top": "2D",  "bot": "2G", "feeds": "M95", "side": "right"},
    "M85": {"round": "R32", "top": "1B",  "bot": "",   "feeds": "M96", "side": "right"},
    "M87": {"round": "R32", "top": "1K",  "bot": "",   "feeds": "M96", "side": "right"},
    # R16
    "M89": {"round": "R16", "top": "",  "bot": "",  "feeds": "M97",  "side": "left",  "from": ["M74", "M77"]},
    "M90": {"round": "R16", "top": "",  "bot": "",  "feeds": "M97",  "side": "left",  "from": ["M73", "M75"]},
    "M93": {"round": "R16", "top": "",  "bot": "",  "feeds": "M98",  "side": "left",  "from": ["M83", "M84"]},
    "M94": {"round": "R16", "top": "",  "bot": "",  "feeds": "M98",  "side": "left",  "from": ["M81", "M82"]},
    "M91": {"round": "R16", "top": "",  "bot": "",  "feeds": "M99",  "side": "right", "from": ["M76", "M78"]},
    "M92": {"round": "R16", "top": "",  "bot": "",  "feeds": "M99",  "side": "right", "from": ["M79", "M80"]},
    "M95": {"round": "R16", "top": "",  "bot": "",  "feeds": "M100", "side": "right", "from": ["M86", "M88"]},
    "M96": {"round": "R16", "top": "",  "bot": "",  "feeds": "M100", "side": "right", "from": ["M85", "M87"]},
    # QF
    "M97":  {"round": "QF",  "top": "", "bot": "", "feeds": "M101", "side": "left",  "from": ["M89", "M90"]},
    "M98":  {"round": "QF",  "top": "", "bot": "", "feeds": "M101", "side": "left",  "from": ["M93", "M94"]},
    "M99":  {"round": "QF",  "top": "", "bot": "", "feeds": "M102", "side": "right", "from": ["M91", "M92"]},
    "M100": {"round": "QF",  "top": "", "bot": "", "feeds": "M102", "side": "right", "from": ["M95", "M96"]},
    # SF
    "M101": {"round": "SF",    "top": "", "bot": "", "feeds": "M103", "side": "left",  "from": ["M97", "M98"]},
    "M102": {"round": "SF",    "top": "", "bot": "", "feeds": "M103", "side": "right", "from": ["M99", "M100"]},
    # Final
    "M103": {"round": "Final", "top": "", "bot": "", "feeds": None,   "side": "center", "from": ["M101", "M102"]},
}

ROUND_ORDER = ["R32", "R16", "QF", "SF", "Final"]

# Left-side R32 matches in visual order (top to bottom)
LEFT_R32_ORDER = ["M74", "M77", "M73", "M75", "M83", "M84", "M81", "M82"]
RIGHT_R32_ORDER = ["M76", "M78", "M79", "M80", "M86", "M88", "M85", "M87"]


def main():
    out_dir = os.path.join("docs", "data")
    os.makedirs(out_dir, exist_ok=True)

    # groups.json
    groups_path = os.path.join(out_dir, "groups.json")
    with open(groups_path, "w") as f:
        json.dump(GROUPS, f, indent=2)
    print(f"groups.json -> {groups_path}")

    # bracket-structure.json
    structure = {
        "matches": MATCHES,
        "round_order": ROUND_ORDER,
        "left_r32_order": LEFT_R32_ORDER,
        "right_r32_order": RIGHT_R32_ORDER,
    }
    struct_path = os.path.join(out_dir, "bracket-structure.json")
    with open(struct_path, "w") as f:
        json.dump(structure, f, indent=2)
    print(f"bracket-structure.json -> {struct_path}")

    # pool-state.json
    state = {
        "phase": "pre-group",
        "resolved_teams": {},
        "third_place_qualifiers": {},
    }
    state_path = os.path.join(out_dir, "pool-state.json")
    if not os.path.exists(state_path):
        with open(state_path, "w") as f:
            json.dump(state, f, indent=2)
        print(f"pool-state.json -> {state_path}")
    else:
        print(f"pool-state.json -> {state_path} (already exists, skipped)")


if __name__ == "__main__":
    main()
