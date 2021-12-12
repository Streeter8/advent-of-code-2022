from typing import Iterable

from aoc.utilities.aoc import AocBase


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.small = not name.isupper()
        self.start = "start" == name
        self.end = "end" == name
        self.connections = set()

    def add_connection(self, cave):
        self.connections.add(cave)


class Aoc(AocBase):
    TEST = 3

    def __init__(self, test: bool):
        super().__init__(test)

        self.start = Cave("start")
        self.caves: dict[str, Cave] = {"start": self.start, "end": Cave("end")}

    @property
    def day(self) -> int:
        return 12

    @property
    def test_solution(self) -> int:
        match self.TEST:
            case 1:
                return 10
            case 2:
                return 19
            case 3:
                return 226

    @property
    def test_solution_part_two(self):
        match self.TEST:
            case 1:
                return 36
            case 2:
                return 103
            case 3:
                return 3509

    def get_cave(self, name: str) -> Cave:
        if name in self.caves:
            return self.caves[name]
        else:
            cave = Cave(name)
            self.caves[name] = cave

            return cave

    def create_map(self) -> None:
        for line in self.input_data_stripped():
            a, b = line.split("-")

            cave_a = self.get_cave(a)
            cave_b = self.get_cave(b)

            if not cave_b.start:
                cave_a.add_connection(cave_b)
            if not cave_a.start:
                cave_b.add_connection(cave_a)

    def get_number_of_paths(self, cave: Cave, current_path: list[str], duplicate_small_path: bool) -> int:
        if cave.end:
            # print(f"Found path: {','.join(current_path + [cave.name])}")
            return 1

        if cave.small and cave.name in current_path:
            if duplicate_small_path:
                return 0
            else:
                duplicate_small_path = True

        return sum(
            self.get_number_of_paths(connection, current_path + [cave.name], duplicate_small_path)
            for connection in cave.connections
        )

    def solve(self):
        self.create_map()

        self.verify_solution(self.get_number_of_paths(self.start, [], True))
        self.verify_solution_part_two(self.get_number_of_paths(self.start, [], False))

    def _run(self):
        self.solve()

    @property
    def input_data(self) -> Iterable:
        if not self.test:
            return [
                "ma-start",
                "YZ-rv",
                "MP-rv",
                "vc-MP",
                "QD-kj",
                "rv-kj",
                "ma-rv",
                "YZ-zd",
                "UB-rv",
                "MP-xe",
                "start-MP",
                "zd-end",
                "ma-UB",
                "ma-MP",
                "UB-xe",
                "end-UB",
                "ju-MP",
                "ma-xe",
                "zd-UB",
                "start-xe",
                "YZ-end",
            ]
        else:
            match self.TEST:
                case 1:
                    return ["start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"]
                case 2:
                    return [
                        "dc-end",
                        "HN-start",
                        "start-kj",
                        "dc-start",
                        "dc-HN",
                        "LN-dc",
                        "HN-end",
                        "kj-sa",
                        "kj-HN",
                        "kj-dc",
                    ]
                case 3:
                    return [
                        "fs-end",
                        "he-DX",
                        "fs-he",
                        "start-DX",
                        "pj-DX",
                        "end-zg",
                        "zg-sl",
                        "zg-pj",
                        "pj-he",
                        "RW-he",
                        "fs-DX",
                        "pj-RW",
                        "zg-RW",
                        "start-pj",
                        "he-WI",
                        "zg-he",
                        "pj-fs",
                        "start-RW",
                    ]
