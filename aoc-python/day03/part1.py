from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    banks = s.splitlines()
    joltages = []

    for bank in banks:
        l = 0
        r = 1
        max_jolt = 0
        while l < len(bank):
            while r < len(bank):
                cur_jolt = int(bank[l] + bank[r])
                if cur_jolt > max_jolt:
                    max_jolt = cur_jolt
                r += 1
            l += 1
            r = l + 1
        joltages.append(max_jolt)

    return sum(joltages)


INPUT_S = '''\
987654321111111
811111111111119
234234234234278
818181911112111
'''
EXPECTED = 357


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
