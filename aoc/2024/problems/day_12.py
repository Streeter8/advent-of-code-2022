from collections.abc import Iterable
from itertools import product
from typing import Self

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 12

    @property
    def test_input_data(self) -> Iterable:
        return [
            "RRRRIICCFF\n",
            "RRRRIICCCF\n",
            "VVRRRCCFFF\n",
            "VVRCCCJFFF\n",
            "VVVVCJJCFE\n",
            "VVIVCCJJEE\n",
            "VVIIICJJEE\n",
            "MIIIIIJJEE\n",
            "MIIISIJEEE\n",
            "MMMISSJEEE\n",
        ]

    @property
    def test_solution(self) -> int:
        return 1930

    @property
    def test_solution_part_two(self) -> int:
        return 1206

    @property
    def _solution(self) -> int:
        return 1375574

    @property
    def _solution_part_two(self) -> int:
        return 830566

    def _run(self):
        land_map = Map.from_input(self.input_data_stripped())
        self.verify_solution(land_map.fencing_cost)
        self.verify_solution_part_two(land_map.bulk_fencing_cost)


def add(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] + tuple_two[0], tuple_one[1] + tuple_two[1]


def sub(tuple_one: tuple[int, int], tuple_two: tuple[int, int]) -> tuple[int, int]:
    return tuple_one[0] - tuple_two[0], tuple_one[1] - tuple_two[1]

NORTH = (0, 1)
EAST = (1, 0)
SOUTH = (0, -1)
WEST = (-1, 0)

TURNS = (NORTH, EAST, SOUTH, WEST)
PERPENDICULAR_TURNS = {
    NORTH: [EAST, WEST],
    EAST: [NORTH, SOUTH],
    SOUTH: [EAST, WEST],
    WEST: [NORTH, SOUTH],
}


def adjacent_coordinates(coordinates: tuple[int, int]) -> list[tuple[int, int]]:
    return [add(coordinates, turn) for turn in TURNS]


class Region:
    def __init__(self, initial_coordinates: set[tuple[int, int]], character: str):
        self.coordinates = initial_coordinates
        self.character = character
        self.sides = {turn: [] for turn in TURNS}

    @property
    def fencing_cost(self) -> int:
        return self.perimeter * self.area

    @property
    def bulk_fencing_cost(self) -> int:
        # print(
        #     f"A region of {self.character} plants with price "
        #     f"{self.area} * {self.number_of_sides} = {self.number_of_sides * self.area}."
        # )
        return self.number_of_sides * self.area

    @property
    def perimeter(self) -> int:
        perimeter = 0
        for coordinates in self.coordinates:
            for _adjacent_coordinates in adjacent_coordinates(coordinates):
                if _adjacent_coordinates not in self.coordinates:
                    perimeter += 1

        return perimeter

    @property
    def number_of_sides(self) -> int:
        all_sides = {turn: [] for turn in TURNS}
        for coordinates in self.coordinates:
            for turn in TURNS:
                if any(coordinates in side for side in all_sides[turn]):
                    continue

                _adjacent_coordinates = add(coordinates, turn)
                if _adjacent_coordinates not in self.coordinates:
                    added = False
                    for sides in all_sides[turn]:
                        for pturn in PERPENDICULAR_TURNS:
                            if add(coordinates, pturn) in sides:
                                sides.add(coordinates)
                                added = True

                    if not added:
                        all_sides[turn].append({coordinates})

        combined_sides = {}
        for coordinates, sides in all_sides.items():
            if len(sides) > 1:
                combined_sides[coordinates] = self.combine_sides(sides)
            else:
                combined_sides[coordinates] = sides

        return sum(len(sides) for sides in combined_sides.values())

    def combine_sides(self, all_sides: list[set[tuple[int, int]]]) -> list[set[tuple[int, int]]]:
        for side_one, side_two in product(all_sides, repeat=2):
            if side_one is side_two:
                continue

            if side_one.intersection(side_two):
                new_sides = [side for side in all_sides if side is not side_one and side is not side_two]
                new_sides.append(side_one.union(side_two))
                return self.combine_sides(new_sides)

        return all_sides

    @property
    def area(self) -> int:
        return len(self.coordinates)

    def is_part_of_region(self, potential_coordinates: tuple[int, int], character: str) -> bool:
        if character != self.character:
            return False

        if potential_coordinates in self.coordinates:
            return True

        for coordinates in self.coordinates:
            if sub(coordinates, potential_coordinates) in TURNS:
                return True

        return False

    def add_coordinates(self, new_coordinates: tuple[int, int]) -> None:
        self.coordinates.add(new_coordinates)

    @classmethod
    def combine_regions(cls, region_one: Self, region_two: Self) -> Self | None:
        if region_one.character != region_two.character:
            return None

        for coordinates in region_one.coordinates:
            for _adjacent_coordinates in adjacent_coordinates(coordinates):
                if _adjacent_coordinates in region_two.coordinates:
                    return Region(region_one.coordinates.union(region_two.coordinates), region_one.character)




class Map:
    def __init__(
        self,
        land_map: dict[tuple[int, int], str],
    ):
        self.land_map = land_map
        self.regions = {}

        self.row_count = max(y for _, y in land_map) + 1
        self.column_count = max(x for x, _ in land_map) + 1

        self.assess_regions()

    @classmethod
    def from_input(cls, lines: Iterable[str]) -> Self:
        lines = list(lines)
        lines.reverse()
        land_map = {}

        for row, line in enumerate(lines):
            for column, character in enumerate(line):
                land_map[(column, row)] = character

        return cls(land_map)

    @property
    def map(self) -> str:
        land_map = ""
        for row in reversed(range(self.row_count)):
            line = ""
            for column in range(self.column_count):
                line = f"{line}{self.land_map[(column, row)]}"

            land_map = f"{land_map}{line}\n"

        return land_map

    @property
    def fencing_cost(self) -> int:
        return sum(sum(region.fencing_cost for region in regions) for regions in self.regions.values())

    @property
    def bulk_fencing_cost(self) -> int:
        return sum(sum(region.bulk_fencing_cost for region in regions) for regions in self.regions.values())

    def assess_regions(self) -> None:
        regions = {}
        for coordinates, character in self.land_map.items():
            for region in regions.get(character) or []:
                if region.is_part_of_region(coordinates, character):
                    region.add_coordinates(coordinates)
                    break
            else:
                if character not in regions:
                    regions[character] = [Region({coordinates}, character)]
                else:
                    regions[character].append(Region({coordinates}, character))

        self.regions = self.combine_regions(regions)

    def combine_regions(self, regions: dict[str, list[Region]]) -> dict[str, list[Region]]:
        new_regions = {}
        for character, character_regions in regions.items():
            if len(character_regions) > 1:
                new_regions[character] = self._combine_regions(character_regions)
            else:
                new_regions[character] = character_regions

        return new_regions

    def _combine_regions(self, regions: list[Region]) -> list[Region]:
        for region_one, region_two in product(regions, repeat=2):
            if region_one is region_two:
                continue

            if new_region := Region.combine_regions(region_one, region_two):
                new_regions = [region for region in regions if region is not region_one and region is not region_two]
                new_regions.append(new_region)
                return self._combine_regions(new_regions)

        return regions

    def print_map(self) -> None:
        print(self.map)
