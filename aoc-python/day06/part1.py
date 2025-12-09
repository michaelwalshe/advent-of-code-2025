from functools import reduce
from pathlib import Path
from operator import add, mul
import pytest

import support


def compute(s: str) -> int:
    lines = s.splitlines()
    columns = [[] for _ in lines[0].split()]
    for j, line in enumerate(lines):
        if j == len(lines) - 1:
            break
        for i, n in enumerate(line.split()):
            columns[i].append(int(n))

    operators = lines[-1].split()
    tot = 0
    for i, col in enumerate(columns):
        op = operators[i]
        if op == '+':
            tot += reduce(add, col, 0)
        else:
            tot += reduce(mul, col, 1)
    return tot


INPUT_S = '''\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
'''
EXPECTED = 4277556


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
