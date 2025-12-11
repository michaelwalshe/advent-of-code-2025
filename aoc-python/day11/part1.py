from collections import deque
from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    graph = {}
    for line in s.splitlines():
        din, douts = line.split(":")
        graph[din] = douts.split()

    start = "you"
    seen = {start}
    queue = deque([(start, [])])
    paths = []
    while queue:
        curr, path = queue.popleft()
        for next_d in graph[curr]:
            if next_d == "out":
                paths.append(path + [next_d])
            elif next_d in seen:
                continue
            else:
                queue.append(
                    (next_d, path + [next_d])
                )

    return len(paths)


INPUT_S = '''\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
'''
EXPECTED = 5


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
