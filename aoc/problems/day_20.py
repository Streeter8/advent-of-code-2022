from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 20

    @property
    def test_input_data(self) -> Iterable:
        return ["1\n", "2\n", "-3\n", "3\n", "-2\n", "0\n", "4\n", "\n"]

    @property
    def test_solution(self):
        return 3

    @property
    def test_solution_part_two(self):
        return 1623178306

    @property
    def _solution(self):
        return 6387

    @property
    def _solution_part_two(self):
        return 2455057187825

    def mix(self, encrypted_gps, decrypting_gps, gps_length):
        for value in encrypted_gps:
            if 0 == value[1]:
                continue

            position = decrypting_gps.index(value)
            new_position = position + value[1]
            if new_position < 0 or gps_length < new_position:
                new_position = new_position % (gps_length - 1)

            # Values being placed at index 0 default to being placed at the end
            if 0 == new_position:
                new_position = gps_length

            del decrypting_gps[position]
            decrypting_gps.insert(new_position, value)

    def get_grove_coordinates(self, decrypting_gps, gps_length):
        decrypted_gps = [value for _, value in decrypting_gps]
        zero_index = decrypted_gps.index(0)

        return (
            decrypted_gps[(zero_index + 1000) % gps_length]
            + decrypted_gps[(zero_index + 2000) % gps_length]
            + decrypted_gps[(zero_index + 3000) % gps_length]
        )

    def part_one(self):
        # Numbers are not unique, so an index/ID is added to track which number each one actually is
        encrypted_gps = [(index, int(value)) for index, value in enumerate(self.input_data_stripped()) if value]
        decrypting_gps = [_ for _ in encrypted_gps]
        gps_length = len(encrypted_gps)

        self.mix(encrypted_gps, decrypting_gps, gps_length)

        grove_coordinates_sum = self.get_grove_coordinates(decrypting_gps, gps_length)
        self.verify_solution(grove_coordinates_sum)

    def part_two(self):
        decryption_key = 811589153

        encrypted_gps = [
            (index, int(value) * decryption_key) for index, value in enumerate(self.input_data_stripped()) if value
        ]
        decrypting_gps = [_ for _ in encrypted_gps]
        gps_length = len(encrypted_gps)

        for _ in range(10):
            self.mix(encrypted_gps, decrypting_gps, gps_length)

        grove_coordinates_sum = self.get_grove_coordinates(decrypting_gps, gps_length)
        self.verify_solution_part_two(grove_coordinates_sum)

    def _run(self):
        self.part_one()
        self.part_two()
