from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    rolls = set()

    lines = s.splitlines()

    max_j = len(lines)
    max_i = len(lines[0])

    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c == "@":
                rolls.add((i, j))

    n_pos = 0
    for (i, j) in rolls:
            n_adj = 0
            for n_i, n_j in support.adjacent_8(i, j):
                if (n_i, n_j) in rolls:
                    n_adj += 1
            if n_adj < 4:
                n_pos += 1

    return n_pos


INPUT_S = '''\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
'''
EXPECTED = 13


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
