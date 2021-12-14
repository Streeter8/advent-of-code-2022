from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 13

    @property
    def test_input_data(self) -> Iterable:
        return [
            "6,10\n",
            "0,14\n",
            "9,10\n",
            "0,3\n",
            "10,4\n",
            "4,11\n",
            "6,0\n",
            "6,12\n",
            "4,1\n",
            "0,13\n",
            "10,12\n",
            "3,4\n",
            "3,0\n",
            "8,4\n",
            "1,10\n",
            "2,14\n",
            "8,10\n",
            "9,0\n",
            "\n",
            "fold along y=7\n",
            "fold along x=5\n",
        ]

    @property
    def test_solution(self) -> int:
        return 17

    def fold(self, coordinates: set[tuple[int, int]], fold: tuple[bool, int]) -> set[tuple[int, int]]:
        new_coordinates = set()
        if fold[0]:  # Fold along a vertical line
            for (x, y) in coordinates:
                if x >= fold[1]:
                    new_coordinates.add((x - 2 * (x - fold[1]), y))
                else:
                    new_coordinates.add((x, y))
        else:  # Fold along a horizontal line
            for (x, y) in coordinates:
                if y >= fold[1]:
                    new_coordinates.add((x, y - 2 * (y - fold[1])))
                else:
                    new_coordinates.add((x, y))

        return new_coordinates

    def solve(self):
        switch = True

        coordinates = set()
        folds = []
        for line in self.input_data_stripped():
            if not line:
                switch = False
                continue

            if switch:
                x, y = line.split(",")
                coordinates.add((int(x), int(y)))
            else:
                coordinate, value = line.replace("fold along ", "").split("=")
                folds.append((coordinate == "x", int(value)))

        result_coordinates = self.fold(coordinates, folds.pop(0))
        self.verify_solution(len(result_coordinates))

        for fold in folds:
            result_coordinates = self.fold(result_coordinates, fold)

        self.print_coordinates(result_coordinates)

    def print_coordinates(self, coordinates: set[tuple[int, int]]) -> None:
        for y in range(max(c[1] for c in coordinates) + 1):
            line = ""
            for x in range(max(c[0] for c in coordinates) + 1):
                line = f"{line}#" if (x, y) in coordinates else f"{line} "

            print(f"{line}\n")

    def _run(self):
        self.solve()
