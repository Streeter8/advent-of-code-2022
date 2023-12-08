from typing import Iterable

from aoc.utilities.aoc import AocBase


class Directions:
    def __init__(self, directions: str):
        self._directions = directions.strip()
        self.directions = []

        characters = ""
        for character in self._directions:
            try:
                int(character)
                characters = f"{characters}{character}"
            except ValueError:
                # append integer
                self.directions.append(int(characters))
                # append direction turn
                self.directions.append(character)
                # reset characters
                characters = ""

        if characters:
            # append any remaining integers
            self.directions.append(int(characters))

    def __str__(self) -> str:
        return "".join(str(_) for _ in self.directions)


class Pipe:
    def __init__(self, initial_index: int, coordinates: list[bool]):
        self.initial_index = initial_index

        self.coordinates = coordinates
        self.length = len(self.coordinates)
        self.indexes = list(range(self.length))
        self.contains_wall = False in self.coordinates

        self.reversed_coordinates = list(reversed(coordinates))
        self.reversed_indexes = list(reversed(self.indexes))

    def move(self, start: int, steps: int, reverse_direction: bool) -> int:
        """
        direction: True if going left or down, False if going up or right
        """
        start = start - self.initial_index
        if reverse_direction:
            start = self.reversed_indexes[start]
            coordinates = self.reversed_coordinates
        else:
            coordinates = self.coordinates

        if self.contains_wall:
            # Rearrange pipe
            if start > 0:
                coordinates = coordinates[start:] + coordinates[:start]

            # find wall: index returns the left most index of the requested element
            first_wall = coordinates.index(False)
            # Set step count
            steps = first_wall - 1 if steps >= first_wall else steps

        new_index = (start + steps) % self.length

        return (self.reversed_indexes[new_index] if reverse_direction else new_index) + self.initial_index


class Map:
    def __init__(self, directions: Directions, lines: list[str]):
        self.directions = directions
        self.max_x = max(len(line) for line in lines)
        self.max_y = len(lines) - 1
        self.coordinates = {}

        self.x_pipes = {}
        self.y_pipes = {}

        y_pipes = {x: [] for x in range(self.max_x)}

        for y, line in enumerate(lines):
            x_pipe = []
            min_x = None
            for x, character in enumerate(line):
                if " " == character:
                    continue

                if min_x is None:
                    min_x = x

                if "." == character:
                    self.coordinates[(x, y)] = True
                    x_pipe.append(True)
                    y_pipes[x].append(True)
                elif "#" == character:
                    self.coordinates[(x, y)] = False
                    x_pipe.append(False)
                    y_pipes[x].append(False)
                else:
                    raise ValueError(f"Unexpected character found in map {character}")

            self.x_pipes[y] = Pipe(min_x, x_pipe)

        for x, pipe in y_pipes.items():
            min_y = min(y for y in (_y for _x, _y in self.coordinates if x == _x))
            self.y_pipes[x] = Pipe(min_y, pipe)

        self.start = (min(x for x, y in self.coordinates if y == self.max_y), self.max_y)
        self.current_position = self.start
        self.current_direction = "r"
        self.turns = {
            "L": {
                "l": "d",
                "d": "r",
                "r": "u",
                "u": "l",
            },
            "R": {
                "l": "u",
                "u": "r",
                "r": "d",
                "d": "l",
            },
        }
        self.facing = {
            "r": 0,
            "d": 1,
            "l": 2,
            "u": 3,
        }

    @property
    def horizontal(self) -> bool:
        return self.current_direction in ["l", "r"]

    @property
    def pipe_index(self) -> int:
        if self.horizontal:
            return self.current_position[1]
        else:
            return self.current_position[0]

    @property
    def current_index(self) -> int:
        if self.horizontal:
            return self.current_position[0]
        else:
            return self.current_position[1]

    @property
    def current_pipe(self) -> Pipe:
        if self.horizontal:
            return self.x_pipes[self.pipe_index]
        else:
            return self.y_pipes[self.pipe_index]

    @property
    def reverse_direction(self) -> bool:
        return self.current_direction in ["l", "d"]

    def turn(self, direction: str) -> None:
        self.current_direction = self.turns[direction][self.current_direction]

    @property
    def facing_value(self) -> int:
        return self.facing[self.current_direction]

    @property
    def password(self) -> int:
        password = (1000 * self.current_position[1]) + (4 * (self.current_position[0] + 1)) + self.facing_value
        print(f"Password: {self.current_position}; {self.current_direction}: {password}")
        row = (self.max_y - self.current_position[1]) + 1
        return (1000 * row) + (4 * (self.current_position[0] + 1)) + self.facing_value

    def print_wall(self):
        if "r" == self.current_direction:
            next_position = (
                self.current_position[0] + 1
            ) % self.current_pipe.length + self.current_pipe.initial_index, self.current_position[1]
        elif "d" == self.current_direction:
            next_position = (
                self.current_position[0],
                (self.current_position[1] - 1) % self.current_pipe.length + self.current_pipe.initial_index,
            )
        elif "l" == self.current_direction:
            next_position = (
                self.current_position[0] - 1
            ) % self.current_pipe.length + self.current_pipe.initial_index, self.current_position[1]
        else:
            next_position = (
                self.current_position[0],
                (self.current_position[1] + 1) % self.current_pipe.length + self.current_pipe.initial_index,
            )

        print(f"    {next_position} {'is a wall' if not self.coordinates[next_position] else 'is not a wall'}")

    def traverse(self) -> int:
        for i, direction in enumerate(self.directions.directions):
            print(f"\n\n==== Step {i} ====")
            if isinstance(direction, int):
                print(f"{self.current_position}: Moving {direction} steps in {self.current_direction} direction")
                new_index = self.current_pipe.move(self.current_index, direction, self.reverse_direction)
                if self.horizontal:
                    self.current_position = (new_index, self.current_position[1])
                else:
                    self.current_position = (self.current_position[0], new_index)
                print(f"    Moved to {self.current_position}")
                self.print_wall()
            elif isinstance(direction, str):
                print(f"Turning {direction} from {self.current_direction}")
                self.turn(direction)
                print(f"    Now facing {self.current_direction}")
            else:
                raise ValueError(f"Unexpected direction {direction}")

        return self.password

    @property
    def map(self) -> str:
        map = ""
        for y in reversed(list(range(self.max_y + 1))):
            line = ""
            for x in range(self.max_x):
                character = self.coordinates.get((x, y))
                if isinstance(character, bool):
                    line = f"{line}{'.' if character else '#'}"
                elif "." in line:
                    break
                else:
                    line = f"{line} "
            map = f"{map}{line}\n"

        return f"{map}\n{self.directions}\n"


class Side:
    pass
    # def __init__():
    #     pass


class CubeMap:
    def __init__(self, directions: Directions, lines: list[str]):
        pass


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 22

    @property
    def test_input_data(self) -> Iterable:
        return [
            "        ...#\n",
            "        .#..\n",
            "        #...\n",
            "        ....\n",
            "...#.......#\n",
            "........#...\n",
            "..#....#....\n",
            "..........#.\n",
            "        ...#....\n",
            "        .....#..\n",
            "        .#......\n",
            "        ......#.\n",
            "\n",
            "10R5L5R10L4R5L5\n",
        ]

    @property
    def test_solution(self):
        return 6032

    @property
    def test_solution_part_two(self):
        return 5031

    @property
    def _solution(self):
        return 89224

    @property
    def _solution_part_two(self):
        return None

    def part_one(self):
        lines = list(reversed(list(_.replace("\n", "") for _ in self.input_data)))
        directions = Directions(lines[0])
        map = Map(directions, lines[2:])
        print(map.map)

        password = map.traverse()

        self.verify_solution(password)

    def part_two(self):
        self.verify_solution_part_two(None)

    def _run(self):
        self.part_one()
        self.part_two()
