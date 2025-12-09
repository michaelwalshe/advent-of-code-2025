from functools import cache
from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    splitters = set()
    lines = s.splitlines()
    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c == "S":
                start = i, j
            elif c == "^":
                splitters.add((i, j))
    splitters = frozenset(splitters)

    @cache
    def get_n_timelines(beam, splitters, max_j):
        next_beam = beam[0], beam[1] + 1
        if next_beam[1] >= max_j:
            return 1
        if next_beam not in splitters:
            return get_n_timelines(next_beam, splitters, max_j)
        nb1 = next_beam[0] - 1, next_beam[1]
        nb2 = next_beam[0] + 1, next_beam[1]
        return get_n_timelines(nb1, splitters, max_j) + get_n_timelines(nb2, splitters, max_j)

    return get_n_timelines(start, splitters, len(lines))


INPUT_S = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
EXPECTED = 40


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
