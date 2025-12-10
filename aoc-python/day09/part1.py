from itertools import combinations
from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    tiles = set()
    for line in s.splitlines():
        tiles.add(tuple(map(int, line.split(","))))

    max_area = 0
    for t1, t2 in combinations(tiles, 2):
        area = (max(t1[0], t2[0]) - min(t1[0], t2[0]) + 1) * (
            max(t1[1], t2[1]) - min(t1[1], t2[1]) + 1
        )
        max_area = max(max_area, area)
    return max_area


INPUT_S = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
EXPECTED = 50


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
