import re
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import pytest

import support


@dataclass
class Machine:
    indicator_target: list[bool]
    buttons: list[list[int]]
    indicators: list[bool]
    pressed_buttons: list[int] = field(default_factory=list)
    n_presses: int = 0


def configure_machine(m: Machine) -> int:
    seen = set()
    queue = deque([m])
    while queue:
        curr_m = queue.popleft()
        for button_i, button_links in enumerate(curr_m.buttons):
            next_m = Machine(
                curr_m.indicator_target,
                curr_m.buttons,
                [
                    not ind if i in button_links else ind
                    for i, ind in enumerate(curr_m.indicators)
                ],
                curr_m.pressed_buttons + [button_i],
                curr_m.n_presses + 1,
            )

            if next_m.indicators == next_m.indicator_target:
                return next_m.n_presses
    
            if tuple(next_m.indicators) not in seen:
                seen.add(tuple(next_m.indicators))
                queue.append(next_m)

    return 0


def compute(s: str) -> int:
    machines = []

    for line in s.splitlines():
        ind_match = re.search(r"\[(.+)\]", line)
        assert ind_match is not None
        indicator_target = [True if c == "#" else False for c in ind_match.group(1)]
        buttons = [
            list(map(int, e.split(","))) for e in re.findall(r"\((.+?)\)+", line)
        ]

        machines.append(
            Machine(
                indicator_target,
                buttons,
                indicators=[False for _ in indicator_target],
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
EXPECTED = 7


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
