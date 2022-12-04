from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 4

    @property
    def test_input_data(self) -> Iterable:
        return ["2-4,6-8\n", "2-3,4-5\n", "5-7,7-9\n", "2-8,3-7\n", "6-6,4-6\n", "2-6,4-8\n"]

    @property
    def test_solution(self):
        return 2

    @property
    def test_solution_part_two(self):
        return 4

    @property
    def _solution(self):
        return 588

    @property
    def _solution_part_two(self):
        return 911

    def solve(self):
        overlap_one = 0
        overlap_two = 0

        for line in self.input_data_stripped():
            one, two = line.split(",")
            start_one, end_one = one.split("-")
            start_two, end_two = two.split("-")

            elf_one = set(range(int(start_one), int(end_one) + 1))
            elf_two = set(range(int(start_two), int(end_two) + 1))

            intersection = elf_one.intersection(elf_two)
            if intersection == elf_one or intersection == elf_two:
                overlap_one += 1
            if intersection:
                overlap_two += 1

        self.verify_solution(overlap_one)
        self.verify_solution_part_two(overlap_two)

    def _run(self):
        self.solve()
