from collections.abc import Iterable
from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo

from aoc.utilities.aoc import AocBase

CENTRAL = ZoneInfo("US/Central")


def now() -> str:
    return datetime.now(CENTRAL).isoformat()


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
        raise NotImplementedError

    @property
    def _solution(self) -> int:
        return 235850

    @property
    def _solution_part_two(self):
        return None

    def part_one(self):
        arrangement = StoneArrangement(self.input_data)
        arrangement.blinks(25)
        self.verify_solution(len(arrangement.stones))

    def part_two(self):
        arrangement = StoneArrangement(self.input_data)
        arrangement.blinks(75)
        self.verify_solution_part_two(len(arrangement.stones))

    def _run(self):
        self.part_one()
        self.part_two()


class StoneArrangement:
    def __init__(self, stones: list[int]):
        self.stones = stones

    def blink(self):
        new_stones = []
        for stone in self.stones:
            new_stones.extend(self.get_new_stones(stone))

        self.stones = new_stones

    @lru_cache(None)
    def get_new_stones(self, stone: int) -> list[int]:
        if 0 == stone:
            return [1]

        sstone = str(stone)
        len_sstone = len(sstone)
        if 0 == len_sstone % 2:
            half_len = len_sstone // 2
            return [int(sstone[:half_len]), int(sstone[half_len:])]

        return [stone * 2024]

    def blinks(self, times: int):
        for times_blinked in range(1, times + 1):
            self.blink()
            print(f"{now()}: {times_blinked} | Stone Count: {len(self.stones)}")
