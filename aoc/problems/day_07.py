from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 7

    @property
    def test_input_data(self) -> Iterable:
        return ["16,1,2,0,4,2,7,1,2,14\n"]

    @property
    def test_solution(self):
        return 37

    @property
    def test_solution_part_two(self):
        return 168

    def solve(self):
        crabs = list(self.single_line_csv_input(input_type=int))

        best_position_simple = 0
        best_fuel_simple = max(crabs) * len(crabs)

        best_position_complex = 0
        best_fuel_complex = max(crabs) * len(crabs) * 1000

        for position in range(min(crabs), max(crabs) + 1):
            fuel = 0
            fuel_complex = 0
            for crab in crabs:
                difference = abs(crab - position)
                fuel += difference
                fuel_complex += int((difference * (difference + 1)) / 2)

            if fuel < best_fuel_simple:
                best_fuel_simple = fuel
                best_position_simple = position

            if fuel_complex < best_fuel_complex:
                best_fuel_complex = fuel_complex
                best_position_complex = position

        print(f"Proposed best position simple: {best_position_simple}")
        self.verify_solution(best_fuel_simple)

        print(f"Proposed best position complex: {best_position_complex}")
        self.verify_solution_part_two(best_fuel_complex)

    def _run(self):
        self.solve()
