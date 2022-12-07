from typing import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 6

    @property
    def case(self) -> int:
        return 1

    @property
    def test_input_data(self) -> Iterable:
        return iter(
            [
                {
                    1: "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
                    2: "bvwbjplbgvbhsrlpgdmjqwftvncz",
                    3: "nppdvjthqldpwncqszvftbrmjlhg",
                    4: "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
                    5: "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
                }[self.case]
            ]
        )

    @property
    def test_solution(self):
        return {1: 7, 2: 5, 3: 6, 4: 10, 5: 11}[self.case]

    @property
    def test_solution_part_two(self):
        return {1: 19, 2: 23, 3: 23, 4: 29, 5: 26}[self.case]

    @property
    def _solution(self):
        return 1623

    @property
    def _solution_part_two(self):
        return 3774

    def solve(self):
        datastream = next(self.input_data)

        start_of_packet_marker_location = None
        start_of_message_location = None

        for index in range(len(datastream)):
            if start_of_packet_marker_location is None:
                packet_letters = datastream[index : index + 4]
                if 4 == len(set(packet_letters)):
                    start_of_packet_marker_location = index + 4
            if start_of_message_location is None:
                message_letters = datastream[index : index + 14]
                if 14 == len(set(message_letters)):
                    start_of_message_location = index + 14

            if start_of_packet_marker_location is not None and start_of_message_location is not None:
                break

        self.verify_solution(start_of_packet_marker_location)
        self.verify_solution_part_two(start_of_message_location)

    def _run(self):
        self.solve()
