from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 3

    @property
    def test_input_data(self) -> Iterable:
        return iter(
            [
                "00100\n",
                "11110\n",
                "10110\n",
                "10111\n",
                "10101\n",
                "01111\n",
                "00111\n",
                "11100\n",
                "10000\n",
                "11001\n",
                "00010\n",
                "01010\n",
            ]
        )

    @property
    def test_solution(self) -> int:
        return 198

    @property
    def test_solution_part_two(self) -> int:
        return 230

    def part_one(self):
        data = self.input_data_stripped()
        first_number = next(data)
        first_number = first_number.replace("\n", "")
        number_of_bits = len(first_number)

        positions = {index: {"0": 0, "1": 0} for index in range(number_of_bits)}

        for index, bit in enumerate(first_number):
            positions[index][bit] += 1

        for number in data:
            number = number.replace("\n", "")
            for index, bit in enumerate(number):
                positions[index][bit] += 1

        gamma_values = []
        epsilon_values = []
        for index in range(number_of_bits):
            value = positions[index]
            if value["0"] > value["1"]:
                gamma_values.append("0")
                epsilon_values.append("1")
            elif value["1"] > value["0"]:
                gamma_values.append("1")
                epsilon_values.append("0")
            else:
                raise ValueError(f"zero and one counts are equal: {index}")

        gamma_rate = int("".join(gamma_values), 2)
        epsilon_rate = int("".join(epsilon_values), 2)
        solution = gamma_rate * epsilon_rate
        self.verify_solution(solution)

    def part_two(self):
        oxygen_rating = self.get_oxygen_rating()
        co2_rating = self.get_co2_rating()
        life_support_rating = oxygen_rating * co2_rating

        self.verify_solution_part_two(life_support_rating)

    def get_oxygen_rating(self):
        data = list(self.input_data_stripped())
        index = 0
        while len(data) > 1:
            data = self.reduce_oxygen_rating(data, index)
            index += 1

        return int(data[0], 2)

    def reduce_oxygen_rating(self, data: Iterable, index: int):
        values = {"0": [], "1": []}
        for datum in data:
            values[datum[index]].append(datum)

        return values["0"] if len(values["0"]) > len(values["1"]) else values["1"]

    def get_co2_rating(self):
        data = list(self.input_data_stripped())
        index = 0
        while len(data) > 1:
            data = self.reduce_co2_rating(data, index)
            index += 1

        return int(data[0], 2)

    def reduce_co2_rating(self, data: Iterable, index: int):
        values = {"0": [], "1": []}
        for datum in data:
            values[datum[index]].append(datum)

        if len(values["0"]) == len(values["1"]):
            print("break")

        return values["1"] if len(values["1"]) < len(values["0"]) else values["0"]

    def _run(self):
        self.part_one()
        self.part_two()
