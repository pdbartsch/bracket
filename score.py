"""Score all bracket entries against actual results and generate standings JSON.

Usage:
    uv run score.py                  # Score and write docs/standings.json
    uv run score.py --verbose        # Also print leaderboard to console
"""

import argparse
import json
import os
from datetime import datetime


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def score_entry(entry: dict, results: dict, scoring: dict) -> dict:
    """Score a single entry against results. Returns score breakdown."""
    points_per_round = scoring["points_per_round"]
    total = 0
    breakdown = {}

    for round_name, point_value in points_per_round.items():
        round_results = results["rounds"].get(round_name, {})
        round_picks = entry["picks"].get(round_name, {})
        correct = 0
        total_matches = 0

        for match_id, winner in round_results.items():
            if not winner:
                continue
            total_matches += 1
            if round_picks.get(match_id) == winner:
                correct += 1

        round_points = correct * point_value
        total += round_points
        breakdown[round_name] = {
            "correct": correct,
            "possible": total_matches,
            "points": round_points,
        }

    # Champion bonus
    champ_bonus = 0
    if results["champion"] and entry.get("champion") == results["champion"]:
        champ_bonus = scoring["champion_bonus"]
        total += champ_bonus

    return {
        "name": entry["name"],
        "total": total,
        "champion_bonus": champ_bonus,
        "champion_pick": entry.get("champion", ""),
        "breakdown": breakdown,
    }


def generate_standings(data_dir: str = "data") -> dict:
    """Score all entries and return standings dict."""
    entries = load_json(os.path.join(data_dir, "entries.json"))
    results = load_json(os.path.join(data_dir, "results.json"))
    scoring = load_json(os.path.join(data_dir, "scoring.json"))

    scores = []
    for entry in entries["entries"]:
        scores.append(score_entry(entry, results, scoring))

    # Sort by total descending
    scores.sort(key=lambda s: s["total"], reverse=True)

    # Assign rank (handle ties)
    for i, s in enumerate(scores):
        if i > 0 and s["total"] == scores[i - 1]["total"]:
            s["rank"] = scores[i - 1]["rank"]
        else:
            s["rank"] = i + 1

    return {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "results_through": results["last_updated"],
        "scoring": scoring,
        "standings": scores,
    }


def main():
    parser = argparse.ArgumentParser(description="Score bracket entries")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    standings = generate_standings()

    out_path = os.path.join("docs", "standings.json")
    os.makedirs("docs", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(standings, f, indent=2)
    print(f"Standings -> {out_path}")

    if args.verbose:
        print(f"\nLast updated: {standings['last_updated']}")
        print(f"Results through: {standings['results_through'] or 'no results yet'}\n")
        print(f"{'Rank':<6}{'Name':<20}{'R32':<6}{'R16':<6}{'QF':<6}{'SF':<6}{'F':<6}{'Champ':<8}{'Total':<6}")
        print("-" * 70)
        for s in standings["standings"]:
            b = s["breakdown"]
            print(
                f"{s['rank']:<6}"
                f"{s['name']:<20}"
                f"{b.get('R32', {}).get('points', 0):<6}"
                f"{b.get('R16', {}).get('points', 0):<6}"
                f"{b.get('QF', {}).get('points', 0):<6}"
                f"{b.get('SF', {}).get('points', 0):<6}"
                f"{b.get('Final', {}).get('points', 0):<6}"
                f"{s['champion_bonus']:<8}"
                f"{s['total']:<6}"
            )


if __name__ == "__main__":
    main()
