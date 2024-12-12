from collections.abc import Iterable
from typing import Self

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 11

    @property
    def _input_data(self):
        return [1950139, 0, 3, 837, 6116, 18472, 228700, 45]

    @property
    def test_input_data(self) -> Iterable:
        return [125, 17]

    @property
    def test_solution(self) -> int:
        return 55312

    @property
    def test_solution_part_two(self):
        return 65601038650482

    @property
    def _solution(self) -> int:
        return 235850

    @property
    def _solution_part_two(self) -> int:
        return 279903140844645

    def part_one(self):
        stones = [Stone(stone) for stone in self.input_data]
        number_of_stones = sum(stone.stones_after_steps(25) for stone in stones)
        self.verify_solution(number_of_stones)

    def part_two(self):
        stones = [Stone(stone) for stone in self.input_data]
        number_of_stones = sum(stone.stones_after_steps(75) for stone in stones)
        self.verify_solution_part_two(number_of_stones)

    def _run(self):
        self.part_one()
        self.part_two()


STEP_CACHE = {0: {1: 1}}


class Stone:
    def __init__(self, stone: int):
        self.stone = stone

    def stones_after_steps(self, steps: int) -> int:
        if result := STEP_CACHE.get(self.stone, {}).get(steps):
            return result

        if 0 == steps:
            return 1

        stones = self.get_stones()
        if 1 == steps:
            return len(stones)

        result = sum(stone.stones_after_steps(steps - 1) for stone in stones)
        if self.stone not in STEP_CACHE:
            STEP_CACHE[self.stone] = {steps: result}
        else:
            STEP_CACHE[self.stone][steps] = result

        return result

    def get_stones(self) -> list[Self]:
        if 0 == self.stone:
            return [Stone(1)]

        sstone = str(self.stone)
        len_sstone = len(sstone)
        if 0 == len_sstone % 2:
            half_len = len_sstone // 2
            return [Stone(int(sstone[:half_len])), Stone(int(sstone[half_len:]))]

        return [Stone(self.stone * 2024)]
