from pathlib import Path
import pytest
import itertools

test_input = "7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3"


def part_one(input_data: str) -> int:
    corners = []
    for line in input_data.splitlines():
        x, y = map(int, line.split(","))
        corners.append((x, y))

    max_area = 0
    for combination in itertools.combinations(corners, 2):
        area = abs(combination[0][0] - combination[1][0] +1) * abs(combination[0][1] - combination[1][1]+1)
        if area > max_area:
            max_area = area

    return max_area


def part_two(input_data: str) -> int:
    corners = []
    for line in input_data.splitlines():
        x, y = map(int, line.split(","))
        corners.append((x, y))

    areas = {}
    for combination in itertools.combinations(corners, 2):
        area = abs(combination[0][0] - combination[1][0] +1) * abs(combination[0][1] - combination[1][1]+1)
        areas[combination] = area
       
    max_combination = sorted(areas, key=lambda x: areas[x], reverse=True)[0]
    max_area = areas[max_combination]
    print(f"Max area between points {max_combination[0]} and {max_combination[1]} is {max_area}")
    return max_area


@pytest.mark.parametrize(
    "input_data, expected_output", 
    [(test_input, 50)]
)
def test_part_one(input_data: str, expected_output: int):
    assert part_one(input_data) == expected_output


@pytest.mark.parametrize(
    "input_data, expected_output", 
    [(test_input, 50)]
)
def test_part_two(input_data: str, expected_output: int):
    assert part_two(input_data) == expected_output


if __name__ == "__main__":
    with Path("../09.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
