from typing import Iterable

from aoc.utilities.aoc import AocBase


class Castle:
    def __init__(self, lines):
        self.walls = []
        for line in lines:
            coordinates = []
            points = line.split(" -> ")
            for point in points:
                coordinates.append(tuple(int(_) for _ in point.split(",")))

            self.walls.append(coordinates)


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 14

    @property
    def test_input_data(self) -> Iterable:
        return ["498,4 -> 498,6 -> 496,6\n", "503,4 -> 502,4 -> 502,9 -> 494,9\n"]

    @property
    def test_solution(self):
        return 24

    @property
    def test_solution_part_two(self):
        raise NotImplementedError

    def part_one(self):
        castle = Castle(self.input_data_stripped())  # noqa: F841
        self.verify_solution(None)

    def part_two(self):
        self.verify_solution_part_two(None)

    def _run(self):
        self.part_one()
        self.part_two()
