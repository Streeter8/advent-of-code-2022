from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 8

    @property
    def test_input_data(self) -> Iterable:
        return ["30373\n", "25512\n", "65332\n", "33549\n", "35390\n"]

    @property
    def test_solution(self):
        return 21

    @property
    def test_solution_part_two(self):
        return 8

    @property
    def _solution(self):
        return 1736

    @property
    def _solution_part_two(self):
        return 268800

    def solve(self):
        trees = {}
        forest = list(self.input_data_stripped())
        # consume trees from bottom to top to preserve coordinate plane
        forest.reverse()

        for row, treeline in enumerate(self.input_data_stripped()):
            for column, tree in enumerate(treeline):
                trees[(column, row)] = tree
        end_columns = [0, column]
        end_rows = [0, row]

        seeable_trees = 0
        scenic_score = 0

        for (x, y), tree in trees.items():
            if x in end_columns or y in end_rows:
                seeable_trees += 1
                continue

            can_see_above, score_above = self.can_see_above(x, y, tree, trees)
            can_see_right, score_right = self.can_see_right(x, y, column, tree, trees)
            can_see_below, score_below = self.can_see_below(x, y, row, tree, trees)
            can_see_left, score_left = self.can_see_left(x, y, tree, trees)

            seeable_trees += can_see_above or can_see_right or can_see_below or can_see_left
            _scenic_score = score_above * score_right * score_below * score_left
            scenic_score = max(scenic_score, _scenic_score)

        self.verify_solution(seeable_trees)
        self.verify_solution_part_two(scenic_score)

    def can_see_above(self, x: int, y: int, tree: int, trees: dict[tuple[int, int], int]) -> tuple[bool, int]:
        count = 0
        for count, y_diff in enumerate(reversed(list(range(y))), start=1):
            if height := trees.get((x, y_diff)):
                if height >= tree:
                    return False, count

        return True, count

    def can_see_right(
        self, x: int, y: int, max_x: int, tree: int, trees: dict[tuple[int, int], int]
    ) -> tuple[bool, int]:
        count = 0
        for count, x_diff in enumerate(range(x + 1, max_x + 1), start=1):
            if height := trees.get((x_diff, y)):
                if height >= tree:
                    return False, count

        return True, count

    def can_see_below(
        self, x: int, y: int, max_y: int, tree: int, trees: dict[tuple[int, int], int]
    ) -> tuple[bool, int]:
        count = 0
        for count, y_diff in enumerate(range(y + 1, max_y + 1), start=1):
            if height := trees.get((x, y_diff)):
                if height >= tree:
                    return False, count

        return True, count

    def can_see_left(self, x: int, y: int, tree: int, trees: dict[tuple[int, int], int]) -> tuple[bool, int]:
        count = 0
        for count, x_diff in enumerate(reversed(list(range(x))), start=1):
            if height := trees.get((x_diff, y)):
                if height >= tree:
                    return False, count

        return True, count

    def _run(self):
        self.solve()
