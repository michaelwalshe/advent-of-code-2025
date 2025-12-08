from pathlib import Path
import pytest

import support


def compute(s: str) -> int:
    rolls = set()

    for j, line in enumerate(s.splitlines()):
        for i, c in enumerate(line):
            if c == "@":
                rolls.add((i, j))

    def check_accessible(p: tuple[int, int], rolls: set[tuple[int, int]]) -> bool:
        n_adj = 0
        for n_i, n_j in support.adjacent_8(p[0], p[1]):
            if (n_i, n_j) in rolls:
                n_adj += 1

        return n_adj < 4

    rolls_removed = 0
    while True:
        rolls_left = [p for p in rolls if check_accessible(p, rolls)]
        if len(rolls_left) == 0:
            break
        for roll in rolls_left:
            rolls_removed += 1
            rolls.remove(roll)
    
    return rolls_removed


INPUT_S = """\
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
"""
EXPECTED = 13


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
