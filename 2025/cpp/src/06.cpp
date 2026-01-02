#include <cassert>
import std;

using namespace std;

const string TEST_INPUT = "123 328  51 64 \n"
                          " 45 64  387 23 \n"
                          "  6 98  215 314\n"
                          "*   +   *   +  \n";

class Homework {
  public:
    enum class ReadDirection { RowWise, ColumnWise };
    Homework(const string& input_data) {
        auto stream = istringstream{input_data};
        string line;
        while (getline(stream, line)) {
            if (!line.empty()) {
                grid.push_back(line);
            }
        }

        // Identify operator indices indicating where columns are
        string& operators = grid.back();
        for (size_t col = 0; col < operators.size(); ++col) {
            if (operators[col] != ' ') {
                operator_indices.push_back(col);
            }
        }
    };

    auto solve(ReadDirection direction) const -> long long {
        vector<long long> results = {};
        // Split by operators first to create "Problems"
        for (size_t i = 0; i < operator_indices.size(); ++i) {
            size_t start_col = operator_indices[i];
            size_t end_col = (i + 1 < operator_indices.size())
                                 ? operator_indices[i + 1]
                                 : grid[0].size();

            vector<long long> numbers = {};

            if (direction == ReadDirection::ColumnWise) {
                for (size_t col_idx = start_col; col_idx < end_col; ++col_idx) {
                    string number_str = "";
                    for (size_t row_idx = 0; row_idx < grid.size() - 1;
                         ++row_idx) {
                        if (grid[row_idx][col_idx] != ' ') {
                            number_str += grid[row_idx][col_idx];
                        }
                    }
                    if (number_str.empty()) {
                        continue;
                    }
                    long long number = stoll(number_str);
                    numbers.push_back(number);
                }
            } else {
                for (size_t row_idx = 0; row_idx < grid.size() - 1; ++row_idx) {
                    string number_str = "";
                    for (size_t col_idx = start_col; col_idx < end_col;
                         ++col_idx) {
                        if (grid[row_idx][col_idx] != ' ') {
                            number_str += grid[row_idx][col_idx];
                        }
                    }
                    long long number = stoll(number_str);
                    numbers.push_back(number);
                }
            }

            char op = grid.back()[start_col];
            switch (op) {
            case '+': {
                long long sum =
                    accumulate(numbers.begin(), numbers.end(), 0LL, plus<>());
                results.push_back(sum);
                break;
            }
            case '*': {
                long long prod = accumulate(numbers.begin(), numbers.end(), 1LL,
                                            multiplies<>());
                results.push_back(prod);
                break;
            }
            }
        }
        long long sum = 0;
        for (auto res : results) {
            sum += res;
        }
        return sum;
    };

  private:
    vector<string> grid;
    vector<size_t> operator_indices;
};

auto part_one(const string& input_data) -> long long {
    auto homework = Homework(input_data);
    return homework.solve(Homework::ReadDirection::RowWise);
}

auto part_two(const string& input_data) -> long long {
    auto homework = Homework(input_data);
    return homework.solve(Homework::ReadDirection::ColumnWise);
}

auto test_part_one() -> void {
    auto expected = 4277556;
    auto result = part_one(TEST_INPUT);
    cout << "Got: " << result << ", Expected: " << expected << "\n";
    assert(result == expected);
}

auto test_part_two() -> void {
    auto expected = 3263827;
    auto result = part_two(TEST_INPUT);
    cout << "Got: " << result << ", Expected: " << expected << "\n";
    assert(result == expected);
}

auto main() -> int {
    test_part_one();
    test_part_two();

    string filepath = "../06.in";
    ifstream file(filepath);
    if (!file) {
        throw runtime_error("Failed to open file: " + filepath);
    }

    string in = string{istreambuf_iterator<char>(file), {}};

    long long result_one = part_one(in);
    long long result_two = part_two(in);
    cout << "Part one: " << result_one << "\n";
    cout << "Part two: " << result_two << "\n";
    return 0;
}
