import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import pytest

import support


@dataclass
class Machine:
    joltage_target: tuple[int, ...]
    buttons: tuple[set[int], ...]
    joltage: tuple[int, ...]
    n_presses: int = 0


def configure_machine(m: Machine) -> int:
    seen = set()
    queue = deque([(m.joltage, m.n_presses)])
    while queue:
        curr_joltage, curr_presses = queue.popleft()
        for button_links in m.buttons:
            next_joltage = tuple(
                jolt + 1 if i in button_links else jolt
                for i, jolt in enumerate(curr_joltage)
            )

            if any(
                j_c > j_t for j_c, j_t in zip(next_joltage, m.joltage_target)
            ):
                continue

            if next_joltage == m.joltage_target:
                return curr_presses + 1

            if next_joltage not in seen:
                seen.add(next_joltage)
                queue.append((next_joltage, curr_presses + 1))

    return 0


def compute(s: str) -> int:
    machines = []

    for line in s.splitlines():
        buttons = [set(map(int, e.split(","))) for e in re.findall(r"\((.+?)\)+", line)]
        j_match = re.search(r"\{(.+)\}", line)
        assert j_match is not None
        joltage_target = tuple(int(n) for n in j_match.group(1).split(","))

        buttons = tuple(sorted(buttons, key=lambda lst: len(lst), reverse=True))

        machines.append(
            Machine(
                joltage_target,
                buttons,
                joltage=tuple(0 for _ in joltage_target),
            )
        )

    presses = 0
    for m in machines:
        presses += configure_machine(m)

    return presses


INPUT_S = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
EXPECTED = 33


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
