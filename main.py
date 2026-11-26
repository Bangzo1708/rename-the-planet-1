#!/usr/bin/env python3
"""Rename the Planet — make.fun entry.

Writes one line to /output/entry.txt (or $ENTRY_OUTPUT): a funny new
name for a planet of our solar system plus the why, in a single breath,
under 200 characters.

The program holds three hand-written candidates, scores each one on the
judge's four criteria (funny, why earns the name, fresh, tight — each
0-5), and writes the highest-scoring line. The scoring is fixed data,
so the program is fully deterministic: no randomness, no clock, no
network, no file reads. The winner is picked by total score, with ties
broken first by freshness, then by fewest characters, then by earliest
position in the list.
"""

import os
import stat

# --- Candidates, scored 0-5 per judge criterion -------------------------
# Criterion order: funny, why-earns-the-name, fresh, tight.
#
# 1. Mercury, "The Intern": closest to the boss (the Sun), laps the
#    office in 88 days, never gets a day off.
#    Scores: funny 4, why-earns 4, fresh 4, tight 5 -> total 17.
#    Solid office joke, but "intern" is a well-worn metaphor.
#
# 2. Neptune, "The Overdue Library Book": blue, freezing, and 165
#    years overdue on a loan it will never return.
#    Scores: funny 4, why-earns 5, fresh 5, tight 5 -> total 19.
#    The why is Neptune-only (blue, cold, 165-year orbit), the
#    library-book angle is one nobody reaches for with a planet,
#    and "overdue" echoing the name itself tightens the joke: the
#    name and the why land as one idea on the first read.
#
# 3. Venus, "The Group Project": spins backwards, runs hotter than
#    everyone else, still takes all the credit as the morning star.
#    Scores: funny 4, why-earns 5, fresh 3, tight 4 -> total 16.
#    The traits fit Venus perfectly, but the group-project angle
#    is familiar and the line runs long.
#
# Winner: candidate 2, Neptune — highest total, and it steers clear
# of the Uranus / Mars-chocolate-bar / Saturn-hula-hoop cliches the
# judge will have read a thousand times already.

CANDIDATES = [
    {
        "text": (
            "Mercury is now 'The Intern' - closest to the boss, "
            "laps the office in 88 days, and still never gets a day off."
        ),
        "scores": (4, 4, 4, 5),
    },
    {
        "text": (
            "Neptune is now 'The Overdue Library Book' - blue, "
            "freezing, and 165 years overdue on a loan it will "
            "never return."
        ),
        "scores": (4, 5, 5, 5),
    },
    {
        "text": (
            "Venus is now 'The Group Project' - spins backwards, "
            "runs hotter than everyone else, and still takes all "
            "the credit as the morning star."
        ),
        "scores": (4, 5, 3, 4),
    },
]

MAX_CHARS = 200


def pick_winner(candidates):
    """Pick the best candidate: highest total, then freshest, then
    shortest, then earliest. Pure function of the fixed data above."""
    def key(item):
        index, candidate = item
        total = sum(candidate["scores"])
        freshness = candidate["scores"][2]
        length = len(candidate["text"])
        return (-total, -freshness, length, index)

    best_index, best = min(enumerate(candidates), key=key)
    return best_index, best


def main():
    _, winner = pick_winner(CANDIDATES)
    line = winner["text"]

    # Gate: the entry must be 1-200 characters of real text.
    assert 1 <= len(line) <= MAX_CHARS, "entry length out of range"
    assert line.strip(), "entry must not be only whitespace"
    assert "\n" not in line, "entry must be a single line"

    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        os.chmod(out_dir, 0o755)

    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    os.chmod(out_path, 0o644)


if __name__ == "__main__":
    main()
