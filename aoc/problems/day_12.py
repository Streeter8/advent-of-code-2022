import sys
from typing import Iterable, Optional

from aoc.utilities.aoc import AocBase

sys.setrecursionlimit(25000)
HEIGHTS = {l: h for h, l in enumerate("SabcdefghijklmnopqrstuvwxyzE")}


class Height(object):
    def __init__(
        self,
        x: int,
        y: int,
        letter: str,
        *,
        north: Optional["Height"] = None,
        east: Optional["Height"] = None,
        south: Optional["Height"] = None,
        west: Optional["Height"] = None,
    ):
        self.x = x
        self.y = y
        self.letter = letter
        self.height = HEIGHTS[letter]

        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.cost_to_end = 0 if self.is_end else None
        self.cheapest_node = None
        self.path_to_end = [] if self.is_end else None

    @property
    def adjacents(self) -> list["Height"]:
        adjacents = []
        for adjacent in [self.north, self.east, self.south, self.west]:
            if not adjacent:
                continue

            if adjacent.height > self.height:
                adjacents = [adjacent] + adjacents
            else:
                adjacents.append(adjacent)

        return adjacents

    def paths(self, paths: set["Height"]) -> Iterable[tuple["Height", set["Height"]]]:
        for adjacent in self.adjacents:
            if adjacent.coordinates in paths:
                continue

            # yield adjacent, paths + [adjacent.coordinates]
            yield adjacent, paths | {adjacent.coordinates}

    def cost(self, other: "Height") -> int:
        if abs(other.height - self.height) <= 1:
            return 1

        return 999999

    def set_cost_to_end(self) -> None:
        if (2, 3) == self.coordinates:
            print("break")
        for node in self.adjacents:
            if node.coordinates in self.path_to_end:
                continue

            cost_to_move = self.cost(node)
            new_cost = self.cost_to_end + cost_to_move

            if node.cost_to_end is None:
                node.cost_to_end = new_cost
                node.path_to_end = self.path_to_end + [self.coordinates]
                self.cheapest_node = node
            elif self.cost_to_end < new_cost:
                node.cost_to_end = new_cost
                self.cheapest_node = node

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def is_start(self) -> bool:
        return "S" == self.letter

    @property
    def is_end(self) -> bool:
        return "E" == self.letter


class Mountain:
    def __init__(self, heightmap: list[str]):
        self.start = None
        self.end = None
        self.map = {}

        x_max = len(heightmap[0]) - 1
        y_max = len(heightmap) - 1
        max_cost = (x_max + 1) * (y_max + 1) + 1  # noqa: F841

        self.deadends = set()
        self.path = set()

        for y, line in enumerate(heightmap):
            if not line:
                continue

            for x, letter in enumerate(line):
                height = Height(x, y, letter)
                self.map[height.coordinates] = height

                if height.is_start:
                    self.start = height
                elif height.is_end:
                    self.end = height

                if x > 0:
                    west = self.map[x - 1, y]
                    # if west.height == height.height:
                    #     height.west = west
                    #     west.east = height
                    # elif west.height + 1 == height.height:
                    #     west.east = height
                    # elif west.height - 1 == height.height:
                    #     height.west = west
                    if height.height in [west.height - 1, west.height, west.height + 1]:
                        west.east = height
                        height.west = west

                if y > 0:
                    north = self.map[x, y - 1]
                    if height.height in [north.height - 1, north.height, north.height + 1]:
                        north.south = height
                        height.north = north

    def solve(self):
        path = self.search(self.end)
        return len(path)

    def search(self, current_node: Height) -> Optional[set[tuple[int, int]]]:
        if current_node.is_start:
            return current_node

        current_node.set_cost_to_end()
        return self.search(current_node.cheapest_node)


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 12

    @property
    def test_input_data(self) -> Iterable:
        return ["Sabqponm\n", "abcryxxl\n", "accszExk\n", "acctuvwj\n", "abdefghi\n"]

    @property
    def test_solution(self):
        return 31

    @property
    def test_solution_part_two(self):
        raise NotImplementedError

    def part_one(self):
        lines = list(_ for _ in self.input_data_stripped() if _)
        # lines.reverse()

        mountain = Mountain(lines)
        path_length = mountain.solve()

        self.verify_solution(path_length)

    def part_two(self):
        self.verify_solution_part_two(None)

    def _run(self):
        self.part_one()
        self.part_two()
