from typing import Iterable

from aoc.utilities.aoc import AocBase


class Blueprint:
    def __init__(self, line: str):
        blueprint_id, blueprint = line.split(": ")

        self.blueprint_id = int(blueprint_id.split(" ")[1])

        ore, clay, obsidian, geode = (_.split("costs ")[1] for _ in blueprint.split(". "))

        self.ore = int(ore[0])
        self.clay = int(clay[0])
        self.obsidian_ore = int(obsidian[0])
        self.obsidian_clay = int(obsidian.split(" and ")[1].split(" clay")[0])
        self.geode_ore = int(geode[0])
        self.geode_obsidian = int(geode.split(" and ")[1].split(" obsidian")[0])


class Simulator:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0

        self.ore_robots = 1
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

    def simulate(self, minutes: int = 24) -> int:
        for minute in range(minutes):  # noqa: B007
            self.spend()

            self.ore += self.ore_robots
            self.clay += self.clay_robots
            self.obsidian += self.obsidian_robots
            self.geode += self.geode_robots

        return self.geode * self.blueprint.blueprint_id

    def spend(self) -> None:
        if self.blueprint.geode_ore <= self.ore and self.blueprint.geode_obsidian <= self.obsidian:
            self.geode_robots += 1
            self.ore -= self.blueprint.geode_ore
            self.obsidian -= self.blueprint.geode_obsidian
        elif (
            not self.geode_robots
            and self.blueprint.obsidian_ore <= self.ore
            and self.blueprint.obsidian_clay <= self.clay
        ):
            self.obsidian_robots += 1
            self.ore -= self.blueprint.obsidian_ore
            self.clay -= self.blueprint.obsidian_clay
        elif not self.obsidian_robots and not self.clay_robots and self.blueprint.clay <= self.ore:
            self.clay_robots += 1
            self.ore -= self.blueprint.clay
        elif (
            not self.geode_robots
            and not self.obsidian_robots
            and not self.clay_robots
            and self.blueprint.ore <= self.ore
        ):
            self.ore_robots += 1
            self.ore -= self.blueprint.ore


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 19

    @property
    def test_input_data(self) -> Iterable:
        return [
            (
                "Blueprint 1: "
                "Each ore robot costs 4 ore. "
                "Each clay robot costs 2 ore. "
                "Each obsidian robot costs 3 ore and 14 clay. "
                "Each geode robot costs 2 ore and 7 obsidian.\n"
            ),
            (
                "Blueprint 2: "
                "Each ore robot costs 2 ore. "
                "Each clay robot costs 3 ore. "
                "Each obsidian robot costs 3 ore and 8 clay. "
                "Each geode robot costs 3 ore and 12 obsidian.\n"
            ),
        ]

    @property
    def test_solution(self):
        return 33

    @property
    def test_solution_part_two(self):
        raise NotImplementedError

    def part_one(self):
        quality_levels = 0
        for line in self.input_data_stripped():
            simulator = Simulator(Blueprint(line))
            quality_levels += simulator.simulate(minutes=24)

        self.verify_solution(quality_levels)

    def part_two(self):
        self.verify_solution_part_two(None)

    def _run(self):
        self.part_one()
        self.part_two()
