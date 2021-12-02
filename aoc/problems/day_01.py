from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_input_data(self) -> Iterable:
        return iter(f"{x}\n" for x in [199, 200, 208, 210, 200, 207, 240, 269, 260, 263])

    @property
    def test_solution(self) -> int:
        return 7

    @property
    def test_solution_part_two(self) -> int:
        return 5

    def part_one(self):
        increase = 0
        no_change = 0
        decrease = 0

        previous = None
        data = self.input_data
        for depth in data:
            depth = int(depth.replace("\n", ""))
            if previous is None:
                previous = depth
                continue

            if depth > previous:
                increase += 1
            elif depth == previous:
                no_change += 1
            else:
                decrease += 1

            previous = depth

        print("=== Part One solution ===")
        print(f"Increases: {increase}")
        print(f"no_change: {no_change}")
        print(f"decrease: {decrease}")
        print("=========================")

        self.verify_solution(increase)

    def part_two(self):
        increase = 0
        no_change = 0
        decrease = 0

        previous = []
        for depth in self.input_data:
            depth = int(depth.replace("\n", ""))
            if len(previous) < 3:
                previous.append(depth)
                continue

            current = previous[1] + previous[2] + depth
            sum_previous = sum(previous)
            if current > sum_previous:
                increase += 1
            elif current == sum_previous:
                no_change += 1
            else:
                decrease += 1

            previous = [previous[1], previous[2], depth]

        print("=== Part Two solution ===")
        print(f"Increases: {increase}")
        print(f"no_change: {no_change}")
        print(f"decrease: {decrease}")
        print("=========================")

        self.verify_solution_part_two(increase)

    def _run(self):
        self.part_one()
        self.part_two()
