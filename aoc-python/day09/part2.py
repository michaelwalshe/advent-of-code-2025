from itertools import combinations
from pathlib import Path
from shapely import Point, Polygon, box

import pytest
import support

def compute(s: str) -> int:
    # Parse red tile positions from input
    red_tiles = []
    for line in s.splitlines():
        red_tiles.append(Point(*list(map(int, line.split(",")))))

    bounds = Polygon(red_tiles)

    max_area = 0
    for t1, t2 in combinations(red_tiles, 2):
        max_x = max(t1.x, t2.x)
        max_y = max(t1.y, t2.y)
        min_x = min(t1.x, t2.x)
        min_y = min(t1.y, t2.y)
        area = (max_x - min_x + 1) * (max_y - min_y + 1)

        if area < max_area:
            continue
        
        # Maths is hard - just use libraries!
        rectangle = box(min_x, min_y, max_x, max_y)

        if bounds.contains(rectangle):
            max_area = area

    return int(max_area)


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
EXPECTED = 24


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
