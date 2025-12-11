import re
from dataclasses import dataclass
from pathlib import Path
import pytest

import z3

import support


@dataclass
class Machine:
    joltage_target: tuple[int, ...]
    buttons: tuple[set[int], ...]
    joltage: tuple[int, ...]
    n_presses: int = 0


def configure_machine(m: Machine) -> int:
    s = z3.Solver()

    # Each button will be pressed an Int number of times
    button_vars = [z3.FreshInt("b") for _ in m.buttons]

    for bv in button_vars:
        s.add(bv >= 0)

    for i, jolt in enumerate(m.joltage_target):
        # For each output joltage, indicated by i
        this_jolt_buttons = []
        for j, b in enumerate(m.buttons):
            if i in b:
                # Check which input buttons will increment this output, add
                # to list of variables
                this_jolt_buttons.append(button_vars[j])
        # Assert that sum of those button presses must equal output joltage
        s.add(jolt == z3.Sum(this_jolt_buttons))

    min_presses = -1
    assert s.check() == z3.sat, "Unsolvable equation!"
    while s.check() == z3.sat:
        # Ensure minimal solution, add constraint of less than previous guess
        # and return last solvable solution
        model = s.model()
        min_presses = sum(model[v].as_long() for v in model)
        s.add(z3.Sum(button_vars) < min_presses)

    return min_presses


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
