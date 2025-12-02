from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    invalid_ids = []
    for line in s.split(","):
        left, right = line.split("-")

        for n in range(int(left), int(right) + 1):
            n_str = str(n)
            if len(n_str) % 2 == 0:
                if n_str[0:len(n_str) // 2] == n_str[len(n_str) // 2:]:
                    invalid_ids.append(n)

    return sum(invalid_ids)

INPUT_S = '''\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
'''
EXPECTED = 1227775554


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
