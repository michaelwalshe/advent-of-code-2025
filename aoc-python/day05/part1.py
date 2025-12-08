from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    ranges_s, ingredients_s = s.split("\n\n")

    ranges = []
    for line in ranges_s.splitlines():
        ranges.append(list(map(int, line.split("-"))))

    ingredients = list(map(int, ingredients_s.splitlines()))

    n_fresh = 0
    for ingredient in ingredients:
        for ing_range in ranges:
            if ing_range[0] <= ingredient <= ing_range[1]:
                n_fresh += 1
                break

    return n_fresh


INPUT_S = '''\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
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
