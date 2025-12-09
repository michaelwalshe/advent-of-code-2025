from functools import reduce
from pathlib import Path
from operator import add, mul
import pytest

import support


def compute(s: str) -> int:
    lines = s.splitlines()
    operators = []
    start = 0
    operator = ""
    for i, c in enumerate(lines[-1]):
        # parse all our operators, use these to determine column start/end positions
        if c != " ":
            # On first iteration operator will be blank, so skip
            if operator:
                operators.append((operator, start, i))
            operator = c
            start = i
    # After finished iteration add final hanging operator
    operators = operators + [(operator, start, i + 2)]

    # Now parse each column
    tot = 0
    for op, start, end in operators:
        nums_c = [""] * (len(lines) - 1)
        for line in lines[:-1]:
            # Get the chunk of each line that's the column we're currently
            # operating on
            for i, c in enumerate(line[start : (end - 1)]):
                # Add to relevent number as string. Will give us extra spaces
                # and blank digits, filter those out before operating
                nums_c[i] += c
        nums = map(int, filter(lambda s: s and not s.isspace(), nums_c))
        if op == "+":
            tot += reduce(add, nums, 0)
        else:
            tot += reduce(mul, nums, 1)

    return tot


INPUT_S = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""
EXPECTED = 3263827

INPUT_S_2 = """\
73 123 328  51 64 
21  45 64  387 23 
1    6 98  215 314
*   +   *   +  
"""
EXPECTED_2 = 3263827 + 1533


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (INPUT_S_2, EXPECTED_2),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S))
    print(compute(INPUT_S_2))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
