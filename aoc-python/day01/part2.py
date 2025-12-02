from pathlib import Path

import pytest

import support

INPUT_TXT = Path(__file__).parent / 'input.txt'


def compute(s: str) -> int:
    moves_dirs = [(int(l[1:]), l[0]) for l in s.splitlines()]

    dial = 50
    tot_zeros = 0

    for move, d in moves_dirs:
        direction = 1 if d == "R" else -1

        while move:
            dial = (dial + direction) % 100
            if dial == 0:
                tot_zeros += 1
            move -= 1

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
EXPECTED = 6

INPUT_S2 = '''\
R1000
'''
EXPECTED2 = 10

@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
        (INPUT_TXT.read_text(), 6475)
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected




def main() -> int:
    print(compute(INPUT_S))
    print(compute(INPUT_S2))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
