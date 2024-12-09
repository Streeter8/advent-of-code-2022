from collections.abc import Iterable
from itertools import combinations
from typing import Self

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 8

    @property
    def test_input_data(self) -> Iterable:
        return [
            "............\n",
            "........0...\n",
            ".....0......\n",
            ".......0....\n",
            "....0.......\n",
            "......A.....\n",
            "............\n",
            "............\n",
            "........A...\n",
            ".........A..\n",
            "............\n",
            "............\n",
        ]

    @property
    def test_solution(self) -> int:
        return 14

    @property
    def test_solution_part_two(self):
        return 34

    @property
    def _solution(self) -> int:
        return 222

    @property
    def _solution_part_two(self):
        return None

    def part_one(self):
        land_map = Map.from_input(self.input_data_stripped())
        land_map.analyze_primitive_annodes()
        self.verify_solution(len(land_map.annodes))

    def part_two(self):
        land_map = Map.from_input(self.input_data_stripped())
        land_map.analyze_annodes()
        self.verify_solution_part_two(len(land_map.annodes))

    def _run(self):
        self.part_one()
        self.part_two()


def add(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] + tuple_two[0], tuple_one[1] + tuple_two[1]


def sub(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] - tuple_two[0], tuple_one[1] - tuple_two[1]


class Map:
    def __init__(
        self,
        land_map: dict[tuple[int, int], str],
        antenna: dict[str, set[tuple[int, int]]],
    ):
        self.land_map = land_map
        self.antenna = antenna

        self.row_count = max(y for _, y in land_map) + 1
        self.column_count = max(x for x, _ in land_map) + 1

        self.annodes = set()

    @classmethod
    def from_input(cls, lines: Iterable[str]) -> Self:
        lines = list(lines)
        lines.reverse()
        land_map = {}
        antenna = {}

        for row, line in enumerate(lines):
            for column, character in enumerate(line):
                land_map[(column, row)] = character

                if "." != character:
                    if character not in antenna:
                        antenna[character] = {(column, row)}
                    else:
                        antenna[character].add((column, row))

        return cls(land_map, antenna)

    @property
    def map(self) -> str:
        land_map = ""
        for row in reversed(range(self.row_count)):
            line = ""
            for column in range(self.column_count):
                position = (column, row)
                if position in self.annodes:
                    line = f"{line}#"
                else:
                    line = f"{line}{self.land_map[(column, row)]}"

            land_map = f"{land_map}{line}\n"

        return land_map

    def analyze_primitive_annodes(self) -> None:
        for positions in self.antenna.values():
            for position_one, position_two in combinations(positions, 2):
                diff = sub(position_one, position_two)
                self.add_annode(add(position_one, diff))
                self.add_annode(sub(position_two, diff))

    def analyze_annodes(self) -> None:
        for positions in self.antenna.values():
            for position_one, position_two in combinations(positions, 2):
                self.add_annode(position_one)
                self.add_annode(position_two)

                diff = sub(position_one, position_two)
                new_anode = add(position_one, diff)
                while self.add_annode(new_anode):
                    new_anode = add(new_anode, diff)

                new_anode = sub(position_two, diff)
                while self.add_annode(new_anode):
                    new_anode = sub(new_anode, diff)

    def add_annode(self, new_annode: tuple[int, int]) -> bool:
        if 0 <= new_annode[0] < self.column_count and 0 <= new_annode[1] < self.row_count:
            self.annodes.add(new_annode)
            return True

        return False

    def print_map(self) -> None:
        print(self.map)
