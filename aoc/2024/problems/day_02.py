from collections.abc import Iterable

from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 2

    @property
    def test_input_data(self) -> Iterable:
        return [
            "7 6 4 2 1\n",
            "1 2 7 8 9\n",
            "9 7 6 2 1\n",
            "1 3 2 4 5\n",
            "8 6 4 4 1\n",
            "1 3 6 7 9\n",
        ]

    @property
    def test_solution(self) -> int:
        return 2

    @property
    def test_solution_part_two(self):
        return 4

    @property
    def _solution(self) -> int:
        return 631

    @property
    def _solution_part_two(self):
        return 665

    def _run(self):
        reports = [Report(report) for report in self.input_data_stripped()]
        safe_reports = sum(report.is_safe for report in reports)
        self.verify_solution(safe_reports)

        reports = [Report(report) for report in self.input_data_stripped()]
        mostly_safe_reports = sum(report.is_mostly_safe for report in reports)
        self.verify_solution_part_two(mostly_safe_reports)


class Report:
    def __init__(self, report: str | list[int]):
        if isinstance(report, str):
            self.levels =  list(map(int, report.strip().split(" ")))
        else:
            self.levels = report

        current_reading = self.levels[0]
        next_reading = self.levels[1]

        self._is_safe = None

        change = next_reading - current_reading
        if change == 0:
            self._is_safe = False
            self.increasing = None
        else:
            self.increasing = change > 0

        self._is_safe = self.change_is_safe(change)

    def change_is_safe(self, change: int) -> bool:
        if self.increasing:
            return 0 < change < 4
        else:
            return -4 < change < 0

    @property
    def is_safe(self) -> bool:
        if self._is_safe is False:
            return False

        current_reading = self.levels[1]

        for index in range(2, len(self.levels)):
            next_reading = self.levels[index]
            change = next_reading - current_reading
            if not self.change_is_safe(change):
                return False

            current_reading = next_reading

        return True

    @property
    def is_mostly_safe(self) -> bool:
        if self._is_safe is False:
            return self.is_safe_with_one_less_level

        current_reading = self.levels[1]

        for index in range(2, len(self.levels)):
            next_reading = self.levels[index]
            change = next_reading - current_reading
            if not self.change_is_safe(change):
                return self.is_safe_with_one_less_level

            current_reading = next_reading

        return True

    @property
    def is_safe_with_one_less_level(self) -> bool:
        for index in range(len(self.levels)):
            new_levels = self.levels[:]
            new_levels.pop(index)
            report = Report(new_levels)
            if report.is_safe:
                return True

        return False
