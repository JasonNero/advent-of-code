from pathlib import Path

import numpy as np
import pytest
import scipy.ndimage as ndimage

test_input = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


class PaperRolls:
    adjacent_kernel = np.array(
        [
            (1, 1, 1),
            (1, 0, 1),
            (1, 1, 1),
        ]
    )

    def __init__(self, grid: str):
        lines = grid.strip().splitlines()
        self.grid = np.zeros((len(lines), len(lines[0])), dtype=int)
        for idx, line in enumerate(lines):
            self.grid[idx, :] = [1 if c == "@" else 0 for c in line]

    def get_accessible_positions(self) -> np.ndarray:
        convolved = ndimage.convolve(
            self.grid, self.adjacent_kernel, mode="constant", cval=0
        )
        accessible = (convolved < 4) & (self.grid == 1)
        return accessible

    def count_accessible_rolls(self) -> int:
        return np.sum(self.get_accessible_positions())

    def remove_accessible_rolls(self):
        accessible = self.get_accessible_positions()
        self.grid[accessible] = 0
        return np.sum(accessible)


def part_one(input_data: str) -> int:
    paper_rolls = PaperRolls(input_data)
    return paper_rolls.count_accessible_rolls()


def part_two(input_data: str) -> int:
    paper_rolls = PaperRolls(input_data)
    total_removed = 0
    while removed := paper_rolls.remove_accessible_rolls():
        total_removed += removed
    return total_removed


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 13)])
def test_part_one(input_data: str, expected_output: int):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 43)])
def test_part_two(input_data: str, expected_output: int):
    assert part_two(input_data) == expected_output


if __name__ == "__main__":
    with Path("../04.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
