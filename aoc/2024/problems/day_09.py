from collections.abc import Iterable
from itertools import islice

from aoc.utilities.aoc import AocBase


def batched(iterable, n, *, strict=False):
    """
    As defined in the Python docs:
    https://docs.python.org/3/library/itertools.html#itertools.batched
    """
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError("batched(): incomplete batch")
        yield batch


class Aoc(AocBase):
    @property
    def day(self) -> int:
        return 9

    @property
    def test_input_data(self) -> Iterable:
        return ["2333133121414131402"]

    @property
    def test_solution(self):
        return 1928

    @property
    def test_solution_part_two(self) -> int:
        return 2858

    @property
    def _solution(self) -> int:
        return 6401092019345

    @property
    def _solution_part_two(self) -> int:
        return 6431472344710

    def _run(self):
        disk = Disk(list(self.input_data_stripped())[0])
        self.verify_solution(disk.bit_checksum)
        self.verify_solution_part_two(disk.file_checksum)


class Disk:
    def __init__(self, disk_map: Iterable[str]):  # noqa: C901
        initial_disk_map = []
        file_sizes = {}
        for file_id, batch in enumerate(batched(disk_map, 2)):
            if not batch:
                continue
            if 1 == len(batch):
                file_blocks = batch[0]
                free_blocks = 0
            else:
                file_blocks, free_blocks = batch

            file_sizes[str(file_id)] = int(file_blocks)
            initial_disk_map.extend([str(file_id)] * int(file_blocks))
            initial_disk_map.extend(["."] * int(free_blocks))

        initial_disk_map_length = len(initial_disk_map) - 1
        new_disk_map = [*initial_disk_map]

        print("Bit optimizing disk space...")
        print(f"{initial_disk_map_length=}")
        # print("".join(new_disk_map))
        for offset, character in enumerate(reversed(new_disk_map)):
            if "." == character:
                continue

            # print(f"{offset=}, being moved")

            left_most_free_block = new_disk_map.index(".")
            block_to_move = initial_disk_map_length - offset

            if block_to_move < left_most_free_block:
                break

            new_disk_map[left_most_free_block], new_disk_map[block_to_move] = (
                new_disk_map[block_to_move],
                new_disk_map[left_most_free_block],
            )
            # print("".join(new_disk_map))

        self.bit_optimized_disk_map = new_disk_map
        # print(self.optimized_disk_map)

        print("File optimizing disk space...")
        print(f"{initial_disk_map_length=}")
        new_disk_map = [*initial_disk_map]
        # print("".join(new_disk_map))

        file_id_handled = {"."}
        for offset, file_id in enumerate(reversed(new_disk_map)):
            if file_id in file_id_handled:
                continue

            if initial_disk_map_length - offset < new_disk_map.index("."):
                break

            print(f"{offset=}, being moved")

            file_size = file_sizes[file_id]
            _disk_map = "".join("." if char == "." else "X" for char in new_disk_map)
            try:
                left_most_free_block = _disk_map.index("." * file_size)
            except ValueError:
                continue

            block_to_move = initial_disk_map_length - offset

            if block_to_move < left_most_free_block:
                continue

            for _offset in range(file_size):
                new_disk_map[left_most_free_block + _offset], new_disk_map[block_to_move - _offset] = (
                    new_disk_map[block_to_move - _offset],
                    new_disk_map[left_most_free_block + _offset],
                )

            # print("".join(new_disk_map))
            file_id_handled.add(file_id)

        self.file_optimized_disk_map = new_disk_map

    @property
    def bit_checksum(self) -> int:
        total = 0
        for position, file_id in enumerate(char for char in self.bit_optimized_disk_map if char != "."):
            total += position * int(file_id)

        return total

    @property
    def file_checksum(self) -> int:
        total = 0
        for position, file_id in enumerate(char for char in self.file_optimized_disk_map):
            if file_id == ".":
                continue

            total += position * int(file_id)

        return total
