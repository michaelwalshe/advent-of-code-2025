from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass

import math as m
import heapq

import pytest

import support


class Point(NamedTuple):
    x: int
    y: int
    z: int


@dataclass(order=True)
class Connection:
    dist: float
    j1: Point
    j2: Point


def get_junction_circuit(
    j: Point, circuits: list[set[Point]]
) -> tuple[int, set[Point]]:
    # Get a circuit containing a junction plus position, or an empty set if no junction exists
    for i, c in enumerate(circuits):
        if j in c:
            return i, c
    return -1, set()


def update_junction_circuit(j1: Point, j2: Point, circuits: list[set[Point]]) -> None:
    # Update a list of circuits with a new connection between j1 and j2
    i1, c1 = get_junction_circuit(j1, circuits)
    i2, c2 = get_junction_circuit(j2, circuits)

    if c1:
        # Have j1 in an existing circuit, update with connection to j2
        c1 |= {j1, j2}
        if c2 and i1 != i2:
            # If j2 is already in a separate circuit, merge them and delete second
            c1 |= c2
            del circuits[i2]
    elif c2:
        # Alternatively have j2 in circuit, add j1
        c2 |= {j1, j2}
    else:
        # Add this new circuit
        circuits.append({j1, j2})


def compute(s: str) -> int:
    junctions = set()
    for line in s.splitlines():
        junctions.add(Point(*[int(n) for n in line.split(",")]))

    # Using a heap, calculate all combinations of junctions and the distances between them,
    # storing in order lowest distance to highest
    all_conn_heap = []
    all_connections = set()
    for j1 in junctions:
        for j2 in junctions:
            if j1 == j2 or (j1, j2) in all_connections or (j2, j1) in all_connections:
                continue
            dist = m.sqrt((j1.x - j2.x) ** 2 + (j1.y - j2.y) ** 2 + (j1.z - j2.z) ** 2)
            all_connections.add((j1, j2))
            heapq.heappush(all_conn_heap, Connection(dist, j1, j2))

    circuits = []

    while True:
        # Get all connections, lowest first, using heap, then add to
        # list of circuits (updating as circuits merge etc)
        conn = heapq.heappop(all_conn_heap)
        update_junction_circuit(conn.j1, conn.j2, circuits)
        if circuits[0] == junctions:
            # Have only 1 circuit with all junctions in
            break

    return conn.j1.x * conn.j2.x


INPUT_S = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
EXPECTED = 25272


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
