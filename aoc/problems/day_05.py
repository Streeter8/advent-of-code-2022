from typing import Iterable

from aoc.utilities.aoc import AocBase


class Line:
    def __init__(self, line: str):
        point_one, point_two = line.split(" -> ")
        point_one = point_one.split(",")
        point_two = point_two.split(",")

        point_one = (int(point_one[0]), int(point_one[1]))
        point_two = (int(point_two[0]), int(point_two[1]))

        if point_one[0] < point_two[0] or (point_one[0] == point_two[0] and point_one[1] < point_two[1]):
            self.x1 = point_one[0]
            self.y1 = point_one[1]
            self.x2 = point_two[0]
            self.y2 = point_two[1]
        else:
            self.x1 = point_two[0]
            self.y1 = point_two[1]
            self.x2 = point_one[0]
            self.y2 = point_one[1]

    @property
    def is_horizontal(self) -> bool:
        return self.y1 == self.y2

    @property
    def is_vertical(self) -> bool:
        return self.x1 == self.x2

    @property
    def is_slanted_up(self) -> bool:
        return self.y1 < self.y2

    @property
    def is_slanted(self) -> bool:
        return not self.is_horizontal and not self.is_vertical

    def data_points(self) -> list[tuple[int, int]]:
        if self.is_horizontal:
            return [(x, self.y1) for x in range(self.x1, self.x2 + 1)]
        elif self.is_vertical:
            return [(self.x1, y) for y in range(self.y1, self.y2 + 1)]
        elif self.is_slanted_up:
            return [(self.x1 + index, self.y1 + index) for index in range(self.x2 - self.x1 + 1)]
        else:
            return [(self.x1 + index, self.y1 - index) for index in range(self.x2 - self.x1 + 1)]


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 5

    @property
    def test_input_data(self) -> Iterable:
        return [
            "0,9 -> 5,9",
            "8,0 -> 0,8",
            "9,4 -> 3,4",
            "2,2 -> 2,1",
            "7,0 -> 7,4",
            "6,4 -> 2,0",
            "0,9 -> 2,9",
            "3,4 -> 1,4",
            "0,0 -> 8,8",
            "5,5 -> 8,2",
        ]

    @property
    def test_solution(self) -> int:
        return 5

    @property
    def test_solution_part_two(self):
        return 12

    def lines(self) -> Iterable[Line]:
        for line in self.input_data_stripped():
            yield Line(line)

    def part_one(self):
        vents = {}
        for line in self.lines():
            if line.is_slanted:
                continue

            for point in line.data_points():
                if point not in vents:
                    vents[point] = 1
                else:
                    vents[point] += 1

        points = 0
        for number_of_vents in vents.values():
            if number_of_vents > 1:
                points += 1

        self.verify_solution(points)

    def part_two(self):
        vents = {}
        for line in self.lines():
            for point in line.data_points():
                if point not in vents:
                    vents[point] = 1
                else:
                    vents[point] += 1

        points = 0
        for number_of_vents in vents.values():
            if number_of_vents > 1:
                points += 1

        self.verify_solution_part_two(points)

    def _run(self):
        self.part_one()
        self.part_two()
