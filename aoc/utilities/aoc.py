import pathlib
from timeit import timeit
from typing import Iterable


class AocBase:
    def __init__(self, test: bool = False):
        self.test = test

    @property
    def day(self) -> int:
        raise not NotImplementedError

    @property
    def z_day(self) -> str:
        return str(self.day).zfill(2)

    @property
    def test_input_data(self) -> Iterable:
        raise NotImplementedError

    @property
    def input_data(self) -> Iterable:
        if self.test:
            return self.test_input_data

        input_file_path = pathlib.Path(__file__).parents[1] / "inputs" / f"day_{self.z_day}.txt"

        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line

    def run(self):
        print(f"Problem {self.day} took {timeit(self._run, number=1)} seconds to execute")

    def _run(self):
        raise NotImplementedError
