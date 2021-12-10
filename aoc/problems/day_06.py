from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 6

    @property
    def test_input_data(self) -> Iterable:
        return ["3,4,3,1,2\n"]

    @property
    def test_solution(self) -> int:
        return 5934

    @property
    def test_solution_part_two(self) -> int:
        return 26984457539

    def new_fish(self) -> dict:
        return {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

    def solve(self):
        fishes = self.new_fish()
        for fish in self.single_line_csv_input(input_type=int):
            fishes[fish] += 1

        for _day in range(256):
            new_fish = self.new_fish()
            new_fish[8] = fishes[0]
            new_fish[7] = fishes[8]
            new_fish[6] = fishes[7] + fishes[0]
            new_fish[5] = fishes[6]
            new_fish[4] = fishes[5]
            new_fish[3] = fishes[4]
            new_fish[2] = fishes[3]
            new_fish[1] = fishes[2]
            new_fish[0] = fishes[1]
            fishes = new_fish

            if _day == 79:
                self.verify_solution(sum(fishes.values()))

        self.verify_solution_part_two(sum(fishes.values()))

    def _run(self):
        self.solve()
