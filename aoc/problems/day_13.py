import json
from typing import Iterable, Optional, Union

from aoc.utilities.aoc import AocBase


def evaluate(left: Union[list, int], right: Union[list, int]) -> Optional[bool]:  # noqa: C901
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False

        return None

    if isinstance(left, list) and isinstance(right, list):
        for index, _left in enumerate(left):
            try:
                result = evaluate(_left, right[index])
            except IndexError:
                return False

            if isinstance(result, bool):
                return result

        if len(left) == len(right):
            return None
        else:
            # Left list is shorter
            return True

    if isinstance(left, list):
        return evaluate(left, [right])
    else:
        return evaluate([left], right)


class Pack:
    def __init__(self, line: str, *, divider: bool = False):
        self.pack = json.loads(line)
        self.divider = divider

    def __lt__(self, other: "Pack") -> bool:
        return evaluate(self.pack, other.pack)

    def __gt__(self, other: "Pack") -> bool:
        return not evaluate(self.pack, other.pack)


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 13

    @property
    def test_input_data(self) -> Iterable:
        return """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".splitlines()

    @property
    def test_solution(self):
        return 13

    @property
    def test_solution_part_two(self):
        return 140

    @property
    def _solution(self):
        return 5684

    def part_one(self):
        parings = list(self.input_data_stripped())
        correct = 0

        for index in range(int(len(parings) / 3) + 1):
            left, right = json.loads(parings[index * 3]), json.loads(parings[index * 3 + 1])
            if evaluate(left, right):
                correct += index + 1

        self.verify_solution(correct)

    def part_two(self):
        parings = list(self.input_data_stripped())
        packs = [Pack("[[2]]", divider=True), Pack("[[6]]", divider=True)]

        for index in range(int(len(parings) / 3) + 1):
            packs.append(Pack(parings[index * 3]))
            packs.append(Pack(parings[index * 3 + 1]))

        packs.sort()

        product = 1
        for index, pack in enumerate(packs, start=1):
            if pack.divider:
                product *= index

        self.verify_solution_part_two(product)

    def _run(self):
        self.part_one()
        self.part_two()
