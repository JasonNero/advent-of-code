from pathlib import Path
import pytest

start_pos = 50

def part_one(input_data) -> int:
    current_pos = start_pos

    at_zero_count = 0

    for line in input_data.splitlines():
        movement = int(line.replace("L", "-").replace("R", "+"))
        current_pos = (current_pos + movement) % 100
        if current_pos == 0:
            at_zero_count += 1

    return at_zero_count

def part_two(input_data) -> int:
    current_pos = start_pos

    total_clicks = 0

    for line in input_data.splitlines():
        movement = int(line.replace("L", "-").replace("R", "+"))

        # One click per full circle.
        full_circle_clicks = abs(movement) // 100
        if movement >= 0:
            rest_movement = movement % 100
        else:
            rest_movement = movement % -100

        new_pos = current_pos + rest_movement

        # Moved out of bounds? Needs a click.
        rest_clicks = 0
        if new_pos <= 0 or new_pos >= 100:
            if current_pos != 0:
                rest_clicks = 1

        new_pos %= 100

        total_clicks += full_circle_clicks
        total_clicks += rest_clicks

        current_pos = new_pos

    return total_clicks

@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n", 3),
    ],
)
def test_part_one(input_data, expected_output):
    assert part_one(input_data) == expected_output

@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n", 6),
        ("L50\nR50", 1),
        ("L50\nL50", 1),
        ("R50\nL50", 1),
        ("R50\nR50", 1),
        ("L150\nL50", 2),
        ("L150\nR50", 2),
        ("R150\nL50", 2),
        ("R150\nR50", 2),
    ]
)
def test_part_two(input_data, expected_output):
    assert part_two(input_data) == expected_output

if __name__ == "__main__":
    with Path("../01.in").open() as f:
        input_data = f.read()

    result1 = part_one(input_data)
    result2 = part_two(input_data)
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
