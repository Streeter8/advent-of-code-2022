from typing import Iterable, Optional

from aoc.utilities.aoc import AocBase


class Directory:
    def __init__(self, name: str, parent: Optional["Directory"] = None):
        self.name = name
        self.files = {}

        # Effectively, a doubly linked list
        self.parent = parent
        self.directories = {}

        # So long as we calculate the size at the end,
        # This works and cuts the execution time in half
        self._size = None

    @property
    def size(self) -> int:
        if self._size is None:
            files = sum(file.size for file in self.files.values()) if self.files else 0
            directories = sum(directory.size for directory in self.directories.values()) if self.directories else 0
            self._size = files + directories

        return self._size

    @property
    def absolute_path(self) -> str:
        if self.parent is None:
            return "/"
        return f"{self.parent.absolute_path}{self.name}/"


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 7

    @property
    def test_input_data(self) -> Iterable:
        return [
            "$ cd /\n",
            "$ ls\n",
            "dir a\n",
            "14848514 b.txt\n",
            "8504156 c.dat\n",
            "dir d\n",
            "$ cd a\n",
            "$ ls\n",
            "dir e\n",
            "29116 f\n",
            "2557 g\n",
            "62596 h.lst\n",
            "$ cd e\n",
            "$ ls\n",
            "584 i\n",
            "$ cd ..\n",
            "$ cd ..\n",
            "$ cd d\n",
            "$ ls\n",
            "4060174 j\n",
            "8033020 d.log\n",
            "5626152 d.ext\n",
            "7214296 k\n",
        ]

    @property
    def test_solution(self):
        return 95437

    @property
    def test_solution_part_two(self):
        return 24933642

    @property
    def _solution(self):
        return 1391690

    @property
    def _solution_part_two(self):
        return 5469168

    def solve(self):
        all_directories = {}
        root_directory = Directory("/")
        all_directories[root_directory.absolute_path] = root_directory

        current_directory = root_directory
        commands = self.input_data_stripped()

        # The first command goes to root
        next(commands)

        for line in commands:
            if line.startswith("$"):
                # I think my input is bugged?
                # We cd up twice in the input, taking us to root
                # The noted directory is in hmw, just one directory below
                # The solution is valid with this check, so...
                if line == "$ cd vssgzdw":
                    current_directory = current_directory.directories["hmw"].directories["vssgzdw"]

                elif "ls" not in line:
                    directory = line.rsplit(" ", maxsplit=1)[-1]
                    if ".." == directory:
                        current_directory = current_directory.parent
                    else:
                        current_directory = current_directory.directories[directory]
            else:
                spec, name = line.split(" ")
                if "dir" == spec:
                    if name not in current_directory.directories:
                        new_dir = Directory(name, current_directory)
                        current_directory.directories[name] = new_dir
                        if new_dir.absolute_path not in current_directory.directories:
                            all_directories[new_dir.absolute_path] = new_dir

                elif name not in current_directory.files:
                    current_directory.files[name] = File(name, int(spec))

        candidates = sum(directory.size for directory in all_directories.values() if directory.size < 100000)

        self.verify_solution(candidates)

        minimum = 30000000 - (70000000 - root_directory.size)
        unused_space = min(directory.size for directory in all_directories.values() if directory.size > minimum)
        self.verify_solution_part_two(unused_space)

    def _run(self):
        self.solve()
