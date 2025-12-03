from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    banks = s.splitlines()
    joltages = []
    n_on = 12

    def calc_jolt(batteries: list[int], bank: str) -> int:
        return int("".join(bank[i] for i in batteries))

    for bank in banks:
        bank_len = len(bank)
        # Initialise batteries as final N in bank (e.g. 87 -- 99)
        batteries = list(range(bank_len - n_on, bank_len))

        for i in range(n_on):
            # For each battery, get range of alternative positions, leftmost will either be 0
            # or the next battery to the left
            if i == 0:
                min_j = 0
            else:
                min_j = batteries[i - 1] + 1

            # Similarly rightmost alternative position is either next battery or final one in bank
            if i == n_on - 1:
                max_j = bank_len
            else:
                max_j = batteries[i + 1]

            # Get current joltage as max, then check alternative positions for this battery to see if it increases it
            max_jolt = calc_jolt(batteries, bank)
            max_jolt_j = batteries[i]
            for j in range(min_j, max_j):
                batteries[i] = j
                new_jolt = calc_jolt(batteries, bank)
                # A new joltage is preferable if it either strictly increases the joltage, or keeps it
                # the same and moves the battery to the left (as that gives more options for later batteries)
                if (new_jolt > max_jolt) or (new_jolt == max_jolt and j <= max_jolt_j):
                    max_jolt = new_jolt
                    max_jolt_j = j

            # Set this battery position to whichever maximum was found
            batteries[i] = max_jolt_j

        # Once all spots have been searched, add joltage
        joltages.append(calc_jolt(batteries, bank))

    return sum(joltages)


INPUT_S = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""
EXPECTED = 3121910778619


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
