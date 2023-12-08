from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 10

    @property
    def test_input_data(self) -> Iterable:
        raise NotImplementedError

    @property
    def test_solution(self):
        raise NotImplementedError

    @property
    def test_solution_part_two(self):
        raise NotImplementedError

    @property
    def _solution(self):
        return None

    @property
    def _solution_part_two(self):
        return None

    def part_one(self):
        self.verify_solution(None)

    def part_two(self):
        self.verify_solution_part_two(None)

    def _run(self):
        self.part_one()
        self.part_two()
