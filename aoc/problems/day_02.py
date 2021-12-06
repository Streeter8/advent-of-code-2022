from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 2

    @property
    def test_input_data(self) -> Iterable:
        return iter(["forward 5\n", "down 5\n", "forward 8\n", "up 3\n", "down 8\n", "forward 2\n"])

    @property
    def test_solution(self) -> int:
        return 150

    @property
    def test_solution_part_two(self) -> int:
        return 900

    def part_one(self):
        x = 0
        y = 0
        for command in self.input_data_stripped():
            direction, magnitude = command.split(" ")
            magnitude = int(magnitude)

            # I don't think this is necessary,
            # But I wanted to give structural pattern matching a try
            # https://www.python.org/dev/peps/pep-0636/
            match direction:
                case "forward":
                    x += magnitude
                case "up":
                    y -= magnitude
                case "down":
                    # down "adds" depth
                    y += magnitude
                case _:
                    raise ValueError(f"An unexpected direction was found: {direction}")

        solution = x * y
        self.verify_solution(solution)

    def part_two(self):
        x = 0
        y = 0
        aim = 0

        for command in self.input_data_stripped():
            direction, magnitude = command.split(" ")
            magnitude = int(magnitude)

            # I don't think this is necessary,
            # But I wanted to give structural pattern matching a try
            # https://www.python.org/dev/peps/pep-0636/
            match direction:
                case "forward":
                    x += magnitude
                    y += magnitude * aim
                case "up":
                    aim -= magnitude
                case "down":
                    # down "adds" depth
                    aim += magnitude
                case _:
                    raise ValueError(f"An unexpected direction was found: {direction}")

        solution = x * y
        self.verify_solution_part_two(solution)

    def _run(self):
        self.part_one()
        self.part_two()
