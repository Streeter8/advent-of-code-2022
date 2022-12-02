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

    @property
    def _solution(self):
        return 13675

    @property
    def _solution_part_two(self):
        return 14184

    def solve(self):
        # A, X: Rock
        # B, Y: Paper
        # C, Z: Scissors
        # (Game 1 Score, Game 2 Score)
        game = {
            "A X": (3 + 1, 0 + 3),
            "A Y": (6 + 2, 3 + 1),
            "A Z": (0 + 3, 6 + 2),
            "B X": (0 + 1, 0 + 1),
            "B Y": (3 + 2, 3 + 2),
            "B Z": (6 + 3, 6 + 3),
            "C X": (6 + 1, 0 + 2),
            "C Y": (0 + 2, 3 + 3),
            "C Z": (3 + 3, 6 + 1),
            "": (0, 0),
        }

        score_one = 0
        score_two = 0
        for line in self.input_data_stripped():
            one, two = game[line]
            score_one += one
            score_two += two

        self.verify_solution(score_one)
        self.verify_solution_part_two(score_two)

    def _run(self):
        self.solve()
