from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 2

    @property
    def test_input_data(self) -> Iterable:
        return ["A Y\n", "B X\n", "C Z\n", "\n"]

    @property
    def test_solution(self):
        return 15

    @property
    def test_solution_part_two(self):
        return 12

    def part_one(self):
        # A, X: Rock
        # B, Y: Paper
        # C, Z: Scissors
        games = {
            "A X": 3 + 1,
            "A Y": 6 + 2,
            "A Z": 0 + 3,
            "B X": 0 + 1,
            "B Y": 3 + 2,
            "B Z": 6 + 3,
            "C X": 6 + 1,
            "C Y": 0 + 2,
            "C Z": 3 + 3,
        }

        score = 0
        for line in self.input_data_stripped():
            if line:
                score += games[line]

        self.verify_solution(score)

    def part_two(self):
        # A, X: Rock
        # B, Y: Paper
        # C, Z: Scissors
        games = {
            "A X": 0 + 3,
            "A Y": 3 + 1,
            "A Z": 6 + 2,
            "B X": 0 + 1,
            "B Y": 3 + 2,
            "B Z": 6 + 3,
            "C X": 0 + 2,
            "C Y": 3 + 3,
            "C Z": 6 + 1,
        }

        score = 0
        for line in self.input_data_stripped():
            if line:
                score += games[line]

        self.verify_solution_part_two(score)

    def _run(self):
        self.part_one()
        self.part_two()
