import math
from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    def __init__(self, test: bool):
        super().__init__(test)
        self.seafloor = {}
        self.low_points = set()
        self.x_length = None
        self.y_length = None

    @property
    def day(self) -> int:
        return 9

    @property
    def test_input_data(self) -> Iterable:
        return [
            "2199943210\n",
            "3987894921\n",
            "9856789892\n",
            "8767896789\n",
            "9899965678\n",
        ]

    @property
    def test_solution(self) -> int:
        return 15

    @property
    def test_solution_part_two(self) -> int:
        return 1134

    def solve(self):
        self.analyze_seafloor()

        basins = {}

        for low_point in self.low_points:
            basin = {low_point}
            analyzed_basin = set()

            while points_to_analyze := basin.difference(analyzed_basin):
                for point in points_to_analyze:
                    for adjacent_point in self.get_adjacent_points(point).difference(analyzed_basin):
                        if self.seafloor[adjacent_point] != 9:
                            basin.add(adjacent_point)
                    analyzed_basin.add(point)

            basins[low_point] = len(basin)

        large_basins = math.prod(sorted(basins.values(), reverse=True)[:3])
        self.verify_solution_part_two(large_basins)

    def get_adjacent_points(self, point: tuple[int, int]) -> set[tuple[int, int]]:
        x, y = point

        adjacent_points = set()

        # Up
        if y != 0:
            adjacent_points.add((x, y - 1))

        # Right
        if x != self.x_length:
            adjacent_points.add((x + 1, y))

        # Down
        if y != self.y_length:
            adjacent_points.add((x, y + 1))

        # Left
        if x != 0:
            adjacent_points.add((x - 1, y))

        return adjacent_points

    def is_low_point(self, point: tuple[int, int], depth: int) -> bool:
        if depth == 9:
            return False

        for adjacent_point in self.get_adjacent_points(point):
            if self.seafloor[adjacent_point] <= depth:
                return False

        return True

    def analyze_seafloor(self):
        x = y = 0

        for y, line in enumerate(self.input_data_stripped()):
            for x, depth in enumerate(line):
                self.seafloor[(x, y)] = int(depth)

        self.x_length = x
        self.y_length = y
        risk_level = 0

        for point, depth in self.seafloor.items():
            if self.is_low_point(point, depth):
                risk_level += depth + 1
                self.low_points.add(point)

        self.verify_solution(risk_level)

    def part_two(self):
        self.verify_solution_part_two(None)

    def _run(self):
        self.solve()
        self.part_two()
