from pathlib import Path

import pytest
import numpy as np

import support


def compute(s: str) -> int:
    shapes_trees = s.split("\n\n")



    presents = []
    for shape_s in shapes_trees[:-1]:
        shape_lines = shape_s.splitlines()
        max_j = len(shape_lines) - 1
        max_i = len(shape_lines[-1])
        shape = np.zeros((max_i, max_j))
        for j, line in enumerate(shape_lines[1:]):
            for i, c in enumerate(line):
                if c == "#":
                    shape[j, i] = 1
        presents.append(shape)

    trees = []
    for tree_s in shapes_trees[-1].splitlines():
        dims_s, required_pres_s = tree_s.split(":")

        dims = tuple(map(int, dims_s.split("x")))
        required_pres = tuple(map(int, required_pres_s.split()))
        trees.append((dims, required_pres))

    n_fit = 0
    for dims, pres in trees:
        total_area_large = 0
        for n_p in pres:
            total_area_large += n_p * (3 * 3)
        total_area_small = 0
        for i, n_p in enumerate(pres):
            total_area_small += n_p * np.sum(presents[i])
        if (dims[0] * dims[1]) >= total_area_large:
            n_fit += 1
        elif (dims[0] * dims[1]) > total_area_small:
            raise NotImplementedError(f"Theoretically could fit this in... {dims} {pres}")
    return n_fit


INPUT_S = '''\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
'''
EXPECTED = 2


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
    # print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
