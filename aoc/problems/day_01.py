from aoc.utilities.aoc import AocBase


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 1

    @property
    def test_data(self) -> list[str]:
        return ["199", "200", "208", "210", "200", "207", "240", "269", "260", "263"]

    @property
    def test_solution(self) -> int:
        return 7

    def _run(self):
        pass
