from typing import Iterable

from aoc.utilities.aoc import AocBase


class Component:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

        self.north_shape = None
        self.south_shape = None
        self.east_shape = None
        self.west_shape = None
        self.up_shape = None
        self.down_shape = None

        self.northern_shape = None
        self.southern_shape = None
        self.eastern_shape = None
        self.western_shape = None
        self.upern_shape = None
        self.downern_shape = None

    @property
    def component_sides(self) -> Iterable["Component"]:
        return (self.north_shape, self.south_shape, self.east_shape, self.west_shape, self.up_shape, self.down_shape)

    @property
    def ern_sides(self) -> Iterable["Component"]:
        return (
            self.northern_shape,
            self.southern_shape,
            self.eastern_shape,
            self.western_shape,
            self.upern_shape,
            self.downern_shape,
        )

    @property
    def coordinates(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z

    def up(self, offset: int = 1) -> tuple[int, int, int]:
        return self.x, self.y, self.z + offset

    def down(self, offset: int = 1) -> tuple[int, int, int]:
        return self.x, self.y, self.z - offset

    def north(self, offset: int = 1) -> tuple[int, int, int]:
        return self.x, self.y + offset, self.z

    def south(self, offset: int = 1) -> tuple[int, int, int]:
        return self.x, self.y - offset, self.z

    def east(self, offset: int = 1) -> tuple[int, int, int]:
        return self.x + offset, self.y, self.z

    def west(self, offset: int = 1) -> tuple[int, int, int]:
        return self.x - offset, self.y, self.z

    @property
    def exposed_sides(self) -> Iterable["Component"]:
        return (_ for _ in self.component_sides if not _)

    @property
    def sides(self) -> int:
        return sum(1 for _ in self.exposed_sides)

    @property
    def noninternal_sides(self) -> Iterable["Component"]:
        # return (_ for _ in self.ern_sides if not _)
        return list(_ for _ in self.ern_sides if _ is True)

    @property
    def external_sides(self) -> int:
        return sum(1 for _ in self.noninternal_sides)


class Shape:
    def __init__(self, lines: Iterable[str]):  # noqa: C901
        _coordinates = set(tuple(int(_) for _ in line.split(",")) for line in lines)
        self.coordinates = {_: Component(*_) for _ in _coordinates}

        for component in self.coordinates.values():
            if shape := self.coordinates.get(component.up()):
                component.up_shape = shape
                component.upern_shape = shape
            if shape := self.coordinates.get(component.down()):
                component.down_shape = shape
                component.downern_shape = shape
            if shape := self.coordinates.get(component.north()):
                component.north_shape = shape
                component.northern_shape = shape
            if shape := self.coordinates.get(component.south()):
                component.south_shape = shape
                component.southern_shape = shape
            if shape := self.coordinates.get(component.east()):
                component.east_shape = shape
                component.eastern_shape = shape
            if shape := self.coordinates.get(component.west()):
                component.west_shape = shape
                component.western_shape = shape

        min_x = min(_[0] for _ in self.coordinates)
        min_y = min(_[1] for _ in self.coordinates)
        min_z = min(_[2] for _ in self.coordinates)

        max_x = max(_[0] for _ in self.coordinates)
        max_y = max(_[1] for _ in self.coordinates)
        max_z = max(_[2] for _ in self.coordinates)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    if component := self.coordinates.get((x, y, z)):
                        component.downern_shape = True
                        break

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                zs = list(range(min_z, max_z + 1))
                zs.reverse()
                for z in zs:
                    if component := self.coordinates.get((x, y, z)):
                        component.upern_shape = True
                        break

        for x in range(min_x, max_x + 1):
            for z in range(min_z, max_z + 1):
                for y in range(min_y, max_y + 1):
                    if component := self.coordinates.get((x, y, z)):
                        component.southern_shape = True
                        break

        for x in range(min_x, max_x + 1):
            for z in range(min_z, max_z + 1):
                ys = list(range(min_y, max_y + 1))
                ys.reverse()
                for y in ys:
                    if component := self.coordinates.get((x, y, z)):
                        component.northern_shape = True
                        break

        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                for x in range(min_x, max_x + 1):
                    if component := self.coordinates.get((x, y, z)):
                        component.western_shape = True
                        break

        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                xs = list(range(min_x, max_x + 1))
                xs.reverse()
                for x in xs:
                    if component := self.coordinates.get((x, y, z)):
                        component.eastern_shape = True
                        break

        #
        # for component in self.coordinates.values():
        #     if component.upern_shape is None:
        #         for z in range(component.z, max_z):
        #             if shape := self.coordinates.get(component.up(z + 1)):
        #                 component.upern_shape = shape
        #
        #     if component.downern_shape is None:
        #         for z in range(min_z, component.z):
        #             if shape := self.coordinates.get((component.x, component.y, z)):
        #                 component.downern_shape = shape
        #
        #     if component.northern_shape is None:
        #         for y in range(component.y, max_y):
        #             if shape := self.coordinates.get(component.north(y + 1)):
        #                 component.northern_shape = shape
        #
        #     if component.southern_shape is None:
        #         for y in range(min_y, component.y):
        #             if shape := self.coordinates.get((component.x, y, component.z)):
        #                 component.southern_shape = shape
        #
        #     if component.eastern_shape is None:
        #         for x in range(component.x, max_x):
        #             if shape := self.coordinates.get(component.east(x + 1)):
        #                 component.eastern_shape = shape
        #
        #     if component.western_shape is None:
        #         for x in range(min_x, component.x):
        #             if shape := self.coordinates.get((x, component.y, component.z)):
        #                 component.western_shape = shape

    @property
    def sides(self) -> int:
        return sum(_.sides for _ in self.coordinates.values())

    @property
    def external_sides(self) -> int:
        return sum(_.external_sides for _ in self.coordinates.values())


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 18

    @property
    def test_input_data(self) -> Iterable:
        return [
            "2,2,2\n",
            "1,2,2\n",
            "3,2,2\n",
            "2,1,2\n",
            "2,3,2\n",
            "2,2,1\n",
            "2,2,3\n",
            "2,2,4\n",
            "2,2,6\n",
            "1,2,5\n",
            "3,2,5\n",
            "2,1,5\n",
            "2,3,5\n",
        ]

    @property
    def test_solution(self):
        return 64

    @property
    def test_solution_part_two(self):
        return 58

    @property
    def _solution(self):
        return 3498

    @property
    def _solution_part_two(self):
        return None

    def solve(self):
        shape = Shape(self.input_data_stripped())
        self.verify_solution(shape.sides)

        sides = shape.external_sides
        # That's not the right answer; your answer is too low. 1686
        # That's not the right answer; your answer is too high. 2090
        assert 1686 < sides < 2090
        self.verify_solution_part_two(sides)

    def _run(self):
        self.solve()
