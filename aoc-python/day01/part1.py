from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    moves_dirs = [(int(l[1:]), l[0]) for l in s.splitlines()]

    dial = 50
    tot_zeros = 0

    for move, d in moves_dirs:
        if d == "R":
            dial = (dial + move) % 100 # 0 to 99 -> 100
        else:
            dial = (dial - move) % 100
        if dial == 0:
            tot_zeros += 1

    return tot_zeros


INPUT_S = '''\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
'''
EXPECTED = 3


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
