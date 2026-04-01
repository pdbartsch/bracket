"""Generate group stage SVG.

Usage:
    uv run generate_groups.py              # SVG only
    uv run generate_groups.py --pdf        # SVG + PDF
    uv run generate_groups.py --open       # open in browser
"""

import argparse
import os
import subprocess
import sys

from bracket.draw_groups import draw_groups


def main():
    parser = argparse.ArgumentParser(description="Generate World Cup group stage")
    parser.add_argument("--pdf", action="store_true", help="Also export to PDF")
    parser.add_argument("--open", action="store_true", help="Open SVG in default viewer")
    parser.add_argument("-o", "--output", default="output/groups.svg", help="Output SVG path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    output = os.path.abspath(args.output)

    svg_path = draw_groups(filename=output)
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
