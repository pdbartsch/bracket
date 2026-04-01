"""Generate bracket SVG (and optionally PDF).

Usage:
    uv run generate.py              # SVG only
    uv run generate.py --pdf        # SVG + PDF
    uv run generate.py --open       # SVG + open in browser
"""

import argparse
import os
import subprocess
import sys

from bracket_print.draw import draw_bracket
from bracket_print.teams import WORLD_CUP_TEAMS


def main():
    parser = argparse.ArgumentParser(description="Generate World Cup bracket")
    parser.add_argument("--pdf", action="store_true", help="Also export to PDF")
    parser.add_argument("--open", action="store_true", help="Open SVG in default viewer")
    parser.add_argument("-o", "--output", default="output/bracket.svg", help="Output SVG path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    output = os.path.abspath(args.output)

    svg_path = draw_bracket(WORLD_CUP_TEAMS, filename=output)
    print(f"SVG -> {svg_path}")

    if args.pdf:
        import cairosvg

        pdf_path = svg_path.replace(".svg", ".pdf")
        cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
        print(f"PDF -> {pdf_path}")

    if args.open:
        if sys.platform == "win32":
            os.startfile(svg_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", svg_path])
        else:
            subprocess.run(["xdg-open", svg_path])


if __name__ == "__main__":
    main()
