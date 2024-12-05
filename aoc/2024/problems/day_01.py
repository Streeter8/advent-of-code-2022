from collections import Counter
from collections.abc import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_input_data(self) -> Iterable:
        return (
            "3   4\n",
            "4   3\n",
            "2   5\n",
            "1   3\n",
            "3   9\n",
            "3   3\n",
        )

    @property
    def test_solution(self) -> int:
        return 11

    @property
    def test_solution_part_two(self) -> int:
        return 31

    @property
    def _solution(self) -> int:
        return 2769675

    @property
    def _solution_part_two(self) -> int:
        return 24643097

    def _run(self):
        row_one = []
        row_two = []

        for row in self.input_data_stripped():
            x, y = map(int, row.split("   "))
            row_one.append(x)
            row_two.append(y)

        row_one.sort()
        row_two.sort()
        counter = Counter(row_two)

        differences = 0
        similarity_score = 0
        for index, value in enumerate(row_one):
            differences += abs(value - row_two[index])
            similarity_score += value * counter.get(value, 0)

        self.verify_solution(differences)
        self.verify_solution_part_two(similarity_score)
