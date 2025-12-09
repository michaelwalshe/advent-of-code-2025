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

    beams = [set() for _ in lines]
    beams[0].add(start)
    n_splits = 0
    for j in range(1, len(lines)):
        for i in range(len(line)):
            if (i, j - 1) not in beams[j - 1]:
                continue

            if (i, j) not in splitters:
                beams[j].add((i, j))
                continue

            n_splits += 1
            beams[j] |= {(i - 1, j), (i + 1, j)}
    return n_splits


INPUT_S = '''\
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
'''
EXPECTED = 21


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / 'input.txt'


def main() -> int:
    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
