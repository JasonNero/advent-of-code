#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cassert>

const int START_POS = 50;

auto part_one(std::istream &in) -> int
{
    int current_pos = START_POS;
    int at_zero_count = 0;

    for (std::string line; std::getline(in, line);)
    {
        if (line[0] == 'L')
            line[0] = '-';
        else if (line[0] == 'R')
            line[0] = '+';

        int move = stoi(line);
        current_pos = (current_pos + move) % 100;
        if (current_pos == 0)
            ++at_zero_count;
    }

    return at_zero_count;
}

auto part_two(std::istream &in) -> int
{
    int current_pos = START_POS;
    int total_clicks = 0;

    for (std::string line; std::getline(in, line);)
    {
        if (line[0] == 'L')
            line[0] = '-';
        else if (line[0] == 'R')
            line[0] = '+';

        int move = stoi(line);

        int full_circle_clicks = abs(move) / 100;
        int rest_move = move % 100;

        int new_pos = current_pos + rest_move;
        int rest_clicks = 0;
        if (new_pos <= 0 || new_pos >= 100)
            if (current_pos != 0)
                rest_clicks = 1;

        // Python handles modulo differently than C++
        // Prevent negative result by adding 100 before modulo
        new_pos = (new_pos + 100) % 100;

        total_clicks += full_circle_clicks;
        total_clicks += rest_clicks;

        current_pos = new_pos;
    }
    return total_clicks;
}

auto test_part_one() -> void
{
    std::istringstream test_input("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n");
    assert(part_one(test_input) == 3);
}

auto test_part_two() -> void
{
    std::istringstream test_input("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n");
    assert(part_two(test_input) == 6);
}

auto main(int argc, char **argv) -> int
{
    test_part_one();
    test_part_two();

    std::string path = "../01.in";
    std::ifstream in(path);
    if (!in)
    {
        std::cerr << "Failed to open '" << path << "'\n";
        return 2;
    }
    int result_one = part_one(in);
    in.clear();
    in.seekg(0);
    int result_two = part_two(in);
    std::cout << "Part one: " << result_one << "\n";
    std::cout << "Part two: " << result_two << "\n";
    return 0;
}
