from functools import cache
from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    graph = {}
    for line in s.splitlines():
        din, douts = line.split(":")
        graph[din] = douts.split()
    graph["out"] = []

    # Recursive graph search with cachings
    @cache
    def count_paths(start: str, end: str) -> int:
        paths = 0
        for dnext in graph[start]:
            if dnext == end:
                paths += 1
            else:
                paths += count_paths(dnext, end)
        return paths

    # All ways of getting from svr to out via dac & fft
    svr_dac = count_paths("svr", "dac")
    svr_fft = count_paths("svr", "fft")
    dac_fft = count_paths("dac", "fft")
    fft_dac = count_paths("fft", "dac")
    dac_out = count_paths("dac", "out")
    fft_out = count_paths("fft", "out")

    # Get number of options of each, add together to give all paths!
    svr_out_1 = svr_dac * dac_fft * fft_out
    svr_out_2 = svr_fft * fft_dac * dac_out

    return svr_out_1 + svr_out_2


INPUT_S = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""
EXPECTED = 2


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
