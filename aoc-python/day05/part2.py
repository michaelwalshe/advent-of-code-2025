from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    ranges_s, _ = s.split("\n\n")

    ranges = []
    for line in ranges_s.splitlines():
        ranges.append(tuple(map(int, line.split("-"))))

    # Get sorted list of all ranges, ready to iteratively merge
    ranges = sorted(ranges, key = lambda r: r[0])

    while True:
        new_ranges = []
        i = 0
        # Flag for if we've finished merging
        made_changes = False

        while i < len(ranges):
            r1 = ranges[i]

            if i == len(ranges) - 1:
                # If on last range, then no comparison with next range and just move on
                new_ranges.append(r1)
                i += 1
                continue

            # Get next range in order
            r2 = ranges[i + 1]

            if not (r2[0] <= r1[1] and r1[0] <= r2[1]):
                # interval does not overlap with next, add to list unchanged and continue
                new_ranges.append(r1)
                i += 1
                continue

            # So range does overlap - in which case add new merged range, and skip next
            new_ranges.append((
                min(r1[0], r2[0]),
                max(r1[1], r2[1])
            ))
            i += 2
            # Mark that we've made a change, as will need to re-scan for more merged changes
            made_changes = True
        ranges = new_ranges[:]
        if not made_changes:
            break

    n_ids = 0
    for lower, upper in ranges:
        n_ids += upper - lower + 1

    return n_ids


INPUT_S = '''\
3-5
10-14
16-20
12-18
5-6

1
5
8
11
17
32
'''
EXPECTED = 15


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
