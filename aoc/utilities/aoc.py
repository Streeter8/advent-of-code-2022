import pathlib
from collections.abc import Callable, Iterable
from timeit import timeit


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
    def test_solution(self):
        return None

    @property
    def test_solution_part_two(self):
        return None

    @property
    def _solution(self):
        return None

    @property
    def _solution_part_two(self):
        return None

    @property
    def solution(self):
        return self.test_solution if self.test else self._solution

    @property
    def solution_part_two(self):
        return self.test_solution_part_two if self.test else self._solution_part_two

    @property
    def input_data(self) -> Iterable:
        return self.test_input_data if self.test else self._input_data

    def input_data_stripped(self) -> Iterable:
        for datum in self.input_data:
            yield datum.rstrip()

    def single_line_csv_input(self, input_type: Callable) -> Iterable:
        for datum in ",".join(self.input_data_stripped()).split(","):
            yield input_type(datum)

    @property
    def _input_data(self):
        input_file_path = pathlib.Path(__file__).parents[1] / "inputs" / f"day_{self.z_day}.txt"

        with open(input_file_path) as input_file:
            for input_line in input_file:
                yield input_line

    def verify_solution(self, solution):
        _solution = self.solution
        if _solution is not None:
            if solution != _solution:
                raise AssertionError(f"{solution} != {_solution}")
            print(f"Part one solution verified: {solution}")
        else:
            print(f"Part one possible solution: {solution}")

    def verify_solution_part_two(self, solution=None):
        if solution is None:
            return

        _solution = self.solution_part_two
        if _solution is not None:
            if solution != _solution:
                raise AssertionError(f"{solution} != {_solution}")
            print(f"Part two solution verified: {solution}")
        else:
            print(f"Part two possible solution: {solution}")

    def run(self):
        number = 1
        execution_time = timeit(self._run, number=number) / number
        if execution_time < 1:
            milliseconds = execution_time * 1000
            print(f"Problem {self.day} took {round(milliseconds, 2)}ms to execute")
        else:
            print(f"Problem {self.day} took {round(execution_time, 3)} seconds to execute")

    def _run(self):
        raise NotImplementedError
