#include <cassert>
#include <fstream>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

const std::string TEST_INPUT = "..@@.@@@@.\n"
                               "@@@.@.@.@@\n"
                               "@@@@@.@.@@\n"
                               "@.@@@@..@.\n"
                               "@@.@@@@.@@\n"
                               ".@@@@@@@.@\n"
                               ".@.@.@.@@@\n"
                               "@.@@@.@@@@\n"
                               ".@@@@@@@@.\n"
                               "@.@.@@@.@.";

class PaperRolls {
  public:
    PaperRolls(const std::string& input) {
        std::ranges::split_view lines = std::views::split(input, '\n');
        for (const auto& line : lines) {
            if (!line.empty()) {
                grid.push_back(std::vector<int>{});
                for (const char c : line) {
                    grid.back().push_back(c == '@' ? 1 : 0);
                }
            }
        }
        height = grid.size();
        width = grid[0].size();
    }

    auto print_grid() const -> void {
        for (const auto& row : grid) {
            for (const auto& cell : row) {
                std::cout << (cell ? '@' : '.');
            }
            std::cout << "\n";
        }
    }

    auto convolve() -> std::vector<std::vector<int>> {
        // Performs a 3x3 convolution over the grid, counting the number of
        // accessible rolls for each cell excluding itself (min 0, max 8)
        std::vector<std::vector<int>> result(height,
                                             std::vector<int>(width, 0));
        for (int i = 0; i < height; ++i) {
            for (int j = 0; j < width; ++j) {
                int sum = 0;
                for (int delta_i = -1; delta_i <= 1; ++delta_i) {
                    for (int delta_j = -1; delta_j <= 1; ++delta_j) {
                        int ni = i + delta_i;
                        int nj = j + delta_j;
                        if (delta_i == 0 && delta_j == 0) {
                            continue; // Skip the center cell
                        }
                        if (ni >= 0 && ni < height && nj >= 0 && nj < width) {
                            sum += grid[ni][nj];
                        }
                    }
                }
                result[i][j] = sum;
            }
        }
        return result;
    }

    auto get_accessible_positions(int max_rolls = 3)
        -> std::vector<std::pair<int, int>> {
        std::vector<std::pair<int, int>> positions;
        auto convolved = convolve();
        for (int i = 0; i < height; ++i) {
            for (int j = 0; j < width; ++j) {
                if (grid[i][j] == 1 && convolved[i][j] <= max_rolls) {
                    positions.emplace_back(i, j);
                }
            }
        }
        return positions;
    }

    auto remove_accessible_rolls() -> int {
        auto positions = get_accessible_positions();
        for (const auto& pos : positions) {
            grid[pos.first][pos.second] = 0; // Remove the roll
        }
        return positions.size();
    }

  private:
    std::vector<std::vector<int>> grid;
    int height;
    int width;
};

auto part_one(const std::string& in) -> int {
    PaperRolls rolls{in};
    // rolls.print_grid();
    auto accessible_positions = rolls.get_accessible_positions();
    return accessible_positions.size();
}

auto part_two(const std::string& in) -> int {
    PaperRolls rolls{in};
    int total_removed = 0;
    int removed;
    while ((removed = rolls.remove_accessible_rolls()) > 0) {
        total_removed += removed;
    }
    return total_removed;
}

auto test_part_one() -> void {
    auto result = part_one(TEST_INPUT);
    std::cout << "Got: " << result << ", Expected: 13" << std::endl;
    assert(result == 13);
}

auto test_part_two() -> void {
    auto result = part_two(TEST_INPUT);
    std::cout << "Got: " << result << ", Expected: 43" << std::endl;
    assert(result == 43);
}

auto main() -> int {
    test_part_one();
    test_part_two();

    std::string filepath = "../04.in";
    std::ifstream file(filepath);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filepath);
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string in{buffer.str()};

    int result_one = part_one(in);
    int result_two = part_two(in);
    std::cout << "Part one: " << result_one << "\n";
    std::cout << "Part two: " << result_two << "\n";
    return 0;
}
