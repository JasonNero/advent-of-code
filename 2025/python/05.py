from pathlib import Path

import pytest

test_input = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def contains(self, number: int) -> bool:
        return self.start <= number <= self.end

    def __len__(self):
        return self.end - self.start + 1


class RangeSet:
    def __init__(self, input_ranges):
        """Merge overlapping and adjacent ranges."""
        if not input_ranges:
            return

        # Sort ranges by start value
        input_ranges.sort(key=lambda r: r.start)
        compressed = []
        current_range = input_ranges[0]

        for next_range in input_ranges[1:]:
            if current_range.end + 1 >= next_range.start:  # Overlapping or adjacent
                current_range.end = max(current_range.end, next_range.end)
            else:
                compressed.append(current_range)
                current_range = next_range

        compressed.append(current_range)
        self.ranges = compressed

    def contains(self, number: int) -> bool:
        return any(r.contains(number) for r in self.ranges)

    def __len__(self):
        return sum(len(r) for r in self.ranges)


def parse_input(input_data: str) -> tuple[list[Range], set[int]]:
    ranges = []
    ids = set()
    in_range_definition = True

    for line in input_data.strip().splitlines():
        if line == "":
            in_range_definition = False
            continue

        if in_range_definition:
            start, end = map(int, line.split("-"))
            ranges.append(Range(start, end))
        else:
            ids.add(int(line))
    return ranges, ids


def part_one(input_data: str) -> int:
    """How many of the IDs are in (any of) the ranges?"""
    ranges, ids = parse_input(input_data)

    fresh_count = 0
    for id_ in ids:
        if any(r.contains(id_) for r in ranges):
            fresh_count += 1
    return fresh_count


def part_two(input_data: str) -> int:
    """Hom many unique fresh IDs exist, making sure not to double count overlapping ranges?"""
    ranges, _ = parse_input(input_data)
    range_set = RangeSet(ranges)
    total_fresh_ids = len(range_set)
    return total_fresh_ids


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 3)])
def test_part_one(input_data: str, expected_output: int):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize("input_data, expected_output", [(test_input, 14)])
def test_part_two(input_data: str, expected_output: int):
    assert part_two(input_data) == expected_output


if __name__ == "__main__":
    with Path("../05.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
